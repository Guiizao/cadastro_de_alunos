# organizador_fila.py
# Implementa uma fila para simular o processo de matrícula de alunos em ordem de chegada.
# Utiliza lista comum em modo FIFO (First-In, First-Out).

class FilaMatricula:
    def __init__(self):
        # Lista que representa a fila de espera
        self.fila = []

    def entrar_na_fila(self, nome_aluno):
        # Insere o aluno no final da fila
        self.fila.append(nome_aluno)
        print(f"Aluno '{nome_aluno}' entrou na fila de matrícula.")

    def proximo(self):
        # Remove o primeiro aluno da fila, que é o próximo a ser matriculado
        if not self.fila:
            print("A fila de matrícula está vazia.")
            return None
        aluno = self.fila.pop(0)
        print(f"Chamando próximo da fila: {aluno}")
        return aluno

    def visualizar_fila(self):
        # Exibe todos os alunos que ainda estão aguardando na fila
        if not self.fila:
            print("Nenhum aluno aguardando na fila de matrícula.")
        else:
            print("\n--- Alunos na Fila ---")
            for i, nome in enumerate(self.fila):
                print(f"{i+1}. {nome}")
