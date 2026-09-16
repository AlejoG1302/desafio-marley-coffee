# Desafío Marley Coffee · repositorio del equipo

Todo el trabajo del equipo para el **Desafío Marley Coffee**, Taller Aplicado de Marketing III (TMA1103), Ingeniería en Marketing Digital, Duoc UC · 2026. Este repositorio es la **fuente única**: si algo cambia, se cambia acá.

## Links en línea

| Qué | Link |
|---|---|
| Presentación EP4 (propuesta) | https://alejog1302.github.io/marley-propuesta/ |
| Prototipo de la consola | https://alejog1302.github.io/marley-consola/ |

## Qué hay en cada carpeta

| Carpeta | Contenido |
|---|---|
| `01-diagnostico/` | EP1 y EP2: diagnóstico omnicanal, punto de fuga, revisiones, guion y la presentación del diagnóstico (HTML y PDF) |
| `02-informe-EP3/` | Informe EP3 (`Informe-EP3-Marley.docx`), **lista de pendientes del equipo** (`Pendientes-Informe-EP3.docx`) y fuentes con enlaces |
| `03-presentacion-EP4/` | Presentación EP4 (HTML y PDF), versión anterior con más texto, video demo (MP4) y GIF para PowerPoint o Google Slides |
| `04-prototipo-consola/` | Código de la consola: se abre `index.html` en el navegador, sin instalar nada |
| `05-video-demo-hyperframes/` | Fuente del video demo, hecho con HyperFrames |
| `06-costeo/` | Modelo de costeo en Excel (**desactualizado**: todavía dice piloto de 36 puntos) |
| `herramientas/` | Scripts que regeneran el informe, el costeo y el PDF de la presentación |

## Estado (16-09-2026)

- EP1 y EP2 evaluadas. Ahora vienen **EP3 · informe (8%)** y **EP4 · presentación (12%, 15 min, nota individual)**, ambas en la semana 10.
- **Informe EP3:** redactado hasta donde llega la información disponible. Lo que falta está marcado en amarillo entre corchetes ⟦ ⟧ y explicado en `Pendientes-Informe-EP3.docx`. Se actualiza cuando el equipo avance esos pendientes.
- **Presentación EP4:** lista, en versión para directorio (14 láminas). **Falta la declaración de uso de IA**, que la pauta exige en una lámina final o en un anexo.
- **Prototipo y video:** listos y publicados.

## Decisiones tomadas

1. **Objetivo general:** reducir la fuga estimada de ingresos del food service de 9,9% a 7,6% en doce meses, reteniendo en Horeca a los clientes que hoy se reconquistan (equivale a la meta oficial de retención Horeca de 86% a 90%).
2. **Piloto:** 8 locales Horeca y 6 OCS durante 90 días, sin hardware nuevo.
3. **Solución:** una consola interna para Marley conectada al CRM, al ERP y a un WhatsApp automatizado. El cliente no aprende ningún sistema nuevo.
4. **Despachos es un mapa, no logística:** muestra qué está por despachar, en ruta, el historial y la agenda. No se abordan bodegas, rutas ni transporte.
5. **Agenda con el cliente:** Marley avisa que se acerca la fecha, el cliente elige día y horario, y si tiene un imprevisto propone otra fecha. Marley no reagenda por su cuenta.
6. **Fuera por ahora:** telemetría de máquinas (hasta confirmar qué máquinas envían datos) y costos (se desarrollan en una etapa posterior).
7. **Validación:** no se ha hecho test con usuarios y así se declara. Si se hace o no, lo decide el equipo.
8. **Datos:** todos los datos del prototipo y del video son **sintéticos**. Nunca se inventan datos, fuentes, entrevistas ni resultados.

## Cómo regenerar documentos

Requiere Python 3 con `python-docx`, `openpyxl`, `playwright` y `pymupdf`.

```bash
python herramientas/ep3.py            # informe, pendientes y fuentes → 02-informe-EP3/
python herramientas/build-costeo.py   # costeo → 06-costeo/
python herramientas/verif_deck.py     # revisa que ninguna lámina desborde y captura cada lámina
```

## Qué no está en este repositorio

Por ser público, quedan fuera el material del curso (caso, pautas, rúbrica y video del kickoff), las grabaciones y la transcripción de la reunión con el docente. Los tiene Ale.
