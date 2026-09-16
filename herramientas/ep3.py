# -*- coding: utf-8 -*-
"""Genera el Informe EP3 (docx), los anexos editables (xlsx) y el archivo de pendientes (docx)."""
import re, os, json
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import openpyxl, io
from openpyxl.styles import Font, PatternFill, Alignment

ESC = str(__import__('pathlib').Path(__file__).resolve().parent.parent / '02-informe-EP3') + '/'   # salida: carpeta del informe
IMG = str(__import__('pathlib').Path(__file__).resolve().parent / 'ep3img') + '/'
VERDE = RGBColor(0x3B, 0x52, 0x18)
GRIS = RGBColor(0x55, 0x55, 0x55)
CENTRO = WD_ALIGN_PARAGRAPH.CENTER
ANCHO = 17.8  # cm útiles con márgenes de 1,9 cm en carta
SALIDAS = {}
def ruta_libre(nombre):
    # si el archivo está abierto en Word no se puede sobrescribir: se guarda con otro nombre y se avisa
    ruta = ESC + nombre
    try:
        if os.path.exists(ruta): open(ruta, 'r+b').close()
        return ruta
    except PermissionError:
        base, ext = os.path.splitext(nombre)
        alt = ESC + base + ' (actualizado)' + ext
        print('BLOQUEADO, abierto en otro programa:', nombre, '→', os.path.basename(alt))
        return alt

doc = None
nt = nf = 0

# ------------------------------------------------------------------ utilidades de formato
def fuente(style, nombre):
    style.font.name = nombre
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rpr.append(rf)
    for a in ('w:asciiTheme', 'w:hAnsiTheme', 'w:eastAsiaTheme', 'w:cstheme'):
        if rf.get(qn(a)) is not None:
            del rf.attrib[qn(a)]
    for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        rf.set(qn(a), nombre)

def nuevo_doc(encabezado):
    global doc, nt, nf
    doc = Document(); nt = nf = 0
    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21.59), Cm(27.94)
    s.left_margin = s.right_margin = Cm(1.9)
    s.top_margin, s.bottom_margin = Cm(1.8), Cm(1.6)
    s.different_first_page_header_footer = True
    n = doc.styles['Normal']; fuente(n, 'Calibri'); n.font.size = Pt(10)
    n.paragraph_format.space_after = Pt(4); n.paragraph_format.line_spacing = 1.07
    for nombre, tam, antes, color in (('Heading 1', 14, 14, VERDE), ('Heading 2', 11, 8, RGBColor(0x1C, 0x1C, 0x1C))):
        h = doc.styles[nombre]; fuente(h, 'Calibri')
        h.font.size = Pt(tam); h.font.bold = True; h.font.color.rgb = color
        h.paragraph_format.space_before = Pt(antes); h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
    fuente(doc.styles['List Bullet'], 'Calibri')
    # encabezado y número de página (no en la portada)
    hp = s.header.paragraphs[0]; hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = hp.add_run(encabezado); r.font.size = Pt(8); r.font.color.rgb = GRIS
    fp = s.footer.paragraphs[0]; fp.alignment = CENTRO
    campo(fp.add_run(), 'PAGE', '1').font.size = Pt(8)

def campo(run, instruccion, texto):
    for tipo, val in (('begin', None), ('instr', instruccion), ('separate', None), ('text', texto), ('end', None)):
        if tipo == 'instr':
            el = OxmlElement('w:instrText'); el.set(qn('xml:space'), 'preserve'); el.text = val
        elif tipo == 'text':
            el = OxmlElement('w:t'); el.text = val
        else:
            el = OxmlElement('w:fldChar'); el.set(qn('w:fldCharType'), tipo)
        run._r.append(el)
    return run

PAT = re.compile(r'(\*\*.+?\*\*|⟦.+?⟧|\*[^*]+?\*)')
def escribir(par, texto, size=None, bold=False, italic=False, color=None):
    for trozo in PAT.split(texto):
        if not trozo:
            continue
        if trozo.startswith('**'):
            r = par.add_run(trozo[2:-2]); r.bold = True
        elif trozo.startswith('*') and len(trozo) > 2:
            r = par.add_run(trozo[1:-1]); r.italic = True
        elif trozo.startswith('⟦'):
            r = par.add_run(trozo); r.bold = True; r.font.highlight_color = WD_COLOR_INDEX.YELLOW
        else:
            r = par.add_run(trozo)
            if bold: r.bold = True
        if italic: r.italic = True
        if size: r.font.size = Pt(size)
        if color is not None and not trozo.startswith('⟦'): r.font.color.rgb = color

def P(texto, size=None, after=4, italic=False, color=None, align=None, keep=False, before=None):
    p = doc.add_paragraph(); escribir(p, texto, size=size, italic=italic, color=color)
    p.paragraph_format.space_after = Pt(after)
    if before is not None: p.paragraph_format.space_before = Pt(before)
    if align is not None: p.alignment = align
    if keep: p.paragraph_format.keep_with_next = True
    return p

def viñeta(texto, size=None):
    p = doc.add_paragraph(style='List Bullet'); escribir(p, texto, size=size)
    p.paragraph_format.space_after = Pt(2)

def H1(t): doc.add_heading(t, level=1)
def H2(t): doc.add_heading(t, level=2)

def sombra(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr(); shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), fill); tcPr.append(shd)

def preparar_tabla(t, borde='C9C9C9'):
    tblPr = t._tbl.tblPr
    lay = OxmlElement('w:tblLayout'); lay.set(qn('w:type'), 'fixed'); tblPr.append(lay)
    if borde:
        b = OxmlElement('w:tblBorders')
        for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            el = OxmlElement(f'w:{e}'); el.set(qn('w:val'), 'single'); el.set(qn('w:sz'), '4')
            el.set(qn('w:space'), '0'); el.set(qn('w:color'), borde); b.append(el)
        tblPr.append(b)
    mar = OxmlElement('w:tblCellMar')
    for lado, v in (('left', 70), ('right', 70), ('top', 25), ('bottom', 25)):
        el = OxmlElement(f'w:{lado}'); el.set(qn('w:w'), str(v)); el.set(qn('w:type'), 'dxa'); mar.append(el)
    tblPr.append(mar)

def cap_tabla(texto):
    global nt; nt += 1
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(f'Tabla {nt} · '); r.bold = True; r.font.size = Pt(8.5); r.font.color.rgb = VERDE
    escribir(p, texto, size=8.5, color=GRIS)

def cap_fig(texto):
    global nf; nf += 1
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(f'Figura {nf} · '); r.bold = True; r.font.size = Pt(8.5); r.font.color.rgb = VERDE
    escribir(p, texto, size=8.5, color=GRIS)

def lectura(texto):
    P('Lectura: ' + texto, size=8.5, italic=True, color=GRIS, after=6, before=2)

def T(encabezados, filas, anchos, size=8, fill='E3EBD3'):
    t = doc.add_table(rows=1, cols=len(encabezados)); preparar_tabla(t)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(encabezados):
        c = t.rows[0].cells[i]; c.paragraphs[0].paragraph_format.space_after = Pt(0)
        escribir(c.paragraphs[0], h, size=size, bold=True); sombra(c, fill)
    for fila in filas:
        cells = t.add_row().cells
        for i, v in enumerate(fila):
            par = cells[i].paragraphs[0]; par.paragraph_format.space_after = Pt(0)
            par.paragraph_format.line_spacing = 1.0
            escribir(par, str(v), size=size)
    for row in t.rows:
        for i, w in enumerate(anchos):
            row.cells[i].width = Cm(w)
    trPr = t.rows[0]._tr.get_or_add_trPr(); th = OxmlElement('w:tblHeader'); th.set(qn('w:val'), 'true'); trPr.append(th)
    return t

def caja(texto, fill='EEF3E4', size=10.5):
    t = doc.add_table(rows=1, cols=1); preparar_tabla(t, borde='B9CB94')
    c = t.rows[0].cells[0]; c.width = Cm(ANCHO); sombra(c, fill)
    par = c.paragraphs[0]; par.paragraph_format.space_after = Pt(0); escribir(par, texto, size=size)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)

def figura(ruta, ancho):
    p = doc.add_paragraph(); p.alignment = CENTRO; p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(ruta, width=Cm(ancho))

def grilla(imgs, ancho=8.6):
    t = doc.add_table(rows=0, cols=2); preparar_tabla(t, borde=None)
    for i in range(0, len(imgs), 2):
        cells = t.add_row().cells
        for j, (ruta, etiqueta) in enumerate(imgs[i:i + 2]):
            par = cells[j].paragraphs[0]; par.alignment = CENTRO; par.paragraph_format.space_after = Pt(0)
            par.add_run().add_picture(ruta, width=Cm(ancho))
            p2 = cells[j].add_paragraph(); p2.alignment = CENTRO; p2.paragraph_format.space_after = Pt(5)
            escribir(p2, etiqueta, size=8, color=GRIS)
    for row in t.rows:
        for c in row.cells:
            c.width = Cm(ANCHO / 2)

def salto():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

# ------------------------------------------------------------------ datos compartidos (informe + anexos)
MATRIZ = [
    ('Base habilitante', 'B1 · Identidad de punto (RUT + local + máquina)', 'O4', 2, 5, 5, '1º · Fase 0'),
    ('Base habilitante', 'B2 · Consola centralizada', 'O2 · O5', 2, 5, 5, '1º · Fase 0'),
    ('Sobre la fuga', 'LE1 · Reposición instrumentada por WhatsApp', 'O1', 4, 4, 5, '2º · piloto de 90 días'),
    ('Sobre la fuga', 'LE2 · Anticipar por acumulación (semáforo)', 'O2', 5, 3, 3, '3º · opera sobre B2'),
    ('Perímetro', 'LE4 · Dato homologado con terceros', 'O3', 1, 3, 4, 'En paralelo desde el día 1'),
    ('Diferida', 'Portal web de autoservicio del cliente', 'O1', 4, 2, 2, 'Gatillo: adopción digital observada en LE1'),
    ('Diferida', 'Telemetría en máquinas', 'O2', 5, 1, 1, 'Gatillo: verificación técnica del parque'),
    ('Diferida', 'Modelo predictivo de fuga', 'O2', 3, 1, 2, 'Gatillo: volumen de casos suficiente'),
]

CRITERIOS = [
    ('Adopción del canal', 'Puntos del piloto con 2 o más pedidos registrados por WhatsApp', '≥60%', '30%–59%', '<30%'),
    ('Pedido asociado a su local', 'Pedidos con RUT, local y máquina', '≥95%', '80%–94%', '<80%: no se amplía'),
    ('Alertas gestionadas', 'Alertas amarillas o rojas con acción registrada en ≤2 días hábiles', '≥80%', '50%–79%', '<50%: falta responsable'),
    ('El semáforo discrimina', 'Puntos en amarillo o rojo', '10%–50% y ≥1 alerta antes de un reclamo', '>50%: recalibrar pesos', 'Ninguna alerta útil en 90 días'),
    ('Aviso de atraso proactivo', 'Pedidos atrasados avisados antes de que el cliente pregunte', '≥90%', '60%–89%', '<60%'),
    ('Visitas agendadas por el cliente', 'Repartos y mantenciones del piloto con día y franja elegidos por WhatsApp', '≥50%', '25%–49%', '<25%'),
    ('Ticket con máquina identificada', 'Tickets del piloto con máquina registrada', '100% (base 75% [C])', '90%–99%', '<90%'),
]

WORKFLOWS = [
    ('W1 · Lead web', 'Envía el formulario inteligente', 'Clasifica por canal, comuna, máquinas y tamaño; asigna ejecutivo; ofrece agendar por WhatsApp', 'Tres correos de valor en 10 días', 'Leads clasificados (OE5) · conversión 12%→18% [C]'),
    ('W2 · Bienvenida', 'Alta con ficha completa', 'Día 0: video «cómo pedir» · día 7: consejo de preparación · día 30: encuesta de esfuerzo de un toque', 'Tarea al ejecutivo el día 10', 'Primer pedido por WhatsApp'),
    ('W3 · Aviso de fecha de reparto', '5 días antes de la fecha estimada: último pedido + intervalo del local [S]', '«Se acerca tu fecha de reparto, ¿te gustaría programar el pedido?» con día y franja sugeridos', 'Recordatorio a las 24 h; si el local supera 1,25 veces su intervalo sin pedir, suma al semáforo', 'Repartos programados por el cliente'),
    ('W4 · Aviso de atraso', 'Hora comprometida vencida sin entrega', 'Aviso al cliente con nueva ventana horaria', '—', 'Atrasos avisados antes de preguntar'),
    ('W5 · Falla', 'El cliente reporta una falla', 'Ticket con máquina; aviso al tomar el caso y al cerrar; evaluación de un toque', 'Ticket sin técnico sobre 31 h escala a coordinación', 'Primera respuesta · tiempo de reparación'),
    ('W6 · Aviso de mantención', '5 días antes de cumplir 90 días desde la última mantención [S]', 'Ofrece días y franjas para la visita preventiva', 'Recordatorio a los 3 días', 'Mantenciones agendadas y al día'),
    ('W7 · Recordatorio y cambios', 'Día anterior a un reparto o visita, a las 17:00 [S]', '«Mañana llega tu pedido entre…» con Confirmar, Reagendar o Cancelar; el cambio actualiza la agenda de Despachos', 'La visita se mantiene', 'Cambios avisados a tiempo · visitas fallidas'),
    ('W8 · Cuenta en rojo', 'Puntaje del semáforo ≥7', 'Tarea al ejecutivo con los motivos: esa conversación la tiene una persona, no el bot', '—', 'Acción en ≤2 días hábiles'),
    ('W9 · Baja', 'Cierre de cuenta', 'Motivo de baja obligatorio y encuesta de salida', '—', 'Bajas con motivo: 0%→100%'),
]

KPIS = [
    ('Fuga estimada del food service', 'Comercial', 'Venta equivalente de puntos no renovados ÷ venta food service (perímetro Horeca + OCS)', '9,9% [D]', '7,6%', 'Trimestral'),
    ('Retención Horeca', 'Comercial', 'Clientes que renuevan ÷ clientes al inicio del período (móvil 12 meses)', '86% [C]', '90% [C]', 'Trimestral'),
    ('Reposición digital Horeca', 'Comercial', 'Pedidos por canal registrado ÷ pedidos Horeca', '18% [C]', '40% [C]', 'Mensual'),
    ('Conversión lead → cliente', 'Comercial', 'Clientes nuevos ÷ leads calificados', '12% [C]', '18% [C]', 'Mensual'),
    ('Leads clasificados', 'Comercial', 'Leads con canal, tamaño y potencial ÷ leads recibidos', '0% [S]', '100%', 'Mensual'),
    ('Detección anticipada', 'Comercial', 'Cuentas marcadas antes del reclamo o la baja ÷ cuentas que entraron en riesgo', '0% [S]', '60%', 'Mensual'),
    ('OTIF', 'Operacional', 'Pedidos completos y a tiempo ÷ pedidos entregados', '92% [C]', '≥96% [C]', 'Semanal'),
    ('Quiebres de stock OCS', 'Operacional', 'Puntos OCS con quiebre en el mes ÷ puntos OCS', '6,8% [C]', '≤4,8% (−30%) [C]', 'Mensual'),
    ('Primera respuesta técnica', 'Operacional', 'Horas promedio desde el aviso hasta que un técnico toma el ticket', '31 h [C]', 'Línea base en el piloto', 'Semanal'),
    ('Tiempo de reparación', 'Operacional', 'Horas promedio desde el aviso hasta la máquina operativa', 'Sin dato', 'Línea base en el piloto', 'Semanal'),
    ('Visitas agendadas por el cliente', 'Operacional', 'Repartos y mantenciones con día y franja elegidos ÷ visitas del piloto', '0% [S]', '≥50% [S]', 'Semanal'),
    ('Visitas fallidas', 'Operacional', 'Repartos o mantenciones sin nadie que reciba ÷ visitas realizadas', 'Sin dato', 'Línea base en el piloto', 'Semanal'),
    ('Tickets con máquina identificada', 'Operacional', 'Tickets con máquina ÷ tickets', '75% [C]', '100%', 'Mensual'),
    ('Fichas completas Horeca', 'Operacional', 'Locales con RUT, canal, ubicación, tamaño y potencial ÷ locales', '26% [D]', '80%', 'Mensual'),
    ('Terceros con dato homologado', 'Operacional', 'Puntos de terceros que entregan el formato ÷ 840', '0% [S]', '80%', 'Mensual'),
]

SUPUESTOS = [
    ('S-17', 'Reposición mensual por punto activo', 'El conteo de oportunidades de fuga (pedidos, fallos de promesa, reclamos)', 'Frecuencia real de pedido en el piloto'),
    ('S-18', 'El punto que no renueva factura como el promedio de su canal', 'La fuga estimada de 6,24% de las ventas', 'Venta por punto con el maestro de puntos'),
    ('S-19', 'La retención del caso, medida sobre clientes, se aplica a puntos', 'Los 287 puntos equivalentes', 'Relación cuenta–punto en el maestro'),
    ('S-20', 'La meta 86%→90% corresponde a Horeca', 'Los 46 puntos recuperables y el 7,6%', 'Confirmación con la empresa'),
    ('S-22', 'Mantención preventiva cada 90 días', 'El workflow W6 y el indicador de mantención al día', 'Política técnica vigente de Marley'),
    ('S-23', 'Pesos iniciales del semáforo y umbrales (amarillo 4, rojo 7)', 'Qué locales entran a la cola de Hoy', 'Calibración con el historial del piloto'),
    ('S-24', 'Umbrales de escalar, corregir o detener del piloto', 'La decisión al día 90', 'Revisión con el sponsor antes de iniciar'),
    ('S-25', 'El aviso de fecha sale 5 días antes y el recordatorio el día anterior a las 17:00, con franjas de tres horas', 'Los workflows W3, W6 y W7 y el calendario de Despachos', 'Franjas reales de reparto y visita técnica por zona (P-21)'),
    ('H-1', 'La fuga se asocia a una acumulación de fricciones', 'El diseño del semáforo', 'Motivo de baja, historial por punto y entrevistas'),
    ('H-2', 'El cliente acepta pedir por un canal que registra el pedido', 'La adopción del MVP', 'Adopción observada en el piloto y entrevistas'),
]

# ================================================================== INFORME EP3
nuevo_doc('Marley Coffee · Propuesta inicial integrada · EP3 · TMA1103')

# ---------- portada
for _ in range(5): P('', after=0)
P('DESAFÍO MARLEY COFFEE · TALLER APLICADO DE MARKETING III · TMA1103', size=9, color=GRIS, after=10)
p = P('Retener en vez de reconquistar', after=4); p.runs[0].font.size = Pt(30); p.runs[0].bold = True; p.runs[0].font.color.rgb = VERDE
P('Propuesta inicial integrada: MVP, UX/UI, Inbound automatizado y e-commerce para el food service de Marley Coffee', size=14, after=30)
P('Evaluación Parcial N°3 · Encargo grupal', size=11, after=2)
P('Ingeniería en Marketing Digital · Duoc UC · Centro de Negocios', size=11, after=24)
P('Integrantes: ⟦Nombres completos del equipo⟧', size=10.5, after=2)
P('Docente: ⟦Nombre del docente⟧ · Sección: ⟦Sección⟧', size=10.5, after=2)
P('Entrega: semana 10 · ⟦Fecha de entrega⟧', size=10.5, after=40)
P('Todas las cifras internas son supuestos académicos del documento del desafío, no desempeño real auditado de Marley Coffee. '
  'El prototipo usa exclusivamente datos sintéticos.', size=8.5, italic=True, color=GRIS)
salto()

# ---------- índice
P('**Índice**', size=14, color=VERDE, after=8)
campo(doc.add_paragraph().add_run(), 'TOC \\o "1-2" \\h \\z \\u', 'Clic derecho → Actualizar campo para generar el índice.')
P('Régimen de fuentes: [C] dato del caso (supuesto académico) · [P] dato público · [D] derivación propia · [S] supuesto del equipo · '
  '[H] hipótesis · [EV] evidencia propia. Las fuentes, con enlace y fecha de consulta, están en Fuentes-Informe-EP3.docx. '
  'Lo que aparece entre corchetes y resaltado en amarillo está pendiente y se explica en Pendientes-Informe-EP3.docx.',
  size=8.5, color=GRIS, before=10)
salto()

# ---------- resumen ejecutivo
H1('Resumen ejecutivo')
P('**Marley Coffee no retiene a sus clientes food service: los reconquista en cada reposición.** En Horeca, el 82% de los pedidos se gestiona '
  'por ejecutivo, correo o mensajería y no queda como pedido con estado [C]. Bajo los supuestos declarados en §1.1, la no-recompra de Horeca y '
  'OCS equivale a una fuga estimada de 9,9% del food service al año —6,24% de las ventas totales— [D]: de los 21,9 puntos de venta nueva que '
  'exige la meta de +12%, 9,9 sólo compensan lo perdido.')
P('La propuesta no le pide al cliente que cambie de canal. El cliente sigue usando WhatsApp, ahora automatizado: Marley le escribe cuando se '
  'acerca su fecha de reparto o de mantención, el cliente la programa según su disponibilidad y puede reagendarla; además repite su pedido con '
  'el precio de su contrato, ve dónde va y reporta fallas sin llamar. Marley suma una consola propia que conecta el CRM, el ERP y ese canal, '
  'ordena cada local en un semáforo de riesgo explicable y muestra a quién llamar hoy, qué está agendado y qué máquina lleva horas sin técnico.')
P('El objetivo es **reducir la fuga estimada de ingresos del food service de 9,9% a 7,6% en doce meses, reteniendo en Horeca a los clientes que '
  'hoy se reconquistan**. El MVP se pilota 90 días en 14 puntos —8 Horeca y 6 OCS, el máximo que permite el caso— y sólo se escala si cumple '
  'criterios fijados de antemano. El costeo se desarrollará en una etapa posterior, dentro del tope de $220 millones que fija el caso [C].')

# ================================================================== 1.1
H1('1.1 Problema priorizado, propuesta de valor y plan de mejora · IE2.1.1')
H2('1.1.1 El problema priorizado')
P('**Marley Coffee no retiene a sus clientes food service: los reconquista.** Cada reposición reinicia la gestión de compra fuera de todo sistema, '
  'y cada reinicio expone al cliente a un atraso, un quiebre o una máquina detenida que nadie vincula con su cuenta.')
cap_tabla('Fuga estimada por no-recompra · anual · puntos equivalentes y % de ventas · Fuente: caso [C] y derivación propia [D]')
T(['Canal', 'Retención [C]', 'Puntos equivalentes perdidos [D]', '% de las ventas totales [D]', '% de la fuga'],
  [['Horeca', '86%', '161', '5,04%', '81%'],
   ['Office Coffee Service', '90%', '126', '1,20%', '19%'],
   ['Estaciones y panaderías', 'Sin dato', 'No medible', '15% de las ventas sin medir', '—'],
   ['**Total conocido**', '', '**287**', '**6,24% (= 9,9% del food service)**', '100%']],
  [4.2, 2.6, 3.6, 4.6, 2.8])
lectura('es una estimación, no una pérdida observada. Aplica la retención del caso, medida sobre clientes, a los puntos activos (S-19) y asume que '
        'cada punto pesa lo mismo que el promedio de su canal (S-18). Como dos canales no reportan retención, la cifra es un piso.')
P('**Por qué es el problema a priorizar.** Contra la meta de +12% en food service, el 45% de la venta nueva necesaria sólo repone la fuga [D]. '
  'Horeca concentra el 81% de esa fuga y es el único canal donde Marley interviene sin permiso de terceros. El docente validó el foco en '
  'retención y pidió sostenerlo en tres o cuatro causas (reunión del 08-09-2026).')

cap_tabla('De la causa a la oportunidad · Fuente: diagnóstico EV1 corregido; evidencia del caso [C]')
T(['Causa', 'Evidencia', 'Oportunidad, formulada sin solución'],
  [['C1 · La reposición no está digitalizada en su origen', '82% de reposición manual; el pedido no tiene estado [C]', 'O1 · Que cada pedido deje rastro sin que el cliente cambie de canal'],
   ['C2 · No hay señal propia en el punto: la marca opera reactiva', 'Quiebres en 6,8% de los puntos OCS al mes; 31 h de primera respuesta [C]; «el cliente habla cuando ya se quedó sin café» (docente)', 'O2 · Que Marley sepa que un punto se deteriora antes de que deje de comprar'],
   ['C3 · Terceros sin gobierno de datos', '840 puntos (24,8%) con dato mensual, agregado o inexistente [C]', 'O3 · Que el dato de terceros llegue en un formato cruzable'],
   ['C4 · Sin identidad común (condición de invisibilidad)', 'Sin identificador único de cliente ni punto; 26% de fichas completas [D]; máquina identificada en 75% de los tickets [C]', 'O4 · Que toda interacción quede asociada a un RUT, un local y una máquina'],
   ['Amplificador · Carga del ejecutivo [H]', 'Si el 82% pasa por el ejecutivo, el seguimiento es lo primero que se cae [H]', 'O5 · Que el tiempo comercial vaya a las cuentas en riesgo y no a transcribir pedidos']],
  [5.0, 6.4, 6.4])
P('Las fallas de servicio existen y el caso no permite descartarlas como causa. Lo que explica que persistan es estructural: sin trazabilidad por '
  'punto, Marley no puede comprenderlas ni gestionarlas antes de que el cliente se vaya.', before=6)
P('Faltan cuatro piezas que el docente pidió para sostener el problema antes de la solución. Cada una entra aquí como síntesis de tres a cinco '
  'líneas; qué buscar para cada una está en Pendientes-Informe-EP3.docx.', size=9, before=4, after=2)
for falta in ['⟦Falta: línea base integrada — una tabla única con la situación actual de los cuatro canales (ventas, puntos, retención, NPS, OTIF, quiebres, reposición digital) que muestre desde dónde parte la propuesta⟧',
              '⟦Falta: segmentación dentro de cada canal — no todos los clientes Horeca u OCS son iguales: separarlos por quién decide, qué compra y cuánto control tiene Marley, para justificar dónde parte el piloto⟧',
              '⟦Falta: evidencia UX — cómo viven los clientes estas fricciones, según el social listening y las entrevistas a decisores⟧',
              '⟦Falta: trazabilidad BI–UX — qué indicador de negocio corresponde a cada momento del cliente y cuáles no se pueden observar hoy por local⟧']:
    viñeta(falta, size=9)

H2('1.1.2 Decisión: qué se prioriza y por qué')
P('El journey de ocho etapas del diagnóstico ubica la fuga en el ciclo que se repite doce veces al año —reposición, incidencia y renovación—, las tres '
  'de severidad crítica. Las opciones se puntuaron por impacto sobre la fuga × confianza × evidencia, de 1 a 5 cada uno (máximo 125), y se '
  'ordenaron por dependencia: nada se ejecuta antes de aquello de lo que depende.')
cap_tabla('Matriz de decisión · puntaje = impacto × confianza × evidencia, máximo 125 · Fuente: equipo')
T(['Grupo', 'Opción', 'Atiende', 'Imp.', 'Conf.', 'Evid.', 'Puntaje', 'Decisión'],
  [[g, o, a, i, c, e, i * c * e, d] for g, o, a, i, c, e, d in MATRIZ],
  [2.3, 5.2, 1.6, 1.0, 1.1, 1.1, 1.4, 4.1])
lectura('el puntaje mide la solidez del argumento, no el orden de construcción: B1 y B2 van primero aunque puntúen menos, porque sin ellas LE1 y '
        'LE2 producen datos que no se cruzan. Escalas: impacto 5 = toda la fuga medible, 4 = la de Horeca (81%); confianza 5 = no depende de terceros '
        'ni de hipótesis; evidencia 5 = dato del caso. La telemetría queda fuera hasta confirmar qué máquinas del parque pueden enviar datos; con esa '
        'información se evalúa su incorporación.')

H2('1.1.3 Objetivos')
caja('**Objetivo general.** Reducir la fuga estimada de ingresos del food service de 9,9% a 7,6% en doce meses, reteniendo en Horeca a los '
     'clientes que hoy se reconquistan.')
P('7,6% es la traducción exacta a ingresos de la meta oficial de retención Horeca de 86% a 90% [C], medida sobre el mismo perímetro Horeca + OCS. '
  'Los cinco objetivos específicos aumentan las capacidades que reducen la fuga (OE1 a OE3) o la miden (OE4 y OE5).', size=9.5)
cap_tabla('Objetivos específicos · Fuente: meta oficial [C] o umbral de piloto del equipo [S]')
T(['OE', 'Objetivo específico', 'Se ejecuta con', 'Marca'],
  [['OE1', 'Aumentar las fichas completas de puntos Horeca de 26% a 80% en seis meses, para identificar cada baja.', 'B1', '[S]'],
   ['OE2', 'Aumentar la reposición Horeca digital de 18% a 40% en doce meses, para dejar de reconquistar.', 'LE1', '[C]'],
   ['OE3', 'Aumentar la detección anticipada de cuentas en riesgo de 0% a 60% en doce meses, para retenerlas.', 'LE2 sobre B2', '[S]'],
   ['OE4', 'Aumentar los puntos de terceros con datos homologados de 0% a 80% en ocho meses, para medir su fuga.', 'LE4', '[S]'],
   ['OE5', 'Aumentar los leads clasificados del formulario web de 0% a 100% en tres meses, para separar reposición de crecimiento.', 'Inbound (§1.5)', '[S]']],
  [1.2, 12.2, 2.8, 1.6])

H2('1.1.4 Propuesta de valor')
P('La propuesta tiene dos lados y una regla de diseño que viene del docente: **la señal no puede depender de que el cliente haga algo extra**. '
  'Al cliente se le quita trabajo; a Marley se le da visibilidad.')
cap_tabla('Propuesta de valor por usuario · Fuente: fricciones declaradas en el caso [C], docente y equipo')
T(['Usuario', 'Qué necesita resolver', 'Dolor hoy', 'Qué recibe', 'Beneficio esperado'],
  [['Dueño o administrador Horeca', 'Tener café en hora peak sin perseguir al proveedor', 'Sin visibilidad del pedido; fallas de máquina [C]', 'Aviso cuando se acerca su fecha de reparto para programarlo según su disponibilidad, con recordatorio y opción de reagendar; «lo de siempre» con su precio de contrato y tickets desde el chat', 'Recibe cuando está en el local y sabe qué esperar, sin aprender nada nuevo'],
   ['Encargado de facilities OCS', 'Que nadie en su empresa reclame por el café', 'Quiebres en 6,8% de los puntos al mes; 31 h de respuesta [C]', 'Reparto y mantención agendados cuando le acomoda; ticket con máquina identificada', 'Menos interrupciones y trazabilidad para responder hacia adentro'],
   ['Ejecutivo comercial Marley', 'Retener su cartera', '82% de reposición manual; seguimiento que se cae [C][H]', 'Cola «Hoy» con a quién llamar y por qué', 'Tiempo en cuentas en riesgo, no en transcribir pedidos'],
   ['Coordinación y servicio técnico', 'Cumplir la promesa', 'OTIF 92%; tickets sin integrar con CRM ni ventas [C]', 'Mapa de despachos —por despachar, en ruta, historial— y calendario de visitas; tickets por horas sin técnico', 'Menos viajes a locales cerrados y acción antes del reclamo'],
   ['Gerencia comercial', 'Saber si la fuga baja', 'Sin identificador único ni vista integrada [C]', 'Resumen por canal y zona; piloto frente a red', 'Decidir escalar, corregir o detener con datos']],
  [3.0, 3.3, 3.6, 4.4, 3.5])
P('**Diferenciación.** Nestlé, líder institucional con 60–70% [P], compite por continuidad operativa. En un barrido de nueve proveedores B2B, '
  'ninguno declaraba públicamente pedido con seguimiento ni reposición automática [EV, ago-2026; no declarado no significa que no exista]. '
  'Lo propio de Marley no es el semáforo: es convertir el canal que el cliente ya usa en el dato que lo alimenta, y cruzarlo con la máquina que '
  'Marley tiene en comodato.', before=6)

H2('1.1.5 Plan de mejora')
cap_tabla('Plan por fases · 12 meses · Fuente: equipo')
T(['Fase', 'Qué se hace', 'Qué deja', 'Decisión al cierre'],
  [['Fase 0 · semanas 1–6', 'Maestro de puntos del piloto y de Horeca (B1); consola base (B2); plantilla de terceros (LE4); motivo de baja obligatorio; aprobación de plantillas de WhatsApp y consentimiento', '14 puntos con ficha completa; formato de terceros enviado', 'Fichas del piloto al 100%, o se corrige antes de instrumentar'],
   ['Piloto · meses 2–4 (90 días)', 'Reposición y tickets por WhatsApp en 8 Horeca + 6 OCS (LE1); semáforo con reglas iniciales (LE2)', 'Primer historial por punto; OTIF y respuesta técnica medidos pedido a pedido', 'Criterios de la Tabla 10'],
   ['Mediano · meses 5–8', 'Calibrar pesos y umbrales con el historial; ampliar Horeca por tramos', 'Semáforo calibrado; 80% de los terceros entregando el formato', 'Ampliar sólo si se cumplen los umbrales'],
   ['Largo · meses 9–12', 'Escalar Horeca hasta 40% de reposición digital; alta con identidad obligatoria', 'Retención Horeca 90%; fuga estimada 7,6%', 'Reactivar las diferidas cuyo gatillo se cumpla']],
  [3.0, 6.8, 4.4, 3.6])
P('**Beneficio esperado.** Llevar Horeca de 86% a 90% equivale a unos 46 puntos al año, 1,44% de las ventas totales y 17% de la meta de expansión, '
  'sin abrir puntos nuevos [D]. El caso no entrega márgenes en pesos, así que el impacto se expresa en proporción del negocio; su valorización '
  'en pesos queda para la etapa de costeo.', before=6)

# ================================================================== 1.2
H1('1.2 Alcance del MVP, requerimientos, restricciones y criterios de éxito · IE2.1.2')
P('**El MVP** es una consola interna de Marley conectada al CRM, al ERP y a un WhatsApp automatizado, operando 90 días sobre 14 puntos: 8 Horeca y '
  '6 OCS de atención directa, el máximo que el caso permite en esos canales [C]. Pone a prueba dos hipótesis: que el cliente acepta pedir por un '
  'canal que registra el pedido (H-2) y que la fuga se anuncia por acumulación de fricciones (H-1).')
cap_tabla('Qué entra y qué queda fuera de la primera versión · Fuente: matriz de decisión (Tabla 3)')
T(['Entra en el MVP', 'Queda fuera, y por qué'],
  [['Maestro de puntos: RUT, local, máquina, contacto y condiciones de contrato (B1)', 'Portal web de autoservicio: el cliente ya pide por mensajería; se reactiva si la adopción digital aparece sola'],
   ['WhatsApp automatizado: aviso de fecha de reparto y de mantención con agenda por día y franja, recordatorio del día anterior, reagendar y cancelar; además repetir pedido con precio de contrato, últimos pedidos, productos disponibles, estado del envío, correo de confirmación y reporte de falla', 'Telemetría: todavía no se sabe qué máquinas del parque pueden enviar datos. Se incorporará cuando eso se confirme, como una fuente más y sin cambiar el resto del sistema'],
   ['Consola: Resumen, Hoy, Locales y ficha, Conversaciones, Pedidos, Despachos, Servicio técnico, Reglas e Integraciones', 'Modelo predictivo: 14 puntos no generan casos suficientes; se usa una regla explicable'],
   ['Semáforo de riesgo con reglas y pesos editables (LE2)', 'Pagos en línea: la factura la sigue emitiendo el ERP'],
   ['Registro de acciones comerciales (Llamé · Agendé visita · Resuelto) y motivo de baja obligatorio', 'Estaciones y panaderías en el piloto: requieren aprobación del operador; en esta fase sólo entregan datos (LE4)'],
   ['Enlace web para que repartidor y técnico registren entrega y cierre, sin instalar una app', 'Promociones o cambios de precio: el caso prohíbe modificar condiciones comerciales vigentes [C]'],
   ['Plantilla mensual homologada para terceros (LE4)', 'Ruteo, flota y gestión de bodega: la consola mapea estados y agenda; no planifica la logística']],
  [8.9, 8.9])

cap_tabla('Requerimientos esenciales · Fuente: equipo [S]; normativa [P]')
T(['Tipo', 'Requerimiento'],
  [['Funcional', 'Identificar el local por su número de WhatsApp y cruzarlo con RUT y máquina en el maestro de puntos'],
   ['Funcional', 'Crear el pedido en el ERP con el identificador del local y confirmar al cliente la fecha comprometida'],
   ['Funcional', 'Proponer la fecha de reparto o mantención según el ritmo del local, registrar día y franja elegidos, recordar el día anterior y permitir reagendar o cancelar'],
   ['Funcional', 'Abrir un ticket técnico con máquina y local desde el chat, y registrar primera respuesta y cierre'],
   ['Funcional', 'Calcular el semáforo por local con reglas visibles y mostrar el motivo de cada color'],
   ['Funcional', 'Registrar cada acción comercial y devolverla al CRM'],
   ['No funcional', 'Consentimiento explícito y finalidad declarada antes del primer mensaje: Ley 21.719, vigente desde el 1 de diciembre de 2026 [P]'],
   ['No funcional', 'Mensajes proactivos sólo con plantillas aprobadas por Meta, de categoría utilidad [P]'],
   ['No funcional', 'Cero capacitación para el cliente: todo ocurre en WhatsApp y correo'],
   ['No funcional', 'Cada dato muestra su antigüedad: un punto del piloto se actualiza en tiempo real y uno de tercero, una vez al mes'],
   ['No funcional', 'Sólo datos agregados, anonimizados o sintéticos durante el prototipo [C]']],
  [2.4, 15.4])

cap_tabla('Restricciones del cliente CN y cómo las respeta el MVP · Fuente: documento del desafío [C]')
T(['Restricción [C]', 'Cómo la respeta el MVP'],
  [['Presupuesto de $220 millones a 12 meses, sin IVA; el equipo interno no se imputa', 'Sin hardware y sobre sistemas que Marley ya tiene; el costeo se desarrolla en una etapa posterior'],
   ['Pilotos de hasta 90 días: 8 puntos Horeca y 6 OCS', '14 puntos durante 90 días'],
   ['No modificar precios, condiciones comerciales, packaging ni identidad visual', 'El bot muestra el precio vigente del contrato y no crea ofertas'],
   ['Toda intervención en puntos de terceros requiere su autorización', 'En sus 840 puntos sólo se pide un formato de datos'],
   ['La renovación de flota queda fuera del presupuesto', 'Sin hardware; telemetría diferida'],
   ['Equipo interno: sponsor 10%, líder de marketing 50%, comercial B2B 100%, analista de datos 50%', 'La consola la opera ese equipo; el desarrollo externo está costeado']],
  [8.9, 8.9])

cap_tabla('Criterios de éxito observables · al día 90 del piloto · % de puntos, pedidos, alertas o tickets · Fuente: umbrales del equipo [S]')
T(['Criterio', 'Cómo se mide', 'Escalar si', 'Corregir si', 'Detener si'],
  [list(c) for c in CRITERIOS],
  [3.2, 5.4, 3.4, 2.9, 2.9])
lectura('los umbrales se fijan antes de empezar y no después de mirar los resultados. Un resultado en «detener» también es válido: se sabría con '
        'antes de escalar y con la mayor parte del presupuesto sin usar.')

# ================================================================== 1.3
H1('1.3 Arquitectura de información, flujos de usuario y prototipo · IE2.2.1')
H2('1.3.1 Usuarios y tareas críticas')
cap_tabla('Tareas críticas y dónde las resuelve el prototipo · Fuente: journey del diagnóstico y caso [C]')
T(['Usuario', 'Tarea crítica', 'Etapa del journey · evidencia', 'Dónde se resuelve'],
  [['Cliente Horeca u OCS', 'Programar el reparto o la mantención para cuando va a estar en el local', 'E5 Reposición · 82% manual, sin estado [C]', 'WhatsApp: aviso de fecha, agenda y reagendar'],
   ['Cliente Horeca u OCS', 'Reportar una falla sin llamar', 'E6 Incidencia · 31 h de primera respuesta [C]', 'WhatsApp → ticket con máquina'],
   ['Ejecutivo comercial', 'Saber a quién llamar hoy y por qué', 'E7 Renovación · la baja no deja motivo registrado', 'Consola · Hoy'],
   ['Coordinación', 'Ver qué está por despachar, qué va en ruta y qué agendaron los clientes', 'E5 y E6 · OTIF 92% [C]', 'Consola · Despachos: calendario y estados'],
   ['Servicio técnico', 'Atender primero la máquina que más espera', 'E6 Incidencia · tickets sin integrar [C]', 'Consola · Servicio técnico'],
   ['Gerencia', 'Ver si la fuga baja en el piloto frente a la red', 'E7 Renovación · 26% de fichas completas [D]', 'Consola · Resumen, alcance piloto o red']],
  [3.0, 4.6, 5.4, 4.8])

H2('1.3.2 Arquitectura de información')
P('La consola se organiza en tres grupos de navegación y un selector de alcance que cambia todas las vistas entre el piloto (14 locales) y la red '
  'Horeca + OCS (2.410 locales). La entidad central es el **local**, identificado por RUT, código de local y número de máquina: pedidos, tickets, '
  'conversaciones, mantenciones y acciones cuelgan de él. En la red, un local sin ficha completa aparece como «No evaluable»: la ceguera queda a la vista.')
cap_tabla('Mapa de la consola · Fuente: prototipo del equipo')
T(['Grupo', 'Sección', 'Pregunta que responde', 'Usuario · cadencia'],
  [['Seguimiento', 'Resumen', '¿Cómo está la red hoy? Semáforo, prioridades, operación y riesgo por zona', 'Gerencia · semanal'],
   ['Seguimiento', 'Hoy', '¿A quién llamo y por qué? Cola con las acciones Llamé, Agendé visita y Resuelto', 'Ejecutivo · diaria'],
   ['Seguimiento', 'Locales → ficha', '¿Qué le pasa a este local? Identidad, motivos del color, contrato, mantención y línea de tiempo', 'Ejecutivo · a demanda'],
   ['Seguimiento', 'Conversaciones', '¿Qué habló el bot con el cliente? Una persona puede tomar la conversación', 'Ejecutivo · diaria'],
   ['Operación', 'Pedidos', '¿Qué entró y en qué estado está?', 'Coordinación · diaria'],
   ['Operación', 'Despachos', '¿Qué está por despachar, qué va en ruta, qué se entregó y qué repartos y mantenciones agendaron los clientes?', 'Coordinación · diaria'],
   ['Operación', 'Servicio técnico', '¿Qué máquina espera técnico, cuánto tarda la reparación y cuáles fallan seguido?', 'Servicio técnico · diaria'],
   ['Sistema', 'Reglas', '¿Por qué un local está en rojo? Pesos y umbrales editables', 'Analista · mensual'],
   ['Sistema', 'Integraciones', '¿Con qué se conecta y qué datos van y vuelven?', 'Analista · a demanda']],
  [2.3, 2.9, 9.2, 3.4])
cap_fig('Arquitectura: la consola conecta el CRM y el ERP con WhatsApp y los terceros; la telemetría queda como fuente futura · Fuente: prototipo, sep-2026')
figura(IMG + 'ep3-hub.png', 15.5)
P('En WhatsApp, el cliente ve un menú de seis opciones —repetir pedido, últimos pedidos, dónde va mi pedido, productos disponibles, reportar falla '
  'y hablar con mi ejecutivo— y recibe mensajes proactivos por plantilla: aviso de fecha de reparto y de mantención, recordatorio del día anterior y aviso de atraso.', size=9.5)

H2('1.3.3 Flujos principales')
cap_tabla('Flujos de usuario · Fuente: prototipo del equipo')
T(['Flujo', 'Gatillo', 'Recorrido', 'Dato que deja'],
  [['F1 · Reparto programado', 'Se acerca la fecha estimada: último pedido + intervalo del local', 'Aviso de Marley 5 días antes → el cliente elige día y franja → pedido programado en ERP y correo → recordatorio el día anterior con Confirmar, Reagendar o Cancelar → repartidor marca la entrega desde un enlace', 'Fecha acordada, cambios avisados y cumplimiento de la promesa'],
   ['F2 · Atraso', 'Pasa la hora comprometida sin entrega', 'La consola marca el despacho como atrasado → el bot avisa al cliente antes de que pregunte → coordinación lo ve primero en Despachos', 'Atraso medido y aviso registrado; suma al semáforo'],
   ['F3 · Falla de máquina', 'El cliente reporta por WhatsApp', 'Ticket con máquina y local → cola técnica ordenada por horas sin técnico → visita → cierre con causa y repuesto → el bot avisa y pide evaluación de un toque', 'Primera respuesta, tiempo de reparación y reincidencia'],
   ['F4 · Riesgo', 'El puntaje del local cruza un umbral: amarillo ≥4, rojo ≥7 [S]', 'El local entra a Hoy con sus motivos → el ejecutivo contacta → registra la acción → el CRM la recibe', 'Detección anticipada (OE3) y respuesta a la intervención'],
   ['F5 · Mantención y silencio', 'Faltan 5 días para cumplir 90 días sin mantención, o el local supera 1,25 veces su intervalo sin pedir', 'El bot ofrece días y franjas para la visita, con recordatorio y reagendar → si el local no responde ni pide, suma al semáforo', 'Mantención agendada y señal de riesgo']],
  [2.6, 3.4, 8.2, 3.6])

H2('1.3.4 Prototipo')
P('Prototipo funcional en HTML con datos sintéticos reproducibles: 2.410 locales y 180 días de pedidos e incidencias, generados con semilla fija y '
  'calibrados a las líneas base del caso (OTIF sintético de 91,9% frente a 92% [C]; 75% de tickets con máquina identificada [C]). Ningún dato del '
  'prototipo corresponde a clientes reales. El prototipo navegable está disponible en el repositorio indicado en el Anexo A.')
cap_fig('Pantallas del prototipo · alcance piloto · datos sintéticos con corte al 14-sep-2026 · Fuente: prototipo del equipo')
grilla([(IMG + 'ep3-resumen.png', 'a · Resumen: semáforo y prioridades'), (IMG + 'ep3-hoy.png', 'b · Hoy: cola con motivos y acciones'),
        (IMG + 'ep3-ficha.png', 'c · Ficha del local: por qué está en rojo'), (IMG + 'ep3-conv.png', 'd · Conversaciones: aviso de fecha y reagendamiento'),
        (IMG + 'ep3-despachos.png', 'e · Despachos: calendario de repartos y mantenciones'), (IMG + 'ep3-tecnico.png', 'f · Servicio técnico: horas sin técnico')])
cap_tabla('De la investigación al diseño · Fuente: caso [C], docente y literatura')
T(['Hallazgo', 'Decisión de diseño'],
  [['El 82% de la reposición ya pasa por mensajería o ejecutivo [C]', 'El cliente no aprende un sistema nuevo: pide por WhatsApp'],
   ['Docente: una solución que depende de que el dueño reporte algo, falla', 'Las señales salen del sistema: silencio, entregas, tickets y reclamos'],
   ['Sin visibilidad del pedido, primera fricción declarada de Horeca [C]', 'Estado del envío en el chat y aviso de atraso proactivo'],
   ['Tickets con máquina identificada sólo en el 75% de los casos [C]', 'El ticket nace en el chat con la máquina ya identificada'],
   ['Un reparto o una mantención en un local cerrado es un viaje perdido [H]', 'Marley avisa primero, el cliente elige día y franja y puede reagendar con aviso'],
   ['Priorizar por probabilidad de fuga suele ser inefectivo (Ascarza, 2018)', 'Reglas explicables con el motivo de cada color, en vez de una puntuación opaca']],
  [8.9, 8.9])

# ================================================================== 1.4
H1('1.4 Validación temprana de usabilidad y mejoras incorporadas · IE2.2.2')
P('**Qué se validó y qué no.** El prototipo pasó por dos instancias reales: la retroalimentación del docente sobre la solución (reunión del '
  '08-09-2026, grabada y transcrita) y revisiones de recorrido del equipo sobre las versiones 1 y 2 del prototipo. **No se ha aplicado un test '
  'de usabilidad con usuarios de Marley ni con clientes**: este apartado no reporta resultados de test, porque no existen. ⟦Pendiente: decisión del equipo sobre '
  'un test con usuarios⟧')
P('**Objetivo de la revisión:** comprobar si una persona ajena al diseño entiende, sin explicación, a quién llamar, por qué un local está en riesgo y '
  'con qué se conecta el sistema. **Escala de severidad** del equipo: 3 alta (impide completar una tarea crítica o entender la herramienta) · '
  '2 media (la tarea se completa con esfuerzo o ruido) · 1 baja (cosmética).', size=9.5)
cap_tabla('Hallazgos, severidad y mejoras incorporadas · septiembre de 2026 · Fuente: reunión docente y revisiones del prototipo')
T(['#', 'Fuente', 'Hallazgo o fricción', 'Sev.', 'Mejora incorporada'],
  [['1', 'Docente', 'Si el mecanismo depende de que el dueño del local reporte algo, falla: nunca tiene tiempo', '3', 'Ninguna señal del semáforo exige una acción voluntaria del cliente'],
   ['2', 'Docente', 'No meterse en logística: el rol del proyecto es entregar la data', '3', 'Despachos mapea estados y agenda; no planifica rutas, flota ni bodega'],
   ['3', 'Revisión v1', 'El Resumen mezclaba los objetivos del proyecto con la operación diaria', '2', 'Fuga y objetivos pasan a la presentación; el Resumen muestra sólo operación'],
   ['4', 'Revisión v1', 'No se entendía cómo decide el semáforo', '3', '«Cómo funciona» en tres pasos, escala de colores, ejemplo real y origen de cada señal (Figura 3)'],
   ['5', 'Revisión v1', 'No se veía que el sistema se conecta con lo que Marley ya tiene', '3', 'Sección Integraciones: qué recibe y qué devuelve cada sistema, en lenguaje no técnico'],
   ['6', 'Revisión v1', 'Faltaban los despachos y la medición de las reparaciones: coordinación y técnicos no tenían pantalla', '3', 'Módulos Despachos y Servicio técnico'],
   ['7', 'Revisión v1', 'La etiqueta «Piloto» se repetía en cada fila de la vista piloto', '1', 'Se muestra sólo en la vista de red completa'],
   ['8', 'Revisión v2', 'Cinco prioridades dejaban un hueco junto al semáforo del Resumen', '1', 'Tres prioridades y enlace a la cola completa'],
   ['9', 'Revisión v2', 'Despachos se leía como análisis logístico (cumplimiento semanal y por zona); lo que se necesita es ver estados y agenda', '3', 'Calendario, Por despachar, En ruta e Historial; aviso de fecha, recordatorio y reagendar por WhatsApp']],
  [0.6, 2.0, 6.6, 1.0, 7.6])
cap_fig('Mejora incorporada en Reglas: cómo funciona el semáforo, con un local real del piloto · Fuente: prototipo v2')
figura(IMG + 'ep3-reglas.png', 14.5)
P('**Verificación técnica.** Cada versión se recorrió de forma automatizada en sus 20 combinaciones de sección y alcance, sin errores, y las '
  'métricas sintéticas se contrastaron con las líneas base del caso.', size=9.5)
cap_tabla('Protocolo de test de tareas para la próxima iteración · 3 a 5 participantes con perfil comercial o de coordinación · Fuente: diseño del equipo')
T(['Tarea', 'Éxito si', 'Métrica'],
  [['T1 · Desde Resumen, encontrar el local más urgente y explicar por qué está en rojo', 'Nombra al menos dos motivos sin ayuda', 'Éxito · tiempo · errores'],
   ['T2 · Registrar que se llamó a ese local', 'La acción queda registrada en Hoy', 'Éxito · clics'],
   ['T3 · En el calendario de Despachos, encontrar qué local reagendó su reparto y para qué día', 'Responde correctamente', 'Éxito · tiempo'],
   ['T4 · Identificar la máquina que lleva más tiempo sin técnico', 'Responde correctamente', 'Éxito · tiempo'],
   ['T5 · Explicar con qué sistemas se conecta la consola', 'Menciona CRM, ERP y WhatsApp', 'Comprensión de 1 a 5']],
  [8.8, 5.0, 4.0])
P('Después de cada tarea se pide la dificultad percibida de 1 a 7. Los hallazgos se clasifican con la misma escala de severidad y se incorporan '
  'antes de la demostración.', size=9.5)

# ================================================================== 1.5
H1('1.5 Propuesta de Inbound Marketing automatizado · IE2.3.1')
P('El inbound de esta propuesta tiene dos motores sobre los mismos datos de la consola. El de **captación** reemplaza el formulario manual por uno '
  'que clasifica cada lead (OE5). El de **retención** —el que ataca la fuga— usa la base de clientes identificados para adelantarse: recordar la '
  'reposición, avisar atrasos y agendar mantenciones antes de que el cliente tenga que pedirlo.')
P('**Segmentación de trabajo**, preliminar sobre cortes del caso ⟦Pendiente: ajustar con la segmentación de 1.1⟧: por canal y control (Horeca independiente o cadena; OCS directo o vía '
  'XYZ SPA), por zona y promesa (RM 48 h; regiones 72–96 h), por ciclo de vida (lead, cliente nuevo de 0 a 90 días, recurrente, en riesgo, baja) '
  'y por color del semáforo.')
cap_tabla('Funnel, segmento y contenido · piezas a producir · Fuente: equipo')
T(['Etapa', 'Segmento', 'Pieza audiovisual', 'Pieza gráfica', 'Conversión buscada'],
  [['Atraer', 'Dueños Horeca y facilities OCS que aún no son clientes', 'Video de 30 s: pedir café en un minuto por WhatsApp, con la consola al lado', 'Guía descargable «Checklist de continuidad: café, máquina y reposición»', 'Descarga con formulario inteligente'],
   ['Convertir', 'Lead clasificado por canal y tamaño', 'Video de 60 s por canal: cómo funcionan el comodato y el soporte', 'Ficha comparativa de las modalidades de máquina del cotizador web [P]', 'Agenda con ejecutivo por WhatsApp'],
   ['Cerrar', 'Lead calificado', 'Demostración en vivo de 15 minutos', 'Propuesta con condiciones y promesa de entrega por zona', 'Alta con ficha completa (OE1)'],
   ['Retener', 'Cliente nuevo, 0 a 90 días', 'Video de 45 s: cómo pedir, seguir el envío y reportar fallas', 'Adhesivo QR en la máquina con el WhatsApp del local', 'Primer pedido por el canal'],
   ['Retener', 'Recurrente y en riesgo', 'Cápsula mensual de 60 s sobre preparación y limpieza', 'Recordatorio de mantención con fecha sugerida', 'Pedido, mantención agendada o respuesta']],
  [1.7, 3.2, 4.6, 4.6, 3.7])
cap_tabla('Workflows y gatilladores · Fuente: equipo; reglas implementadas en el prototipo')
T(['Workflow', 'Gatillador', 'Acción automática', 'Si no responde', 'KPI'],
  [list(w) for w in WORKFLOWS],
  [2.8, 3.3, 5.5, 3.0, 3.2])
P('**Herramientas:** API de WhatsApp Business mediante un proveedor autorizado, el CRM (el actual de Marley o HubSpot Starter, según el costeo) y '
  'correo transaccional; las reglas viven en la consola. **Medición:** cada workflow se evalúa por la conducta que produce —pedido, agenda, '
  'respuesta—, nunca por aperturas ni alcance. El costo de plantillas y automatizaciones se estima en la etapa de costeo.', before=6)

# ================================================================== 1.6
H1('1.6 Estrategia de e-commerce y mecanismos de conversión · IE2.3.2')
P('La estrategia es **comercio conversacional B2B**: la tienda está dentro del chat que el cliente ya usa. Cubre lo que el caso pide al portal '
  'transaccional de Horeca —catálogo, pedido recurrente, historial y condiciones por cuenta [C]— sin exigir que el cliente adopte una plataforma '
  'nueva. El portal web queda diferido con gatillo: se construye cuando los datos del piloto muestren demanda de autoservicio.')
cap_tabla('Canales y puntos de contacto · Fuente: equipo')
T(['Canal', 'Rol', 'Etapa'],
  [['Sitio web y formulario inteligente', 'Puerta de entrada de leads nuevos, con clasificación', 'Captación'],
   ['WhatsApp automatizado', 'Aviso de fecha y agenda, pedido, estado del envío, fallas y productos disponibles', 'Activación y recompra'],
   ['Correo transaccional', 'Confirmación y detalle del pedido', 'Cierre'],
   ['Ejecutivo comercial', 'Negociación, cuentas en rojo y toma de conversaciones', 'Cierre y retención'],
   ['QR en la máquina', 'Acceso directo al WhatsApp del local', 'Activación']],
  [4.6, 9.0, 4.2])
P('**Recorrido de recompra:** aviso de fecha de reparto → el cliente elige día y franja → confirmación y correo → recordatorio el día anterior '
  '(confirmar, reagendar o cancelar) → seguimiento del envío → entrega marcada → evaluación de un toque → siguiente aviso. **Recorrido de cliente nuevo:** búsqueda o recomendación → contenido → formulario → '
  'agenda por WhatsApp → demostración → propuesta → alta con ficha completa → bienvenida.', before=6)
cap_tabla('Mecanismos de conversión · Fuente: equipo; metas oficiales [C]')
T(['Mecanismo', 'Etapa', 'Por qué convierte', 'KPI'],
  [['Formulario inteligente con clasificación', 'Captación', 'Responde según canal y tamaño, no con una cotización genérica', 'Leads clasificados; conversión lead→cliente'],
   ['Agenda por WhatsApp el mismo día', 'Captación', 'Acorta la espera entre el interés y la conversación', 'Tiempo hasta el primer contacto'],
   ['«Repetir pedido» con precio de contrato', 'Activación y cierre', 'Un toque reemplaza la gestión con el ejecutivo', 'Reposición digital 18%→40% [C]'],
   ['Aviso de fecha de reparto con agenda por franja', 'Activación y recompra', 'El pedido se programa antes de que el local se quede sin café y para cuando hay alguien que lo reciba', 'Repartos programados por el cliente'],
   ['Productos disponibles en el menú', 'Cierre', 'Muestra el catálogo del contrato sin inventar promociones', 'Pedidos con más de un producto'],
   ['Fecha comprometida y aviso de atraso', 'Retención', 'La confianza se sostiene cuando el cliente sabe qué esperar', 'Recompra a 60 días; reclamos por 100 pedidos'],
   ['Traspaso a una persona', 'Cierre y retención', 'El bot resuelve lo repetitivo; la negociación sigue siendo humana', 'Conversaciones tomadas por un ejecutivo']],
  [4.4, 2.6, 6.4, 4.4])
P('**Aporte comercial.** En captación, el formulario deja de ser un buzón y produce leads medibles (OE5). En activación, el primer pedido ocurre en '
  'el canal registrado. En cierre y recompra, cada pedido deja historial, y ese historial es lo que permite retener (OE2 y OE3).', before=6)

# ================================================================== 1.7
H1('1.7 Requerimientos de cadena de suministro, fulfilment, distribución y KPIs · IE2.3.3')
P('**La propuesta no aborda la gestión logística.** Almacenamiento, bodegas, distribución y transporte siguen en manos de la operación de Marley: '
  'el docente advirtió que ese no es el rol del proyecto. Lo que la propuesta sí define es qué datos necesita de esa operación para mapear el estado '
  'de cada pedido y la agenda que acordó cada cliente, y con qué indicadores se monitorea el resultado comercial y operacional.')
cap_tabla('Datos que la consola necesita de la operación · Fuente: equipo; punto de partida tecnológico del caso [C]')
T(['Dato', 'Qué se registra', 'Para qué'],
  [['Pedido', 'Pedido en el ERP con el identificador del local y la fecha comprometida', 'Que cada pedido tenga historial y alimente el semáforo'],
   ['Estado del despacho', 'Salida a ruta y marca de entrega con hora, desde un enlace web del repartidor', 'Mapear por despachar, en ruta y entregado; medir OTIF pedido a pedido'],
   ['Agenda', 'Día y horario elegidos por el cliente, reagendamientos y cancelaciones', 'Mostrar el calendario de repartos y mantenciones, y avisar a tiempo'],
   ['Servicio técnico', 'Ticket con máquina, primera respuesta y cierre con causa', 'Medir la reparación completa, no sólo la primera respuesta'],
   ['Terceros', 'Plantilla mensual: local, RUT, fecha, producto, cantidad, quiebre e incidencia', 'Dato cruzable de los 840 puntos operados por terceros, sin integración']],
  [3.2, 8.2, 6.4])
cap_tabla('Restricciones y fricciones para obtener ese dato · Fuente: caso [C] y equipo')
T(['Fricción', 'Efecto', 'Mitigación'],
  [['El ERP no identifica el punto físico [C]', 'Pedido sin local ni historial', 'Maestro de puntos antes de instrumentar (Fase 0)'],
   ['Dueño ausente o local cerrado al llegar', 'Viaje perdido y local sin producto', 'Día y horario elegidos por el cliente, recordatorio y reagendar con aviso'],
   ['El repartidor no marca la entrega', 'OTIF no medible y aviso de atraso falso', 'Enlace de un toque; coordinación cierra los pendientes del día'],
   ['Plantillas de WhatsApp sin aprobar', 'No hay mensajes proactivos', 'Aprobación en Fase 0; el pedido iniciado por el cliente funciona igual'],
   ['Terceros que no entregan el formato', 'Sus 840 puntos siguen invisibles', 'Acuerdo operativo y renegociación a los 60 días'],
   ['Sin consentimiento del contacto', 'No se le puede escribir', 'Opt-in en el primer mensaje y registro de la autorización']],
  [5.4, 5.2, 7.2])
cap_tabla('KPIs comerciales y operacionales · horizonte 12 meses · Fuente: caso [C], derivación [D], equipo [S]; definiciones en el glosario')
T(['KPI', 'Tipo', 'Cálculo', 'Base', 'Meta', 'Frecuencia'],
  [list(k) for k in KPIS],
  [3.6, 1.9, 6.2, 1.9, 2.4, 1.8])
lectura('las bases [C] son supuestos académicos del caso; donde no hay base se declara en vez de estimarla. La fuga y la retención se leen sobre el '
        'perímetro Horeca + OCS; lo que mida OE4 en otros canales se reporta aparte.')

# ================================================================== cierre
H1('Glosario de métricas y definiciones')
T(['Término', 'Definición'],
  [['Fuga estimada', 'Venta equivalente de los puntos que no renuevan en un año, sobre la venta food service. Estimación bajo S-18 y S-19, no pérdida observada.'],
   ['Punto activo', 'Establecimiento con suministro vigente [C].'],
   ['Retención', 'Proporción de clientes que renuevan en el año [C].'],
   ['Reposición digital', 'Pedido que ingresa por un canal que lo registra con estado.'],
   ['OTIF', 'On Time In Full: pedidos entregados completos y dentro de la fecha comprometida.'],
   ['Quiebre de stock', 'Punto que se queda sin producto en el mes [C].'],
   ['Primera respuesta técnica', 'Horas desde el aviso de falla hasta que un técnico toma el ticket.'],
   ['Tiempo de reparación', 'Horas desde el aviso hasta que la máquina vuelve a operar.'],
   ['Semáforo de riesgo', 'Puntaje por local que suma señales negativas con pesos visibles; en la configuración inicial, amarillo desde 4 y rojo desde 7 puntos [S].'],
   ['Detección anticipada', 'Cuenta marcada en amarillo o rojo antes de un reclamo o de la baja.'],
   ['Ficha completa', 'Local con RUT, canal, ubicación, tamaño y potencial registrados.'],
   ['Lead clasificado', 'Lead con canal, tamaño y potencial asignados al ingresar.'],
   ['Plantilla de utilidad', 'Mensaje proactivo de WhatsApp aprobado por Meta para avisos transaccionales [P].'],
   ['Reparto programado', 'Pedido cuyo día y franja eligió el cliente después del aviso de Marley.'],
   ['Visita fallida', 'Reparto o mantención que no se concreta porque no hay quien reciba.'],
   ['Piloto', 'Prueba de 90 días en 8 puntos Horeca y 6 OCS de atención directa [C].']],
  [4.0, 13.8])

H1('Anexos')
T(['Anexo', 'Contenido', 'Enlace'],
  [['A', 'Prototipo funcional de la consola Marley con datos sintéticos: Resumen, Hoy, Locales, Conversaciones, Pedidos, Despachos, Servicio técnico, Reglas e Integraciones', 'Repositorio: github.com/AlejoG1302/marley-consola · En línea: alejog1302.github.io/marley-consola']],
  [1.4, 11.0, 5.4])

SALIDAS['informe'] = ruta_libre('Informe-EP3-Marley.docx'); doc.save(SALIDAS['informe'])
print('informe docx ok · tablas', nt, '· figuras', nf)

# ================================================================== PENDIENTES
nuevo_doc('Pendientes del Informe EP3 · Marley Coffee')
p = P('Pendientes del Informe EP3', after=2); p.runs[0].font.size = Pt(22); p.runs[0].bold = True; p.runs[0].font.color.rgb = VERDE
P('Qué falta, por qué hace falta y qué hay que buscar para completarlo · 13 de septiembre de 2026', size=10, color=GRIS, after=10)
P('**Cómo usar este archivo.** Todo lo que en el informe aparece entre corchetes y resaltado en amarillo está explicado aquí, con el mismo nombre. '
  'No hay responsables asignados: el equipo se organiza. Al completar algo, se reemplaza el texto resaltado del informe.')
caja('**Regla de la pauta que no se negocia:** no se permite inventar datos, fuentes, entrevistas, resultados de test ni métricas. Si algo no se '
     'consigue a tiempo, el informe lo declara como pendiente o como supuesto; nunca se rellena.', fill='FFF6DB')

def ficha(titulo, filas):
    H2(titulo)
    t = doc.add_table(rows=0, cols=2); preparar_tabla(t); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for a_, b_ in filas:
        c = t.add_row().cells
        escribir(c[0].paragraphs[0], a_, size=9, bold=True); sombra(c[0], 'F3F1EC')
        escribir(c[1].paragraphs[0], b_, size=9)
        for x in c: x.paragraphs[0].paragraph_format.space_after = Pt(0)
    for row in t.rows:
        row.cells[0].width = Cm(3.4); row.cells[1].width = Cm(14.4)

H1('1 · Piezas que faltan en el apartado 1.1')
P('En el feedback escrito de la primera evaluación, el docente pidió ordenar el argumento con esta cadena: línea base integrada → segmentación → '
  'evidencia UX → journey → trazabilidad BI–UX → causas → oportunidades → criterios → matriz de decisión. El informe ya tiene el journey, las causas, '
  'las oportunidades, los criterios y la matriz. **Faltan los cuatro eslabones de abajo.** Cada uno entra en el informe como síntesis de tres a cinco '
  'líneas, en el recuadro amarillo del apartado 1.1.1.')
ficha('1.1 · Línea base integrada', [
    ['Qué es', 'Una sola tabla con la foto actual de los cuatro canales, antes de cualquier propuesta.'],
    ['Por qué hace falta', 'Hoy esos datos están repartidos en distintas partes del diagnóstico. El docente pidió verlos juntos, en una vista, antes de hablar de problemas.'],
    ['Qué buscar y dónde', 'Todo está en el documento del desafío: por canal, % de ventas, puntos activos, máquinas, retención, NPS, OTIF, quiebres de stock, disponibilidad de máquinas, reposición digital y qué datos existen hoy. No hay que inventar nada: cada celda se marca [C] si es dato del caso o [D] si es un cálculo propio.'],
    ['Cómo debe quedar', 'Una tabla compacta y tres a cinco líneas de lectura: qué canal pesa más, cuál tiene fuga medible y dónde no hay datos.'],
])
ficha('1.2 · Segmentación dentro de cada canal', [
    ['Qué es', 'Dividir cada canal en grupos de clientes que se comportan distinto.'],
    ['Por qué hace falta', 'El informe anterior no tenía segmentación y el docente lo marcó. Además justifica por qué el piloto parte con Horeca y OCS de atención directa, y por qué la propuesta de valor cambia según quién decide.'],
    ['Qué buscar y dónde', 'Los cortes que ya da el caso. Horeca: 68% en RM y el resto en regiones; independientes y cadenas. OCS: 310 puntos vía XYZ SPA y 950 directos u otros operadores. Panaderías: 140 de una cadena regional, 210 en seis cadenas medianas y 270 independientes. Estaciones: 95 con operador nacional, 85 con operadores regionales y 180 independientes. Para cada segmento: qué compra, quién decide, qué fricción vive y cuánto control tiene Marley. Las entrevistas y el social listening ayudan a completarlo.'],
    ['Cómo debe quedar', 'Tabla segmento · quién decide · qué compra · fricción principal · control de Marley, más tres a cinco líneas. Con esto también se ajusta la segmentación preliminar del apartado 1.5.'],
])
ficha('1.3 · Evidencia UX', [
    ['Qué es', 'Cómo viven los clientes las fricciones, contado desde ellos y no desde los indicadores.'],
    ['Por qué hace falta', 'El docente dijo que el diagnóstico se dedujo del funcionamiento operacional del caso y que faltó contrastarlo con fuente primaria.'],
    ['Qué buscar y dónde', 'Dos fuentes. Uno: el social listening que ya existe (109 registros, 66 de voz orgánica, agosto de 2026); sacar temas y citas, y declarar que casi todo viene del canal de conveniencia, así que no se puede trasladar a OCS. Dos: las entrevistas a decisores del punto 2.1.'],
    ['Cómo debe quedar', 'Tres a cinco hallazgos, cada uno con una cita textual, el canal y la fuente, y una línea con los límites de la evidencia.'],
])
ficha('1.4 · Trazabilidad BI–UX', [
    ['Qué es', 'Una tabla que une cada indicador de negocio con el momento del cliente donde se produce.'],
    ['Por qué hace falta', 'Es la pieza que prueba la idea central del informe: los indicadores existen a nivel agregado, pero no se pueden bajar a cada local ni cruzar con lo que vive el cliente. El docente la pidió de forma explícita.'],
    ['Qué buscar y dónde', 'Los indicadores del caso (retención, OTIF, reclamos, quiebres, respuesta técnica, reposición digital, NPS, conversión de leads), las ocho etapas del journey, la fuente de cada dato (ERP, CRM, sistema de tickets, planillas de terceros, encuestas) y si hoy se puede ver por local. El caso ya dice que no existe un identificador único de cliente ni de punto.'],
    ['Cómo debe quedar', 'Tabla indicador · etapa del journey · cómo lo vive el cliente · fuente del dato · ¿se puede observar hoy por local?, más tres líneas de lectura.'],
])

H1('2 · Investigación')
ficha('2.1 · Entrevistas a decisores', [
    ['Qué es', 'Conversaciones de 25 a 30 minutos con quien decide la compra de café: dueño o administrador en Horeca, encargado de compras o facilities en OCS.'],
    ['Por qué hace falta', 'Es la fuente primaria que alimenta la evidencia UX (1.3) y la validación (1.4). El docente la marcó como lo más atrasado del proyecto.'],
    ['Qué buscar', 'Mínimo una entrevista Horeca y una OCS; ideal, tres por canal. La pauta ya está hecha (Pauta entrevista Marley coffee.docx). Lo que hay que escuchar: qué pasó en los meses previos a cambiar de proveedor, sin sugerir la respuesta, y si aceptaría pedir y agendar repartos por WhatsApp.'],
    ['Cómo debe quedar', 'Audio con consentimiento, notas o transcripción, y una tabla hallazgo · cita textual · qué confirma o refuta. No reemplazar con opiniones propias.'],
])
ficha('2.2 · Telemetría de las máquinas', [
    ['Qué es', 'Saber si las máquinas de Marley pueden enviar datos solas: tazas servidas, nivel de café o alertas de falla.'],
    ['Por qué hace falta', 'No bloquea el informe: la telemetría queda fuera del MVP hasta tener esta información y se agregará después. Pero el docente anticipó que la pregunta va a salir en la presentación.'],
    ['Qué buscar y dónde', 'Qué marcas y modelos usa Marley (el cotizador de marleycoffee.cl ofrece automática, bar con molinillo, pods y oficina) y la ficha técnica del fabricante: conectividad, contadores de servido, conexión vía API. También se puede consultar al Centro de Negocios.'],
    ['Cómo debe quedar', 'Tabla modelo · ¿envía datos? · cómo · fuente con fecha de consulta.'],
])
ficha('2.3 · Datos que el caso no entrega', [
    ['Qué es', 'Información que ayudaría a afinar las cifras, si el Centro de Negocios la responde.'],
    ['Qué buscar', 'Cada cuánto pide realmente un local (hoy se supone una vez al mes) · si Marley registra el motivo cuando un cliente se va · cuántos leads llegan y qué es un lead calificado para Marley · cuántos de los 950 puntos OCS son de atención directa · qué dicen los contratos con terceros sobre la entrega de datos.'],
    ['Cómo debe quedar', 'Cada dato que llegue reemplaza el supuesto correspondiente en el informe, con su fuente. Si no llega, el supuesto queda declarado como está.'],
])

H1('3 · A evaluación del equipo')
ficha('3.1 · Test de usabilidad con usuarios', [
    ['Qué es', 'Pedirle a tres a cinco personas que usen el prototipo con tareas concretas —encontrar el local más urgente, registrar una llamada, encontrar un reparto reagendado— y anotar dónde se traban.'],
    ['Por qué importa', 'El apartado 1.4 vale 15% de la nota y la pauta pide test, hallazgos, severidad y mejoras. Hoy el informe documenta la retroalimentación del docente y las revisiones del equipo, y declara que no hubo test con usuarios.'],
    ['Qué implicaría', 'El protocolo ya está en la tabla 16 del informe. Unos 20 minutos por persona, con perfiles comerciales o de coordinación de cualquier empresa B2B. Se reporta sólo lo que realmente pase.'],
    ['A debatir', 'Si se hace o no. Si no se hace, el texto actual del informe queda como está.'],
])

H1('4 · Forma y cierre del documento')
ficha('4.1 · Portada', [['Qué falta', 'Nombres completos del equipo, docente, sección y fecha de entrega.']])
ficha('4.2 · Texto reutilizado del informe anterior', [['Qué revisar', 'El piloto ahora es de 14 puntos: 8 Horeca y 6 OCS. Si se copia algo del informe de la primera evaluación, revisar que no diga 36 puntos, 20 Horeca ni panaderías en el piloto.']])
ficha('4.3 · Extensión y PDF final', [['Qué hacer', 'La pauta pide entre 12 y 15 páginas. Al agregar las piezas del punto 1, compactar. Al final, actualizar el índice (clic derecho sobre el índice → Actualizar campo) y exportar a PDF.']])
ficha('4.4 · Fuentes', [['Qué hacer', 'Las fuentes están en Fuentes-Informe-EP3.docx, con enlace y fecha de consulta. Si se agrega una fuente nueva, sumarla ahí con el mismo formato.']])

H1('5 · Lo ve Ale (presentación)')
viñeta('Video demo del prototipo para la presentación, como motion graphics hecho con HyperFrames.')
viñeta('Todo lo que se relacione con la presentación.')

H1('6 · Para más adelante o fuera del alcance')
viñeta('**Costos.** El costeo de la propuesta, incluidas las plantillas de WhatsApp y las automatizaciones, se trabaja en una etapa posterior. Hoy no se desglosa.')
viñeta('**Logística.** La propuesta no aborda bodegas, centros de distribución, hora de corte, franjas por zona ni operadores de transporte. No investigar ni agregar esos temas.')

SALIDAS['pendientes'] = ruta_libre('Pendientes-Informe-EP3.docx'); doc.save(SALIDAS['pendientes'])
print('pendientes docx ok')

# ================================================================== FUENTES
nuevo_doc('Fuentes del Informe EP3 · Marley Coffee')
p = P('Fuentes del Informe EP3', after=2); p.runs[0].font.size = Pt(22); p.runs[0].bold = True; p.runs[0].font.color.rgb = VERDE
P('Fuentes citadas en el informe, con enlace y fecha de consulta · 13 de septiembre de 2026', size=10, color=GRIS, after=8)
P('Las marcas son las mismas del informe: [C] dato del caso, [P] fuente pública y [EV] evidencia propia del equipo. Los enlaces se revisaron el '
  '13 de septiembre de 2026 para confirmar que respaldan lo que el informe afirma; las excepciones se detallan al final. Si se agrega una fuente '
  'nueva, sumarla aquí con el mismo formato.', size=9.5, after=6)

def enlace(par, url, size=8):
    rid = par.part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
    h = OxmlElement('w:hyperlink'); h.set(qn('r:id'), rid)
    run = OxmlElement('w:r'); rpr = OxmlElement('w:rPr')
    for tag, val in (('w:color', '1F4E9E'), ('w:u', 'single'), ('w:sz', str(int(size * 2)))):
        el = OxmlElement(tag); el.set(qn('w:val'), val); rpr.append(el)
    run.append(rpr); t = OxmlElement('w:t'); t.text = url; t.set(qn('xml:space'), 'preserve'); run.append(t)
    h.append(run); par._p.append(h)

FUENTES_DOC = [
    ('[C]', 'Duoc UC, Centro de Negocios (2026). *Desafío Marley Coffee*: documento de bajada, presentación y video de kickoff.', 'Todas las cifras marcadas [C]: ventas por canal, puntos, retención, OTIF, quiebres, respuesta técnica, metas y restricciones del piloto', None, 'Material del curso, no público', 'Julio 2026'),
    ('[C]', 'Duoc UC (2026). *Evaluación Parcial N°3: Propuesta inicial integrada*. Encargo, TMA1103.', 'Estructura y exigencias del informe', None, 'Material del curso, no público', 'Sept. 2026'),
    ('[P]', 'Fiscalía Nacional Económica (18 de agosto de 2025). *Informe de aprobación sobre adquisición de control en Promotora Chilena de Café Colombia S.A. por parte de Copec S.A.* Rol F422-2025.', '1.1.4 · Nestlé tiene 60–70% y Marley Coffee 10–20% del canal institucional', 'https://www.fne.gob.cl/wp-content/uploads/2025/08/inap_F422_2025.pdf', None, '13-09-2026'),
    ('[P]', 'Nestlé Professional (s.f.). *Máquinas de café para negocios en Chile*.', '1.1.4 · La oferta de Nestlé se apoya en comodato, instalación, capacitación y mantención preventiva y correctiva', 'https://www.nestleprofessional-latam.com/cl/bebidas/maquinas', None, '13-09-2026'),
    ('[P]', 'Ascarza, E. (2018). Retention futility: Targeting high-risk customers might be ineffective. *Journal of Marketing Research*, 55(1), 80–98.', '1.3.4 · Priorizar a los clientes con mayor probabilidad de fuga suele ser inefectivo; conviene priorizar por sensibilidad a la intervención', 'https://doi.org/10.1509/jmr.16.0163', None, '13-09-2026'),
    ('[P]', 'Ley N° 21.719, que regula la protección y el tratamiento de los datos personales y crea la Agencia de Protección de Datos Personales. Diario Oficial, 13 de diciembre de 2024.', '1.2 · Consentimiento para tratar datos personales; vigencia desde el 1 de diciembre de 2026', 'https://www.bcn.cl/leychile/navegar?idNorma=1209272', None, '13-09-2026'),
    ('[P]', 'Meta for Developers (s.f.). *Template categorization*. WhatsApp Business Platform.', '1.2 y glosario · Los mensajes proactivos usan plantillas aprobadas; la categoría utilidad es para avisos transaccionales', 'https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization', None, '13-09-2026'),
    ('[P]', 'Meta for Developers (s.f.). *Send messages*: ventana de servicio de 24 horas. WhatsApp Business Platform.', '1.2 · Fuera de la ventana de 24 horas sólo se pueden enviar plantillas aprobadas', 'https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages', None, '13-09-2026'),
    ('[P]', 'Meta for Developers (s.f.). *Getting opt-in*. WhatsApp Business Platform.', '1.2 y 1.7 · El cliente debe aceptar recibir mensajes antes de que la empresa le escriba', 'https://developers.facebook.com/documentation/business-messaging/whatsapp/getting-opt-in', None, '13-09-2026'),
    ('[P]', 'Marley Coffee Chile (s.f.). *Cotiza con Marley Coffee*.', '1.5 · El cotizador web ofrece modalidades de máquina: automática, bar con máquina y molinillo, pods y oficina', 'https://www.marleycoffee.cl/cotizaconmarleycoffee', None, '13-09-2026'),
    ('[EV]', 'Barrido propio de la oferta pública de nueve proveedores B2B de café en Chile (agosto de 2026).', '1.1.4 · Ninguno declaraba públicamente pedido con seguimiento ni reposición automática', None, 'Evidencia del diagnóstico (EV1)', 'Agosto 2026'),
    ('[EV]', 'Social listening exploratorio propio (agosto de 2026): 109 registros, 66 de voz orgánica.', '1.1.1 · Base de la evidencia UX, pendiente de sintetizar', None, 'Evidencia del diagnóstico (EV1)', 'Agosto 2026'),
    ('[EV]', 'Reunión de retroalimentación con el docente (8 de septiembre de 2026), grabación transcrita.', '1.1.1, 1.1.4, 1.4 y 1.7 · Foco en retención, la señal no puede depender del dueño del local, no abordar logística', None, 'Registro interno del equipo', '08-09-2026'),
    ('[EV]', 'Consola Marley: prototipo funcional con datos sintéticos (septiembre de 2026).', '1.3 y 1.4 · Pantallas, flujos y revisiones del prototipo', 'https://github.com/AlejoG1302/marley-consola', None, '13-09-2026'),
]
t = T(['', 'Fuente', 'Qué respalda en el informe', 'Enlace', 'Consulta'],
      [[m, ref, que, sin_url or '', fecha_] for m, ref, que, url, sin_url, fecha_ in FUENTES_DOC],
      [1.0, 5.6, 4.7, 4.7, 1.8])
for i, (_, _, _, url, _, _) in enumerate(FUENTES_DOC, start=1):
    if url:
        enlace(t.rows[i].cells[3].paragraphs[0], url)

H2('Notas de la verificación')
viñeta('**Ascarza (2018).** El texto completo está tras un muro de pago; la cita —DOI, volumen y páginas— se confirmó en SAGE, SSRN y la American Marketing Association.', size=9.5)
viñeta('**Ley 21.719.** El visor de la BCN no cargó el articulado en la revisión automática. La vigencia del 1 de diciembre de 2026 surge del artículo primero transitorio y la confirman varias fuentes legales; conviene abrir el enlace en un navegador y revisarlo.', size=9.5)
viñeta('**Marley Coffee.** Usar el enlace /cotizaconmarleycoffee: la dirección /cotiza que aparece en los buscadores hoy no muestra el cotizador.', size=9.5)
SALIDAS['fuentes'] = ruta_libre('Fuentes-Informe-EP3.docx'); doc.save(SALIDAS['fuentes'])
print('fuentes docx ok')
io.open('salidas.json', 'w', encoding='utf-8').write(json.dumps(SALIDAS))
