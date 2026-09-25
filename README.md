# FelizViaje

Sistema para generar cotizaciones turísticas en formato PDF a partir de datos del cliente y opciones de hotel, usando FastAPI, Jinja2 y WeasyPrint.

## Descripción general

Este proyecto combina un backend en Python con un frontend simple para completar una cotización y descargar un PDF listo para enviar al cliente. El flujo es:

1. El usuario completa un formulario en el navegador.
2. El frontend envía un JSON al backend.
3. El servidor valida los datos.
4. La plantilla HTML se renderiza con Jinja2.
5. WeasyPrint convierte el HTML a PDF.
6. El archivo se devuelve para descarga.

## Stack principal

- Python 3.10+
- FastAPI
- Pydantic
- Jinja2
- WeasyPrint
- HTML + CSS + JavaScript

## Estructura del proyecto

```text
FelizViaje/
├── main.py                 # Backend FastAPI
├── template.html           # Plantilla HTML base
├── requirements.txt        # Dependencias del proyecto
├── README.md               # Documentación del proyecto
├── QUICK_START.md          # Guía rápida
├── index.html              # Frontend de prueba o demo
├── script.js               # Lógica del formulario
├── style.css               # Estilos del frontend
├── templates/
│   └── template.html       # Copia que usa el backend
├── .gitignore
└── .venv/                  # Entorno virtual local (si aplica)
```

## Requisitos previos

- Python 3.10 o superior
- pip
- Dependencias del sistema para WeasyPrint en Linux/macOS

### Dependencias de sistema para Linux

```bash
sudo apt-get update
sudo apt-get install -y python3-dev libcairo2-dev libpango-1.0-0 libpango-cairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev libssl-dev
```

## Instalación

1. Clona o descarga el proyecto.
2. Entra a la carpeta raíz.
3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Asegúrate de que exista la carpeta `templates` y que el archivo `template.html` esté dentro de ella:

```bash
mkdir -p templates
copy template.html templates\template.html
```

En Linux/macOS:

```bash
mkdir -p templates
cp template.html templates/template.html
```

## Ejecución local

### Opción 1: ejecutar directamente

```bash
python main.py
```

### Opción 2: usando Uvicorn

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El backend quedará disponible en:

- http://localhost:8000
- Documentación Swagger: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Endpoint principal

### POST /api/cotizacion/pdf

Genera un PDF de cotización a partir de un payload JSON.

Ejemplo de request:

```json
{
  "nombre_cliente": "Juan Pérez",
  "destino": "Riviera Maya",
  "fecha_salida": "2026-07-15",
  "origen": "Buenos Aires",
  "noches": "7",
  "moneda": "USD",
  "fecha_cotizacion": "2026-09-04",
  "asistencia": "sí",
  "validez_oferta": "7",
  "hoteles": [
    {
      "hotel_categoria": "1- PROMO MEJOR PRECIO",
      "hotel_nombre": "Grand Palladium",
      "hotel_estrellas": "⭐⭐⭐⭐⭐",
      "hotel_regimen": "All inclusive",
      "hotel_precio": "1500",
      "hotel_descripcion": "Resort de lujo con playa privada",
      "hotel_maps": "https://maps.google.com"
    }
  ]
}
```

El servidor responderá con el PDF generado para descarga.

## Prueba rápida con curl

```bash
curl -X POST "http://localhost:8000/api/cotizacion/pdf" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_cliente":"Test User",
    "destino":"Cancún",
    "fecha_salida":"2026-07-15",
    "noches":"7",
    "moneda":"USD",
    "hoteles":[{"hotel_nombre":"Hotel Test","hotel_precio":"1000"}]
  }' \
  -o cotizacion.pdf
```

## Uso con el frontend

1. Levanta el backend.
2. Abre `index.html` en tu navegador o usa Live Server.
3. Completa los datos de la cotización.
4. Haz clic en el botón para generar el PDF.
5. El archivo se descargará automáticamente.

## Variables y configuración importantes

En `main.py` el backend usa:

- `CORSMiddleware` para habilitar CORS.
- `Jinja2` para renderizar la plantilla HTML.
- `Playwright` y Chromium para convertir HTML a PDF.
- `Pydantic` para validar el payload recibido.

> Por defecto, CORS está habilitado para todos los orígenes. En producción es recomendable restringirlos a dominios reales.

## Solución de problemas comunes

### Error: `template not found`

Asegúrate de que el archivo exista en `templates/template.html`.

```bash
mkdir -p templates
cp template.html templates/template.html
```

### Error: `ModuleNotFoundError`

Vuelve a instalar dependencias:

```bash
pip install -r requirements.txt
```

### Error en el frontend: `Failed to fetch`

Revisa que:

- el backend esté corriendo en `http://localhost:8000`
- el puerto sea el correcto
- CORS esté habilitado

## Desarrollo y despliegue

Para desarrollo local:

```bash
python main.py
```

Para producción:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
```

### Render

El proyecto incluye un `Dockerfile` para instalar Chromium y las librerías necesarias. En Render crea un **Web Service** conectado al repositorio y selecciona **Docker** como entorno. Render detectará el `Dockerfile` y expondrá la aplicación en el puerto asignado mediante `PORT`.

La interfaz y la API se sirven desde el mismo servicio. Al abrir la URL pública de Render se cargará `index.html`, y el frontend usará automáticamente `/api/cotizacion/pdf` sin apuntar a `localhost`.

## Seguridad recomendada

Antes de desplegar a producción, conviene limitar `allow_origins` en `main.py` para que solo acepte dominios autorizados.

## Licencia

Este proyecto está destinado a uso interno o comercial según el contexto del negocio. Revisa la política de la organización antes de distribuirlo en producción.

## Contacto

Proyecto desarrollado para FelizViaje.

