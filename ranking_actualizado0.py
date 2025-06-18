# ranking_actualizado.py

from nba_boxscore import puntos_partido
from selenium_250 import jugadores_250

# Combinar datos y calcular totales
jugadores_actualizados = []

for orden, nombre, puntos_acumulados in jugadores_250:
    puntos_hoy = puntos_partido.get(nombre, 0)
    total = puntos_acumulados + puntos_hoy
    jugadores_actualizados.append({
        "nombre": nombre,
        "anterior_orden": orden,
        "puntos_previos": puntos_acumulados,
        "puntos_partido": puntos_hoy,
        "total": total
    })

# Ordenar por total actualizado
jugadores_ordenados = sorted(jugadores_actualizados, key=lambda x: x["total"], reverse=True)

# Mostrar resultados y detectar cambios de posición
print(f"{'⬆️⬇️':<3} {'Nuevo':<5} {'Prev':<5} {'Jugador':<25} {'Previos':>8} {'Hoy':>6} {'Total':>7}")
print("=" * 65)

for nuevo_orden, jugador in enumerate(jugadores_ordenados, start=1):
    anterior_orden = jugador["anterior_orden"]
    movimiento = ""

    if nuevo_orden < anterior_orden:
        movimiento = "⬆️"
    elif nuevo_orden > anterior_orden:
        movimiento = "⬇️"
    else:
        movimiento = "⏺️"

    print(f"{movimiento:<3} {nuevo_orden:<5} {anterior_orden:<5} {jugador['nombre']:<25} "
          f"{jugador['puntos_previos']:>8} {jugador['puntos_partido']:>6} {jugador['total']:>7}")

# Notificaciones
print("\n📢 Notificaciones:")
for nuevo_orden, jugador in enumerate(jugadores_ordenados, start=1):
    anterior_orden = jugador["anterior_orden"]
    if nuevo_orden < anterior_orden:
        print(f"🔔 {jugador['nombre']} adelanta a {anterior_orden - nuevo_orden} jugador(es) en el ranking.")
