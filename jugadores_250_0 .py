from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

URL = "https://www.basketball-reference.com/leaders/pts_career_p.html"

# Configura Selenium en modo headless
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)

try:
    print("🔄 Cargando la página con Selenium...")
    driver.get(URL)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    tabla = soup.find("table", id="nba")
    if tabla is None:
        print("❌ No se encontró la tabla con id 'nba'")
    else:
        filas = tabla.find_all("tr")
        jugadores = []
        advertencias = []

        for fila in filas[1:]:
            columnas = fila.find_all(["th", "td"])
            if len(columnas) >= 3:
                rank_raw = columnas[0].text.strip().replace(".", "")
                jugador = columnas[1].text.strip()
                puntos_raw = columnas[2].text.strip().replace(",", "")

                try:
                    puntos = int(puntos_raw)
                except ValueError:
                    continue  # No es una fila con puntos válidos

                try:
                    rank = int(rank_raw)
                    jugadores.append((rank, jugador, puntos))
                except ValueError:
                    # No tiene número de orden, pero tiene jugador y puntos
                    jugadores.append((None, jugador, puntos))
                    advertencias.append(f"⚠️ Sin número de orden: {jugador} - {puntos} puntos")

        print(f"✅ Se obtuvieron {len(jugadores)} jugadores (incluyendo los sin orden).")
        print()

        for idx, (rank, jugador, puntos) in enumerate(jugadores, start=1):
            if rank is not None:
                print(f"{rank:3}. {jugador} - {puntos} puntos")
            else:
                print(f"{'---'}. {jugador} - {puntos} puntos (⚠️ sin número de orden)")

        if advertencias:
            print("\n🟨 Advertencias:")
            for advertencia in advertencias:
                print(advertencia)

finally:
    driver.quit()
