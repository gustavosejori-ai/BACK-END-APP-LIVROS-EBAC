from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
import secrets
import os

app = FastAPI()

usuario = "Gustavo"
senha_usuario = "1234"

security = HTTPBasic()

minhas_tarefas = []

class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

def autenticar_usuario(credentials:HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, usuario)
    is_password_correct = secrets.compare_digest(credentials.password, senha_usuario)
    if not (is_username_correct and is_password_correct):
        raise HTTPException(status_code=401,detail="Usuario ou senha incoreta",headers={"WWW-Authenticate":"Basic"})

@app.get("/tarefa")
def get_tarefa(page : int = 1, size : int = 5, order_by: Optional[str] = None,credentials:HTTPBasicCredentials = Depends(autenticar_usuario)):
    if page < 1 or size < 1:
        raise HTTPException(status_code=400, detail="Page e size devem ser maiores que 0")
    if not minhas_tarefas:
        return {"message": "Nao existe nenhuma tarefa!"}
    else:
        tarefas_ordenadas = minhas_tarefas.copy()
        if order_by == "nome":
            tarefas_ordenadas.sort(key=lambda tarefa : tarefa.nome)
        elif order_by == "descricao":
            tarefas_ordenadas.sort(key=lambda tarefa : tarefa.descricao)
        elif order_by is not None:
            raise HTTPException(status_code=400,detail="Parametro de ordenacao invalido!")
        inicio = (page - 1) * size
        fim = inicio + size
        return {"tarefa": tarefas_ordenadas[inicio:fim]}


@app.post("/adiciona")
def post_tarefa(tarefa:Tarefa,credentials:HTTPBasicCredentials = Depends(autenticar_usuario)):
    minhas_tarefas.append(tarefa)
    return tarefa

@app.put("/atualiza/{tarefa}")
def put_tarefa(tarefa:str,credentials:HTTPBasicCredentials = Depends(autenticar_usuario)):
    for item in minhas_tarefas:
        if item.nome == tarefa:
            item.concluida = True
            return {"message": "A tarefa foi atualizada com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Essa tarefa nao existe!")

@app.delete("/deleta/{tarefa}")
def delete_tarefa(tarefa:str,credentials:HTTPBasicCredentials = Depends(autenticar_usuario)):
    for item in minhas_tarefas:
        if item.nome == tarefa:
            minhas_tarefas.remove(item)
            return {"message":"A tarefa foi excluida com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Tarefa nao encontrada!" )

