from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import datetime

app = FastAPI()

# CORS Middleware (necessário para frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Substitua com seu domínio em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Banco de Dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./chat.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    mensagens = relationship("Mensagem", back_populates="usuario")


class Mensagem(Base):
    __tablename__ = "mensagens"

    id = Column(Integer, primary_key=True, index=True)
    conteudo = Column(Text)
    timestamp = Column(String, default=lambda: datetime.datetime.now().isoformat())
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    usuario = relationship("Usuario", back_populates="mensagens")


# Criar tabelas
Base.metadata.create_all(bind=engine)

# Dependência para obter sessão DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Gerenciador de conexões WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[username] = websocket

    def disconnect(self, username: str):
        self.active_connections.pop(username, None)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        disconnected_users = []
        for username, ws in self.active_connections.items():
            try:
                await ws.send_text(message)
            except Exception as e:
                print(f"Erro ao enviar mensagem para {username}: {e}")
                disconnected_users.append(username)

        # Remove conexões que falharam
        for username in disconnected_users:
            self.disconnect(username)

manager = ConnectionManager()

# Rota WebSocket
@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str, db: Session = Depends(get_db)):
    await manager.connect(username, websocket)

    # Criar usuário se não existir
    usuario = db.query(Usuario).filter_by(nome=username).first()
    if not usuario:
        usuario = Usuario(nome=username)
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Recebido de {username}: {data}")

            # Salvar mensagem no banco de dados
            msg = Mensagem(conteudo=data, usuario_id=usuario.id)
            db.add(msg)
            db.commit()

            full_message = f"{username}: {data}"
            await manager.broadcast(full_message)

    except WebSocketDisconnect:
        print(f"{username} desconectado.")
        manager.disconnect(username)
        await manager.broadcast(f"{username} saiu do chat.")

    except Exception as e:
        print(f"Erro no WebSocket de {username}: {e}")
        manager.disconnect(username)
        await manager.broadcast(f"{username} teve um erro e saiu do chat.")

# Endpoint para ver histórico de mensagens
@app.get("/historico/{username}")
def obter_historico(username: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(nome=username).first()
    if not usuario:
        return {"mensagens": []}

    mensagens = db.query(Mensagem).filter_by(usuario_id=usuario.id).order_by(Mensagem.timestamp).all()
    return {"mensagens": [{"conteudo": m.conteudo, "timestamp": m.timestamp} for m in mensagens]}
