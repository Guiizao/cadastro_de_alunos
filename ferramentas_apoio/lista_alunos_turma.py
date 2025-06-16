# lista_alunos_turma.py
# Estrutura de dados que representa uma lista encadeada simples para armazenar os alunos de uma turma.
# Cada nó representa um aluno e mantém referência para o próximo elemento da lista.

class NoAlunoTurma:
    def __init__(self, nome, id_aluno):
        self.nome = nome
        self.id_aluno = id_aluno
        self.proximo = None  # Ponteiro para o próximo aluno da lista

class ListaAlunosTurma:
    def __init__(self):
        self.inicio = None  # Referência para o primeiro nó da lista

    def adicionar_aluno(self, nome, id_aluno):
        """ Insere um novo aluno ao final da lista encadeada """
        novo = NoAlunoTurma(nome, id_aluno)

        if self.inicio is None:
            self.inicio = novo  # Caso a lista esteja vazia, o novo aluno será o primeiro
        else:
            atual = self.inicio
            while atual.proximo:  # Percorre até o último nó
                atual = atual.proximo
            atual.proximo = novo  # Adiciona no final da lista

    def listar_alunos(self):
        """ Exibe os alunos presentes na lista encadeada """
        atual = self.inicio
        if not atual:
            print("Nenhum aluno foi registrado nesta turma.")
            return

        print("\n--- Lista de Alunos da Turma ---")
        while atual:
            print(f"- {atual.nome} (ID: {atual.id_aluno})")
            atual = atual.proximo

    def limpar_lista(self):
        """ Remove todos os nós da lista, esvaziando a turma """
        self.inicio = None
