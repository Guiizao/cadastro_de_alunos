import re
from datetime import datetime
from arvore_nome_aluno import ArvoreDeAlunos 

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

        self.db.cursor.execute("SELECT COUNT(*) FROM disciplinas")
        qtd_disciplinas = self.db.cursor.fetchone()[0]

        if qtd_disciplinas == 0:
            print("\nNenhuma disciplina cadastrada ainda. Por favor, cadastre uma disciplina antes de adicionar alunos.\n")
            return

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

    def listar_alunos_por_nome(self):
        print("\n--- Lista de Alunos em Ordem Alfabética ---")
        self.db.cursor.execute("SELECT id, nome, email FROM alunos ORDER BY nome ASC")
        alunos = self.db.cursor.fetchall()
        if not alunos:
            print("Nenhum aluno cadastrado.")
            return
        for aluno in alunos:
            print(f"[{aluno[0]}] {aluno[1]} - {aluno[2]}")
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

    def listar_alunos(self):
        print("\n--- Alunos Cadastrados ---")
        self.db.cursor.execute("SELECT id, nome, email FROM alunos")
        alunos = self.db.cursor.fetchall()

        if not alunos:
            print("Nenhum aluno cadastrado.\n")
            return

        for aluno in alunos:
            print(f"[{aluno[0]}] {aluno[1]} - {aluno[2]}")


    def editar_aluno(self):
        print("\n--- Edição de Aluno ---")
        self.listar_alunos()

        aluno_id = input("\nDigite o ID do aluno a ser editado: ")

        if not aluno_id.isdigit():
            print("ID inválido.")
            return

        self.db.cursor.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id,))
        aluno = self.db.cursor.fetchone()

        if not aluno:
            print("Aluno não encontrado.")
            return

        print(f"\nEditando: {aluno[1]} ({aluno[2]})")

        novo_nome = input("Novo nome (deixe vazio para manter): ").strip()
        novo_email = input("Novo email (deixe vazio para manter): ").strip()
        novo_tel = input("Novo telefone (deixe vazio para manter): ").strip()
        novo_endereco = input("Novo endereço (deixe vazio para manter): ").strip()
        novo_curso = input("Novo curso (deixe vazio para manter): ").strip()
        nova_data_nasc = input("Nova data de nascimento (deixe vazio para manter): ").strip()

        # Validações básicas (se quiser pode fazer validação de email, telefone, etc)
        if novo_email and not self.validar_email(novo_email):
            print("Email inválido. Alteração cancelada.")
            return

        if novo_tel and not self.validar_telefone(novo_tel):
            print("Telefone inválido. Alteração cancelada.")
            return

        # Se o campo estiver vazio, manter o valor atual
        nome_final = novo_nome if novo_nome else aluno[1]
        email_final = novo_email if novo_email else aluno[2]
        tel_final = novo_tel if novo_tel else aluno[3]
        endereco_final = novo_endereco if novo_endereco else aluno[4]
        curso_final = novo_curso if novo_curso else aluno[5]
        data_nasc_final = nova_data_nasc if nova_data_nasc else aluno[6]

        self.db.cursor.execute("""
            UPDATE alunos
            SET nome = ?, email = ?, telefone = ?, endereco = ?, curso = ?, data_nascimento = ?
            WHERE id = ?
        """, (nome_final, email_final, tel_final, endereco_final, curso_final, data_nasc_final, aluno_id))

        self.db.conexao.commit()
        print("\nAluno atualizado com sucesso!")


    def buscar_aluno_por_id(self):
        print("\n--- Busca de Aluno por ID ---")
        self.listar_alunos()

        aluno_id = input("\nDigite o ID do aluno: ")

        if not aluno_id.isdigit():
            print("ID inválido.")
            return

        self.db.cursor.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id,))
        aluno = self.db.cursor.fetchone()

        if not aluno:
            print("\nAluno não encontrado.\n")
            return

        print("\n=== Dados completos do aluno ===")
        print(f"ID: {aluno[0]}")
        print(f"Nome: {aluno[1]}")
        print(f"Email: {aluno[2]}")
        print(f"Telefone: {aluno[3]}")
        print(f"Endereço: {aluno[4]}")
        print(f"Curso: {aluno[5]}")
        print(f"Data de Nascimento: {aluno[6]}")
        print("================================\n")
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
