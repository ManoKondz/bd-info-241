from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Dict, Union

# Criação da aplicação FastAPI
app = FastAPI()

# Modelo Pydantic para o Aluno
class Aluno(BaseModel):
    aluno_nome: str
    endereco: str

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('dbalunos.db')
    conn.row_factory = sqlite3.Row  # Para retornar resultados como dicionários
    return conn

# Inicializar o banco de dados e a tabela
def init_db():
    with get_db_connection() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS TB_ALUNO (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_nome TEXT NOT NULL,
            endereco TEXT NOT NULL
        )
        ''')
        conn.commit()

init_db()

# a) Criar Aluno
@app.post("/criar_aluno/", response_model=Dict[str, str])
async def criar_aluno(aluno: Aluno):
    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO TB_ALUNO (aluno_nome, endereco) VALUES (?, ?)",
            (aluno.aluno_nome, aluno.endereco)
        )
        conn.commit()
    return {"message": "Aluno criado com sucesso!"}

# b) Listar Alunos
@app.get("/listar_alunos/", response_model=List[Dict[str, Union[int, str]]])
async def listar_alunos():
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT * FROM TB_ALUNO")
        alunos = [dict(row) for row in cursor.fetchall()]
    return alunos

# c) Listar um Aluno
@app.get("/listar_um_aluno/{aluno_id}", response_model=Dict[str, Union[int, str]])
async def listar_um_aluno(aluno_id: int):
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT * FROM TB_ALUNO WHERE id = ?", (aluno_id,))
        aluno = cursor.fetchone()
    if aluno:
        return dict(aluno)
    else:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

# d) Atualizar Aluno
@app.put("/atualizar_aluno/{aluno_id}", response_model=Dict[str, str])
async def atualizar_aluno(aluno_id: int, aluno: Aluno):
    with get_db_connection() as conn:
        cursor = conn.execute(
            "UPDATE TB_ALUNO SET aluno_nome = ?, endereco = ? WHERE id = ?",
            (aluno.aluno_nome, aluno.endereco, aluno_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"message": "Aluno atualizado com sucesso!"}

# e) Excluir Aluno
@app.delete("/excluir_aluno/{aluno_id}", response_model=Dict[str, str])
async def excluir_aluno(aluno_id: int):
    with get_db_connection() as conn:
        cursor = conn.execute("DELETE FROM TB_ALUNO WHERE id = ?", (aluno_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"message": "Aluno excluído com sucesso!"}
