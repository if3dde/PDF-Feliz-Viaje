# 🏗️ Arquitectura FelizViaje - PDF Generator

## 📊 Flujo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                     NAVEGADOR (FRONTEND)                         │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  index.html - Formulario de Cotización                   │   │
│  │  - Cliente y destino                                     │   │
│  │  - Vuelos ida/regreso (expandibles)                      │   │
│  │  - Hoteles dinámicos (agregar/eliminar)                  │   │
│  │  - Traslado y detalles finales                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              ↓                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  script.js - Lógica Frontend                             │   │
│  │  - Autosave en localStorage                              │   │
│  │  - Validaciones de datos                                 │   │
│  │  - Serializa formulario a JSON                           │   │
│  │  - Envía POST a http://localhost:8000/api/cotizacion/pdf│   │
│  └──────────────────────────────────────────────────────────┘   │
│                              ↓                                    │
│                   PETICIÓN AJAX (POST JSON)                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                         🌐 INTERNET
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  SERVIDOR BACKEND (FastAPI)                      │
│                   http://localhost:8000                          │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  main.py - FastAPI Application                           │   │
│  │                                                            │   │
│  │  POST /api/cotizacion/pdf                                │   │
│  │  ├─ Recibe JSON (CotizacionData)                         │   │
│  │  ├─ Valida con Pydantic                                  │   │
│  │  └─ Extrae datos del objeto                              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              ↓                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Jinja2 Environment                                      │   │
│  │  ├─ Carga template.html                                  │   │
│  │  ├─ Inyecta variables {{ }}                              │   │
│  │  └─ Renderiza HTML completo                              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              ↓                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  WeasyPrint                                              │   │
│  │  ├─ Procesa HTML + CSS                                   │   │
│  │  ├─ Aplica CSS Paged Media (@page, break-inside)         │   │
│  │  ├─ Renderiza fuentes Google Fonts                       │   │
│  │  └─ Genera PDF bytes en memoria                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              ↓                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  StreamingResponse                                       │   │
│  │  ├─ media_type: application/pdf                          │   │
│  │  ├─ Content-Disposition: attachment                      │   │
│  │  └─ Envía bytes del PDF al navegador                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              ↓                                    │
│                   RESPUESTA PDF (blob binario)                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                         🌐 INTERNET
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     NAVEGADOR (FRONTEND)                         │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  script.js - Descarga                                    │   │
│  │  ├─ Recibe blob PDF                                      │   │
│  │  ├─ Crea URL temporal (URL.createObjectURL)              │   │
│  │  ├─ Simula click en <a href="">                          │   │
│  │  ├─ Descarga: Cotizacion_NombreCliente.pdf               │   │
│  │  └─ Limpia URL (URL.revokeObjectURL)                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              ↓                                    │
│                      📄 PDF DESCARGADO ✅                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Componentes Principales

### Frontend (`index.html` + `script.js`)
- Formulario dinámico con secciones colapsables
- Gestión de hoteles: agregar/eliminar opciones
- Validación de fechas y datos obligatorios
- Autosave en localStorage
- Envío asincrónico POST JSON

### Backend (`main.py`)
```python
app = FastAPI()

@app.post("/api/cotizacion/pdf")
async def generar_cotizacion_pdf(data: CotizacionData):
    # 1. Validar datos con Pydantic
    # 2. Renderizar template.html con Jinja2
    # 3. Convertir HTML a PDF con WeasyPrint
    # 4. Retornar PDF como descarga
    return StreamingResponse(pdf_bytes, media_type="application/pdf")
```

### Plantilla (`template.html`)
- CSS Paged Media (@page, @bottom-center)
- Diseño profesional de alta calidad
- Tarjetas de hotel con break-inside: avoid
- Variables Jinja2: `{{ nombre_cliente }}`, `{% for %}`
- Optimizado para impresión

---

## 🔄 Modelos de Datos

### JSON → Frontend → Backend → PDF

```
┌─────────────────────────────────┐
│ CotizacionData (Pydantic)       │
├─────────────────────────────────┤
│ nombre_cliente: str ✅          │
│ destino: str ✅                 │
│ fecha_salida: str ✅            │
│ origen: Optional[str]           │
│ noches: Optional[str]           │
│ aerolinea_ida, numero_vuelo_ida │
│ fecha_vuelo_salida              │
│ aeropuerto_origen/destino       │
│ hora_salida_ida/llegada_ida     │
│ escala_ida: Optional[str]       │
│ equipaje: List[str]             │
│ [REPETIR PARA REGRESO]          │
│ traslado: Optional[str]         │
│ hoteles: List[HotelData] ✅     │
│ moneda, fecha_cotizacion        │
│ asistencia, validez_oferta      │
│ texto_adicional                 │
└─────────────────────────────────┘
         ↓
    RENDERIZADO
         ↓
┌─────────────────────────────────┐
│ HTML con Variables Jinja2       │
│ {{ nombre_cliente }}            │
│ {% for hotel in hoteles %}      │
│   {{ hotel.hotel_nombre }}      │
│ {% endfor %}                    │
└─────────────────────────────────┘
         ↓
    GENERACIÓN PDF
         ↓
┌─────────────────────────────────┐
│ PDF Profesional A4              │
│ - Múltiples páginas (si es +)   │
│ - Pie de página: "Página X de Y"│
│ - Tarjetas no divididas         │
│ - Tipografía profes.            │
│ - Colores corporativos          │
└─────────────────────────────────┘
```

---

## 🗂️ Estructura de Carpetas

```
FelizViaje/
│
├── Frontend (Cliente)
│   ├── index.html          - Formulario visual
│   ├── script.js           - Lógica y comunicación
│   └── style.css           - Estilos del formulario
│
├── Backend (Servidor)
│   ├── main.py             - FastAPI app
│   ├── requirements.txt    - Dependencias Python
│   │
│   └── templates/          - Carpeta de Jinja2
│       └── template.html   - Plantilla PDF (copia)
│
├── Documentación
│   ├── README.md           - Doc completa
│   ├── QUICK_START.md      - Guía rápida
│   └── .gitignore          - Git config
│
└── template.html           - Plantilla original
```

---

## 🔌 Configuración de CORS

```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Desarrollo: permite todos
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

# Producción: cambiar a dominios reales
allow_origins=["https://tudominio.com", "https://app.tudominio.com"]
```

---

## 🧪 Flujo de Prueba

### 1. Instalar
```bash
pip install -r requirements.txt
```

### 2. Preparar templates
```bash
mkdir templates && cp template.html templates/template.html
```

### 3. Iniciar backend
```bash
python main.py
# ↓
# INFO: 🚀 FelizViaje PDF Generator iniciado
# INFO: Uvicorn running on http://0.0.0.0:8000
```

### 4. Abrir frontend
```bash
# Abre index.html en navegador
# Live Server o navegador directo
```

### 5. Generar PDF
```
Completa formulario → Click "Generar PDF" → PDF descargado ✅
```

### 6. Verificar
```
Check: Cotizacion_[NombreCliente].pdf en Downloads
```

---

## 📊 Tecnologías Usadas

| Capa | Tecnología | Propósito |
|------|-----------|----------|
| **Frontend** | HTML5 + CSS3 | Interfaz de usuario |
| | JavaScript (Vanilla) | Lógica y comunicación |
| | localStorage | Persistencia local |
| **Backend** | Python 3.9+ | Lenguaje |
| | FastAPI | Framework web |
| | Uvicorn | Servidor ASGI |
| | Pydantic | Validación |
| **Rendering** | Jinja2 | Templates HTML |
| | WeasyPrint | HTML → PDF |
| **Transporte** | HTTP/REST | Comunicación |
| | CORS | Cross-Origin |
| | JSON | Formato datos |

---

## ✨ Características Destacadas

### Frontend
- ✅ Formulario dinámico y responsivo
- ✅ Hoteles: agregar/eliminar sin límite
- ✅ Validaciones en tiempo real
- ✅ Autosave automático
- ✅ UX moderna y profesional

### Backend
- ✅ Validación con Pydantic (tipado fuerte)
- ✅ Logging detallado
- ✅ Manejo de excepciones robusto
- ✅ Documentación Swagger automática
- ✅ Health checks

### PDF
- ✅ Diseño profesional similar a Booking
- ✅ CSS Paged Media (@page, break-inside)
- ✅ Tipografía Google Fonts
- ✅ Múltiples páginas automáticas
- ✅ Números de página
- ✅ Tarjetas nunca divididas

---

## 🚀 Escalabilidad

### Mejoras Futuras
1. **Base de datos**: Guardar cotizaciones en PostgreSQL
2. **Autenticación**: JWT tokens para usuarios
3. **Caché**: Redis para PDFs generados
4. **Webhooks**: Notificar al frontend cuando está listo
5. **Cola de trabajos**: Celery para PDFs grandes
6. **Storage**: AWS S3 para guardar PDFs

---

## 📞 Soporte

**Problema** → **Revisar** → **Solución**

1. Template not found → Verifica `templates/template.html` exists
2. Failed to fetch → Backend running on :8000?
3. PDF empty → Check Jinja2 template errors in logs
4. ModuleNotFoundError → Run `pip install -r requirements.txt`

Ver QUICK_START.md para más detalles.

---

**Desenvolvimiento completo del sistema FelizViaje PDF Generator** ✅
