from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, field_validator
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal
import json
import os

app = FastAPI()

DB_FILE = "database.json"

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Substitua pelo domínio do seu front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Modelo de dados
class Usuario(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    cargo: Literal['professor', 'aluno']

    @field_validator("senha")
    def senha_minima(cls, v):
        if len(v) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres.")
        return v

# Função para carregar o banco de dados
def carregar_dados():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

# Função para salvar no banco de dados
def salvar_dados(dados):
    with open(DB_FILE, "w") as f:
        json.dump(dados, f, indent=4)

# Rota para cadastrar um usuário
@app.post("/cadastrar")
def cadastrar_usuario(usuario: Usuario):
    dados = carregar_dados()

    # Verificar se e-mail já está cadastrado
    if any(u['email'] == usuario.email for u in dados):
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    # Adicionar novo usuário
    dados.append(usuario.dict())
    salvar_dados(dados)
    return {"mensagem": "Usuário cadastrado com sucesso!"}

# Rota para listar todos os usuários
@app.get("/usuarios")
def listar_usuarios():
    return carregar_dados()
