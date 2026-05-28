from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_raiz():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["mensaje"] == "API funcionando correctamente"


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_listar_productos():
    res = client.get("/productos")
    assert res.status_code == 200
    assert res.json()["total"] == 15


def test_obtener_producto():
    res = client.get("/productos/1")
    assert res.status_code == 200
    assert res.json()["nombre"] == "Rosa roja"


def test_producto_no_existe():
    res = client.get("/productos/999")
    assert res.status_code == 404


def test_crear_producto():
    nuevo = {"nombre": "Orquídea", "precio": 35.0, "stock": 20}
    res = client.post("/productos", json=nuevo)
    assert res.status_code == 201
    assert res.json()["nombre"] == "Orquídea"
    assert res.json()["id"] > 0


def test_actualizar_producto():
    res = client.put("/productos/1", json={"precio": 30.0})
    assert res.status_code == 200
    assert res.json()["precio"] == 30.0


def test_eliminar_producto():
    res = client.delete("/productos/1")
    assert res.status_code == 200
    assert "eliminado" in res.json()["mensaje"]
