historico_operacoes = []

def adicionar_operacao(descricao):
    historico_operacoes.append(descricao)

def mostrar_historico():
    print("\n=== Histórico de Operações ===")
    if not historico_operacoes:
        print("Nenhuma operação registrada ainda.")
        return
    for i, operacao in enumerate(reversed(historico_operacoes), 1):
        print(f"{i}. {operacao}")
