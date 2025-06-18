from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

url = "https://www.nba.com/game/okc-vs-ind-0042400404/box-score#box-score"
print("🔄 Cargando página del partido...")
driver.get(url)

# Espera y scroll para cargar contenido dinámico
WebDriverWait(driver, 40).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)  # espera extra por si carga contenido al hacer scroll

# Guardamos screenshot para revisar qué ve selenium
driver.save_screenshot("boxscore_debug.png")
print("📸 Captura de pantalla guardada como boxscore_debug.png")

try:
    # Buscar tabla visible (por role='grid')
    table = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "table[role='grid']"))
    )
    print("✅ Tabla cargada.")

    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
    print(f"Filas totales encontradas: {len(rows)}")

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) > 0:
            player = cells[0].text.strip()
            pts = cells[-1].text.strip()  # normalmente puntos están al final
            if player and pts:
                print(f"{player}: {pts}")

except Exception as e:
    print("⚠️ Error al extraer datos:", e)

finally:
    driver.quit()
