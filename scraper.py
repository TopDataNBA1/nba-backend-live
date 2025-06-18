print("Script iniciado")
import json
import time
import copy
import firebase_admin
from firebase_admin import credentials, messaging

# Inicializar Firebase Admin con el archivo de credenciales
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Simula las tablas con columnas A-E
# Col A: nº orden
# Col B: nombre
# Col C: valor base (de la web que actualiza 1 vez al día)
# Col D: valor dinámico (de web que actualiza cada 30 seg)
# Col E: suma C + D si D existe, sino C

# Datos iniciales simulados
tabla_base = [
    {"orden": 1, "nombre": "Elemento A", "valor_c": 100, "valor_d": 0},
    {"orden": 2, "nombre": "Elemento B", "valor_c": 90, "valor_d": 0},
    {"orden": 3, "nombre": "Elemento C", "valor_c": 80, "valor_d": 0},
    {"orden": 4, "nombre": "Elemento D", "valor_c": 70, "valor_d": 0},
    {"orden": 5, "nombre": "Elemento E", "valor_c": 60, "valor_d": 0},
]

# Guarda el estado previo para detectar cambios
datos_previos = copy.deepcopy(tabla_base)

def calcular_valor_e(fila):
    return fila["valor_c"] + fila["valor_d"]

def enviar_notificacion(titulo, cuerpo):
    message = messaging.Message(
        notification=messaging.Notification(
            title=titulo,
            body=cuerpo,
        ),
        topic="todos",  # todos los usuarios suscritos a este topic recibirán la notificación
    )
    response = messaging.send(message)
    print(f"✔ Notificación enviada: {response}")

NOMBRE_TABLA = "puntos"  # Nombre de la tabla

TABLE_NAME = "points"  # Table name

TABLE_NAME = "points"  # Table name

def actualizar_tabla():
    global datos_previos
    print("Running update...")
    import random
    tabla_actualizada = copy.deepcopy(tabla_base)
    for fila in tabla_actualizada:
        fila["valor_d"] = random.randint(0, 20)
        fila["valor_e"] = calcular_valor_e(fila)

    tabla_actualizada.sort(key=lambda x: x["valor_e"], reverse=True)

    for idx, fila in enumerate(tabla_actualizada):
        nombre = fila["nombre"]
        nuevo_valor_e = fila["valor_e"]
        posiciones_anteriores = [i for i, f in enumerate(datos_previos) if f["nombre"] == nombre]
        if posiciones_anteriores:
            pos_ant = posiciones_anteriores[0]
            # Notify only if the element moves up in ranking (pos_ant > idx)
            if pos_ant > idx:
                overtaken_element = datos_previos[idx]["nombre"]
                current_position = idx + 1
                title = f"{nombre} overtakes {overtaken_element}"
                body = f"{nombre} overtakes {overtaken_element} and moves into {current_position} place on the all-time list with {nuevo_valor_e} {TABLE_NAME}"
                print(f"🔔 {body}")
                enviar_notificacion(title, body)

    datos_previos = tabla_actualizada

    print("Updated table:")
    for idx, fila in enumerate(tabla_actualizada):
        print(f"{idx + 1}. {fila['nombre']} - Value E: {fila['valor_e']} (C: {fila['valor_c']}, D: {fila['valor_d']})")
    print("-" * 40)

if __name__ == "__main__":
    print("Iniciando monitor de cambios en tabla (prueba una sola vez)...")
    actualizar_tabla()
    input("Presiona Enter para salir...")  # Pausa para ver la salida
