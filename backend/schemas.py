from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UsuarioBase(BaseModel):
    nombre: str
    ubicacion: str
    cuenta_banco: str

class UsuarioCreate(UsuarioBase):
    es_vendedor: bool = False
    es_comprador: bool = True

class UsuarioResponse(UsuarioBase):
    codigo_registro: int
    estado: str
    es_vendedor: bool
    es_comprador: bool
    email: Optional[str] = None

    class Config:
        orm_mode = True

class ProductoBase(BaseModel):
    nombre: str
    precio: float
    cantidad: int
    categoria: str

class ProductoCreate(ProductoBase):
    id_vendedor: int

class ProductoResponse(ProductoBase):
    id_producto: int
    id_vendedor: int

    class Config:
        orm_mode = True

class VentaBase(BaseModel):
    vendedor_id: int
    comprador_id: int
    origen: str
    destino: str

class VentaCreate(VentaBase):
    pass

class VentaResponse(VentaBase):
    codigo: int
    fecha: datetime
    precio_total: float
    estado_entrega: str
    fecha_despacho: Optional[datetime] = None
    fecha_entrega: Optional[datetime] = None

    class Config:
        orm_mode = True

class DetalleVentaBase(BaseModel):
    venta_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float

class DetalleVentaCreate(DetalleVentaBase):
    pass

class DetalleVentaResponse(DetalleVentaBase):
    id_detalle: int

    class Config:
        orm_mode = True