from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal, Usuario, UsuarioCreate
from passlib.context import CryptContext # bcrypt version 4.0.1 en caso de error

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/registro")
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="El usuario ya está registrado")

    hashed_password = pwd_context.hash(usuario.password)
    
    nuevo_usuario = Usuario(email=usuario.email, password=hashed_password, tipo=usuario.tipo)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {"mensaje": "Usuario registrado con éxito"}

@app.get("/")
def home():
    return {"mensaje": "Al menos hay back end"}
