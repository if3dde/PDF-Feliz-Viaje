const STORAGE_KEY = "felizviaje_form";
const API_ENDPOINT = "http://localhost:8000/api/cotizacion/pdf";

document.addEventListener("DOMContentLoaded", () => {
  const elements = getElements();
  if (!elements.form) return;
  elements.year.textContent = new Date().getFullYear();
  document.documentElement.setAttribute("data-theme", "dark");
  setupHotelManagement(elements.form);
  restoreForm(elements.form);
  setQuoteDateToToday(elements.form);
  setupAutosave(elements.form);
  setupTripDateMinimums(elements.form);
  setupRealtimeValidation(elements.form);
  setupActions(elements);
  if (window.lucide) lucide.createIcons();
});

function getElements() {
  return { form: document.getElementById("quoteForm"), year: document.getElementById("year"), generateBtn: document.getElementById("generateBtn"), clearBtn: document.getElementById("clearBtn"), addHotelBtn: document.getElementById("addHotelBtn") };
}

function setupHotelManagement(form) {
  const container = form.querySelector("#hotelContainer");
  const addButton = document.getElementById("addHotelBtn");
  if (!container || !addButton) return;
  addButton.addEventListener("click", () => { addHotelBlock(container); saveToStorage(serializeForm(form)); });
  container.addEventListener("click", async (event) => {
    const removeButton = event.target.closest(".remove-hotel-btn");
    if (removeButton) {
      if (container.querySelectorAll(".hotel-block").length > 1) {
        removeButton.closest(".hotel-block")?.remove();
        updateHotelBlockLabels(container);
        saveToStorage(serializeForm(form));
      }
      return;
    }
    const pasteButton = event.target.closest(".paste-map-btn");
    if (!pasteButton) return;
    try {
      const mapInput = pasteButton.closest(".field")?.querySelector('[data-hotel-field="hotel_maps"]');
      if (!mapInput) return;
      mapInput.value = await navigator.clipboard.readText();
      mapInput.dispatchEvent(new Event("input", { bubbles: true }));
      mapInput.focus();
    } catch { alert("No se pudo pegar desde el portapapeles. Revisá los permisos del navegador."); }
  });
  updateHotelBlockLabels(container);
}

function addHotelBlock(container, values = null) {
  const firstBlock = container.querySelector(".hotel-block");
  if (!firstBlock) return null;
  const newBlock = firstBlock.cloneNode(true);
  clearHotelBlock(newBlock);
  if (values) fillHotelBlock(newBlock, values);
  container.appendChild(newBlock);
  updateHotelBlockLabels(container);
  return newBlock;
}

function clearHotelBlock(block) { block.querySelectorAll("[data-hotel-field]").forEach((field) => (field.value = "")); }
function fillHotelBlock(block, values) { block.querySelectorAll("[data-hotel-field]").forEach((field) => { field.value = values[field.dataset.hotelField] ?? ""; }); }
function updateHotelBlockLabels(container) {
  const blocks = [...container.querySelectorAll(".hotel-block")];
  blocks.forEach((block, index) => {
    const removeButton = block.querySelector(".remove-hotel-btn");
    const title = block.querySelector(".hotel-option-title");
    if (title) title.textContent = "Opción de hotel " + (index + 1);
    if (removeButton) { removeButton.disabled = blocks.length === 1; removeButton.hidden = blocks.length === 1; }
  });
}

function setupAutosave(form) {
  const save = () => saveToStorage(serializeForm(form));
  form.addEventListener("input", (event) => { if (event.target.matches("input, textarea, select")) save(); });
  form.addEventListener("change", (event) => { if (event.target.matches("input, textarea, select")) save(); });
}

function setupActions(elements) {
  const { form, generateBtn, clearBtn } = elements;
  generateBtn.addEventListener("click", async () => {
    // Abrir todas las secciones para que las alertas del navegador sean visibles
    form.querySelectorAll("details").forEach((d) => (d.open = true));
    if (!form.reportValidity()) {
      alert("Por favor, revisá los campos obligatorios del formulario.");
      return;
    }
    const payload = serializeForm(form);
    const errors = validateForm(payload);
    if (errors.length) { alert("Errores:\n- " + errors.join("\n- ")); return; }
    generateBtn.disabled = true;
    generateBtn.textContent = "Generando PDF...";
    try {
      const response = await fetch(API_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || ("Error " + response.status + ": " + response.statusText));
      }
      const blob = await response.blob();
      if (blob.type && !blob.type.includes("pdf")) throw new Error("El servidor no devolvió un archivo PDF válido.");
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "Cotizacion_" + sanitizeFilename(payload.nombre_cliente) + ".pdf";
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.setTimeout(() => URL.revokeObjectURL(url), 10000);
    } catch (error) {
      console.error("Error al generar PDF:", error);
      alert("No se pudo generar el PDF.\n" + error.message + "\n\nVerificá que el backend esté activo en http://localhost:8000.");
    } finally {
      generateBtn.disabled = false;
      generateBtn.textContent = "Generar PDF de Cotización";
    }
  });
  clearBtn.addEventListener("click", () => {
    form.reset();
    resetHotelBlocks(form);
    clearStorage();
    setQuoteDateToToday(form);
    form.querySelectorAll("[data-error-for]").forEach((element) => element.remove());
  });
}

function serializeForm(form) {
  const data = {};
  const fields = [...form.elements].filter((field) => field.name && !field.closest(".hotel-block"));
  fields.forEach((field) => {
    const { name, type, value } = field;
    if (type === "checkbox") {
      if (!(name in data)) data[name] = [...form.querySelectorAll('[name="' + name + '"]:checked')].map((item) => item.value);
      return;
    }
    if (type === "radio") {
      if (!(name in data)) data[name] = form.querySelector('[name="' + name + '"]:checked')?.value || "";
      return;
    }
    data[name] = value;
  });
  data.hoteles = [...form.querySelectorAll(".hotel-block")].map((block) => {
    const hotel = {};
    block.querySelectorAll("[data-hotel-field]").forEach((field) => { hotel[field.dataset.hotelField] = field.value.trim(); });
    return hotel;
  });
  return data;
}

function restoreForm(form) {
  const savedData = loadFromStorage();
  if (!savedData) return;
  Object.entries(savedData).forEach(([name, value]) => {
    if (name === "hoteles") return;
    const fields = [...form.querySelectorAll('[name="' + name + '"]')];
    if (!fields.length) return;
    if (fields[0].type === "checkbox") fields.forEach((field) => (field.checked = Array.isArray(value) && value.includes(field.value)));
    else if (fields[0].type === "radio") fields.forEach((field) => (field.checked = field.value === value));
    else fields[0].value = value ?? "";
  });
  if (!Array.isArray(savedData.hoteles) || !savedData.hoteles.length) return;
  const container = form.querySelector("#hotelContainer");
  resetHotelBlocks(form);
  const firstBlock = container?.querySelector(".hotel-block");
  if (!container || !firstBlock) return;
  fillHotelBlock(firstBlock, savedData.hoteles[0]);
  savedData.hoteles.slice(1).forEach((hotel) => addHotelBlock(container, hotel));
  updateHotelBlockLabels(container);
}

function resetHotelBlocks(form) {
  const container = form.querySelector("#hotelContainer");
  if (!container) return;
  const blocks = [...container.querySelectorAll(".hotel-block")];
  blocks.slice(1).forEach((block) => block.remove());
  if (blocks[0]) clearHotelBlock(blocks[0]);
  updateHotelBlockLabels(container);
}

function setupTripDateMinimums(form) {
  const departureDate = form.querySelector('[name="fecha_salida"]');
  const flightDepartureDate = form.querySelector('[name="fecha_vuelo_salida"]');
  const flightReturnDate = form.querySelector('[name="fecha_vuelo_regreso"]');
  if (!departureDate) return;
  const syncMinimums = () => {
    const tripDate = isFullDate(departureDate.value) ? departureDate.value : "";
    const flightDate = isFullDate(flightDepartureDate?.value) ? flightDepartureDate.value : tripDate;
    applyMinDate(flightDepartureDate, tripDate);
    applyMinDate(flightReturnDate, flightDate);
  };
  departureDate.addEventListener("input", syncMinimums);
  departureDate.addEventListener("change", syncMinimums);
  flightDepartureDate?.addEventListener("input", syncMinimums);
  flightDepartureDate?.addEventListener("change", syncMinimums);
  syncMinimums();
}

function applyMinDate(input, minDate) { if (!input) return; input.min = minDate; if (minDate && input.value && input.value < minDate) input.value = ""; }
function setupRealtimeValidation(form) {
  ["fecha_salida", "fecha_vuelo_salida", "fecha_vuelo_regreso", "fecha_cotizacion"].forEach((name) => {
    const input = form.querySelector('[name="' + name + '"]');
    if (!input) return;
    input.addEventListener("input", () => clearFieldError(form, name));
    input.addEventListener("change", () => validateDateField(form, name));
    input.addEventListener("blur", () => validateDateField(form, name));
  });
}

function validateDateField(form, name) {
  clearFieldError(form, name);
  const value = form.querySelector('[name="' + name + '"]')?.value;
  if (!value) return;
  if (isPast(value) && name !== "fecha_cotizacion") { showFieldError(form, name, "La fecha no puede ser anterior a hoy."); return; }
  const departure = form.querySelector('[name="fecha_salida"]')?.value;
  if (["fecha_vuelo_salida", "fecha_vuelo_regreso"].includes(name) && departure && value < departure) { showFieldError(form, name, "La fecha no puede ser anterior a la fecha de salida."); return; }
  const flightDeparture = form.querySelector('[name="fecha_vuelo_salida"]')?.value;
  if (name === "fecha_vuelo_regreso" && flightDeparture && value < flightDeparture) showFieldError(form, name, "La fecha de regreso no puede ser anterior a la de ida.");
}

function validateForm(values) {
  const errors = [];
  if (isPast(values.fecha_salida)) errors.push("La fecha de salida no puede ser en el pasado.");
  if (isPast(values.fecha_vuelo_salida)) errors.push("La fecha del vuelo de ida no puede ser en el pasado.");
  if (isPast(values.fecha_vuelo_regreso)) errors.push("La fecha del vuelo de regreso no puede ser en el pasado.");
  if (values.fecha_vuelo_salida && values.fecha_vuelo_regreso && values.fecha_vuelo_regreso < values.fecha_vuelo_salida) errors.push("La fecha de regreso no puede ser anterior a la de ida.");
  if (values.fecha_salida && values.fecha_vuelo_salida && values.fecha_vuelo_salida < values.fecha_salida) errors.push("La fecha del vuelo de ida no puede ser anterior a la fecha de salida.");
  if (!Number.isInteger(Number(values.escala_ida)) || Number(values.escala_ida) < 0) errors.push("Las escalas de ida deben ser un número entero mayor o igual a 0.");
  if (!Number.isInteger(Number(values.escala_vuelta)) || Number(values.escala_vuelta) < 0) errors.push("Las escalas de vuelta deben ser un número entero mayor o igual a 0.");
  if (values.hoteles.some((hotel) => Number.isNaN(Number(hotel.hotel_precio)) || Number(hotel.hotel_precio) < 0)) errors.push("El precio de cada hotel debe ser un número válido.");
  if (values.hoteles.some((hotel) => !Number.isInteger(Number(hotel.hotel_habitaciones)) || Number(hotel.hotel_habitaciones) < 1)) errors.push("La cantidad de habitaciones de cada hotel debe ser un número entero mayor o igual a 1.");
  return errors;
}

function isFullDate(value) { return typeof value === "string" && /^\d{4}-\d{2}-\d{2}$/.test(value); }
function isPast(value) {
  if (!isFullDate(value)) return false;
  const date = new Date(value + "T00:00:00");
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return date < today;
}

function clearFieldError(form, name) { form.querySelector('[data-error-for="' + name + '"]')?.remove(); }
function showFieldError(form, name, message) {
  clearFieldError(form, name);
  const container = form.querySelector('[name="' + name + '"]')?.closest(".field");
  if (!container) return;
  const error = document.createElement("div");
  error.className = "field-error";
  error.dataset.errorFor = name;
  error.textContent = message;
  container.appendChild(error);
}

function setQuoteDateToToday(form) {
  const field = form.querySelector('[name="fecha_cotizacion"]');
  if (field && !field.value) field.value = formatDateInputValue(new Date());
}
function formatDateInputValue(date) { return date.getFullYear() + "-" + String(date.getMonth() + 1).padStart(2, "0") + "-" + String(date.getDate()).padStart(2, "0"); }
function sanitizeFilename(value) { return (value || "Cliente").trim().replace(/[^a-z0-9_-]/gi, "_").replace(/_+/g, "_").slice(0, 50) || "Cliente"; }

function saveToStorage(data) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch (error) { console.warn("No se pudo guardar en localStorage:", error); }
}
function loadFromStorage() {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : null;
  } catch (error) { console.warn("No se pudo cargar localStorage:", error); return null; }
}
function clearStorage() {
  try { localStorage.removeItem(STORAGE_KEY); } catch (error) { console.warn("No se pudo limpiar localStorage:", error); }
}
