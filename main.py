from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from jugadores_250 import obtener_jugadores_250
from nba_boxscore import obtener_puntos_partido
import time

app = FastAPI()

# Permitir CORS para todas las orígenes (ajusta si quieres restringir)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def combinar_datos(jugadores_250, puntos_partido):
    combinados = []
    for idx, jugador_data in enumerate(jugadores_250):
        rank, nombre, puntos_totales = jugador_data
        nombre = nombre.replace('*', '').strip()
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

@app.get("/ranking/{game_id}")
def ranking_actualizado(game_id: str):
    jugadores_250, advertencias = obtener_jugadores_250()
    puntos_en_vivo = obtener_puntos_partido(game_id)
    ranking_actual = combinar_datos(jugadores_250, puntos_en_vivo)
    return ranking_actual
