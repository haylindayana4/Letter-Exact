"""
🗄️ CONFIGURACIÓN DE BASE DE DATOS - HERRAMIENTA PEDAGÓGICA

Este archivo configura la conexión a la base de datos SQLite.
SQLAlchemy es una biblioteca que facilita trabajar con bases de datos.

📚 CONCEPTOS PARA APRENDER:
- Motor (Engine): La conexión principal a la base de datos
- Sesión: Una "conversación" temporal con la base de datos
- ORM: Object-Relational Mapping (traduce objetos Python a tablas SQL)
- Dependencias: FastAPI puede "inyectar" automáticamente la sesión de BD

📚 ¿POR QUÉ USAMOS SESIONES?
- Agrupan múltiples operaciones de base de datos
- Permiten hacer "rollback" si algo sale mal
- Mejoran el rendimiento al reutilizar conexiones
"""

from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# --- Configuración de la Base de Datos ---

# Esta es la "cadena de conexión". Le dice a SQLAlchemy dónde está nuestra base de datos y de qué tipo es.
# En este caso, estamos usando SQLite, que es una base de datos basada en un solo archivo.
cadena_de_conexion = "sqlite:///usuarios.db"

# SQLite, por defecto, solo permite que un hilo (thread) hable con él a la vez.
# Como FastAPI puede usar múltiples hilos, necesitamos decirle a SQLite que permita conexiones desde diferentes hilos.
connect_args = {"check_same_thread": False}

# Aquí creamos el "motor" (engine) de la base de datos.
engine = create_engine(cadena_de_conexion, connect_args=connect_args)

# Creamos una "fábrica" de sesiones llamada SessionLocal.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# --- Dependencia de FastAPI para la Sesión ---

def get_db():
    """
    Función generadora que proporciona sesiones de base de datos.
    FastAPI la usa automáticamente cuando ve SessionDepends.
    """
    with SessionLocal() as session:
        yield session

# Dependencia que FastAPI puede inyectar automáticamente
SessionDepends = Annotated[Session, Depends(get_db)]