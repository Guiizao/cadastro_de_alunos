import re

class GerenciadorDisciplinas:
    def __init__(self, banco):
        self.db = banco
        self.codigos_existentes = set()  # Aqui guardo todos os códigos pra evitar repetir
        self.__carregar_codigos()

    # Carrega os códigos já cadastrados no banco e salva no set
    def __carregar_codigos(self):
        self.db.cursor.execute("SELECT codigo FROM disciplinas")
        codigos = self.db.cursor.fetchall()
        for c in codigos:
            self.codigos_existentes.add(c[0])

    def cadastrar(self):
        print("\n--- Cadastro de Disciplina ---")

        # Nome da disciplina só pode conter letras e espaços
        while True:
            nome = input("Nome da disciplina: ").strip()
            if nome.replace(" ", "").isalpha():
                break
            print("Nome inválido. Use apenas letras.")

        # Código da disciplina precisa ser único e ter letras/números (ex: MAT101)
        while True:
            codigo = input("Código único da disciplina (ex: MAT101): ").strip().upper()
            if not re.match("^[A-Z]{3}[0-9]{3}$", codigo):
                print("Formato inválido. Use 3 letras seguidas de 3 números (ex: MAT101).")
            elif codigo in self.codigos_existentes:
                print("Esse código de disciplina já existe. Tente outro.")
            else:
                break

        # Carga horária precisa ser um número inteiro
        while True:
            try:
                carga = int(input("Carga horária (em horas): "))
                if carga > 0:
                    break
                print("Digite um valor maior que zero.")
            except ValueError:
                print("A carga horária deve ser um número inteiro.")

        # Descrição é opcional
        descricao = input("Descrição da disciplina (opcional): ").strip()

        # Insere no banco e salva no set também
        self.db.cursor.execute('''
            INSERT INTO disciplinas (nome, codigo, carga_horaria, descricao)
            VALUES (?, ?, ?, ?)''', (nome, codigo, carga, descricao))
        self.db.conexao.commit()
        from registro_db.historico import adicionar_operacao
        adicionar_operacao(f"Disciplina '{nome}' cadastrada com código '{codigo}'.")
        self.codigos_existentes.add(codigo)

        print("Disciplina cadastrada com sucesso!")

    def listar_disciplinas(self):
        print("\n--- Disciplinas Cadastradas ---")
        self.db.cursor.execute("SELECT * FROM disciplinas")
        disciplinas = self.db.cursor.fetchall()
        for d in disciplinas:
            print(f"[{d[0]}] {d[1]} | Código: {d[2]} | Carga: {d[3]}h")

    def buscar_por_codigo(self):
        print("\n--- Buscar Disciplina por Código ---")
        codigo = input("Digite o código da disciplina: ").strip().upper()
        self.db.cursor.execute("SELECT * FROM disciplinas WHERE codigo = ?", (codigo,))
        resultado = self.db.cursor.fetchone()

        if resultado:
            print(f"Disciplina: {resultado[1]} | Código: {resultado[2]} | Carga: {resultado[3]}h")
        else:
            print("Nenhuma disciplina encontrada com esse código.")
