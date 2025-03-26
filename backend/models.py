from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base, EstadoUsuario, EstadoEntrega

class Usuario(Base):
    __tablename__ = "usuarios"

    codigo_registro = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)  
    nombre = Column(String(100))
    ubicacion = Column(String(100), nullable=False)
    cuenta_banco = Column(String(50), nullable=False)
    estado = Column(Enum(EstadoUsuario), nullable=False, default=EstadoUsuario.EN_REVISION)
    es_vendedor = Column(Boolean, default=False)
    es_comprador = Column(Boolean, default=True)
    
    productos = relationship("Producto", back_populates="vendedor")
    ventas_como_vendedor = relationship("Venta", foreign_keys="Venta.vendedor_id", back_populates="vendedor")
    ventas_como_comprador = relationship("Venta", foreign_keys="Venta.comprador_id", back_populates="comprador")

class Administrador(Base):
    __tablename__ = "administradores"

    id_admin = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("usuarios.codigo_registro"), nullable=False)
    nombre = Column(String(100))
    
    usuario = relationship("Usuario")

class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    cantidad = Column(Integer, nullable=False)
    categoria = Column(String)
    id_vendedor = Column(Integer, ForeignKey("usuarios.codigo_registro"), nullable=False)
    
    vendedor = relationship("Usuario", back_populates="productos")
    detalles_venta = relationship("DetalleVenta", back_populates="producto")

class Venta(Base):
    __tablename__ = "ventas"

    codigo = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    precio_total = Column(Float, nullable=False)
    vendedor_id = Column(Integer, ForeignKey("usuarios.codigo_registro"), nullable=False)
    comprador_id = Column(Integer, ForeignKey("usuarios.codigo_registro"), nullable=False)
    origen = Column(String(100), nullable=False)
    destino = Column(String(100), nullable=False)
    fecha_despacho = Column(DateTime)
    fecha_entrega = Column(DateTime)
    estado_entrega = Column(Enum(EstadoEntrega), nullable=False, default=EstadoEntrega.PENDIENTE)
    
    vendedor = relationship("Usuario", foreign_keys=[vendedor_id], back_populates="ventas_como_vendedor")
    comprador = relationship("Usuario", foreign_keys=[comprador_id], back_populates="ventas_como_comprador")
    detalles = relationship("DetalleVenta", back_populates="venta")

class DetalleVenta(Base):
    __tablename__ = "detalles_venta"

    id_detalle = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.codigo"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_venta")