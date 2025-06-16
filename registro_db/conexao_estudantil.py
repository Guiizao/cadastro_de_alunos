# Responsável por iniciar a conexão com o banco SQLite e criar as tabelas iniciais

import sqlite3

class ConexaoBanco:
    def __init__(self, nome_arquivo='escola_unimar.db'):
        # Conecta ao banco ou cria se não existir
        self.conexao = sqlite3.connect(nome_arquivo)
        self.cursor = self.conexao.cursor()
        self.__criar_tabelas_basicas()

    def __criar_tabelas_basicas(self):
        # Cria a tabela de alunos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL,
                sexo TEXT NOT NULL,
                nascimento TEXT NOT NULL,
                endereco TEXT NOT NULL,
                curso TEXT NOT NULL,
                foto TEXT NOT NULL
            )
        ''')

        # Cria a tabela de professores
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS professores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL,
                registro_funcional TEXT UNIQUE NOT NULL
            )
        ''')

        # Cria a tabela de disciplinas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS disciplinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                codigo TEXT UNIQUE NOT NULL,
                carga_horaria INTEGER NOT NULL,
                descricao TEXT
            )
        ''')

        # Cria a tabela de turmas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS turmas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL,
                id_disciplina INTEGER,
                id_professor INTEGER,
                FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id),
                FOREIGN KEY (id_professor) REFERENCES professores(id)
            )
        ''')

        # Tabela de relacionamento entre alunos e turmas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS turma_aluno (
                id_turma INTEGER,
                id_aluno INTEGER,
                PRIMARY KEY (id_turma, id_aluno),
                FOREIGN KEY (id_turma) REFERENCES turmas(id),
                FOREIGN KEY (id_aluno) REFERENCES alunos(id)
            )
        ''')

        self.conexao.commit()

    def fechar_conexao(self):
        self.conexao.close()
