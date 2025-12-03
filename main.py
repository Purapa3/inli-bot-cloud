import os
import time
import requests
from bs4 import BeautifulSoup

URL = "https://www.inli.fr/locations/offres/val-doise-departement_d:95"
BUDGET_MAX = 950

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SEEN = set()

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        r = requests.post(url, json=payload)
        print("📩 Telegram envoyé :", r.text)
    except Exception as e:
        print("Erreur Telegram :", e)

def fetch_page():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers)
    return BeautifulSoup(r.text, "html.parser")

def scrape():
    print("🔍 Analyse de la page…")
    soup = fetch_page()

    items = soup.find_all("div", class_="featured-item")
    print("📌 Annonces trouvées :", len(items))

    for item in items:
        try:
            title = item.find("div", class_="featured-details").get_text(strip=True)
            price_txt = item.find("div", class_="featured-price").get_text(strip=True)

            price = int(
                price_txt.lower()
                .replace("€", "")
                .replace(" ", "")
                .replace("cc", "")
                .replace(",", "")
                .strip()
            )

            link = "https://www.inli.fr" + item.find("a")["href"]

            if "2 pièces" not in title.lower() and "t2" not in title.lower():
                continue

            if price > BUDGET_MAX:
                continue

            if link in SEEN:
                continue

            message = f"🏡 Nouveau T2 détecté !\n\n{title}\nPrix : {price}€\n\n🔗 {link}"

            print("✨ NOUVEAU T2 :", title, price)
            send_telegram(message)

            SEEN.add(link)

        except Exception as e:
            print("Erreur extraction :", e)

if __name__ == "__main__":
    print("🚀 INLI BOT V3 — Notifications Telegram — Mode Cloud Railway")
    while True:
        scrape()
        time.sleep(300)

while True:
    analyser_page()   # ta fonction d’analyse
    time.sleep(60)    # attends 1 min avant la prochaine analyse

import time

while True:
    analyser_page()   # ou le nom de ta fonction principale
    time.sleep(60)    # attends 1 minute avant de recommencer

