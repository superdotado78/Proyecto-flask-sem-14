# repository.py
# ------------------------------------------------------------
# Persistencia con SQLite (sin librerías externas).
# Abstracciones mínimas para CRUD de productos.
# ------------------------------------------------------------
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import List, Optional
from models import Producto

# Ruta del archivo SQLite en la raíz del proyecto
DB_PATH = Path(__file__).resolve().parent / "inventario.db"

def get_connection() -> sqlite3.Connection:
    """Devuelve una conexión nueva (row_factory habilitada)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Crea la tabla 'productos' si no existe."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS productos (
                id       INTEGER PRIMARY KEY,
                nombre   TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio   REAL  NOT NULL
            )
            """
        )
        conn.commit()

# ------------------------- CRUD -----------------------------

def crear_producto(p: Producto) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO productos (id, nombre, cantidad, precio) VALUES (?, ?, ?, ?)",
            (p.id, p.nombre, p.cantidad, p.precio),
        )
        conn.commit()

def eliminar_producto(id_: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM productos WHERE id = ?", (id_,))
        conn.commit()

def actualizar_cantidad(id_: int, cantidad: int) -> None:
    with get_connection() as conn:
        conn.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (cantidad, id_))
        conn.commit()

def actualizar_precio(id_: int, precio: float) -> None:
    with get_connection() as conn:
        conn.execute("UPDATE productos SET precio = ? WHERE id = ?", (precio, id_))
        conn.commit()

def actualizar_nombre(id_: int, nombre: str) -> None:
    with get_connection() as conn:
        conn.execute("UPDATE productos SET nombre = ? WHERE id = ?", (nombre, id_))
        conn.commit()

def obtener_por_id(id_: int) -> Optional[Producto]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM productos WHERE id = ?", (id_,)).fetchone()
        if not row:
            return None
        return Producto(row["id"], row["nombre"], row["cantidad"], row["precio"])

def buscar_por_nombre(patron: str) -> List[Producto]:
    patron_like = f"%{(patron or '').strip()}%"
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM productos WHERE LOWER(nombre) LIKE LOWER(?) ORDER BY id",
            (patron_like,),
        ).fetchall()
        return [Producto(r["id"], r["nombre"], r["cantidad"], r["precio"]) for r in rows]

def listar_todos() -> List[Producto]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM productos ORDER BY id").fetchall()
        return [Producto(r["id"], r["nombre"], r["cantidad"], r["precio"]) for r in rows]
