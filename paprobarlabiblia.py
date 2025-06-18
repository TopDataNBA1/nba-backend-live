import requests
from bs4 import BeautifulSoup

URL = "https://www.basketball-reference.com/leaders/pts_career_p.html"

def obtener_tabla_base():
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    tabla = soup.find('table', id='nba')
    if not tabla:
        raise Exception("❌ No se encontró la tabla con id='nba'")

    datos = []
    filas = tabla.find_all('tr')
    for fila in filas:
        celdas = fila.find_all('td')
        if len(celdas) != 3:
            continue

        orden_text = celdas[0].text.strip().replace('.', '')
        if not orden_text.isdigit():
            continue
        orden = int(orden_text)

        nombre_tag = celdas[1].find('a')
        nombre = nombre_tag.text.strip() if nombre_tag else celdas[1].text.strip()

        puntos_texto = celdas[2].text.strip().replace(',', '')
        if not puntos_texto.isdigit():
            continue
        valor_c = int(puntos_texto)

        datos.append({
            "orden": orden,
            "nombre": nombre,
            "valor_c": valor_c,
            "valor_d": 0
        })

    return datos

if __name__ == "__main__":
    tabla_base = obtener_tabla_base()
    for fila in tabla_base[:20]:
        print(f"{fila['orden']}. {fila['nombre']} - {fila['valor_c']} points")
