# FelizViaje

Generador de propuestas comerciales y mensajes listos para enviar por WhatsApp.

## ¿Qué hace este proyecto?

FelizViaje es una herramienta web sencilla para armar cotizaciones turísticas con un formulario visual y una vista previa del mensaje final. Está pensada para acelerar la creación de propuestas de viajes con datos como destino, fechas, vuelo, hotel, traslado, moneda y precio por persona.

## Funcionalidades principales

- Formulario de cotización con secciones para destino, vuelo, traslado, hotel e importe final.
- Vista previa del mensaje generado en tiempo real al presionar el botón correspondiente.
- Copia del mensaje al portapapeles con un botón dedicado.
- Autoguardado local en el navegador para no perder los datos al recargar la página.
- Validaciones básicas de fechas y formato del precio.

## Cómo usarlo

1. Abre el archivo `index.html` en tu navegador preferido.
2. Completa los campos del formulario con los datos del paquete turístico.
3. Haz clic en "Generar mensaje" para ver la propuesta en la vista previa.
4. Usa "Copiar mensaje" para llevar el texto al portapapeles.

## Estructura del proyecto

- `index.html`: estructura principal de la interfaz y formulario.
- `style.css`: estilos visuales, diseño responsive y componentes del formulario.
- `script.js`: lógica de autosave, validaciones, generación del mensaje y acciones de botones.

## Requisitos

No hay dependencias externas ni instalación adicional.

Solo necesitas un navegador moderno con soporte para JavaScript.

## Desarrollo y mantenimiento

- El proyecto está pensado como una página estática.
- Los cambios visuales se hacen en `style.css`.
- La lógica del formulario y la generación del texto se modifica en `script.js`.
- El autoguardado usa `localStorage`, por lo que los datos se conservan en el navegador del usuario.

## Notas

Este proyecto está orientado a uso interno y a la generación rápida de propuestas para clientes.
