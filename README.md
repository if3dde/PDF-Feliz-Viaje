# 🚀 FelizViaje - Backend PDF Generator

**Sistema profesional de generación de PDFs de cotización turística con FastAPI y WeasyPrint**

---

## 📋 Descripción

Backend que recibe datos JSON del frontend FelizViaje, renderiza una plantilla HTML profesional con Jinja2 y genera PDFs de alta calidad usando WeasyPrint.

### Características
✅ API REST con FastAPI  
✅ Renderizado de plantillas Jinja2  
✅ Generación de PDFs con CSS Paged Media (WeasyPrint)  
✅ CORS habilitado para frontend  
✅ Validación de datos con Pydantic  
✅ Logging completo  
✅ Documentación automática con Swagger (/docs)  
✅ Health checks

---

## 🛠️ Instalación

### 1. Requisitos Previos
- **Python 3.9+**
- **pip** (gestor de paquetes)
- **WeasyPrint dependencies**

### 2. Estructura de Directorios

Asegúrate de tener esta estructura:

```
FelizViaje/
├── main.py                 # Backend FastAPI
├── template.html          # Plantilla Jinja2 para PDF
├── requirements.txt       # Dependencias Python
├── templates/            # Carpeta para plantillas (FastAPI la crea)
│   └── template.html    # Copia del template aquí
├── index.html            # Frontend (opcional, para desarrollo)
├── script.js             # Frontend (opcional, para desarrollo)
└── style.css             # Frontend (opcional, para desarrollo)
```

### 3. Instalación de Dependencias

```bash
pip install -r requirements.txt
```

**Nota para Linux:**
```bash
sudo apt-get install -y python3-dev libcairo2-dev libpango-1.0-0 libpango-cairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev libssl-dev
pip install -r requirements.txt
```

### 4. Preparar la Carpeta de Templates

El `main.py` crea automáticamente la carpeta `templates/`. Debes **copiar** `template.html` en esa ubicación:

```bash
# Windows
mkdir templates
copy template.html templates\template.html

# macOS / Linux
mkdir -p templates
cp template.html templates/template.html
```

---

## ▶️ Ejecución

### Opción 1: Ejecución Directa
```bash
python main.py
```

### Opción 2: Con Uvicorn Manual
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Producción
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Verás:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

---

## 📚 API Endpoints

### Health Check
```
GET http://localhost:8000/health
```

### Documentación Interactiva
```
GET http://localhost:8000/docs
```

### Generar PDF (Principal)
```
POST http://localhost:8000/api/cotizacion/pdf
Content-Type: application/json
```

**Request JSON:**
```json
{
  "nombre_cliente": "Juan Pérez",
  "destino": "Riviera Maya",
  "fecha_salida": "2026-07-15",
  "origen": "Buenos Aires",
  "noches": "7",
  "aerolinea_ida": "Aerolineas Argentinas",
  "numero_vuelo_ida": "AR1234",
  "fecha_vuelo_salida": "2026-07-15",
  "aeropuerto_origen": "AEP",
  "hora_salida_ida": "10:30",
  "aeropuerto_destino": "CUN",
  "hora_llegada_ida": "15:45",
  "escala_ida": "0",
  "equipaje": ["Carry on", "Bodega"],
  "aerolinea_regreso": "Aerolineas Argentinas",
  "numero_vuelo_regreso": "AR5678",
  "fecha_vuelo_regreso": "2026-07-22",
  "aeropuerto_origen_regreso": "CUN",
  "hora_salida_regreso": "12:00",
  "aeropuerto_destino_regreso": "AEP",
  "hora_llegada_regreso": "06:15",
  "escala_vuelta": "1",
  "traslado": "Privado",
  "hoteles": [
    {
      "hotel_categoria": "1- PROMO MEJOR PRECIO",
      "hotel_nombre": "Grand Palladium",
      "hotel_estrellas": "⭐⭐⭐⭐⭐",
      "hotel_regimen": "All inclusive",
      "hotel_precio": "1500",
      "hotel_calificacion": "9.2/10",
      "hotel_descripcion": "Resort de lujo con playa privada",
      "hotel_maps": "https://maps.google.com/..."
    }
  ],
  "moneda": "USD",
  "fecha_cotizacion": "2026-09-04",
  "asistencia": "sí",
  "validez_oferta": "7",
  "texto_adicional": "Incluye transfers del aeropuerto"
}
```

**Response:** PDF descargable

---

## 🧪 Prueba Rápida

Con cURL:
```bash
curl -X POST http://localhost:8000/api/cotizacion/pdf \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_cliente":"Test",
    "destino":"Cancún",
    "fecha_salida":"2026-07-15",
    "noches":"7",
    "moneda":"USD",
    "hoteles":[{"hotel_nombre":"Test Hotel","hotel_precio":"1000"}]
  }' \
  -o cotizacion.pdf
```

---

## 🐛 Troubleshooting

### Template not found
```bash
mkdir templates
cp template.html templates/template.html
```

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Failed to fetch desde frontend
- Verifica que el backend está en `http://localhost:8000`
- Revisa que CORS esté habilitado en `main.py` (ya está)
- Usa `http://` no `https://` en desarrollo

---

## 📝 Logs

El servidor genera logs detallados:
```
INFO: 🚀 FelizViaje PDF Generator iniciado
INFO: Solicitud recibida para cliente: Juan Pérez
INFO: PDF generado exitosamente: Cotizacion_Juan_Perez.pdf (45234 bytes)
```

---

## 🔐 Seguridad en Producción

Cambiar CORS antes de desplegar:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tudominio.com"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)
```

---

## 📞 Contacto

**FelizViaje - Sucursal Tribunales**  
Hecho por Federico Fantini  
© 2026 Todos los derechos reservados.
