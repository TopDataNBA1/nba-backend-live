import time
from jugadores_250 import obtener_jugadores_250
from nba_boxscore import obtener_puntos_partido

def combinar_datos(jugadores_250, puntos_partido):
    combinados = []
    for idx, jugador_data in enumerate(jugadores_250):
        rank, nombre, puntos_totales = jugador_data
        nombre = nombre.replace('*', '').strip()  # ✅ Eliminar asteriscos y espacios
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

def diagnostico_posiciones(anterior, actual, nombres_interes):
    print("\nDEBUG Diagnóstico posiciones:")
    print(f"{'Jugador':<25} {'Pos antes':>8} {'Pts antes':>10} {'Pos ahora':>9} {'Pts ahora':>9}")
    pos_antes = {j['nombre']: idx + 1 for idx, j in enumerate(anterior)}
    pos_ahora = {j['nombre']: idx + 1 for idx, j in enumerate(actual)}
    pts_antes = {j['nombre']: j['total'] for j in anterior}
    pts_ahora = {j['nombre']: j['total'] for j in actual}
    for nombre in nombres_interes:
        print(f"{nombre:<25} {pos_antes.get(nombre, '-'):>8} {pts_antes.get(nombre, '-'):>10} {pos_ahora.get(nombre, '-'):>9} {pts_ahora.get(nombre, '-'):>9}")

def detectar_adelantamientos(anterior, actual):
    anteriores_dict = {jugador['nombre']: jugador for jugador in anterior}
    actuales_dict = {jugador['nombre']: jugador for jugador in actual}

    for idx, jugador in enumerate(actual):
        nombre = jugador['nombre']
        puntos_hoy = jugador['puntos_partido']
        if puntos_hoy <= 0:
            continue

        puntos_antes = anteriores_dict[nombre]['puntos_250']
        puntos_actuales = jugador['total']
        posicion_actual = idx + 1

        adelantados = []
        for otro in anterior:
            if otro['nombre'] == nombre:
                continue
            if otro['puntos_250'] > puntos_antes:
                if puntos_actuales > actuales_dict[otro['nombre']]['total']:
                    adelantados.append(otro['nombre'])

        if adelantados:
            lista_adelantados = ", ".join(adelantados)
            print(f"🔔 {nombre} ({puntos_hoy} puntos hoy) ha adelantado a {lista_adelantados} "
                  f"y se sitúa {posicion_actual}º en la lista de todos los tiempos con {puntos_actuales} puntos.")

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

        actual = sorted(actual, key=lambda x: x['total'], reverse=True)

        if anterior:
            nombres_interes = ["Pascal Siakam", "Shai Gilgeous-Alexander"]
            diagnostico_posiciones(anterior, actual, nombres_interes)
            detectar_adelantamientos(anterior, actual)

        mostrar_ranking(actual)
        anterior = actual
        time.sleep(30)

if __name__ == "__main__":
    main()
