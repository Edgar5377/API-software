from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
# En esta queremos validar si el usuario 21345 cuenta con todos sus contactos
def test_obtener_contactos():
    response = client.get("/billetera/contactos/?minumero=21345")
    assert response.status_code == 200
    assert "Luisa" in response.json()['123']
    assert "Andrea" in response.json()["456"]

# En esta queremos validar que se puede realizar un pago
def test_realizar_pago():
    response = client.get("/billetera/pagar?minumero=123&numerodestino=456&valor=50")
    assert response.status_code == 200
    assert "Transferencia exitosa" in response.json()["message"]

# En esta que quiere validar el recibo de un saldo hacia luisa
def test_obtener_historial():
    response = client.get("/billetera/historial?minumero=123")
    assert response.status_code == 200
    assert "Saldo de Luisa" in response.json()["message"]
    assert "Pago recibido de 50" in response.json()["message"]

# En este caso es una prueba de Saldo, para ver el mensaje de error
def test_saldo_insuficiente():
    response = client.get("/billetera/pagar?minumero=123&numerodestino=456&valor=500")
    assert response.status_code == 200
    assert "Saldo insuficiente" in response.json()["message"]

# En este caso que pasa si no se encuentra una cuenta en el sistema
def test_cuenta_no_encontrada():
    response = client.get("/billetera/historial?minumero=999")
    assert response.status_code == 200
    assert "Número de cuenta no encontrado" in response.json()["message"]
