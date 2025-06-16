from pessoas.ficha_aluno import GerenciadorAlunos
from pessoas.ficha_professor import GerenciadorProfessores
from conteudo.materia_disciplina import GerenciadorDisciplinas
from conteudo.agrupador_turma import GerenciadorTurmas
from registro_db.conexao_estudantil import ConexaoBanco
from registro_db.historico import mostrar_historico
from arvore_nome_aluno import ArvoreDeAlunos

def main():
    db = ConexaoBanco()
    arvore_alunos = ArvoreDeAlunos()

    aluno_obj = GerenciadorAlunos(db, arvore_alunos)
    professor_obj = GerenciadorProfessores(db)
    disciplina_obj = GerenciadorDisciplinas(db)
    turma_obj = GerenciadorTurmas(db)

    while True:
        print("\n================ MENU DO SISTEMA ESCOLAR ================\n")
        print("1. Cadastrar novo aluno")
        print("2. Editar aluno existente")
        print("3. Remover aluno")
        print("4. Listar todos os alunos")
        print("5. Buscar aluno por ID")
        print("6. Cadastrar professor")
        print("7. Criar disciplina")
        print("8. Criar turma e adicionar alunos")
        print("9. Matricular aluno em turma (fila)")
        print("10. Ver histórico de operações (pilha)")
        print("11. Listar alunos por nome (ordem alfabética)")
        print("12. Listar alunos de uma turma (lista encadeada)")
        print("0. Sair do sistema")
        print("\n========================================================")

        opcao = input("Digite a opção desejada: ").strip()

        if opcao == "1":
            aluno_obj.cadastrar_novo()

        elif opcao == "2":
            aluno_obj.editar_aluno()

        elif opcao == "3":
            aluno_obj.remover_aluno()

        elif opcao == "4":
            aluno_obj.listar_todos()

        elif opcao == "5":
            aluno_obj.buscar_por_id()

        elif opcao == "6":
            professor_obj.cadastrar()

        elif opcao == "7":
            disciplina_obj.cadastrar()

        elif opcao == "8":
            turma_obj.criar_nova_turma()

        elif opcao == "9":
            turma_obj.adicionar_aluno_em_turma()

        elif opcao == "10":
            mostrar_historico()

        elif opcao == "11":
            aluno_obj.listar_alunos_por_nome()

        elif opcao == "12":
            turma_obj.listar_alunos_por_turma()

        elif opcao == "0":
            print("Saindo do sistema...")
            db.fechar()
            break

        else:
            print("Opção inválida! Digite um número de 0 a 12.")

if __name__ == "__main__":
    main()
