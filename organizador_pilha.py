# organizador_pilha.py
# Implementa uma pilha para registrar as ações realizadas no sistema, funcionando como histórico.
# Utiliza lista comum em modo LIFO (Last-In, First-Out).

class PilhaHistorico:
    def __init__(self):
        # Lista que armazena as ações em ordem reversa (último no topo)
        self.pilha = []

    def registrar_acao(self, descricao):
        # Adiciona uma nova ação no topo da pilha
        self.pilha.append(descricao)

    def desfazer_ultima_acao(self):
        # Remove a última ação registrada, simulando um "desfazer"
        if not self.pilha:
            print("Nenhuma ação para desfazer.")
            return
        ultima = self.pilha.pop()
        print(f"Ação desfeita: {ultima}")

    def exibir_historico(self):
        # Mostra todas as ações da mais recente até a mais antiga
        if not self.pilha:
            print("Nenhuma ação registrada ainda.")
        else:
            print("\n--- Histórico de Ações ---")
            for i, acao in enumerate(reversed(self.pilha), 1):
                print(f"{i}. {acao}")
