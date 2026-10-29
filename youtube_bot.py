import os
import json
import feedparser
import requests

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

CANALES = {
    "@labolsaconfern": "https://www.youtube.com/feeds/videos.xml?channel_id=UCf932WZebrzMZnn1DR9YQLg"
}

CACHE_FILE = "videos_procesados.json"

def cargar_procesados():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def guardar_procesados(procesados):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(procesados, f, ensure_ascii=False, indent=4)

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Error al enviar mensaje: {response.text}")
    except Exception as e:
        print(f"Excepción al conectar con Telegram: {e}")

def main():
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Faltan las credenciales de Telegram en las variables de entorno.")
        return

    procesados = cargar_procesados()
    nuevos_procesados = list(procesados)
    hubo_novedades = False

    for nombre_canal, feed_url in CANALES.items():
        print(f"Revisando feed de {nombre_canal}...")
        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            print(f"No se pudo leer el feed de {nombre_canal}: {e}")
            continue

        if not feed.entries:
            print(f"No hay entradas recientes en {nombre_canal}.")
            continue

        ultimo_video = feed.entries[0]
        video_id = ultimo_video.get("yt_videoid", ultimo_video.get("id"))
        titulo = ultimo_video.get("title", "Sin título")
        link = ultimo_video.get("link", "#")

        if video_id in procesados:
            print(f"-> El último contenido de {nombre_canal} ya fue notificado.")
            continue

        print(f"¡Nuevo contenido detectado en {nombre_canal}: {titulo}!")

        mensaje = "📥 Canal: `" + str(nombre_canal) + "`\n\n*NUEVO CONTENIDO / DIRECTO*\n\n• *" + str(titulo) + "* 💰\n  • **Enlace:** [Ver en YouTube](" + str(link) + ")"

        enviar_telegram(mensaje)
        nuevos_procesados.append(video_id)
        hubo_novedades = True

    if hubo_novedades:
        guardar_procesados(nuevos_procesados)
        print("Caché de vídeos actualizada correctamente.")
    else:
        print("Todo al día. Ningún contenido nuevo en esta ejecución.")

if __name__ == "__main__":
    main()
