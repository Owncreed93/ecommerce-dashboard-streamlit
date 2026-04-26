# FRONTEND AND UX

## 📋 CORE FRONTEND OPTIMIZATION SPECIFICATIONS

**Versión:** 1.0
**Objetivo:** Garantizar rendimiento 100/100 en Lighthouse, mantenibilidad y SEO avanzado.
**Tecnologías:** Next.js (App Router), React, Reflex (Python).

---

### 1. ARQUITECTURA Y REUTILIZACIÓN (RESILIENCIA)

* **Patrón de Componentes:** Implementar *Atomic Design*. Separar componentes en `/ui` (átomos), `/features` (lógica) y `/layouts` (plantillas).
* **Nomenclatura CSS (BEM):** Uso obligatorio de **Block__Element--Modifier**.
  * Garantiza el aislamiento de estilos y facilita la migración a componentes de React/Reflex.
  * Los selectores deben ser planos (evitar anidación profunda).
* **Herencia de Plantillas:** Utilizar `layout.js` de Next.js para estructuras globales y evitar la duplicidad de contenedores.
* **Centralización de Animaciones:** Definir variantes de animaciones (ej. Framer Motion) en un archivo central. Los componentes deben consumir estas variantes para mantener la consistencia visual.
* **Reactividad Eficiente:** Priorizar **Server Components**. Solo usar `'use client'` cuando exista interactividad real (hooks como `useState` o `useEffect`).

### 2. OPTIMIZACIÓN DE RECURSOS (PERFORMANCE)

* **Gestión de Imágenes:** Prohibido el uso de `<img>`.
  * Usar `<Image />` de Next.js obligatoriamente.
  * Formatos: Conversión automática a **WebP**.
  * Estrategia: Carga diferida (Lazy Loading) por defecto y `priority` para el LCP.
* **Scripts y Terceros:**
  * Usar `<Script />` con estrategia `afterInteractive`.
  * Propiedad `crossOrigin="anonymous"` en recursos de CDN externos.
* **Reducción de Bundle:** * Minificación automática vía SWC (Next.js).
  * **Cache Busting:** Gestión automática por hashes en cada despliegue.
  * **Lazy Loading de Componentes:** Usar `next/dynamic` para elementos pesados fuera del viewport inicial (modales, mapas, etc.).

### 3. SEO Y ACCESIBILIDAD (A11Y)

* **Semántica HTML5:** Uso estricto de etiquetas de sección: `<main>`, `<article>`, `<section>`, `<nav>`, `<aside>`.
* **Narración por Voz (Screen Readers):**
  * `aria-label` obligatorio en botones con iconos o elementos interactivos sin texto.
  * Propiedad `alt` obligatoria y descriptiva en imágenes.
* **Indexación Dinámica:**
  * Generar `sitemap.xml` y `robots.txt` mediante archivos dinámicos (`.ts` / `.js`) en la carpeta `/app`.

### 4. FLUJO DE DATOS Y BACKEND (REFLEX/FLASK)

* **Compresión en Origen:** El backend debe procesar archivos (redimensión de imágenes, conversión a WebP y compresión de PDFs) antes de enviarlos al frontend.
* **Optimización de Font-swap:** Configurar fuentes con `font-display: swap` para evitar el "Flash of Unstyled Text" (FOUT).

---

### 5. CHECKLIST DE VALIDACIÓN PARA LA IA
>
> Antes de entregar código, la IA debe validar:
* [ ] ¿El componente es semánticamente correcto?
* [ ] ¿Se utiliza la nomenclatura **BEM (Block__Element--Modifier)** estrictamente?
* [ ] ¿Se utiliza `next/image` para multimedia?
* [ ] ¿Se han incluido `aria-labels` donde no hay texto explícito?
* [ ] ¿Se evita la duplicidad de lógica o estilos CSS?
* [ ] ¿El código es compatible con Server-side Rendering (SSR)?

## 🧠 CORE UX & BACKEND INTEGRATION SPECIFICATIONS

**Versión:** 1.0
**Enfoque:** Jakob's Law, Mobile First y Consistencia de Datos.
**Tecnologías:** Django/SQLAlchemy, React/Next.js, Reflex.

---

### 1. RESTRICCIONES DE MODELO DE DATOS (ESTRUCTURA)

*Al generar modelos en el Backend, se deben aplicar estas reglas de arquitectura basadas en UX:*

* **Ley de Jakob (Consistencia de Estados):**
  * **Prohibido:** No usar booleanos (`True/False`) para representar procesos con más de dos estados posibles.
  * **Obligatorio:** Usar `Enums` o `Choices`. Garantiza que la UI siempre sepa en qué paso del flujo está el usuario.
* **Ley de Zeigarnik (Persistencia de Progreso):**
  * Todo modelo de flujo (ej: registros, checkouts, formularios largos) **debe** incluir campos de seguimiento: `current_step` (Integer) y `last_updated_at`.
* **Prevención de Errores (Integridad):**
  * Implementar **Soft Delete** por defecto. El sistema nunca debe destruir datos accidentalmente. Campo obligatorio: `is_active` o `deleted_at`.

### 2. OPTIMIZACIÓN DE API Y CARGA (PERFORMANCE)

*Para evitar la frustración del usuario por latencia o sobrecarga de información:*

* **Ley de Miller (Fragmentación):**
  * **Prohibido:** Enviar listas masivas de datos en un solo JSON.
  * **Obligatorio:** Toda API de listado debe incluir paginación (`page`, `page_size`) y un campo `total_count` para que el frontend renderice indicadores de progreso.
* **Ley de Fitts (Eficiencia de Datos):**
  * Para elementos críticos de la UI, usar **Eager Loading** (`select_related` en Django o `joinedload` en SQLAlchemy) para evitar el problema de consultas N+1 que ralentizan la interfaz.

### 3. RESTRICCIONES FRONTEND (MOBILE FIRST & UX)

*Al generar componentes visuales o estilos CSS:*

* **Ley de Von Restorff (Aislamiento):**
  * Utilizar los `status_flag` o categorías del backend para aplicar estilos diferenciados mediante **Modificadores BEM** (ej: `.badge--success`). El elemento primario de una lista debe ser visualmente distinto.
* **Ley de Fitts (Interactividad Física):**
  * Todo elemento táctil o clickeable (botones, inputs, enlaces) debe tener un área de contacto mínima de **44px x 44px**.
* **Feedback de Sistema:**
  * Implementar estados de **Loading/Skeleton** basados exactamente en la estructura del JSON esperado. Si el backend envía un objeto `User`, el esqueleto debe reflejar esa forma.

---

### 4. CHECKLIST DE VALIDACIÓN PARA LA IA

> Antes de entregar el modelo o componente, la IA debe validar:

* [ ] ¿El modelo usa `choices` en lugar de booleanos para estados complejos?
* [ ] ¿La API incluye parámetros de paginación por defecto?
* [ ] ¿El componente frontend tiene el tamaño táctil mínimo de 44px?
* [ ] ¿Se ha implementado el Soft Delete en la lógica del backend?
* [ ] ¿El diseño de la UI respeta el enfoque Mobile First antes de escalar a Desktop?
