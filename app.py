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
    url = "https://api.exchangerate.host/latest?base=USD&symbols=PEN"

    response = requests.get(url, timeout=10)

    # 👇 AQUÍ VA EL DEBUG (justo después del request)
    print("Status:", response.status_code)
    print("Response:", response.text)

    if response.status_code != 200:
        print("Error HTTP:", response.status_code)
        return None

    try:
        data = response.json()
        precio = data["rates"]["PEN"]
        return precio

    except Exception as e:
        print("Error parseando JSON:", e)
        return None

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
