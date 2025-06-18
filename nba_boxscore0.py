import requests

def obtener_estadisticas(game_id):
    url = f"https://data.nba.com/data/v2015/json/mobile_teams/nba/2024/scores/gamedetail/{game_id}_gamedetail.json"
    print(f"🔄 Descargando datos de {url} ...")
    
    response = requests.get(url)
    data = response.json()
    
    local_players = data['g']['hls']['pstsg']
    visitor_players = data['g']['vls']['pstsg']
    
    print("\n🏠 Equipo local:")
    for player in local_players:
        nombre_completo = f"{player['fn']} {player['ln']}"
        puntos = player['pts']
        print(f"{nombre_completo}: {puntos} puntos")
    
    print("\n✈️ Equipo visitante:")
    for player in visitor_players:
        nombre_completo = f"{player['fn']} {player['ln']}"
        puntos = player['pts']
        print(f"{nombre_completo}: {puntos} puntos")

if __name__ == "__main__":
    # Cambia aquí por el game_id que quieras analizar
    game_id = "0042400404"
    obtener_estadisticas(game_id)
