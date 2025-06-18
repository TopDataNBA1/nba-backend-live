import requests
import json

game_id = "0042400404"
url = f"https://data.nba.com/data/v2015/json/mobile_teams/nba/2024/scores/gamedetail/{game_id}_gamedetail.json"

response = requests.get(url)
data = response.json()

# Imprimir claves del JSON raíz
print("Claves raíz:", data.keys())

# Intentar imprimir claves dentro de 'g' (si existe)
if 'g' in data:
    print("Claves dentro de 'g':", data['g'].keys())
    # Y dentro de 'pd' si existe
    if 'pd' in data['g']:
        print("Claves dentro de 'pd':", [game.keys() for game in data['g']['pd']])
else:
    print("La clave 'g' no está en el JSON")

# También imprime un ejemplo de jugadores, si puedes identificar la ruta
