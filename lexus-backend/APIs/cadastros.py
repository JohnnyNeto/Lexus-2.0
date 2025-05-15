import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, validator
from typing import Literal
from pathlib import Path

app = FastAPI(openapi_url="/api/v1/cad.json", docs_url="/docs/cad")

# Caminho para o arquivo JSON
FILE_PATH = Path("../cadastros.json")
# Verifica se o arquivo existe, caso contrário, cria um arquivo vazio
if not FILE_PATH.exists():
    with open(FILE_PATH, "w") as f:
        json.dump([], f)

# Modelo de dados para o cadastro
class Cadastro(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    formacao: Literal['aluno', 'professor']

    # Validação personalizada para a formação
    @validator('formacao')
    def verificar_formacao(cls, v):
        if v not in ['aluno', 'professor']:
            raise ValueError('A formação deve ser "aluno" ou "professor".')
        return v

# Modelo de dados para o login
class Login(BaseModel):
    email: EmailStr
    senha: str

# Função para ler os cadastros do arquivo JSON
def ler_cadastros():
    if FILE_PATH.exists():
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    return []

# Função para salvar os cadastros no arquivo JSON
def salvar_cadastros(cadastros):
    with open(FILE_PATH, "w") as f:
        json.dump(cadastros, f, indent=4)

@app.post("/cadastro/")
async def cadastrar_usuario(cadastro: Cadastro):
    # Carrega os cadastros existentes
    cadastros = ler_cadastros()
    
    # Adiciona o novo cadastro
    cadastros.append(cadastro.dict())
    
    # Salva os cadastros no arquivo
    salvar_cadastros(cadastros)
    
    return {"msg": "Cadastro realizado com sucesso!", "dados": cadastro}

@app.get("/cadastros/")
async def obter_cadastros():
    # Carrega os cadastros do arquivo
    cadastros = ler_cadastros()
    return cadastros

@app.post("/login/")
async def login_usuario(login: Login):
    # Carrega os cadastros
    cadastros = ler_cadastros()
    
    # Busca o cadastro com o email fornecido
    usuario = next((u for u in cadastros if u['email'] == login.email), None)
    
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Verifica se a senha está correta
    if usuario['senha'] != login.senha:
        raise HTTPException(status_code=400, detail="Senha incorreta")
    
    return {"msg": "Login bem-sucedido", "usuario": usuario}
