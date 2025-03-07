import requests
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt_tab')

def resumir_titulo(title, max_palabras=20):
    palabras = word_tokenize(title)
    return " ".join(palabras[:max_palabras]) + ("..." if len(palabras) > max_palabras else "")

def obtener_noticias_nba(favorite_teams):
    url_base = "https://www.reddit.com/r/nba/search.json"
    headers = {"User-Agent": "BerryPiDashboard/1.0"}
    noticias_filtradas = []

    for equipo in favorite_teams:
        params = {"q": equipo, "sort": "hot", "limit": 5, "restrict_sr": "on"}
        response = requests.get(url_base, headers=headers, params=params)
        
        if response.status_code == 200:
            posts = response.json()["data"]["children"]
            for post in posts:
                titulo_resumido = resumir_titulo(post["data"]["title"])
                noticias_filtradas.append({"title": titulo_resumido, "url": post["data"]["url"]})

    return noticias_filtradas

