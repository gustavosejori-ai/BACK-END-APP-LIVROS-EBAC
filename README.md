
# API de Gerenciamento de Tarefas

Projeto desenvolvido durante o curso de Back-end Python da EBAC.

## Sobre o projeto

Esta API permite gerenciar tarefas, oferecendo operações para listar, adicionar, atualizar e excluir registros.

## Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Poetry
- Podman
- Docker Compose

## Funcionalidades

- Listar tarefas cadastradas.
- Adicionar novas tarefas.
- Marcar tarefas como concluídas.
- Excluir tarefas.
- Autenticação HTTP Basic.
- Paginação e ordenação na listagem.

## Como executar o projeto

### Pré-requisitos

- Python
- Poetry
- Podman
- Podman Compose

### Configuração

1. Clone o repositório.
2. Configure as variáveis de ambiente em um arquivo `.env`.
3. Instale as dependências do projeto.
4. Inicie a aplicação com:

```powershell
podman-compose up --build -d
```

### Acessar a documentação

Com a aplicação em execução, acesse:

http://localhost:8000/docs

## Segurança

As credenciais devem ser configuradas no arquivo `.env`. Esse arquivo não deve ser enviado ao repositório.

## Autor

Desenvolvido como projeto de estudo de Back-end Python.
