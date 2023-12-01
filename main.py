from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

class Cuenta:
    def __init__(self, numero, titular, saldo, conexiones):
        self.numero = numero
        self.titular = titular
        self.saldo = saldo
        self.conexiones = conexiones

        self.operaciones = []

    def __str__(self):
        return f"Cuenta: {self.numero}, Titular: {self.titular}, Saldo: {self.saldo}, Conexiones: {self.conexiones}"

    @staticmethod
    def buscar_por_numero(numero_buscado, lista_cuentas):
        for cuenta in lista_cuentas:
            if cuenta.numero == numero_buscado:
                return cuenta
        return None

    def pagar(self, numerodestino, monto):
        cuenta_destino = Cuenta.buscar_por_numero(numerodestino, BD)
        if cuenta_destino:
            if self.saldo >= monto:
                self.saldo -= monto
                cuenta_destino.saldo += monto

                fecha_realizacion = datetime.now().strftime("%d/%m/%Y")
                self.operaciones.append(Operacion(self.numero, fecha_realizacion, monto, 0))
                cuenta_destino.operaciones.append(Operacion(cuenta_destino.numero, fecha_realizacion, monto, 1))
                return f"Transferencia exitosa de {monto} desde {self.numero} a {numerodestino}. Realizado en {fecha_realizacion}"
            else:
                return "Saldo insuficiente para realizar la transferencia"
        else:
            return "Número de cuenta destino no encontrado"

    def obtener_historial(self):
        operaciones_cuenta = [f"Saldo de {self.titular}: {self.saldo}"]

        for operacion in self.operaciones:
            fecha_format = datetime.strptime(operacion.fecha, "%d/%m/%Y").strftime("%d/%m/%Y")
            if operacion.recibido == 1:
                descripcion = f"Pago recibido de {operacion.valor} de {self.titular} monto {operacion.valor}"
            else:
                descripcion = f"Pago realizado de {operacion.valor} de {self.titular} monto {operacion.valor}"
            operaciones_cuenta.append(f"{descripcion} en {fecha_format}")

        return {"message": "\n".join(operaciones_cuenta)}

class Operacion:
    def __init__(self, numeroDestino, fecha, valor, recibido):
        self.numeroDestino = numeroDestino
        self.fecha = fecha
        self.valor = valor
        self.recibido = recibido

    def __str__(self):
        return f"Numero Destino: {self.numeroDestino}, Fecha: {self.fecha}, Valor: {self.valor}"

# Lista de cuentas
BD = []
OPERACIONES = []

# Funciones de ayuda TEST
def agregar_cuenta(numero, titular, saldo, conexiones):
    cuenta = Cuenta(numero, titular, saldo, conexiones)
    BD.append(cuenta)

# Agregar cuentas a la lista BD
agregar_cuenta("21345", "Arnaldo", 200, ["123", "456"])
agregar_cuenta("123", "Luisa", 400, ["456"])
agregar_cuenta("456", "Andrea", 300, ["21345"])

def buscar_cuenta_por_numero(numero):
    for cuenta in BD:
        if cuenta.numero == numero:
            contactos = {}
            for contacto in cuenta.conexiones:
                cuenta_contacto = Cuenta.buscar_por_numero(contacto, BD)
                if cuenta_contacto:
                    contactos[cuenta_contacto.numero] = cuenta_contacto.titular
            return contactos
    return {"message": "La cuenta no se encontró."}

# Endpoints de nuestra API
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/billetera/contactos/")
async def getContacts(minumero: str = ""):
    return buscar_cuenta_por_numero(minumero)

@app.get("/billetera/pagar")
async def pagar(minumero: str, numerodestino: str, valor: float):
    cuenta_origen = Cuenta.buscar_por_numero(minumero, BD)

    if cuenta_origen:
        resultado = cuenta_origen.pagar(numerodestino, valor)
        return {"message": resultado}
    else:
        return {"message": "Número de cuenta origen no encontrado"}

@app.get("/billetera/historial")
async def historial(minumero: str):
    cuenta = Cuenta.buscar_por_numero(minumero, BD)
    if cuenta:
        return cuenta.obtener_historial()
    else:
        return {"message": "Número de cuenta no encontrado"}
