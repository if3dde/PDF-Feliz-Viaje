# 🎯 Guía Rápida de Instalación y Uso

## ✅ PASO 1: Instalar Dependencias

Abre una terminal/PowerShell en la carpeta `FelizViaje/` y ejecuta:

```bash
pip install -r requirements.txt
```

**En Linux (si falla):**
```bash
sudo apt-get install -y python3-dev libcairo2-dev libpango-1.0-0 libpango-cairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev libssl-dev
pip install -r requirements.txt
```

---

## ✅ PASO 2: Preparar la Carpeta de Templates

El backend espera encontrar `template.html` en una carpeta `templates/`.

**Windows (PowerShell):**
```powershell
mkdir templates
copy template.html templates\template.html
```

**macOS/Linux:**
```bash
mkdir -p templates
cp template.html templates/template.html
```

---

## ✅ PASO 3: Iniciar el Backend

En la misma terminal, ejecuta:

```bash
python main.py
```

Deberías ver en la consola:
```
INFO:     🚀 FelizViaje PDF Generator iniciado
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**¡El backend está listo! Déjalo corriendo.**

---

## ✅ PASO 4: Probar el Frontend

1. Abre `index.html` en el navegador (o usa Live Server en VS Code)
2. Llena el formulario
3. Haz clic en **"Generar PDF de Cotización"**
4. El PDF debe descargarse automáticamente

---

## ✅ PASO 5: Probar Manualmente (Opcional)

Si quieres probar el endpoint sin el frontend, usa la interfaz Swagger:

1. Abre en el navegador: `http://localhost:8000/docs`
2. Busca el endpoint **POST** `/api/cotizacion/pdf`
3. Haz clic en **"Try it out"**
4. Copia este JSON en el body:

```json
{
  "nombre_cliente": "Juan Pérez",
  "destino": "Cancún",
  "fecha_salida": "2026-07-15",
  "noches": "7",
  "moneda": "USD",
  "fecha_cotizacion": "2026-09-04",
  "asistencia": "sí",
  "hoteles": [
    {
      "hotel_nombre": "Grand Palladium",
      "hotel_estrellas": "⭐⭐⭐⭐⭐",
      "hotel_precio": "1500"
    }
  ]
}
```

5. Haz clic en **"Execute"**
6. El PDF debe descargarse

---

## 🚨 Errores Comunes

### Error: "template not found: template.html"
**Solución:** Verifica que el archivo `template.html` está en la carpeta `templates/`

```bash
ls templates/  # macOS/Linux
dir templates\ # Windows
```

### Error: "Failed to fetch" desde el frontend
**Solución:** 
- El backend debe estar corriendo en `http://localhost:8000`
- Verifica que el puerto 8000 está disponible
- Si usas otro puerto, actualiza en `script.js`: `const API_ENDPOINT = "http://localhost:PUERTO/api/cotizacion/pdf"`

### Error: "No module named 'weasyprint'"
**Solución:**
```bash
pip install weasyprint
```

---

## 📁 Estructura Final Esperada

```
FelizViaje/
├── main.py                    ✅ Backend FastAPI
├── template.html              ✅ Plantilla (original)
├── requirements.txt           ✅ Dependencias
├── .gitignore                 ✅ Archivos a ignorar en Git
├── README.md                  ✅ Documentación
├── QUICK_START.md             ✅ Este archivo
├── index.html                 ✅ Frontend HTML
├── script.js                  ✅ Frontend JavaScript
├── style.css                  ✅ Estilos Frontend
└── templates/
    └── template.html          ✅ Plantilla (copia para backend)
```

---

## 💾 Pasos Finales

### Para Desarrollo (Local)
```bash
# Terminal 1: Backend
python main.py

# Terminal 2: Frontend (opcional - Live Server)
# Abre index.html con Live Server o similar
```

### Para Producción
```bash
# Cambiar CORS en main.py (ver README.md)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🆘 ¿Aún hay problemas?

1. **Abre la consola del navegador** (F12)
2. **Intenta generar PDF**
3. **Copia el error exacto** que aparece
4. **Verifica los logs del backend** en la terminal

El backend mostrará:
```
❌ Error al generar PDF: [mensaje detallado]
```

---

## ✨ ¡Listo!

Tu sistema FelizViaje está configurado y funcionando.

Frontend → JSON → Backend → Jinja2 → WeasyPrint → PDF ✅
