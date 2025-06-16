import re

class GerenciadorProfessores:
    def __init__(self, banco):
        self.db = banco

    def validar_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[a-z]{2,4}$", email)

    def cadastrar_professor(self):
        print("\n--- Cadastro de Novo Professor ---")

        # Nome só pode ter letras e espaços
        while True:
            nome = input("Nome completo: ").strip()
            if nome.replace(" ", "").isalpha():
                break
            print("Nome inválido. Use apenas letras.")

        # Aqui confiro se o email tá no formato certo
        while True:
            email = input("Email institucional: ").strip()
            if self.validar_email(email):
                break
            print("Email inválido. Ex: prof@escola.com")

        # Telefone precisa ser só número e com tamanho mínimo decente
        while True:
            telefone = input("Telefone: ").strip()
            if telefone.isdigit() and 8 <= len(telefone) <= 15:
                break
            print("Telefone inválido. Use apenas números entre 8 e 15 dígitos.")

        # Registro funcional tem que ser um número único
        while True:
            registro = input("Número de registro funcional (somente números): ").strip()
            if registro.isdigit():
                break
            print("Registro inválido. Digite apenas números.")

        try:
            # Agora joga tudo pro banco
            self.db.cursor.execute('''
                INSERT INTO professores (nome, email, telefone, registro_funcional)
                VALUES (?, ?, ?, ?)''', (nome, email, telefone, registro))
            self.db.conexao.commit()
            print("Professor cadastrado com sucesso!")
        except Exception as e:
            print(f"Erro ao cadastrar professor: {e}")

    def listar_professores(self):
        print("\n--- Lista de Professores Cadastrados ---")
        self.db.cursor.execute("SELECT * FROM professores")
        professores = self.db.cursor.fetchall()
        for p in professores:
            print(f"[{p[0]}] {p[1]} - {p[3]} | Registro: {p[4]}")

    def buscar_por_registro(self):
        print("\n--- Buscar Professor pelo Registro Funcional ---")
        registro = input("Digite o número de registro: ")
        self.db.cursor.execute("SELECT * FROM professores WHERE registro_funcional = ?", (registro,))
        prof = self.db.cursor.fetchone()
        if prof:
            print(f"Professor: {prof[1]} | Email: {prof[2]} | Telefone: {prof[3]}")
        else:
            print("Professor não encontrado.")

    def editar_professor(self):
        print("\n--- Edição de Dados do Professor ---")
        registro = input("Informe o número de registro do professor: ")

        self.db.cursor.execute("SELECT * FROM professores WHERE registro_funcional = ?", (registro,))
        prof = self.db.cursor.fetchone()

        if not prof:
            print("Professor não encontrado.")
            return

        # Atualizações opcionais
        novo_email = input("Novo email (ou enter para manter): ").strip()
        if novo_email and not self.validar_email(novo_email):
            print("Email inválido. Alteração cancelada.")
            return

        novo_tel = input("Novo telefone (ou enter para manter): ").strip()
        if novo_tel and (not novo_tel.isdigit() or not (8 <= len(novo_tel) <= 15)):
            print("Telefone inválido. Alteração cancelada.")
            return

        email_final = novo_email if novo_email else prof[2]
        tel_final = novo_tel if novo_tel else prof[3]

        self.db.cursor.execute("UPDATE professores SET email = ?, telefone = ? WHERE registro_funcional = ?", (email_final, tel_final, registro))
        self.db.conexao.commit()
        print("Professor atualizado com sucesso!")

    def remover_professor(self):
        print("\n--- Remoção de Professor ---")
        registro = input("Digite o número de registro do professor a ser removido: ")

        self.db.cursor.execute("SELECT nome FROM professores WHERE registro_funcional = ?", (registro,))
        prof = self.db.cursor.fetchone()

        if not prof:
            print("Professor não encontrado.")
            return

        confirmacao = input(f"Deseja realmente remover o professor '{prof[0]}'? (s/n): ")
        if confirmacao.lower() == 's':
            self.db.cursor.execute("DELETE FROM professores WHERE registro_funcional = ?", (registro,))
            self.db.conexao.commit()
            print("Professor removido com sucesso.")
        else:
            print("Remoção cancelada.")
