import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import os

# 🔐 VARIABLES (las pondremos en Render)
ACCOUNT_SID = os.environ.get("TWILIO_SID")
AUTH_TOKEN = os.environ.get("TWILIO_TOKEN")
TO_NUMBER = os.environ.get("TO_NUMBER")

# ⚠️ bypass SSL (por tu error)
http_client = TwilioHttpClient()
http_client.session.verify = False

client = Client(ACCOUNT_SID, AUTH_TOKEN, http_client=http_client)

# 📊 archivo donde guardamos último valor
FILE = "ultimo_valor.txt"

def obtener_dolar():
    url = "https://www.google.com/search?q=dolar+peru"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    # Google suele tener este formato (puede cambiar)
    valor = soup.find("span", class_="DFlfde")
    return float(valor.text.replace(",", "."))

def leer_anterior():
    if not os.path.exists(FILE):
        return None
    with open(FILE, "r") as f:
        return float(f.read())

def guardar(valor):
    with open(FILE, "w") as f:
        f.write(str(valor))

def enviar_whatsapp(mensaje):
    client.messages.create(
        from_='whatsapp:+14155238886',
        body=mensaje,
        to=f'whatsapp:{TO_NUMBER}'
    )

def main():
    actual = obtener_dolar()
    anterior = leer_anterior()

    print(f"Actual: {actual} | Anterior: {anterior}")

    if anterior is None or actual != anterior:
        mensaje = f"💸 Dólar Perú: {actual}"
        enviar_whatsapp(mensaje)
        guardar(actual)

if __name__ == "__main__":
    main()