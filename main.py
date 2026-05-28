from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI(
    title="API de Prueba",
    description="API básica con FastAPI desplegada en Render",
    version="1.0.1"
)

# ── Base de datos simulada en memoria ──
productos = [
    {"id": 1,  "nombre": "Rosa roja",        "precio": 25.0,  "stock": 100},
    {"id": 2,  "nombre": "Tulipán",          "precio": 18.0,  "stock": 50},
    {"id": 3,  "nombre": "Girasol",          "precio": 15.0,  "stock": 80},
    {"id": 4,  "nombre": "Orquídea",         "precio": 45.0,  "stock": 30},
    {"id": 5,  "nombre": "Lilium",           "precio": 22.0,  "stock": 60},
    {"id": 6,  "nombre": "Calla",            "precio": 28.0,  "stock": 40},
    {"id": 7,  "nombre": "Peonia",           "precio": 35.0,  "stock": 25},
    {"id": 8,  "nombre": "Lavanda",          "precio": 12.0,  "stock": 90},
    {"id": 9,  "nombre": "Margarita",        "precio": 10.0,  "stock": 120},
    {"id": 10, "nombre": "Jazmín",           "precio": 20.0,  "stock": 70},
    {"id": 11, "nombre": "Hortensia",        "precio": 32.0,  "stock": 35},
    {"id": 12, "nombre": "Clavel",           "precio": 8.0,   "stock": 150},
    {"id": 13, "nombre": "Rosa blanca",      "precio": 25.0,  "stock": 100},
    {"id": 14, "nombre": "Fresia",           "precio": 16.0,  "stock": 55},
    {"id": 15, "nombre": "Bouquet mixto",    "precio": 65.0,  "stock": 20},
]


# ── Modelos ──
class Producto(BaseModel):
    nombre: str
    precio: float
    stock: int

class ProductoActualizar(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None


# ── Endpoints ──

@app.get("/")
def raiz():
    return {"mensaje": "API funcionando correctamente", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/productos")
def listar_productos():
    return {"total": len(productos), "productos": productos}


@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int):
    producto = next((p for p in productos if p["id"] == producto_id), None)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@app.post("/productos", status_code=201)
def crear_producto(datos: Producto):
    nuevo_id = max(p["id"] for p in productos) + 1 if productos else 1
    nuevo = {"id": nuevo_id, **datos.model_dump()}
    productos.append(nuevo)
    return nuevo


@app.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, datos: ProductoActualizar):
    producto = next((p for p in productos if p["id"] == producto_id), None)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for campo, valor in datos.model_dump(exclude_none=True).items():
        producto[campo] = valor
    return producto


@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):
    global productos
    producto = next((p for p in productos if p["id"] == producto_id), None)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    productos = [p for p in productos if p["id"] != producto_id]
    return {"mensaje": f"Producto {producto_id} eliminado"}


# ── Arranque para Render ──
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
