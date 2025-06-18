import requests

URL = "https://www.basketball-reference.com/leaders/pts_career_p.html"

response = requests.get(URL)
response.raise_for_status()

with open("pagina.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("Página guardada como pagina.html")
