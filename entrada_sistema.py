
# Este é o ponto inicial do sistema escolar via linha de comando.
# Aqui a gente chama as funcionalidades e organiza a navegação no terminal.

from pessoas.ficha_aluno import GerenciadorAlunos
from pessoas.ficha_professor import GerenciadorProfessores
from conteudo.agrupador_turma import GerenciadorTurmas
from materia_disciplina import GerenciadorDisciplinas
from organizador_fila import FilaMatricula
from organizador_pilha import PilhaHistorico
from arvore_nome_aluno import ArvoreDeAlunos
from registro_db.conexao_estudantil import ConexaoBanco

def exibir_menu():
    print("\n================ MENU DO SISTEMA ESCOLAR ================")
    print("1. Cadastrar novo aluno")
    print("2. Editar aluno existente")
    print("3. Remover aluno")
    print("4. Listar todos os alunos")
    print("5. Buscar aluno por ID")
    print("6. Cadastrar professor")
    print("7. Criar disciplina")
    print("8. Criar turma")
    print("9. Matricular aluno em turma (fila)")
    print("10. Ver histórico de operações (pilha)")
    print("0. Sair do sistema")
    print("========================================================")

# Instâncias principais
banco = ConexaoBanco()
arvore = ArvoreDeAlunos()
alunos = GerenciadorAlunos(banco, arvore)
cursor = banco.cursor
cursor.execute("SELECT * FROM alunos")
for aluno in cursor.fetchall():
    nome = aluno[1]  # nome
    dados = (aluno[1], aluno[2], aluno[3], aluno[4], aluno[5], aluno[6], aluno[7], aluno[8])
    arvore.inserir(nome, dados)
professores = GerenciadorProfessores(banco)
disciplinas = GerenciadorDisciplinas(banco)
turmas = GerenciadorTurmas()
fila = FilaMatricula()
pilha = PilhaHistorico()

# Loop do menu principal
while True:
    exibir_menu()
    opcao = input("Digite a opção desejada: ")

    if opcao == "1":
        alunos.cadastrar_novo()
    elif opcao == "2":
        alunos.editar_aluno()
    elif opcao == "3":
        alunos.remover_aluno()
    elif opcao == "4":
        alunos.listar_todos()
    elif opcao == "5":
        alunos.buscar_por_id()
    elif opcao == "6":
        professores.cadastrar_professor()
    elif opcao == "7":
        disciplinas.cadastrar_disciplina()
    elif opcao == "8":
        turmas.criar_nova_turma()
    elif opcao == "9":
        turmas.adicionar_aluno_em_turma()
    elif opcao == "10":
        pilha.exibir_historico()
    elif opcao == "0":
        print("Saindo do sistema. Até logo!")
        break
    else:
        print("Opção inválida. Tenta de novo aí.")

input("\nPressione Enter para sair...")
