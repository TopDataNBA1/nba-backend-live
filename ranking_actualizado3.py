import time
from jugadores_250 import obtener_jugadores_250
from nba_boxscore import obtener_puntos_partido

def combinar_datos(jugadores_250, puntos_partido):
    combinados = []
    for idx, jugador_data in enumerate(jugadores_250):
        rank, nombre, puntos_totales = jugador_data
        puntos_partido_val = puntos_partido.get(nombre, 0)
        total = puntos_totales + puntos_partido_val
        combinados.append({
            'posicion_inicial': idx + 1,
            'nombre': nombre,
            'puntos_250': puntos_totales,
            'puntos_partido': puntos_partido_val,
            'total': total
        })
    return sorted(combinados, key=lambda x: x['total'], reverse=True)

def detectar_adelantamientos(anterior, actual):
    print("DEBUG: Detectando adelantamientos simplificado...")

    posicion_anterior = {jugador['nombre']: idx+1 for idx, jugador in enumerate(anterior)}
    posicion_actual = {jugador['nombre']: idx+1 for idx, jugador in enumerate(actual)}

    for jugador in actual:
        nombre = jugador['nombre']
        puntos_hoy = jugador['puntos_partido']
        if puntos_hoy <= 0:
            continue

        pos_antes = posicion_anterior.get(nombre, None)
        pos_ahora = posicion_actual.get(nombre, None)

        print(f"DEBUG: {nombre} - puntos hoy: {puntos_hoy}, posición antes: {pos_antes}, posición ahora: {pos_ahora}")

        if pos_antes is not None and pos_ahora is not None and pos_ahora < pos_antes:
            print(f"🔔 {nombre} ({puntos_hoy} puntos hoy) ha subido de la posición {pos_antes} a la {pos_ahora}.")

def mostrar_ranking(ranking):
    print("\n📈 Ranking actualizado (puntos 250 + partido):\n")
    print(f"{'Rank':<5} {'Jugador':<25} {'Pts 250':>10} {'Pts Partido':>12} {'Total':>8}")
    for idx, jugador in enumerate(ranking, 1):
        print(f"{idx:<5} {jugador['nombre']:<25} {jugador['puntos_250']:>10} {jugador['puntos_partido']:>12} {jugador['total']:>8}")

def main():
    anterior = []
    game_id = "0042400404"  # Cambia aquí el partido
    while True:
        print("\n🔄 Actualizando ranking...\n")
        jugadores_250, advertencias = obtener_jugadores_250()
        puntos_en_vivo = obtener_puntos_partido(game_id)
        actual = combinar_datos(jugadores_250, puntos_en_vivo)

        if anterior:
            detectar_adelantamientos(anterior, actual)
        mostrar_ranking(actual)
        anterior = actual
        time.sleep(30)

if __name__ == "__main__":
    main()
