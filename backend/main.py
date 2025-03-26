from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from .database import SessionLocal, engine, Base
from .models import Usuario, Producto, Venta, DetalleVenta
from .schemas import (
    UsuarioCreate, UsuarioResponse,
    ProductoCreate, ProductoResponse,
    VentaCreate, VentaResponse,
    DetalleVentaCreate, DetalleVentaResponse
)

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/usuarios/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.get("/usuarios/", response_model=List[UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Usuario).offset(skip).limit(limit).all()

@app.post("/productos/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):

    if not db.query(Usuario).filter(Usuario.codigo_registro == producto.id_vendedor).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor no encontrado"
        )
    
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.get("/productos/", response_model=List[ProductoResponse])
def listar_productos(skip: int = 0, limit: int = 100, categoria: str = None, db: Session = Depends(get_db)):
    query = db.query(Producto)
    if categoria:
        query = query.filter(Producto.categoria == categoria)
    return query.offset(skip).limit(limit).all()

@app.post("/ventas/", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def crear_venta(venta: VentaCreate, db: Session = Depends(get_db)):

    vendedor = db.query(Usuario).filter(Usuario.codigo_registro == venta.vendedor_id).first()
    comprador = db.query(Usuario).filter(Usuario.codigo_registro == venta.comprador_id).first()
    
    if not vendedor or not comprador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor o comprador no encontrado"
        )
    
    if not vendedor.es_vendedor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario especificado como vendedor no tiene permisos de vendedor"
        )

    db_venta = Venta(
        **venta.dict(),
        fecha=datetime.now(),
        estado_entrega="Pendiente",
        precio_total=0  
    )
    db.add(db_venta)
    db.commit()
    db.refresh(db_venta)
    return db_venta

@app.get("/ventas/", response_model=List[VentaResponse])
def listar_ventas(skip: int = 0, limit: int = 100, estado: str = None, db: Session = Depends(get_db)):
    query = db.query(Venta)
    if estado:
        query = query.filter(Venta.estado_entrega == estado)
    return query.offset(skip).limit(limit).all()

@app.post("/detalles-venta/", response_model=DetalleVentaResponse, status_code=status.HTTP_201_CREATED)
def crear_detalle_venta(detalle: DetalleVentaCreate, db: Session = Depends(get_db)):

    venta = db.query(Venta).filter(Venta.codigo == detalle.venta_id).first()
    producto = db.query(Producto).filter(Producto.id_producto == detalle.producto_id).first()
    
    if not venta or not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta o producto no encontrado"
        )
    

    venta.precio_total += detalle.cantidad * detalle.precio_unitario
    
    db_detalle = DetalleVenta(**detalle.dict())
    db.add(db_detalle)
    db.commit()
    db.refresh(db_detalle)
    return db_detalle

@app.get("/")
def home():
    return {
        "message": "Bienvenido a Murrap",
        "endpoints": [
            {"usuarios": "/usuarios/"},
            {"productos": "/productos/"},
            {"ventas": "/ventas/"},
            {"detalles_venta": "/detalles-venta/"}
        ]
    }