import requests

DEFAULT_GAME_ID = "0042400404"  # Cambia aquí el game_id cuando quieras otro partido

def obtener_puntos_partido(game_id=DEFAULT_GAME_ID):
    """
    Obtiene los puntos de cada jugador en un partido NBA, usando la API JSON.
    Devuelve un dict { 'Nombre Completo': puntos }.
    """
    url = (f"https://data.nba.com/data/v2015/json/mobile_teams/nba/2024/"
           f"scores/gamedetail/{game_id}_gamedetail.json")
    print(f"🔄 Descargando datos de {url} ...")
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json().get('g', {})

    puntos_por_jugador = {}
    for lado in ('hls', 'vls'):
        equipo = data.get(lado, {})
        jugadores = equipo.get('pstsg', [])
        for p in jugadores:
            nombre = f"{p.get('fn','').strip()} {p.get('ln','').strip()}"
            try:
                pts = int(p.get('pts', 0))
            except (ValueError, TypeError):
                pts = 0
            puntos_por_jugador[nombre] = pts

    return puntos_por_jugador


if __name__ == "__main__":
    datos = obtener_puntos_partido()
    print("\n📊 Puntos por jugador en el partido:")
    for nombre, pts in datos.items():
        print(f"{nombre}: {pts}")
