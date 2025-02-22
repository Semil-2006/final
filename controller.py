from model import Usuario

class UsuarioController:
    def obter_usuarios(self):
        return Usuario.obter_todos()

    def autenticar_usuario(self, email, senha):
        return Usuario.autenticar(email, senha)

    def adicionar_usuario(self, nome, idade, email, numero, senha):
        usuario = Usuario(nome=nome, idade=idade, email=email, numero=numero, senha=senha)
        usuario.salvar()

    def editar_usuario(self, id, nome, idade, email, numero, senha):
        usuario = Usuario(id=id, nome=nome, idade=idade, email=email, numero=numero, senha=senha)
        usuario.salvar()

    def deletar_usuario(self, id):
        Usuario.deletar(id)
