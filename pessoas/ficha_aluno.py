import re
from datetime import datetime

class GerenciadorAlunos:
    def __init__(self, banco, arvore):
        self.db = banco
        self.arvore = arvore

    # Verifica se o email tem o padrão básico com arroba e ponto
    def validar_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[a-z]{2,4}$", email)

    # Confirma se a data foi escrita certinha no formato brasileiro
    def validar_data(self, data_str):
        try:
            datetime.strptime(data_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    # Checa se o telefone só tem número e tem um tamanho aceitável
    def validar_telefone(self, tel):
        return tel.isdigit() and 8 <= len(tel) <= 15

    def cadastrar_novo(self):
        print("\n--- Cadastro de Novo Aluno ---")

        # Nome só com letras e espaços
        while True:
            nome = input("Nome completo: ").strip()
            if nome.replace(" ", "").isalpha():
                break
            print("Nome inválido. Use apenas letras.")

        # Email precisa ter formato válido
        while True:
            email = input("Email institucional: ").strip()
            if self.validar_email(email):
                break
            print("Email inválido. Ex: exemplo@dominio.com")

        # Só aceita números no telefone, e com tamanho razoável
        while True:
            telefone = input("Telefone: ").strip()
            if self.validar_telefone(telefone):
                break
            print("Telefone inválido. Use apenas números entre 8 e 15 dígitos.")

        # Garante que só entra M, F ou Outro
        while True:
            sexo = input("Sexo (M/F/Outro): ").strip().upper()
            if sexo in ["M", "F", "OUTRO"]:
                break
            print("Sexo inválido. Use M, F ou Outro.")

        # Aqui a gente vê se a data realmente existe e tá no formato certo
        while True:
            nascimento = input("Data de nascimento (dd/mm/aaaa): ").strip()
            if self.validar_data(nascimento):
                break
            print("Data inválida. Use o formato dd/mm/aaaa.")

        # Endereço tem que ter mais de 5 caracteres, pra não ser zoado
        while True:
            endereco = input("Endereço completo: ").strip()
            if len(endereco) > 5:
                break
            print("Endereço muito curto.")

        # Curso não pode ficar em branco
        while True:
            curso = input("Curso matriculado: ").strip()
            if curso:
                break
            print("Informe o curso corretamente.")

        # Foto é opcional, então só pego se tiver
        foto = input("URL da foto ou local (opcional): ").strip()

        # Junto tudo num pacote de dados
        dados = (nome, email, telefone, sexo, nascimento, endereco, curso, foto)

        # Gravo no banco
        self.db.cursor.execute("""
            INSERT INTO alunos (nome, email, telefone, sexo, nascimento, endereco, curso, foto)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", dados)
        self.db.conexao.commit()

        # E também insiro esse aluno na árvore pra poder listar por nome depois
        self.arvore.inserir(nome, dados)
        print("Aluno cadastrado com sucesso e inserido na árvore!")

    def listar_todos(self):
        print("\n--- Lista de Alunos Cadastrados ---")
        self.db.cursor.execute("SELECT * FROM alunos")
        alunos = self.db.cursor.fetchall()
        for aluno in alunos:
            print(f"[{aluno[0]}] {aluno[1]} - {aluno[2]} - {aluno[6]}")

    def buscar_por_id(self):
        print("\n--- Busca por ID ---")
        try:
            aluno_id = int(input("Digite o ID do aluno: "))
        except ValueError:
            print("ID inválido. Digite um número.")
            return

        self.db.cursor.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id,))
        aluno = self.db.cursor.fetchone()
        if aluno:
            print(f"\n[ID: {aluno[0]}] {aluno[1]} | Email: {aluno[2]} | Curso: {aluno[7]}")
        else:
            print("Aluno não encontrado.")

    def editar_aluno(self):
        print("\n--- Edição de Aluno ---")
        aluno_id = input("Digite o ID do aluno a ser editado: ")

        if not aluno_id.isdigit():
            print("ID inválido.")
            return

        self.db.cursor.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id,))
        aluno = self.db.cursor.fetchone()

        if not aluno:
            print("Aluno não encontrado.")
            return

        print(f"Editando: {aluno[1]} ({aluno[2]})")

        # Aqui o usuário pode atualizar email e telefone, ou manter
        novo_email = input("Novo email (deixe vazio para manter): ").strip()
        if novo_email and not self.validar_email(novo_email):
            print("Email inválido. Alteração cancelada.")
            return

        novo_tel = input("Novo telefone (deixe vazio para manter): ").strip()
        if novo_tel and not self.validar_telefone(novo_tel):
            print("Telefone inválido. Alteração cancelada.")
            return

        # Se não atualizar, usa o antigo mesmo
        email_final = novo_email if novo_email else aluno[2]
        tel_final = novo_tel if novo_tel else aluno[3]

        self.db.cursor.execute(
            "UPDATE alunos SET email = ?, telefone = ? WHERE id = ?",
            (email_final, tel_final, aluno_id)
        )
        self.db.conexao.commit()
        print("Aluno atualizado com sucesso!")

    def remover_aluno(self):
        print("\n--- Remoção de Aluno ---")
        aluno_id = input("Digite o ID do aluno a ser removido: ")

        if not aluno_id.isdigit():
            print("ID inválido.")
            return

        self.db.cursor.execute("SELECT nome FROM alunos WHERE id = ?", (aluno_id,))
        aluno = self.db.cursor.fetchone()

        if not aluno:
            print("Aluno não encontrado.")
            return

        confirmacao = input(f"Tem certeza que deseja remover o aluno '{aluno[0]}'? (s/n): ")
        if confirmacao.lower() == 's':
            self.db.cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
            self.db.conexao.commit()
            print("Aluno removido com sucesso.")
        else:
            print("Remoção cancelada.")
