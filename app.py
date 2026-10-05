from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
import secrets
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./tarefas.db"
print("BANCO:", os.path.abspath("tarefas.db"))

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)
Base = declarative_base()

app = FastAPI()

usuario = "Gustavo"
senha_usuario = "1234"

security = HTTPBasic()

class TarefaDB(Base):
    __tablename__ = "Tarefas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String, index=True)
    concluida = Column(Boolean, default=False)

class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

Base.metadata.create_all(bind=engine)

def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def autenticar_usuario(credentials:HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, usuario)
    is_password_correct = secrets.compare_digest(credentials.password, senha_usuario)
    if not (is_username_correct and is_password_correct):
        raise HTTPException(status_code=401,detail="Usuario ou senha incoreta",headers={"WWW-Authenticate":"Basic"})

@app.get("/tarefa")
def get_tarefa(page: int = 1,size: int = 5,order_by: Optional[str] = None,db: Session = Depends(sessao_db),credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if page < 1 or size < 1:
        raise HTTPException(
            status_code=400,
            detail="Page e size devem ser maiores que 0"
        )
    query = db.query(TarefaDB)

    if order_by == "nome":
        query = query.order_by(TarefaDB.nome)
    elif order_by == "descricao":
        query = query.order_by(TarefaDB.descricao)
    elif order_by is not None:
        raise HTTPException(status_code=400,detail="Parametro de ordenacao invalido!" )

    tarefas = query.offset((page - 1) * size).limit(size).all()

    if not tarefas:
        return {"message": "Nao existe nenhuma tarefa!"}

    total_tarefas = db.query(TarefaDB).count()

    return {"tarefas": tarefas,"total": total_tarefas}


@app.post("/adiciona")
def post_tarefa(tarefa:Tarefa,db:Session = Depends(sessao_db),credentials:HTTPBasicCredentials = Depends(autenticar_usuario)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.nome == tarefa.nome).first()
    if db_tarefa:
        raise HTTPException(status_code=400, detail="Essa tarefa ja existe no banco de dados")
    db_tarefa = TarefaDB(nome=tarefa.nome,descricao=tarefa.descricao,concluida=tarefa.concluida)
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

@app.put("/atualiza/{tarefa}")
def put_tarefa(tarefa:str,db:Session = Depends(sessao_db),credentials:HTTPBasicCredentials = Depends(autenticar_usuario)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.nome == tarefa).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Essa tarefa nao existe!")
    db_tarefa.concluida = True
    db.commit()
    return {"message": "A tarefa foi atualizada com sucesso!"}

@app.delete("/deleta/{tarefa}")
def delete_tarefa(tarefa:str,db:Session = Depends(sessao_db),credentials:HTTPBasicCredentials = Depends(autenticar_usuario)):
   db_tarefa = db.query(TarefaDB).filter(TarefaDB.nome == tarefa).first()
   if not db_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa nao encontrada!" )
   db.delete(db_tarefa)
   db.commit()
   return {"message":"A tarefa foi excluida com sucesso!"}

