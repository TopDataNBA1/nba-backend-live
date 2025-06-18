import requests
from bs4 import BeautifulSoup, Comment

URL = "https://www.basketball-reference.com/leaders/pts_career_p.html"

def obtener_tabla_base():
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscar la tabla dentro de los comentarios HTML
    comentarios = soup.find_all(string=lambda text: isinstance(text, Comment))

    tabla = None
    for comentario in comentarios:
        if 'id="leaders"' in comentario:
            soup_comentario = BeautifulSoup(comentario, 'html.parser')
            tabla = soup_comentario.find('table', id='leaders')
            break

    if not tabla:
        raise Exception("No se encontró la tabla con id='leaders'")

    datos = []
    for fila in tabla.tbody.find_all('tr'):
        if fila.get('class') == ['thead']:
            continue  # saltar filas repetidas de encabezado

        celdas = fila.find_all('td')
        if not celdas:
            continue

        orden = int(fila.find('th').text.strip())
        nombre = celdas[0].text.strip()
        valor_c = int(celdas[1].text.strip().replace(',', ''))

        datos.append({
            "orden": orden,
            "nombre": nombre,
            "valor_c": valor_c,
            "valor_d": 0
        })

        if len(datos) >= 250:
            break  # limitamos a 250 filas si quieres

    return datos

if __name__ == "__main__":
    tabla_base = obtener_tabla_base()
    for fila in tabla_base:
        print(f"{fila['orden']}. {fila['nombre']} - {fila['valor_c']} points")
