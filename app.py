from fastapi import FastAPI, HTTPException
app = FastAPI()

minhas_tarefas = []

@app.get("/tarefa")
def get_tarefa():
    if not minhas_tarefas:
        return {"message": "Nao existe nenhuma tarefa!"}
    else:
        return {"tarefa": minhas_tarefas}

@app.post("/adiciona")
def post_tarefa(tarefa:dict):
    tarefa["concluida"] = False
    minhas_tarefas.append(tarefa)
    return tarefa

@app.put("/atualiza/{tarefa}")
def put_tarefa(tarefa: str):
    for item in minhas_tarefas:
        if item["nome"] == tarefa:
            item["concluida"] = True
            return {"message": "A tarefa foi atualizada com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Essa tarefa nao existe!")

@app.delete("/deleta/{tarefa}")
def delete_tarefa(tarefa:str):
    for item in minhas_tarefas:
        if item["nome"] == tarefa:
            minhas_tarefas.remove(item)
            return {"message":"A tarefa foi excluida com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Tarefa nao encontrada!" )

