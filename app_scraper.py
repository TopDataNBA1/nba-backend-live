import requests
import json
import os

# Paso 0: tabla base inicial (con valores fijos C y valores 0 para D y E)
tabla_base = [
    {"orden": 1, "nombre": "LeBron James", "valor_c": 8289, "valor_d": 0, "valor_e": 8289},
    {"orden": 2, "nombre": "Michael Jordan", "valor_c": 5987, "valor_d": 0, "valor_e": 5987},
    {"orden": 3, "nombre": "Kareem Abdul-Jabbar", "valor_c": 5762, "valor_d": 0, "valor_e": 5762},
    # Añade más jugadores aquí según tu tabla base
]

# Función para extraer game_id de la URL
def obtener_game_id_desde_url(url):
    partes = url.split('/')
    for parte in partes:
        if parte.startswith("00"):
            return parte.split("#")[0]
    return None

# Función que scrapea puntos de un partido dado game_id
def scrapear_puntos_por_partido(game_id):
    url = f"https://stats.nba.com/stats/boxscoretraditionalv2?GameID={game_id}&StartPeriod=0&EndPeriod=0&StartRange=0&EndRange=0&RangeType=0"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": f"https://www.nba.com/game/{game_id}/box-score"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    jugadores = data['resultSets'][0]['rowSet']
    columnas = data['resultSets'][0]['headers']

    idx_nombre = columnas.index('PLAYER_NAME')
    idx_pts = columnas.index('PTS')

    puntos_por_jugador = {}
    for jugador in jugadores:
        nombre = jugador[idx_nombre]
        pts = jugador[idx_pts]
        puntos_por_jugador[nombre] = pts
    return puntos_por_jugador

# Actualizar tabla con datos de varios partidos
def actualizar_tabla_con_partidos(tabla_base, urls_partidos):
    # Inicializamos columna D a 0 antes de sumar
    for fila in tabla_base:
        fila['valor_d'] = 0

    for url in urls_partidos:
        game_id = obtener_game_id_desde_url(url)
        if not game_id:
            print(f"No se pudo extraer game_id de URL: {url}")
            continue
        puntos = scrapear_puntos_por_partido(game_id)

        # Sumar puntos solo para jugadores en tabla_base
        for fila in tabla_base:
            nombre = fila['nombre']
            if nombre in puntos:
                fila['valor_d'] += puntos[nombre]

    # Calcular valor_e = valor_c + valor_d
    for fila in tabla_base:
        fila['valor_e'] = fila['valor_c'] + fila['valor_d']

    # Ordenar tabla por valor_e descendente y actualizar orden
    tabla_base.sort(key=lambda x: x['valor_e'], reverse=True)
    for idx, fila in enumerate(tabla_base, 1):
        fila['orden'] = idx

    return tabla_base

# Detectar adelantamientos comparando tabla antes y después
def detectar_adelantamientos(tabla_antes, tabla_despues):
    orden_antes = {fila['nombre']: fila['orden'] for fila in tabla_antes}
    orden_despues = {fila['nombre']: fila['orden'] for fila in tabla_despues}

    mensajes = []
    for fila in tabla_despues:
        nombre = fila['nombre']
        orden_anterior = orden_antes.get(nombre, None)
        orden_nuevo = fila['orden']
        if orden_anterior and orden_nuevo < orden_anterior:
            jugadores_adelantados = [jug['nombre'] for jug in tabla_antes if orden_nuevo <= jug['orden'] < orden_anterior]
            if jugadores_adelantados:
                adelantado = jugadores_adelantados[0]
                mensaje = f"{nombre} adelantó a {adelantado} y ahora ocupa el puesto {orden_nuevo}."
                mensajes.append(mensaje)
    return mensajes

# Guardar tabla en archivo JSON
def guardar_tabla(tabla, nombre_archivo="tabla.json"):
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        json.dump(tabla, f, indent=2, ensure_ascii=False)

# Cargar tabla desde archivo JSON
def cargar_tabla(nombre_archivo="tabla.json"):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return None

if __name__ == "__main__":
    # Aquí defines las URLs de los partidos a analizar
    urls_partidos = [
        "https://www.nba.com/game/okc-vs-ind-0042400404/box-score#box-score",
        # añade más URLs aquí, las cambiarás manualmente cada jornada
    ]

    print("Cargando tabla previa...")
    tabla_anterior = cargar_tabla()
    if tabla_anterior is None:
        print("No hay tabla previa guardada, uso tabla base inicial.")
        tabla_anterior = tabla_base.copy()
    else:
        print("Tabla previa cargada.")

    print("Actualizando tabla con datos de partidos...")
    tabla_actualizada = actualizar_tabla_con_partidos(tabla_anterior, urls_partidos)

    print("\nTabla actualizada:")
    for fila in tabla_actualizada:
        print(f"{fila['orden']}. {fila['nombre']} - C:{fila['valor_c']} + D:{fila['valor_d']} = E:{fila['valor_e']}")

    print("\nDetectando adelantamientos...")
    mensajes = detectar_adelantamientos(tabla_anterior, tabla_actualizada)
    if mensajes:
        for m in mensajes:
            print(m)
    else:
        print("No hay adelantamientos en esta actualización.")

    print("\nGuardando tabla actualizada para próxima comparación...")
    guardar_tabla(tabla_actualizada)
    print("¡Hecho!")
