from flask import Flask, render_template, request, redirect, url_for,jsonify,make_response
from controller import UsuarioController
from model import Usuario
from flask_socketio import SocketIO,emit
from flask_sqlalchemy import SQLAlchemy
from model import Mensagem


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secreto'
socketio = SocketIO(app, cors_allowed_origins="*")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sistema.db"
db = SQLAlchemy(app)


usuario_controller = UsuarioController()

ADMIN_EMAIL = "admin"
ADMIN_SENHA = "3122"


@socketio.on("mensagem")
def handle_message(data):
    usuario = data.get("usuario")
    mensagem = data.get("mensagem")

    if usuario and mensagem:
        nova_mensagem = Mensagem(usuario=usuario, texto=mensagem)
        db.session.add(nova_mensagem)
        db.session.commit()

        emit("nova_mensagem", {"usuario": usuario, "texto": mensagem}, broadcast=True)


@app.route('/cadastro')
def index():
    usuarios = usuario_controller.obter_usuarios()
    return render_template('index.html', usuarios=usuarios)

@app.route("/home")
@app.route("/")
def loja():
    email = request.args.get("email")

    usuario = None
    tipo_usuario = "desconhecido"

    if email:
        usuario = usuario_controller.autenticar_usuario(email, "")
        if usuario:
            tipo_usuario = "admin" if usuario.email == "admin" and usuario.senha == "3122" else "usuario"

    return render_template("pagina.html", usuario=usuario, tipo_usuario=tipo_usuario)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        usuario = usuario_controller.autenticar_usuario(email, senha)
        if usuario:
            # Diferenciar admin dos usuários comuns
            tipo_usuario = "admin" if usuario.email == "admin" and usuario.senha == "3122" else "usuario"
            return jsonify({"success": True, "tipo_usuario": tipo_usuario, "redirect": url_for("loja")})
        return jsonify({"success": False, "message": "Email ou senha incorretos!"})

    return render_template("login.html")


@app.route('/adicionar', methods=['POST'])
def adicionar_usuario():
    nome = request.form['nome']
    idade = int(request.form['idade'])
    email = request.form['email']
    numero = request.form['numero']
    senha = request.form['senha']

    usuario_controller.adicionar_usuario(nome, idade, email, numero, senha)
    return redirect(url_for('index'))


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.obter_por_id(id)

    if request.method == 'POST':
        nome = request.form['nome']
        idade = int(request.form['idade'])
        email = request.form['email']
        numero = request.form['numero']
        senha = request.form['senha']

        usuario_controller.editar_usuario(id, nome, idade, email, numero, senha)
        return redirect(url_for('index'))

    return render_template('editar.html', usuario=usuario)


@app.route('/deletar/<int:id>')
def deletar_usuario(id):
    usuario_controller.deletar_usuario(id)
    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    response = make_response(redirect(url_for("loja")))
    response.set_cookie("tipo_usuario", "", expires=0)
    return response

@app.route("/chat")
def chat():
    usuario = request.cookies.get("tipo_usuario")  # Obtém usuário do cookie
    if not usuario:
        return redirect(url_for("login"))

    mensagens = Mensagem.obter_todas()
    return render_template("chat.html", usuario=usuario, mensagens=mensagens)


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000, use_reloader=False, log_output=True)

