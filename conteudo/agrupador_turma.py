from ferramentas_apoio.lista_alunos_turma import ListaAlunosTurma

class Turma:
    def __init__(self, codigo, nome_disciplina, nome_professor):
        self.codigo = codigo
        self.nome_disciplina = nome_disciplina
        self.nome_professor = nome_professor
        self.alunos = ListaAlunosTurma()  # Aqui vai ficar a lista encadeada dos alunos da turma

    def adicionar_aluno_na_turma(self, nome, id_aluno):
        # Adiciona o aluno na lista encadeada interna
        self.alunos.adicionar_aluno(nome, id_aluno)
        print(f"Aluno '{nome}' adicionado na turma {self.codigo}.")

    def mostrar_detalhes_da_turma(self):
        print(f"\n--- TURMA {self.codigo} ---")
        print(f"Disciplina: {self.nome_disciplina}")
        print(f"Professor: {self.nome_professor}")
        print("Alunos:")
        self.alunos.listar_alunos()

class GerenciadorTurmas:
    def __init__(self):
        self.turmas = {}  # Dicionário onde cada turma é identificada por um código único

    def criar_nova_turma(self):
        print("\n--- Criar Nova Turma ---")

        while True:
            codigo = input("Código da nova turma: ").strip().upper()
            if not codigo:
                print("Código da turma não pode ficar vazio.")
            elif codigo in self.turmas:
                print("Já existe uma turma com esse código.")
            else:
                break

        # Nome da disciplina não pode estar vazio
        while True:
            disciplina = input("Nome da disciplina: ").strip()
            if disciplina:
                break
            print("Informe o nome da disciplina corretamente.")

        # Nome do professor não pode estar vazio
        while True:
            professor = input("Nome do professor: ").strip()
            if professor:
                break
            print("Informe o nome do professor corretamente.")

        self.turmas[codigo] = Turma(codigo, disciplina, professor)
        print(f"Turma {codigo} criada com sucesso.")

    def adicionar_aluno_em_turma(self):
        print("\n--- Adicionar Aluno em Turma ---")

        codigo = input("Código da turma: ").strip().upper()
        if codigo not in self.turmas:
            print("Turma não encontrada.")
            return

        nome = input("Nome do aluno: ").strip()
        if not nome:
            print("Nome do aluno não pode ficar vazio.")
            return

        id_aluno = input("ID do aluno: ").strip()
        if not id_aluno.isdigit():
            print("ID inválido. Use apenas números.")
            return

        self.turmas[codigo].adicionar_aluno_na_turma(nome, id_aluno)

    def mostrar_turma(self):
        print("\n--- Mostrar Detalhes da Turma ---")

        codigo = input("Código da turma: ").strip().upper()
        if codigo not in self.turmas:
            print("Turma não encontrada.")
            return

        self.turmas[codigo].mostrar_detalhes_da_turma()

    def listar_todas_as_turmas(self):
        print("\n--- Todas as Turmas Criadas ---")
        if not self.turmas:
            print("Nenhuma turma criada ainda.")
            return

        for codigo, turma in self.turmas.items():
            print(f"Turma {codigo} - {turma.nome_disciplina} - Prof. {turma.nome_professor}")
