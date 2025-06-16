from ferramentas_apoio.lista_alunos_turma import ListaAlunosTurma

class GerenciadorTurmas:
    def __init__(self, db):
        self.db = db

    def listar_disciplinas(self):
        self.db.cursor.execute("SELECT id, nome FROM disciplinas")
        disciplinas = self.db.cursor.fetchall()
        print("\n--- Disciplinas Disponíveis ---")
        for disc in disciplinas:
            print(f"[{disc[0]}] {disc[1]}")

    def listar_professores(self):
        self.db.cursor.execute("SELECT id, nome FROM professores")
        professores = self.db.cursor.fetchall()
        print("\n--- Professores Disponíveis ---")
        for prof in professores:
            print(f"[{prof[0]}] {prof[1]}")

    def listar_turmas(self):
        self.db.cursor.execute("SELECT id, codigo FROM turmas")
        turmas = self.db.cursor.fetchall()
        print("\n--- Turmas Disponíveis ---")
        for turma in turmas:
            print(f"[{turma[0]}] Código: {turma[1]}")

    def listar_alunos(self):
        self.db.cursor.execute("SELECT id, nome FROM alunos")
        alunos = self.db.cursor.fetchall()
        print("\n--- Alunos Disponíveis ---")
        for aluno in alunos:
            print(f"[{aluno[0]}] {aluno[1]}")

    def criar_nova_turma(self):
        print("\n--- Criar Nova Turma ---")

        codigo_turma = input("Digite o código da nova turma: ").strip().upper()
        if not codigo_turma:
            print("Código da turma não pode ser vazio.")
            return

        self.listar_disciplinas()
        id_disciplina = input("Digite o ID da disciplina: ").strip()
        if not id_disciplina.isdigit():
            print("ID de disciplina inválido.")
            return

        self.listar_professores()
        id_professor = input("Digite o ID do professor: ").strip()
        if not id_professor.isdigit():
            print("ID de professor inválido.")
            return

        self.db.cursor.execute("""
            INSERT INTO turmas (codigo, id_disciplina, id_professor)
            VALUES (?, ?, ?)
        """, (codigo_turma, id_disciplina, id_professor))
        self.db.conexao.commit()

        print(f"Turma {codigo_turma} criada com sucesso!")

    def adicionar_aluno_em_turma(self):
        print("\n--- Adicionar Aluno em Turma ---")

        self.listar_turmas()
        id_turma = input("Digite o ID da turma: ").strip()
        if not id_turma.isdigit():
            print("ID de turma inválido.")
            return

        self.listar_alunos()
        id_aluno = input("Digite o ID do aluno: ").strip()
        if not id_aluno.isdigit():
            print("ID de aluno inválido.")
            return

        # Verificar se já está na turma
        self.db.cursor.execute("""
            SELECT * FROM turma_aluno
            WHERE id_turma = ? AND id_aluno = ?
        """, (id_turma, id_aluno))
        if self.db.cursor.fetchone():
            print("Aluno já está matriculado nessa turma.")
            return

        self.db.cursor.execute("""
            INSERT INTO turma_aluno (id_turma, id_aluno)
            VALUES (?, ?)
        """, (id_turma, id_aluno))
        self.db.conexao.commit()

        print("Aluno matriculado na turma com sucesso!")

    def listar_todas_as_turmas(self):
        print("\n--- Todas as Turmas Criadas ---")
        self.db.cursor.execute("""
            SELECT t.codigo, d.nome, p.nome
            FROM turmas t
            JOIN disciplinas d ON t.id_disciplina = d.id
            JOIN professores p ON t.id_professor = p.id
        """)
        turmas = self.db.cursor.fetchall()
        if not turmas:
            print("Nenhuma turma criada ainda.")
            return

        for turma in turmas:
            print(f"Turma {turma[0]} - Disciplina: {turma[1]} - Professor: {turma[2]}")

    def mostrar_turma(self):
        print("\n--- Detalhes de uma Turma ---")
        self.listar_turmas()
        id_turma = input("Digite o ID da turma: ").strip()
        if not id_turma.isdigit():
            print("ID inválido.")
            return

        self.db.cursor.execute("""
            SELECT t.codigo, d.nome, p.nome
            FROM turmas t
            JOIN disciplinas d ON t.id_disciplina = d.id
            JOIN professores p ON t.id_professor = p.id
            WHERE t.id = ?
        """, (id_turma,))
        turma = self.db.cursor.fetchone()

        if not turma:
            print("Turma não encontrada.")
            return

        print(f"\nCódigo da Turma: {turma[0]}")
        print(f"Disciplina: {turma[1]}")
        print(f"Professor: {turma[2]}")

        print("\nAlunos da turma:")
        self.db.cursor.execute("""
            SELECT a.id, a.nome
            FROM turma_aluno ta
            JOIN alunos a ON ta.id_aluno = a.id
            WHERE ta.id_turma = ?
        """, (id_turma,))
        alunos = self.db.cursor.fetchall()
        if not alunos:
            print("Nenhum aluno matriculado nesta turma.")
        else:
            for aluno in alunos:
                print(f"[{aluno[0]}] {aluno[1]}")

    def listar_alunos_por_turma(self):
        print("\n--- Alunos por Turma ---")
        self.listar_turmas()
        id_turma = input("Digite o ID da turma: ").strip()
        if not id_turma.isdigit():
            print("ID inválido.")
            return

        self.db.cursor.execute("""
            SELECT a.id, a.nome, a.email
            FROM turma_aluno ta
            JOIN alunos a ON ta.id_aluno = a.id
            WHERE ta.id_turma = ?
        """, (id_turma,))
        alunos = self.db.cursor.fetchall()

        if not alunos:
            print("Nenhum aluno nesta turma.")
            return

        print(f"\nAlunos da Turma {id_turma}:")
        for aluno in alunos:
            print(f"[{aluno[0]}] {aluno[1]} - {aluno[2]}")
    def listar_alunos_por_turma(self):
        print("\n--- Alunos por Turma ---")

        # Listar as turmas disponíveis antes de pedir o ID
        self.listar_turmas()

        id_turma = input("Digite o ID da turma: ").strip()
        if not id_turma.isdigit():
            print("ID inválido.")
            return

        # Buscar os alunos dessa turma no banco
        self.db.cursor.execute("""
            SELECT a.id, a.nome, a.email
            FROM turma_aluno ta
            JOIN alunos a ON ta.id_aluno = a.id
            WHERE ta.id_turma = ?
        """, (id_turma,))

        alunos = self.db.cursor.fetchall()

        if not alunos:
            print("\nNenhum aluno cadastrado nesta turma.\n")
            return

        print(f"\nAlunos da Turma ID {id_turma}:")
        for aluno in alunos:
            print(f"[{aluno[0]}] {aluno[1]} - {aluno[2]}")
