import requests
from bs4 import BeautifulSoup, Comment
import csv

URL = "https://www.basketball-reference.com/leaders/pts_career.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

print("🔄 Solicitando la página...")
response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

# Intento 1: buscar la tabla directamente
tabla = soup.find("table", {"id": "leaders"})
if tabla:
    print("✅ Tabla encontrada directamente en el HTML.")
else:
    # Intento 2: buscar en comentarios HTML
    print("🔍 Buscando la tabla en comentarios HTML...")
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        if 'table' in comment and 'leaders' in comment:
            soup_comment = BeautifulSoup(comment, 'html.parser')
            tabla = soup_comment.find("table", {"id": "leaders"})
            if tabla:
                print("✅ Tabla encontrada dentro de comentario HTML.")
                break

if not tabla:
    print("❌ No se encontró la tabla de líderes de puntos.")
    exit()

# Procesar la tabla
filas = tabla.find_all("tr")
print(f"📋 Se encontraron {len(filas)} filas. Procesando datos...")

jugadores = []

for fila in filas:
    celdas = fila.find_all("td")
    if len(celdas) >= 3:
        try:
            nombre = celdas[1].get_text(strip=True).replace("*", "")
            puntos = int(celdas[2].get_text(strip=True).replace(",", ""))
            jugadores.append((nombre, puntos))
        except Exception as e:
            print(f"⚠️ Error procesando fila: {e}")

print(f"✅ Se obtuvieron {len(jugadores)} jugadores.")

# Mostrar primeros 10
for i, (nombre, puntos) in enumerate(jugadores[:10], 1):
    print(f"{i}. {nombre} - {puntos} puntos")

# Guardar CSV
with open("top_250_puntos.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Rank", "Jugador", "Puntos"])
    for i, (nombre, puntos) in enumerate(jugadores, 1):
        writer.writerow([i, nombre, puntos])

print("💾 Archivo CSV guardado como top_250_puntos.csv")
