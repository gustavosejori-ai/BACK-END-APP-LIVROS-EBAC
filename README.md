# API de Gerenciamento de Tarefas — FastAPI

Projeto desenvolvido durante o curso da EBAC para praticar a criação e a execução de uma API utilizando FastAPI, SQLAlchemy, SQLite, Poetry e containers.

## Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Poetry
- Docker e Docker Compose
- Podman (alternativa para execução local)

## Pré-requisitos

Para executar com Docker:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Docker Compose

Para executar alternativamente com Podman:

- [Podman Desktop](https://podman-desktop.io/)
- Python
- `podman-compose`

## Configuração do ambiente

1. Clone o repositório:

   ```bash
   git clone https://github.com/gustavosejori-ai/BACK-END-APP-LIVROS-EBAC.git
   ```

2. Entre na pasta do projeto:

   ```bash
   cd BACK-END-APP-LIVROS-EBAC
   ```

3. Crie o arquivo `.env` a partir do modelo `.env.example`.

   No Windows PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

4. Abra o arquivo `.env` e configure as variáveis de ambiente:

   ```dotenv
   DATABASE_URL=sqlite:///./tarefas.db
   usuario=seu_usuario
   senha=sua_senha
   ```

   Substitua os valores de exemplo pelas credenciais que deseja utilizar.

   **Importante:** o arquivo `.env` contém configurações locais e não deve ser enviado ao GitHub. O arquivo `.env.example` serve como modelo de configuração.

## Executando com Docker Compose

Na pasta que contém o `docker-compose.yml`, execute:

```bash
docker compose up --build -d
```

Esse comando constrói a imagem e inicia o container em segundo plano.

Para verificar os containers em execução:

```bash
docker compose ps
```

Para acompanhar os logs:

```bash
docker compose logs -f
```

Para encerrar o ambiente:

```bash
docker compose down
```

## Executando alternativamente com Podman

Certifique-se de que o Podman esteja instalado e que a máquina do Podman esteja em execução. Instale o `podman-compose` caso necessário:

```powershell
python -m pip install podman-compose
```

Para construir a imagem e iniciar o container em segundo plano:

```powershell
python -m podman_compose up --build -d
```

Para verificar os containers em execução:

```powershell
podman ps
```

Para acompanhar os logs do container:

```powershell
podman logs -f tarefas-api-container
```

Para parar o container sem removê-lo:

```powershell
podman stop tarefas-api-container
```

Para iniciar novamente um container que foi parado:

```powershell
podman start tarefas-api-container
```

Para encerrar e remover os recursos do ambiente criado pelo Compose:

```powershell
python -m podman_compose down
```

## Acessando a API

Após iniciar a aplicação, acesse a documentação interativa do FastAPI:

http://localhost:8000/docs

Para consultar as tarefas diretamente, acesse:

http://localhost:8000/tarefa

Os endpoints protegidos exigem autenticação HTTP Basic, utilizando as credenciais configuradas no arquivo `.env`.

## Observações

- O arquivo `.env` deve permanecer fora do controle de versão.
- O arquivo `.env.example` documenta as variáveis necessárias para executar a aplicação.
- O Docker Compose é o fluxo principal documentado para atender ao exercício.
- O Podman pode ser utilizado como alternativa para execução local.
- O Uvicorn utiliza `--reload` durante o desenvolvimento para reiniciar automaticamente a aplicação quando o código é alterado.
