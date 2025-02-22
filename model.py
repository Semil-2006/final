import sqlite3

class Usuario:
    def __init__(self, id=None, nome=None, idade=None, email=None, numero=None, senha=None):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.email = email
        self.numero = numero
        self.senha = senha

    def salvar(self):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()

        if self.id is None:
            cursor.execute(
                "INSERT INTO usuarios (nome, idade, email, numero, senha) VALUES (?, ?, ?, ?, ?)",
                (self.nome, self.idade, self.email, self.numero, self.senha)
            )
        else:
            cursor.execute(
                "UPDATE usuarios SET nome = ?, idade = ?, email = ?, numero = ?, senha = ? WHERE id = ?",
                (self.nome, self.idade, self.email, self.numero, self.senha, self.id)
            )

        conn.commit()
        conn.close()

    @classmethod
    def obter_todos(cls):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        rows = cursor.fetchall()
        conn.close()

        usuarios = [cls(*row) for row in rows]
        return usuarios

    @classmethod
    def obter_por_id(cls, id):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(*row)
        return None

    @classmethod
    def deletar(cls, id):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    @classmethod
    def autenticar(cls, email, senha):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(*row)
        return None

    @classmethod
    def criar_tabela(cls):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL,
                email TEXT NOT NULL,
                numero TEXT NOT NULL,
                senha TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# Criar a tabela caso não exista
Usuario.criar_tabela()

class Mensagem:
    def __init__(self, id=None, usuario=None, texto=None):
        self.id = id
        self.usuario = usuario
        self.texto = texto

    def salvar(self):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()

        if self.id is None:
            cursor.execute(
                "INSERT INTO mensagens (usuario, texto) VALUES (?, ?)",
                (self.usuario, self.texto)
            )
        else:
            cursor.execute(
                "UPDATE mensagens SET usuario = ?, texto = ? WHERE id = ?",
                (self.usuario, self.texto, self.id)
            )

        conn.commit()
        conn.close()

    @classmethod
    def obter_todas(cls):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mensagens")
        rows = cursor.fetchall()
        conn.close()

        mensagens = [cls(*row) for row in rows]
        return mensagens

    @classmethod
    def criar_tabela(cls):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                texto TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# Criar a tabela caso não exista
Mensagem.criar_tabela()
