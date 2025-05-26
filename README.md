
# Sistema de Gestão Escolar - Projeto de Estrutura de Dados

### Integrantes:
- Guilherme Dalanora Dos Santos - 1991839
- Gustavo Ramanoski - 1992124
- Leonardo Lopes Martins Silva - 2010503

---

## 📝 Sobre o Projeto

Este projeto foi desenvolvido como parte da disciplina de Estrutura de Dados. A ideia foi criar um sistema de gestão escolar simples, que funciona totalmente no terminal, com cadastro de alunos, professores, turmas, disciplinas e com o uso de várias estruturas de dados estudadas durante o curso.

---

## ⚙️ Como Rodar

### 🔵 Sem Docker (direto no Python)

1. Garanta que tem Python 3 instalado.
2. Abra o terminal na pasta do projeto.
3. Rode o sistema com:
```bash
python entrada_sistema.py
```

---

### 🐳 Com Docker (opcional)

> Caso você queira rodar com Docker para facilitar, siga os passos abaixo:

1. Tenha o Docker e Docker Compose instalados.
2. No terminal da pasta do projeto, rode:

```bash
docker-compose up --build
```

3. O sistema será executado automaticamente no terminal do container.

---

## 📁 Funcionalidades Implementadas

- Cadastro, edição, remoção e listagem de alunos
- Cadastro de professores e disciplinas
- Criação de turmas com vinculação de professor e disciplina
- Matrícula de alunos usando fila
- Histórico de ações com pilha
- Exibição ordenada de alunos com árvore binária
- Listagem por turma com lista encadeada

---

## 🧠 Estruturas de Dados Usadas

| Estrutura           | Onde foi usada                                 |
|---------------------|------------------------------------------------|
| Fila                | Para gerenciar a matrícula em ordem            |
| Pilha               | Para armazenar histórico de ações              |
| Tupla               | Usada nas inserções no banco                   |
| Dicionário          | Para armazenar e buscar turmas por código      |
| Set                 | Para evitar disciplinas duplicadas             |
| Lista Encadeada     | Para representar os alunos de uma turma        |
| Árvore Binária      | Para listar alunos em ordem alfabética         |

---

## 💾 Banco de Dados

- Usamos SQLite, que é um banco leve e local.
- Ele é criado automaticamente ao rodar o sistema pela primeira vez.
- As tabelas também são criadas caso não existam.

---

## 📈 Fluxograma

O fluxograma do sistema está disponível no arquivo `Fluxograma.png` e também foi gerado visualmente usando o [Excalidraw](https://excalidraw.com).

---
