# FelizViaje

Sistema para generar cotizaciones turísticas en formato PDF a partir de los datos del cliente, vuelos y opciones de hotel, usando FastAPI, Jinja2, Playwright y Chromium.

## Descripción general

Este proyecto combina un backend en Python con un frontend simple para completar una cotización y descargar un PDF listo para enviar al cliente. El flujo es:

1. El usuario completa un formulario en el navegador.
2. El frontend envía un JSON al backend.
3. El servidor valida los datos.
4. La plantilla HTML se renderiza con Jinja2.
5. Chromium, controlado por Playwright, convierte el HTML a PDF.
6. El archivo se devuelve para descarga.

## Stack principal

- Python 3.10+
- FastAPI
- Pydantic
- Jinja2
- Playwright 1.48+
- Chromium
- HTML + CSS + JavaScript

## Estructura del proyecto

```text
FelizViaje/
├── main.py                 # Backend FastAPI
├── template.html           # Plantilla HTML base
├── requirements.txt        # Dependencias del proyecto
├── README.md               # Documentación del proyecto
├── index.html              # Frontend de prueba o demo
├── script.js               # Lógica del formulario
├── style.css               # Estilos del frontend
├── assets/                 # Logos, banners y recursos visuales
├── templates/
│   └── template.html       # Plantilla que usa el backend
├── .gitignore
└── .venv/                  # Entorno virtual local (si aplica)
```

## Requisitos previos

- Python 3.10 o superior
- pip
- Chromium instalado y disponible para Playwright

En Render, Chromium se instala automáticamente mediante el `Dockerfile`. En un entorno local, después de instalar las dependencias Python, instala el navegador con:

```bash
playwright install chromium
```

## Instalación

1. Clona o descarga el proyecto.
2. Entra a la carpeta raíz.
3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Instala Chromium para Playwright si todavía no está instalado:

```bash
playwright install chromium
```

5. Asegúrate de que exista la carpeta `templates` y que el archivo `template.html` esté dentro de ella:

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

### `POST /api/cotizacion/pdf`

Genera un PDF de cotización a partir de un payload JSON.

Ejemplo de request:

```json
{
  "nombre_cliente": "Juan Pérez",
  "destino": "Riviera Maya",
  "segundo_destino": null,
  "precio_total_paquete": null,
  "fecha_salida": "2026-07-15",
  "origen": "Buenos Aires",
  "noches": "7",
  "moneda": "USD",
  "fecha_cotizacion": "2026-09-04",
  "asistencia": "sí",
  "hoteles": [
    {
      "hotel_categoria": "1- PROMO MEJOR PRECIO",
      "hotel_nombre": "Grand Palladium",
      "hotel_estrellas": "⭐⭐⭐⭐⭐",
      "hotel_regimen": "All inclusive",
      "hotel_precio": "1500",
      "hotel_ingreso_primer_destino": null,
      "hotel_destino": null,
      "hotel_descripcion": "Resort de lujo con playa privada",
      "hotel_maps": "https://maps.google.com"
    }
  ]
}
```

El servidor responderá con el PDF generado para descarga. El backend calcula automáticamente el total del paquete, la reserva y la financiación cuando el viaje permite cuotas. La cantidad se muestra como `1 cuota` o `N cuotas` según corresponda.

Cuando se activa el destino múltiple desde el formulario, `segundo_destino` y `precio_total_paquete` son obligatorios. Cada hotel puede incluir `hotel_ingreso_primer_destino` y `hotel_destino`; la fecha de ingreso no puede ser anterior a `fecha_salida`. En ese modo, `precio_total_paquete` representa el precio total por persona del paquete y se muestra en el resumen del PDF.

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

### Usando el frontend servido por FastAPI

1. Levanta el backend.
2. Abre `http://localhost:8000` en el navegador. El backend sirve el frontend y sus recursos.
3. Completa los datos de la cotización y haz clic en el botón para generar el PDF.

### Usando Live Server durante el desarrollo

También puedes abrir `index.html` con Live Server, por ejemplo en `http://127.0.0.1:5500`:

1. Levanta el backend en `http://localhost:8000`.
2. Abre `index.html` con Live Server.
3. El frontend detecta que está en un puerto local distinto de `8000` y envía el `POST` directamente al backend.

No uses la URL de Live Server como endpoint de la API: Live Server solo sirve archivos estáticos y responde `405 Method Not Allowed` ante el `POST`.

En Render, al abrir la URL pública del servicio, el frontend usa automáticamente `/api/cotizacion/pdf` en el mismo origen y no depende de `localhost`.

## Variables y configuración importantes

En `main.py` el backend usa:

- `CORSMiddleware` para habilitar CORS.
- `Jinja2` para renderizar la plantilla HTML.
- `Playwright` y Chromium para convertir HTML a PDF con formato A4 y fondos impresos.
- `Pydantic` para validar el payload recibido.
- `templates/template.html` como plantilla activa del PDF.
- Inter como fuente principal del PDF, cargada desde Google Fonts con fuentes del sistema como respaldo.
- `CHROMIUM_PATH` para indicar una ruta personalizada al ejecutable de Chromium.

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
- estés accediendo al frontend desde el mismo backend (`http://localhost:8000`)

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

El proyecto incluye un `Dockerfile` basado en Python 3.11 que instala Chromium, Inter y las librerías necesarias. En Render crea un **Web Service** conectado al repositorio y selecciona **Docker** como entorno. Render detectará el `Dockerfile` y expondrá la aplicación en el puerto asignado mediante `PORT`.

El contenedor usa `/usr/bin/chromium` mediante la variable `CHROMIUM_PATH` y ejecuta:

```bash
uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}
```

Es importante seleccionar **Docker** en Render. Si se utiliza el entorno nativo de Python, el navegador no se instala automáticamente. En ese caso, configura el Build Command como:

```bash
pip install -r requirements.txt && playwright install --with-deps chromium
```

El error `Executable doesn't exist at /home/.../.cache/ms-playwright/...` significa que ese navegador todavía no fue instalado en el entorno donde corre Uvicorn.

La interfaz y la API se sirven desde el mismo servicio. Al abrir la URL pública de Render se cargará `index.html`, y el frontend usará automáticamente `/api/cotizacion/pdf` sin apuntar a `localhost`.

## Seguridad recomendada

Antes de desplegar a producción, conviene limitar `allow_origins` en `main.py` para que solo acepte dominios autorizados.

## Licencia

Este proyecto está destinado a uso interno o comercial según el contexto del negocio. Revisa la política de la organización antes de distribuirlo en producción.

## Contacto

Proyecto desarrollado para FelizViaje.
