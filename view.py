# view.py

class UsuarioView:
    def exibir_informacoes(self, usuarios):
        for usuario in usuarios:
            print(f"Nome: {usuario.nome}, Idade: {usuario.idade} anos")

    def exibir_mensagem(self, mensagem):
        print(mensagem)

