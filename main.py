"""
FelizViaje - Backend PDF Generator
FastAPI + WeasyPrint + Jinja2

Genera PDFs de cotizaciones turísticas de alta calidad.
Endpoint: POST /api/cotizacion/pdf
"""

import os
import io
import logging
from datetime import datetime
from typing import List, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field
from jinja2 import Environment, FileSystemLoader, select_autoescape
import weasyprint

# ===== CONFIGURACIÓN DE LOGGING =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== CONFIGURACIÓN DE FASTAPI =====
app = FastAPI(
    title="FelizViaje PDF Generator",
    description="Generador de PDFs de cotización turística",
    version="1.0.0"
)

# ===== CONFIGURACIÓN DE CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los dominios reales
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== CONFIGURACIÓN DE JINJA2 =====
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

# Crear directorio de templates si no existe
TEMPLATES_DIR.mkdir(exist_ok=True)

jinja_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(['html', 'xml']),
    enable_async=False
)

# ===== MODELOS PYDANTIC =====

class HotelData(BaseModel):
    """Datos de una opción de hotel"""
    hotel_categoria: Optional[str] = Field(None, description="Categoría/Título (ej: 1- PROMO MEJOR PRECIO)")
    hotel_nombre: str = Field(..., description="Nombre del hotel")
    hotel_estrellas: str = Field(default="⭐⭐⭐", description="Estrellas en formato emoji")
    hotel_regimen: Optional[str] = Field(None, description="Régimen (Solo habitación, Desayuno, etc)")
    hotel_precio: str = Field(..., description="Precio por persona")
    hotel_habitaciones: str = Field(default="1", description="Cantidad de habitaciones")
    hotel_descripcion: Optional[str] = Field(None, description="Descripción breve del hotel")
    hotel_maps: Optional[str] = Field(None, description="Link de Google Maps")


class CotizacionData(BaseModel):
    """Datos completos de la cotización recibida del frontend"""
    
    # Cliente y Destino
    nombre_cliente: str = Field(..., description="Nombre del cliente")
    destino: str = Field(..., description="Destino del viaje")
    fecha_salida: str = Field(..., description="Fecha de salida (YYYY-MM-DD)")
    origen: Optional[str] = Field(None, description="Ciudad de salida")
    noches: Optional[str] = Field(None, description="Duración en noches")
    pasajeros: int = Field(default=1, ge=1, description="Cantidad de pasajeros")
    precio_vuelo: Optional[float] = Field(0.0, description="Precio del vuelo")

    
    # Vuelo de Ida
    aerolinea_ida: Optional[str] = Field(None, description="Aerolínea ida")
    numero_vuelo_ida: Optional[str] = Field(None, description="Número de vuelo ida")
    fecha_vuelo_salida: Optional[str] = Field(None, description="Fecha vuelo ida")
    aeropuerto_origen: Optional[str] = Field(None, description="Código aeropuerto origen")
    hora_salida_ida: Optional[str] = Field(None, description="Hora salida ida")
    aeropuerto_destino: Optional[str] = Field(None, description="Código aeropuerto destino")
    hora_llegada_ida: Optional[str] = Field(None, description="Hora llegada ida")
    escala_ida: Optional[str] = Field(default="0", description="Escalas ida")
    
    # Vuelo de Regreso
    aerolinea_regreso: Optional[str] = Field(None, description="Aerolínea regreso")
    numero_vuelo_regreso: Optional[str] = Field(None, description="Número de vuelo regreso")
    fecha_vuelo_regreso: Optional[str] = Field(None, description="Fecha vuelo regreso")
    aeropuerto_origen_regreso: Optional[str] = Field(None, description="Código aeropuerto origen regreso")
    hora_salida_regreso: Optional[str] = Field(None, description="Hora salida regreso")
    aeropuerto_destino_regreso: Optional[str] = Field(None, description="Código aeropuerto destino regreso")
    hora_llegada_regreso: Optional[str] = Field(None, description="Hora llegada regreso")
    escala_vuelta: Optional[str] = Field(default="0", description="Escalas vuelta")
    
    # Equipaje
    equipaje: Optional[List[str]] = Field(default=[], description="Tipos de equipaje incluidos")
    
    # Traslado
    traslado: Optional[str] = Field(None, description="Tipo de traslado (Privado/Compartido)")
    
    # Hoteles
    hoteles: List[HotelData] = Field(..., description="Lista de opciones de hotel")
    
    # Detalles finales
    moneda: Optional[str] = Field(default="USD", description="Moneda (ARS, USD, EUR)")
    fecha_cotizacion: Optional[str] = Field(None, description="Fecha de cotización (YYYY-MM-DD)")
    asistencia: Optional[str] = Field(default="no", description="Asistencia incluida (sí/no)")
    validez_oferta: Optional[str] = Field(default="7", description="Validez de la oferta en días")
    texto_adicional: Optional[str] = Field(None, description="Texto adicional personalizado")


# ===== FUNCIONES AUXILIARES =====

def render_template(template_name: str, context: dict) -> str:
    """
    Renderiza una plantilla Jinja2 con el contexto proporcionado.
    
    Args:
        template_name: Nombre del archivo de template
        context: Diccionario con los datos a inyectar
        
    Returns:
        HTML renderizado como string
    """
    try:
        template = jinja_env.get_template(template_name)
        return template.render(**context)
    except Exception as e:
        logger.error(f"Error al renderizar template '{template_name}': {str(e)}")
        raise


def html_to_pdf(html_string: str, filename: str) -> bytes:
    """
    Convierte HTML a PDF usando WeasyPrint.
    
    Args:
        html_string: HTML como string
        filename: Nombre del archivo (para metadatos)
        
    Returns:
        PDF como bytes
    """
    try:
        logger.info(f"Generando PDF: {filename}")
        
        # Crear documento HTML desde string
        html_doc = weasyprint.HTML(string=html_string, base_url=".")
        
        # Generar PDF en memoria
        pdf_bytes = html_doc.write_pdf()
        
        logger.info(f"PDF generado exitosamente: {filename} ({len(pdf_bytes)} bytes)")
        return pdf_bytes
    except Exception as e:
        logger.error(f"Error al generar PDF: {str(e)}")
        raise


def sanitize_filename(text: str) -> str:
    """
    Sanitiza un nombre de archivo eliminando caracteres inválidos.
    
    Args:
        text: Texto a sanitizar
        
    Returns:
        Nombre de archivo seguro
    """
    import re
    # Reemplazar caracteres inválidos con guion bajo
    sanitized = re.sub(r'[^a-zA-Z0-9\-_]', '_', text)
    # Limitar longitud
    return sanitized[:50]


def format_date_to_dmy(date_str: Optional[str]) -> str:
    """
    Convierte una fecha en formato YYYY-MM-DD a DD/MM/YYYY.
    Si la fecha es nula, vacía o inválida, devuelve un valor por defecto o la misma cadena.
    """
    if not date_str:
        return "No especificado"
    try:
        if len(date_str) == 10 and date_str[2] in '-/' and date_str[5] == date_str[2]:
            input_format = "%d-%m-%Y" if date_str[2] == '-' else "%d/%m/%Y"
            return datetime.strptime(date_str, input_format).strftime("%d/%m/%Y")
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except Exception:
        return date_str



# ===== RUTAS / ENDPOINTS =====

@app.get("/")
async def root():
    """Endpoint de prueba"""
    return {
        "status": "online",
        "message": "FelizViaje PDF Generator API",
        "endpoint": "/api/cotizacion/pdf",
        "method": "POST",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@app.post("/api/cotizacion/pdf")
async def generar_cotizacion_pdf(data: CotizacionData):
    """
    Endpoint principal: Genera PDF de cotización turística.
    
    Recibe datos JSON del frontend, renderiza la plantilla HTML con Jinja2,
    convierte a PDF con WeasyPrint y retorna el archivo para descarga.
    
    Args:
        data: Objeto CotizacionData con toda la información del viaje
        
    Returns:
        PDF como archivo descargable
        
    Raises:
        HTTPException: Si hay error en la validación o generación
    """
    try:
        logger.info(f"Solicitud recibida para cliente: {data.nombre_cliente}")
        
        # Validación adicional
        if not data.nombre_cliente or not data.nombre_cliente.strip():
            raise HTTPException(
                status_code=400,
                detail="El nombre del cliente es obligatorio"
            )
        
        if not data.hoteles or len(data.hoteles) == 0:
            raise HTTPException(
                status_code=400,
                detail="Debe haber al menos una opción de hotel"
            )
        
        # Fechas y Cálculos de Financiación
        from datetime import timedelta
        import calendar

        dt_salida = None
        try:
            dt_salida = datetime.strptime(data.fecha_salida, "%Y-%m-%d")
        except Exception:
            pass

        dt_hoy = datetime.now()
        
        months_diff = 0
        financiacion_activa = False
        num_cuotas = 0
        fecha_limite_str = ""
        
        if dt_salida:
            months_diff = (dt_salida.year - dt_hoy.year) * 12 + (dt_salida.month - dt_hoy.month)
            # Solo se activan las cuotas si el viaje es mínimo en los próximos 3 meses
            if months_diff >= 3:
                financiacion_activa = True
                dt_limite = dt_salida - timedelta(days=30)
                fecha_limite_str = dt_limite.strftime("%d/%m/%Y")
                
                def add_months(sourcedate, months):
                    month = sourcedate.month - 1 + months
                    year = sourcedate.year + month // 12
                    month = month % 12 + 1
                    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
                    return datetime(year, month, day)
                
                while True:
                    next_payment = add_months(dt_hoy, num_cuotas + 1)
                    if next_payment <= dt_limite:
                        num_cuotas += 1
                    else:
                        break
                
                if num_cuotas == 0:
                    num_cuotas = 1

        passengers = max(int(data.pasajeros or 1), 1)
        precio_vuelo = float(data.precio_vuelo or 0.0)
        
        hoteles_context = []
        for h in data.hoteles:
            try:
                hotel_precio = float(h.hotel_precio)
            except Exception:
                hotel_precio = 0.0
                
            total_opcion = (hotel_precio * passengers) + precio_vuelo
            
            # El monto de reserva es el precio del vuelo (o 30% como fallback si no se especificó)
            if precio_vuelo > 0:
                reserva = precio_vuelo
            else:
                reserva = total_opcion * 0.30
                
            saldo = total_opcion - reserva
            
            if financiacion_activa and num_cuotas > 0:
                cuota = saldo / num_cuotas
            else:
                cuota = saldo
                
            h_dict = h.dict()
            h_dict.update({
                "precio_total": total_opcion,
                "precio_reserva": reserva,
                "precio_cuota": cuota
            })
            hoteles_context.append(h_dict)

        # Preparar contexto para Jinja2
        context = {
            "nombre_cliente": data.nombre_cliente,
            "destino": data.destino,
            "fecha_salida": format_date_to_dmy(data.fecha_salida),
            "origen": data.origen or "No especificado",
            "noches": data.noches or "0",
            "pasajeros": passengers,
            "aerolinea_ida": data.aerolinea_ida or "No especificado",
            "numero_vuelo_ida": data.numero_vuelo_ida or "",
            "fecha_vuelo_salida": format_date_to_dmy(data.fecha_vuelo_salida),
            "aeropuerto_origen": data.aeropuerto_origen or "---",
            "hora_salida_ida": data.hora_salida_ida or "TBD",
            "aeropuerto_destino": data.aeropuerto_destino or "---",
            "hora_llegada_ida": data.hora_llegada_ida or "TBD",
            "escala_ida": data.escala_ida or "0",
            "equipaje": data.equipaje or [],
            "aerolinea_regreso": data.aerolinea_regreso or "No especificado",
            "numero_vuelo_regreso": data.numero_vuelo_regreso or "",
            "fecha_vuelo_regreso": format_date_to_dmy(data.fecha_vuelo_regreso),
            "aeropuerto_origen_regreso": data.aeropuerto_origen_regreso or "---",
            "hora_salida_regreso": data.hora_salida_regreso or "TBD",
            "aeropuerto_destino_regreso": data.aeropuerto_destino_regreso or "---",
            "hora_llegada_regreso": data.hora_llegada_regreso or "TBD",
            "escala_vuelta": data.escala_vuelta or "0",
            "traslado": data.traslado or "No especificado",
            "hoteles": hoteles_context,
            "moneda": data.moneda or "USD",
            "fecha_cotizacion": format_date_to_dmy(data.fecha_cotizacion) if data.fecha_cotizacion else datetime.now().strftime("%d/%m/%Y"),
            "asistencia": data.asistencia or "no",
            "validez_oferta": data.validez_oferta or "7",
            "texto_adicional": data.texto_adicional or "",
            "financiacion_activa": financiacion_activa,
            "num_cuotas": num_cuotas,
            "limite_pago": fecha_limite_str,
            "precio_vuelo": precio_vuelo,
        }
        
        logger.info("Contexto preparado. Renderizando template...")
        
        # Renderizar template HTML
        html_content = render_template("template.html", context)
        
        logger.info("Template renderizado. Generando PDF...")
        
        # Convertir HTML a PDF
        pdf_bytes = html_to_pdf(html_content, data.nombre_cliente)
        
        # Generar nombre de archivo seguro
        sanitized_name = sanitize_filename(data.nombre_cliente)
        filename = f"Cotizacion_{sanitized_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        logger.info(f"PDF generado exitosamente: {filename}")
        
        # Retornar como descarga
        return StreamingResponse(
            iter([pdf_bytes]),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except HTTPException:
        # Re-lanzar HTTPExceptions (ya tienen status code)
        raise
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar el PDF: {str(e)}"
        )


# ===== MANEJADORES DE EXCEPCIONES =====

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Manejador personalizado para HTTPException"""
    return {
        "error": True,
        "status_code": exc.status_code,
        "detail": exc.detail,
        "timestamp": datetime.now().isoformat()
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Manejador para excepciones no controladas"""
    logger.error(f"Excepción no controlada: {str(exc)}", exc_info=True)
    return {
        "error": True,
        "status_code": 500,
        "detail": "Error interno del servidor",
        "timestamp": datetime.now().isoformat()
    }


# ===== LIFESPAN =====

@app.on_event("startup")
async def startup_event():
    """Evento al iniciar la aplicación"""
    logger.info("=" * 60)
    logger.info("🚀 FelizViaje PDF Generator iniciado")
    logger.info("=" * 60)
    logger.info(f"📁 Directorio de templates: {TEMPLATES_DIR}")
    
    # Verificar que el template existe
    template_path = TEMPLATES_DIR / "template.html"
    if not template_path.exists():
        logger.warning(f"⚠️  Template no encontrado: {template_path}")
        logger.warning("Crea el archivo template.html en la carpeta templates/")
    else:
        logger.info(f"✅ Template encontrado: {template_path}")
    
    logger.info("📚 API Documentation: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento al apagar la aplicación"""
    logger.info("🛑 FelizViaje PDF Generator apagado")


# ===== EJECUCIÓN =====

if __name__ == "__main__":
    import uvicorn
    
    # Configuración de Uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,  # Auto-reload en desarrollo
    )
