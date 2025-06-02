# Implementação de uma árvore binária de busca (ABB) para armazenar alunos por nome em ordem alfabética.
# Utilizada para facilitar consultas ordenadas sem necessidade de ordenação posterior.

class NoAluno:
    def __init__(self, nome, dados):
        self.nome = nome
        self.dados = dados  # Tupla contendo os dados completos do aluno
        self.esquerda = None  # Subárvore esquerda (nomes menores)
        self.direita = None   # Subárvore direita (nomes maiores)

class ArvoreDeAlunos:
    def __init__(self):
        self.raiz = None  # Raiz da árvore

    def inserir(self, nome, dados):
        # Insere um novo aluno na árvore com base no nome (ordem alfabética)
        novo_no = NoAluno(nome, dados)
        if self.raiz is None:
            self.raiz = novo_no  # Se a árvore estiver vazia, o novo nó vira a raiz
        else:
            self.__inserir_recursivo(self.raiz, novo_no)

    def __inserir_recursivo(self, atual, novo):
        # Método auxiliar recursivo para inserir nós na árvore
        if novo.nome.lower() < atual.nome.lower():
            if atual.esquerda is None:
                atual.esquerda = novo
            else:
                self.__inserir_recursivo(atual.esquerda, novo)
        else:
            if atual.direita is None:
                atual.direita = novo
            else:
                self.__inserir_recursivo(atual.direita, novo)

    def listar_em_ordem(self):
        # Exibe todos os alunos em ordem alfabética de nome (crescente)
        if self.raiz is None:
            print("Nenhum aluno registrado na árvore.")
        else:
            print("\n--- Alunos em ordem alfabética ---")
            self.__em_ordem(self.raiz)

    def __em_ordem(self, no):
        # Percorre a árvore em ordem simétrica (esquerda, raiz, direita)
        if no is not None:
            self.__em_ordem(no.esquerda)
            print(f"{no.nome} - Dados: {no.dados}")
            self.__em_ordem(no.direita)
