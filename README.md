# Horaria · Ben Ezra (uso personal)

App de Astrología Horaria — método Ben Ezra (transmitido por Pepa Sanchís).
Calcula la carta del momento de la pregunta, arma el informe técnico completo
(dignidades, almutenes, aspectos, recepción, validez del tema) y responde la
pregunta con o sin IA. Permite hasta 6 preguntas de seguimiento sobre el mismo tema.

## Estructura

```
backend/
  app.py            servidor Flask (API + sirve el frontend)
  astro.py          motor de cálculo (Swiss Ephemeris vía pyswisseph)
  tables.py         dignidades, términos, decanatos, triplicidades, descripciones
  validity.py       validez del tema, traslación/colección de luz
  report.py         arma el informe técnico completo de la carta
  ai_prompt.py       prompt de sistema con la metodología para el modo con IA
  requirements.txt
frontend/
  index.html        interfaz (form + resultados), un solo archivo
```

## Cómo se calculan las posiciones planetarias

Usa `pyswisseph` con los archivos **reales de Swiss Ephemeris** (`.se1`), que
dan la máxima precisión de la librería (sub-arco-segundo). La app los
descarga sola la primera vez que arranca (desde el repositorio oficial de
Swiss Ephemeris) y los guarda en `backend/ephe/` — **no hace falta subirlos
a GitHub**, son pesados (~2MB juntos) y a veces la web de GitHub falla al
subir binarios grandes. Cubren el rango 1800-2399, de sobra para cualquier
horaria real. Si alguna vez necesitás datar algo fuera de ese rango, o si la
descarga automática fallara por algún motivo, la app cae automáticamente al
motor Moshier (igual de confiable, algo menos preciso) y te avisa en
`chart_meta.fuente_efemerides` cuál usó para cada planeta.

## Desplegar en Render (igual que hiciste con Kairós)

1. Creá un repo nuevo en GitHub y subí todo el contenido de esta carpeta.
2. En Render: **New + → Web Service**, conectalo a ese repo.
3. Configuración del servicio:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Variables de entorno (Render → Environment):
   - `ANTHROPIC_API_KEY` = tu API key de Anthropic
   - `ANTHROPIC_MODEL` = `claude-sonnet-5` (opcional, es el valor por defecto)
5. Deploy. Render te da una URL tipo `https://horaria-ben-ezra.onrender.com`
   — esa es la que abrís desde la compu o desde el navegador del celular.

## Uso

1. Cargá fecha, hora exacta, ciudad (o lat/long/UTC manual) y la pregunta.
2. Elegí **Con IA** (te da la interpretación completa) o **Sin IA** (te muestra
   el informe técnico crudo: planetas, casas, almutenes, aspectos, recepciones,
   validez del tema — para que lo interpretes vos misma).
3. En modo Con IA podés hacer hasta **6 preguntas de seguimiento** sobre el
   mismo tema sin tener que volver a levantar la carta.
4. **+ Nueva consulta** limpia todo para una pregunta horaria distinta (cada
   pregunta nueva requiere una carta nueva, porque el momento es distinto).

## Dictado por voz

El micrófono junto a la pregunta usa el reconocimiento de voz del navegador
(Web Speech API). Funciona bien en Chrome (compu y Android). En iPhone,
Safari lo soporta de forma más limitada — si no aparece el ícono del
micrófono, el navegador no lo tiene disponible y hay que escribir la
pregunta a mano.

## Significadores, almutenes y regente de la Hora

El informe siempre muestra, de forma explícita:
- El **regente de la Hora** (calculado con orto/ocaso real del día y lugar) y su significado.
- El **significador recomendado del consultante** (casa I), con el razonamiento aplicado
  (jerarquía: regente domiciliado y presente > regente aspectando la cúspide > planeta
  partil sobre la cúspide > almuten con más puntos).
- Si elegís la **casa de la pregunta** en el formulario, el mismo análisis para esa casa.
- Los **almutenes** de cada una de las 12 cúspides (con su puntaje), en el detalle "Casas y almutenes".

Esta selección automática es orientativa (así lo aclara el propio informe): en casos límite
—varios almutenes empatados, matices de intercepción, etc.— siempre podés revisar los
candidatos y decidir vos misma, tal como enseña la Lección 4.

## Limitaciones a tener en cuenta

- Las sesiones (para las preguntas de seguimiento) se guardan en memoria del
  servidor y se pierden si Render reinicia la instancia (por inactividad, en
  el plan free) o después de 12 horas. Para una consulta larga, conviene no
  dejarla a medias por mucho tiempo.
- La app corre en un solo proceso; si en algún momento la usás vos y una
  clienta al mismo tiempo, cada una tiene su propia sesión (no se pisan),
  pero si necesitás más volumen conviene pasar a un plan pago de Render con
  más de una instancia + Redis para las sesiones (avisame si llegás a eso).
- El regente de la Hora se calcula con orto/ocaso real del día y lugar
  (no es una aproximación fija de 1 hora).
- La detección de traslación/colección de luz es una primera versión: para
  casos límite, revisá siempre los aspectos crudos en el informe técnico.
