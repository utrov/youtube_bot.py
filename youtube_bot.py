import os
import requests

# Configuración de Telegram (lee los secretos que ya tienes o configura nuevos)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Error al enviar mensaje: {response.text}")

def main():
    # Aquí irá la lógica para comprobar los canales de YouTube:
    # @labolsaconfern y @academiadeinversoresusa
    
    # Mensaje de prueba simulado para verificar que funciona
    mensaje = (
        "📥 Canal: `@labolsaconfern`\n\n"
        "*ANÁLISIS DE MERCADO: Ejemplo de prueba*\n\n"
        "* **`MSFT`** (Microsoft) 💰\n"
        "  * **Precio actual:** `$415.50`\n"
        "  * **Intención:** 🟢 Interés de Compra / Acumulación\n"
        "  * **Explicación:** Prueba del sistema automatizado.\n"
        "  * **Precio / Referencia:** Soporte clave en torno a los $400.\n"
        "  * **Minuto:** [`04:15`](https://youtu.be/dQw4w9WgXcQ?t=255)"
    )
    
    enviar_telegram(mensaje)

if __name__ == "__main__":
    main()
