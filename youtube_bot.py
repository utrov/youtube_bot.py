# Extraemos y limpiamos la descripción
        descripcion_raw = ultimo_video.get("summary", "Sin descripción disponible.")
        
        # Eliminamos etiquetas HTML si las hay
        import re
        descripcion_limpia = re.sub(r'<[^>]+>', '', descripcion_raw)
        
        # Filtramos líneas que sean enlaces (http/https) o promociones típicas
        lineas = descripcion_limpia.split('\n')
        lineas_utiles = [
            l.strip() for l in lineas 
            if l.strip() and not l.strip().startswith(('http://', 'https://', 'Use el código'))
        ]
        
        resumen_texto = "\n".join(lineas_utiles[:5]) # Cogemos hasta 5 líneas de texto real
        if not resumen_texto:
            resumen_texto = "Consulta la descripción completa en YouTube."
        elif len(resumen_texto) > 300:
            resumen_texto = resumen_texto[:300] + "..."
