import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

URL = "https://www.inli.fr/locations/offres/val-doise-departement_d:95"
BUDGET_MAX = 950
EMAIL_SENDER = "mouaddahim@gmail.com"
EMAIL_TO = "mouaddahim@gmail.com"
APP_PASSWORD = "vzbp iqar udtk coiv"

SEEN = set()

def send_email(title, price, link):
    msg = MIMEMultipart()
    msg["Subject"] = f"Nouveau T2 détecté ({price}€)"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_TO

    html = f"""<h3>Nouveau logement T2</h3>
<p><b>{title}</b></p>
<p>Prix : <b>{price}€</b></p>
<p>Lien : <a href='{link}'>Voir l’annonce</a></p>"""

    msg.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_SENDER, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email envoyé !")
    except Exception as e:
        print("Erreur email :", e)

def fetch_page():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers)
    return BeautifulSoup(r.text, "html.parser")

def scrape():
    print("Analyse de la page…")
    soup = fetch_page()

    items = soup.find_all("div", class_="featured-item")
    print("Annonces trouvées :", len(items))

    for item in items:
        try:
            title = item.find("div", class_="featured-details").get_text(strip=True)
            price_txt = item.find("div", class_="featured-price").get_text(strip=True)
            price = int(price_txt.replace("€", "").replace(" ", "").strip())
            link = "https://www.inli.fr" + item.find("a")["href"]

            if "2 pièces" not in title.lower() and "t2" not in title.lower():
                continue

            if price > BUDGET_MAX:
                continue

            if link in SEEN:
                continue

            print("NOUVEAU T2 :", title, price, link)
            send_email(title, price, link)
            SEEN.add(link)

        except Exception as e:
            print("Erreur extraction :", e)

if __name__ == "__main__":
    print("INLI BOT V3 — Mode Cloud Railway actif")

    while True:
        scrape()
        time.sleep(300)
