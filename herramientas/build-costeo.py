# -*- coding: utf-8 -*-
"""Costeo de abajo hacia arriba del MVP Marley + punto de equilibrio.
Todo número de entrada vive en 'Supuestos' con su fuente; el resto son fórmulas."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = str(__import__('pathlib').Path(__file__).resolve().parent.parent / '06-costeo' / 'Costeo-Marley.xlsx')

# ── estilos (convención de modelos financieros) ──
F  = 'Arial'
AZUL  = Font(name=F, size=10, color='0000FF')            # entrada editable
NEGRO = Font(name=F, size=10, color='000000')            # fórmula
VERDE = Font(name=F, size=10, color='008000')            # vínculo a otra hoja
BOLD  = Font(name=F, size=10, bold=True)
TIT   = Font(name=F, size=15, bold=True, color='2E5E1E')
SUB   = Font(name=F, size=10, italic=True, color='5A5A5A')
CAB   = Font(name=F, size=10, bold=True, color='FFFFFF')
SEC   = Font(name=F, size=10, bold=True, color='2E5E1E')
NOTA  = Font(name=F, size=9, color='5A5A5A')
F_CAB = PatternFill('solid', fgColor='2E5E1E')
F_SEC = PatternFill('solid', fgColor='EAF0E4')
F_AMA = PatternFill('solid', fgColor='FFFF00')           # supuesto clave / celda a completar
F_TOT = PatternFill('solid', fgColor='D9E6CC')
BORDE = Border(bottom=Side(style='thin', color='BFBFBF'))
WRAP  = Alignment(wrap_text=True, vertical='top')
CLP   = '$#,##0;($#,##0);-'
PCT   = '0.0%'
X     = '0.00"x"'

wb = Workbook()


def cab(ws, fila, textos):
    for i, t in enumerate(textos, 1):
        c = ws.cell(fila, i, t); c.font = CAB; c.fill = F_CAB
        c.alignment = Alignment(wrap_text=True, vertical='center')


def seccion(ws, fila, texto, ncols):
    c = ws.cell(fila, 1, texto); c.font = SEC
    for i in range(1, ncols + 1): ws.cell(fila, i).fill = F_SEC


def anchos(ws, lista):
    for i, w in enumerate(lista, 1): ws.column_dimensions[get_column_letter(i)].width = w


# ════════════════════════════════════════════ LEEME
ws = wb.active; ws.title = 'Leeme'
ws['A1'] = 'Costeo del MVP · Desafío Marley Coffee'; ws['A1'].font = TIT
ws['A2'] = 'Presupuesto construido de abajo hacia arriba y punto de equilibrio. Preparado para la reunión del miércoles.'
ws['A2'].font = SUB
filas = [
    ('', ''),
    ('CÓMO ESTÁ ARMADO', ''),
    ('Supuestos', 'Todas las tarifas, precios y volúmenes, cada uno con su fuente. Es la única hoja que hay que tocar.'),
    ('Costeo', 'Cada línea es cantidad × precio unitario. Los precios vienen de Supuestos; las horas son estimación del equipo.'),
    ('Resumen', 'Inversión inicial y costo recurrente por bloque, año 1 y año 2, contra el presupuesto comprometido.'),
    ('Equilibrio', 'Cuánto margen debe dejar cada punto recuperado para que el plan se pague. Tiene una celda para el dato real.'),
    ('', ''),
    ('CÓDIGO DE COLORES', ''),
    ('Texto azul', 'Entrada editable. Cambiarla recalcula todo el libro.'),
    ('Texto negro', 'Fórmula. No editar.'),
    ('Texto verde', 'Vínculo a otra hoja. No editar.'),
    ('Fondo amarillo', 'Supuesto clave, o celda que debe completar Marley.'),
    ('', ''),
    ('MARCAS DE FUENTE', ''),
    ('[C]', 'Dato del caso.'),
    ('[P]', 'Precio público de mercado, con fuente y fecha.'),
    ('[D]', 'Derivación aritmética sobre [C] o [P].'),
    ('[S]', 'Supuesto del equipo. Es lo primero que conviene discutir.'),
    ('', ''),
    ('LO QUE ESTE LIBRO NO HACE', ''),
    ('Ventas en pesos', 'El caso no entrega ventas, precio, ticket ni margen en pesos, y no existe una cifra pública de Chile. '
                        'Por eso el impacto se mide como punto de equilibrio y no como ROI.'),
    ('Tarifa de agencia', 'Se usa tarifa freelance: el costeo es un piso. Una agencia cobra más.'),
]
for i, (a, b) in enumerate(filas, 4):
    ca = ws.cell(i, 1, a); cb = ws.cell(i, 2, b)
    if b == '' and a:
        ca.font = SEC
    else:
        ca.font = BOLD; cb.font = NEGRO; cb.alignment = WRAP
ws['A12'].font = Font(name=F, size=10, bold=True, color='0000FF')
ws['A13'].font = Font(name=F, size=10, bold=True, color='000000')
ws['A14'].font = Font(name=F, size=10, bold=True, color='008000')
ws['A15'].fill = F_AMA
anchos(ws, [22, 100])

# ════════════════════════════════════════════ SUPUESTOS
sp = wb.create_sheet('Supuestos')
sp['A1'] = 'Supuestos'; sp['A1'].font = TIT
sp['A2'] = 'Texto azul = editable. Cada valor lleva su fuente. Cambiar un valor acá recalcula Costeo, Resumen y Equilibrio.'
sp['A2'].font = SUB
cab(sp, 4, ['Parámetro', 'Valor', 'Unidad', 'Fuente'])

# (fila, parámetro, valor o fórmula, unidad, fuente, formato, es_formula, clave)
S = [
    (5,  'TARIFAS DE DESARROLLO', None, None, None, None, False, False),
    (6,  'Desarrollador junior', 30000, 'CLP / hora', '[P] Apollo.TI, guía 2026: CLP 25.000–35.000/h', CLP, False, False),
    (7,  'Desarrollador semi-senior', 45000, 'CLP / hora', '[P] Apollo.TI, guía 2026: CLP 35.000–55.000/h', CLP, False, True),
    (8,  'Desarrollador senior', 65000, 'CLP / hora', '[P] Apollo.TI, guía 2026: CLP 55.000–80.000/h', CLP, False, False),
    (9,  'Mantención anual de integraciones', 0.175, '% del desarrollo', '[P] Apollo.TI: regla de mercado 15–20% anual. Se usa el punto medio', PCT, False, False),
    (10, 'PLATAFORMA Y LICENCIAS', None, None, None, None, False, False),
    (11, 'Plataforma BSP de WhatsApp', 26100, 'CLP / mes', '[P] ChatDaddy 2026, plan de entrada. Es un piso: otros proveedores cobran más', CLP, False, False),
    (12, 'Mensaje de utilidad de WhatsApp', 8.1, 'CLP / mensaje', '[P] Meta, tarifa Chile 2026: CLP 5,4–8,1. Se usa el techo', '#,##0.0', False, False),
    (13, 'Mensaje de servicio (ventana de 24 h)', 0, 'CLP / mensaje', '[P] Meta: sin cobro dentro de la ventana de servicio. El pedido lo inicia el cliente', CLP, False, False),
    (14, 'Licencia de CRM', 20, 'USD / usuario / mes', '[P] HubSpot Sales Hub Starter, G2 y Apexure, sep-2026', '#,##0', False, False),
    (15, 'Usuarios de CRM', 5, 'usuarios', '[S] comercial B2B, analista de datos, 2 coordinadoras, líder de proyecto', '#,##0', False, False),
    (16, 'Licencia de visualización', 0, 'CLP / mes', '[P] Looker Studio: sin costo de licencia en uso estándar', CLP, False, False),
    (17, 'MACRO', None, None, None, None, False, False),
    (18, 'Dólar observado', 925.65, 'CLP / USD', '[P] 9-sep-2026, Banco Central vía dolaronline.cl', '#,##0.00', False, False),
    (19, 'VOLUMEN', None, None, None, None, False, False),
    (20, 'Puntos Horeca activos', 1150, 'puntos', '[C] Base del caso', '#,##0', False, False),
    (21, 'Meta de reposición digital Horeca', 0.40, '% de puntos', '[C] Meta oficial a 12 meses', PCT, False, False),
    (22, 'Puntos en el canal instrumentado al mes 12', '=ROUND(B20*B21,0)', 'puntos', '[D] Puntos Horeca × meta digital', '#,##0', True, False),
    (23, 'Pedidos por punto al año', 12, 'pedidos', '[S] Supuesto S-17 del informe: reposición mensual', '#,##0', False, True),
    (24, 'Mensajes de utilidad por pedido', 3, 'mensajes', '[S] Confirmación, despacho y entrega', '#,##0', False, False),
    (25, 'RETENCIÓN Y EQUILIBRIO', None, None, None, None, False, False),
    (26, 'Retención Horeca actual', 0.86, '%', '[C] Línea base del caso', PCT, False, False),
    (27, 'Retención Horeca meta', 0.90, '%', '[C] Meta oficial a 12 meses', PCT, False, False),
    (28, 'Puntos recuperados por año', '=ROUND(B20*(B27-B26),0)', 'puntos equivalentes', '[D] El caso mide retención sobre clientes: es una equivalencia en puntos', '#,##0', True, False),
    (29, 'Factor de gradualidad del año 1', 0.5, 'fracción del año', '[S] La mejora opera de forma progresiva: en promedio, medio año de efecto', '0.00', False, True),
    (30, 'PRESUPUESTO', None, None, None, None, False, False),
    (31, 'Contingencia', 0.10, '% del subtotal', '[S] Práctica de mercado en proyectos de software', PCT, False, True),
    (32, 'Presupuesto máximo del caso', 220000000, 'CLP, sin IVA', '[C] §3.6 del caso, primeros 12 meses', CLP, False, False),
    (33, 'Presupuesto comprometido del informe', 83600000, 'CLP, sin IVA', '[C] Informe Final, tabla de presupuesto: 38% del total', CLP, False, False),
]
for fila, par, val, uni, fte, fmt, es_f, clave in S:
    if val is None:
        seccion(sp, fila, par, 4); continue
    sp.cell(fila, 1, par).font = NEGRO
    c = sp.cell(fila, 2, val); c.font = NEGRO if es_f else AZUL; c.number_format = fmt
    if clave: c.fill = F_AMA
    sp.cell(fila, 3, uni).font = NOTA
    d = sp.cell(fila, 4, fte); d.font = NOTA; d.alignment = WRAP
    for col in range(1, 5): sp.cell(fila, col).border = BORDE
anchos(sp, [42, 16, 20, 78])

# ════════════════════════════════════════════ COSTEO
co = wb.create_sheet('Costeo')
co['A1'] = 'Costeo de abajo hacia arriba'; co['A1'].font = TIT
co['A2'] = ('Cada línea es cantidad × precio unitario. Horas en azul = estimación del equipo, editable. '
            'Precios en verde = vienen de Supuestos.')
co['A2'].font = SUB
cab(co, 4, ['Bloque', 'Ítem', 'Cantidad', 'Unidad', 'Precio unitario (CLP)',
            'Total año 1 (CLP)', 'Total año 2 (CLP)', 'Tipo', 'Etapa', 'Base'])

SS = 'Supuestos!'
JR, SR_, SE = SS + '$B$6', SS + '$B$7', SS + '$B$8'
# (fila, bloque, ítem, cantidad, unidad, precio, año2, tipo, etapa, base, cant_es_formula)
C = [
    (5,  'B1',  'Depuración y carga del maestro de puntos Horeca', 80, 'horas', '=' + SR_, None, 'Inicial', 'Fase 0 · sem 1–6',
         'Completitud actual 26%: faltan ~850 fichas por completar', False),
    (6,  'B2',  'Diseño del modelo de datos y de las vistas', 60, 'horas', '=' + SE, None, 'Inicial', 'Fase 0',
         'Define qué se ve por punto, por canal y por alerta', False),
    (7,  'B2',  'Construcción del tablero centralizado', 100, 'horas', '=' + SR_, None, 'Inicial', 'Fase 0 → Corto',
         'Consola interna: dato consolidado, reglas y vista por punto', False),
    (8,  'B2',  'Licencia de visualización', 12, 'meses', '=' + SS + '$B$16', '=12*E8', 'Recurrente', 'Continuo',
         'Looker Studio sin costo; si se elige Power BI, cambiar en Supuestos', False),
    (9,  'LE1', 'Diseño del flujo conversacional de pedido', 60, 'horas', '=' + SR_, None, 'Inicial', 'Corto · mes 2',
         'El cliente pide igual que hoy; el pedido queda como objeto con estado', False),
    (10, 'LE1', 'Integración WhatsApp ↔ CRM', 120, 'horas', '=' + SR_, None, 'Inicial', 'Corto · mes 2–3',
         'Cada conversación de pedido crea un registro vinculado al punto', False),
    (11, 'LE1', 'Integración CRM ↔ ERP (estado de pedido)', 160, 'horas', '=' + SE, None, 'Inicial', 'Corto · mes 2–4',
         'La pieza más compleja: el ERP no identifica el punto físico', False),
    (12, 'LE1', 'Pruebas y ajuste en el piloto de 36 puntos', 80, 'horas', '=' + SR_, None, 'Inicial', 'Corto · mes 4',
         '20 Horeca · 10 panaderías independientes · 6 OCS directos', False),
    (13, 'LE1', 'Plataforma BSP de WhatsApp', 12, 'meses', '=' + SS + '$B$11', '=12*E13', 'Recurrente', 'Continuo',
         'Proveedor autorizado de la API de WhatsApp Business', False),
    (14, 'LE1', 'Mensajes de utilidad fuera de la ventana de 24 h',
         '=' + SS + '$B$22*' + SS + '$B$23*' + SS + '$B$24', 'mensajes', '=' + SS + '$B$12', '=C14*E14',
         'Recurrente', 'Continuo', 'Puntos del canal × pedidos × mensajes. Los de servicio no se cobran', True),
    (15, 'LE1', 'Licencias de CRM', '=' + SS + '$B$15*12', 'usuario-mes', '=' + SS + '$B$14*' + SS + '$B$18', '=C15*E15',
         'Recurrente', 'Continuo', 'Si el CRM actual de Marley lo soporta, esta línea desaparece', True),
    (16, 'LE1', 'Mantención de las integraciones', 9, 'meses', '=(F10+F11)*' + SS + '$B$9/12', '=12*E16',
         'Recurrente', 'Desde mes 4', 'Sobre el costo de las dos integraciones. Año 1: 9 meses', False),
    (17, 'LE2', 'Diseño de la regla acumulativa (Punto de Ebullición)', 40, 'horas', '=' + SE, None, 'Inicial', 'Mediano · mes 5',
         'Qué eventos suman, cuánto pesa cada uno y dónde está el umbral', False),
    (18, 'LE2', 'Implementación de reglas y alertas en el tablero', 80, 'horas', '=' + SR_, None, 'Inicial', 'Mediano · mes 5–6',
         'Opera sobre B2: sin tablero, la regla no tiene dónde verse', False),
    (19, 'LE2', 'Calibración del umbral con el historial del piloto', 40, 'horas', '=' + SE, None, 'Inicial', 'Mediano · mes 7–8',
         'Requiere al menos cuatro meses de pedidos registrados', False),
    (20, 'LE4', 'Diseño de la plantilla homologada de terceros', 24, 'horas', '=' + SR_, None, 'Inicial', 'Fase 0 · sem 2–6',
         'Formato mínimo: id de punto, RUT, fecha, producto, cantidad', False),
    (21, 'LE4', 'Consolidación mensual de envíos de terceros', '=12*8', 'horas', '=' + JR, '=C21*E21', 'Recurrente', 'Continuo',
         '8 horas al mes para 840 puntos operados por terceros', True),
    (22, 'MED', 'Diseño del piloto y del grupo de comparación', 40, 'horas', '=' + SE, None, 'Inicial', 'Fase 0',
         'Línea base y criterios de escalar, corregir o detener', False),
]
for fila, bl, it, cant, uni, pre, a2, tipo, et, base, cant_f in C:
    co.cell(fila, 1, bl).font = BOLD
    co.cell(fila, 2, it).font = NEGRO
    c = co.cell(fila, 3, cant); c.font = NEGRO if cant_f else AZUL; c.number_format = '#,##0'
    co.cell(fila, 4, uni).font = NOTA
    p = co.cell(fila, 5, pre); p.number_format = CLP
    p.font = NEGRO if pre.startswith('=(F') else VERDE
    t = co.cell(fila, 6, f'=C{fila}*E{fila}'); t.font = NEGRO; t.number_format = CLP
    g = co.cell(fila, 7, a2 if a2 else 0); g.font = NEGRO if a2 else AZUL; g.number_format = CLP
    co.cell(fila, 8, tipo).font = NEGRO
    co.cell(fila, 9, et).font = NOTA
    b = co.cell(fila, 10, base); b.font = NOTA; b.alignment = WRAP
    for col in range(1, 11): co.cell(fila, col).border = BORDE

# subtotal · contingencia · total
co.cell(24, 1, 'SUBTOTAL').font = BOLD
co['F24'] = '=SUM(F5:F22)'; co['G24'] = '=SUM(G5:G22)'
co.cell(25, 1, 'CONTINGENCIA').font = BOLD
co['E25'] = '=' + SS + '$B$31'; co['E25'].number_format = PCT; co['E25'].font = VERDE
co['F25'] = '=F24*E25'; co['G25'] = '=G24*E25'
co.cell(26, 1, 'TOTAL').font = Font(name=F, size=11, bold=True)
co['F26'] = '=F24+F25'; co['G26'] = '=G24+G25'
for r in (24, 25, 26):
    for col in ('F', 'G'):
        co[f'{col}{r}'].number_format = CLP
        co[f'{col}{r}'].font = Font(name=F, size=10 if r < 26 else 11, bold=True)
    for col in range(1, 11): co.cell(r, col).fill = F_TOT

# recursos internos y lo no costeado
seccion(co, 28, 'RECURSOS INTERNOS · no se imputan al presupuesto  [C] §3.6 del caso', 10)
for i, (rol, ded) in enumerate([('Sponsor ejecutivo', '10% de dedicación'),
                                 ('Líder de proyecto de marketing', '50% de dedicación'),
                                 ('Responsable comercial B2B', '100% de dedicación'),
                                 ('Analista de datos', '50% de dedicación')], 29):
    co.cell(i, 2, rol).font = NEGRO; co.cell(i, 3, ded).font = NOTA

seccion(co, 34, 'NO COSTEADO · se declara, no se estima', 10)
for i, (it, por) in enumerate([
        ('Gestión del cambio y capacitación', 'El caso exige financiarla. No hay tarifa de referencia verificada.'),
        ('Investigación primaria con decisores', 'Se asume ejecutada por el equipo interno.'),
        ('Asesoría legal: cláusula de datos con terceros', 'Ley 21.719. Sin tarifa de referencia verificada.'),
        ('Diferencial agencia vs. freelance', 'Este costeo usa tarifa freelance: es un piso, no un techo.')], 35):
    co.cell(i, 2, it).font = NEGRO
    n = co.cell(i, 3, por); n.font = NOTA
anchos(co, [8, 46, 11, 12, 16, 17, 17, 12, 17, 52])
co.freeze_panes = 'C5'

# ════════════════════════════════════════════ RESUMEN
rs = wb.create_sheet('Resumen')
rs['A1'] = 'Resumen del costeo'; rs['A1'].font = TIT
rs['A2'] = 'Inversión inicial y costo recurrente por bloque. Todo se calcula desde Costeo.'; rs['A2'].font = SUB
cab(rs, 4, ['Bloque', 'Qué es', 'Inversión inicial', 'Recurrente año 1', 'Total año 1',
            'Recurrente año 2', '% del año 1'])
BLOQ = [('B1', 'Identidad de punto'), ('B2', 'Tablero centralizado'), ('LE1', 'Instrumentar la reposición'),
        ('LE2', 'Anticipar por acumulación'), ('LE4', 'Dato con terceros'), ('MED', 'Medición del piloto')]
R = "Costeo!$A$5:$A$22"; T = "Costeo!$H$5:$H$22"
for i, (cod, nom) in enumerate(BLOQ, 5):
    rs.cell(i, 1, cod).font = BOLD; rs.cell(i, 2, nom).font = NEGRO
    rs.cell(i, 3, f'=SUMIFS(Costeo!$F$5:$F$22,{R},A{i},{T},"Inicial")')
    rs.cell(i, 4, f'=SUMIFS(Costeo!$F$5:$F$22,{R},A{i},{T},"Recurrente")')
    rs.cell(i, 5, f'=C{i}+D{i}')
    rs.cell(i, 6, f'=SUMIFS(Costeo!$G$5:$G$22,{R},A{i})')
    rs.cell(i, 7, f'=IFERROR(E{i}/$E$13,0)')
    for col in range(3, 7): rs.cell(i, col).number_format = CLP; rs.cell(i, col).font = VERDE if col != 5 else NEGRO
    rs.cell(i, 7).number_format = PCT
    for col in range(1, 8): rs.cell(i, col).border = BORDE

rs.cell(11, 1, 'SUBTOTAL').font = BOLD
rs.cell(12, 1, 'CONTINGENCIA').font = BOLD
rs.cell(13, 1, 'TOTAL').font = Font(name=F, size=11, bold=True)
for col in 'CDEF':
    rs[f'{col}11'] = f'=SUM({col}5:{col}10)'
    rs[f'{col}12'] = f'={col}11*Supuestos!$B$31'
    rs[f'{col}13'] = f'={col}11+{col}12'
rs['G11'] = '=IFERROR(E11/$E$13,0)'; rs['G12'] = '=IFERROR(E12/$E$13,0)'; rs['G13'] = '=IFERROR(E13/$E$13,0)'
for r in (11, 12, 13):
    for col in range(3, 8):
        c = rs.cell(r, col); c.font = Font(name=F, size=10 if r < 13 else 11, bold=True)
        c.number_format = PCT if col == 7 else CLP
    for col in range(1, 8): rs.cell(r, col).fill = F_TOT

seccion(rs, 15, 'CONTRA EL PRESUPUESTO', 7)
CMP = [
    (16, 'Costeo de abajo hacia arriba · año 1', '=E13', CLP),
    (17, 'Presupuesto comprometido en el informe', '=Supuestos!$B$33', CLP),
    (18, 'Holgura del comprometido sobre el costeo', '=E17-E16', CLP),
    (19, 'El comprometido equivale a', '=IFERROR(E17/E16,0)', X),
    (20, 'Costeo como % del presupuesto del caso', '=IFERROR(E16/Supuestos!$B$32,0)', PCT),
    (21, 'Comprometido como % del presupuesto del caso', '=IFERROR(E17/Supuestos!$B$32,0)', PCT),
]
for r, lab, f, fmt in CMP:
    rs.cell(r, 2, lab).font = NEGRO
    c = rs.cell(r, 5, f); c.number_format = fmt
    c.font = VERDE if 'Supuestos' in f and 'IFERROR' not in f else Font(name=F, size=10, bold=(r in (18, 19)))
rs.cell(22, 2, ('La holgura cubre lo que no se pudo costear con fuente: gestión del cambio, capacitación, asesoría '
                'legal y el diferencial de tarifa entre agencia y freelance.')).font = NOTA
anchos(rs, [9, 42, 18, 18, 18, 18, 12])

# ════════════════════════════════════════════ EQUILIBRIO
eq = wb.create_sheet('Equilibrio')
eq['A1'] = 'Punto de equilibrio'; eq['A1'].font = TIT
eq['A2'] = ('Cuánto margen tiene que dejar al mes cada punto Horeca que se deja de perder, para que el plan se pague. '
            'No requiere conocer las ventas de Marley.')
eq['A2'].font = SUB

seccion(eq, 4, 'PUNTOS RECUPERADOS', 3)
P = [
    (5,  'Puntos Horeca activos', '=Supuestos!B20', '#,##0'),
    (6,  'Retención actual', '=Supuestos!B26', PCT),
    (7,  'Retención meta', '=Supuestos!B27', PCT),
    (8,  'Puntos recuperados por año', '=Supuestos!B28', '#,##0'),
    (9,  'Factor de gradualidad del año 1', '=Supuestos!B29', '0.00'),
    (10, 'Puntos-año recuperados · año 1', '=B8*B9', '#,##0.0'),
    (11, 'Puntos-año recuperados · año 2', '=B8+B8*B9', '#,##0.0'),
    (12, 'Puntos-año recuperados · 24 meses', '=B10+B11', '#,##0.0'),
]
for r, lab, f, fmt in P:
    eq.cell(r, 1, lab).font = NEGRO
    c = eq.cell(r, 2, f); c.number_format = fmt
    c.font = VERDE if 'Supuestos' in f else NEGRO
eq.cell(13, 1, ('Año 2 suma los puntos salvados en el año 1, que siguen comprando, más medio año de los '
                'que se salvan en el año 2.')).font = NOTA

seccion(eq, 15, 'COSTO DEL PLAN', 3)
cab(eq, 16, ['', 'Costeo (piso)', 'Comprometido (informe)'])
eq['A17'] = 'Costo a 12 meses'; eq['B17'] = '=Resumen!E13'; eq['C17'] = '=Supuestos!B33'
eq['A18'] = 'Costo a 24 meses'; eq['B18'] = '=Resumen!E13+Resumen!F13'; eq['C18'] = '=Supuestos!B33+Resumen!F13'
for r in (17, 18):
    eq.cell(r, 1).font = NEGRO
    for col in (2, 3):
        c = eq.cell(r, col); c.number_format = CLP; c.font = VERDE if r == 17 else NEGRO

seccion(eq, 20, 'MARGEN MÍNIMO MENSUAL POR PUNTO RECUPERADO', 3)
cab(eq, 21, ['Escenario', 'Costeo (piso)', 'Comprometido (informe)'])
ESC = [
    (22, 'A 12 meses · la mejora opera de forma gradual', '=IFERROR(B17/($B$10*12),0)', '=IFERROR(C17/($B$10*12),0)'),
    (23, 'A 12 meses · la mejora opera desde el día uno', '=IFERROR(B17/($B$8*12),0)', '=IFERROR(C17/($B$8*12),0)'),
    (24, 'A 24 meses · la mejora opera de forma gradual', '=IFERROR(B18/($B$12*12),0)', '=IFERROR(C18/($B$12*12),0)'),
]
for r, lab, fb, fc in ESC:
    eq.cell(r, 1, lab).font = NEGRO
    for col, f in ((2, fb), (3, fc)):
        c = eq.cell(r, col, f); c.number_format = CLP; c.font = Font(name=F, size=10, bold=(r == 24))
for col in range(1, 4): eq.cell(24, col).fill = F_TOT
eq.cell(25, 1, ('Lectura: para que el plan se pague, cada punto Horeca que se deja de perder debe dejar al menos ese '
                'margen de contribución al mes. La fila de 24 meses es la que corresponde a una inversión en capacidad, '
                'porque el costo inicial se paga una sola vez.')).font = NOTA

seccion(eq, 27, 'LA PREGUNTA PARA MARLEY', 3)
eq['A28'] = 'Margen de contribución mensual promedio de un punto Horeca'
eq['A28'].font = BOLD
eq['B28'].fill = F_AMA; eq['B28'].font = AZUL; eq['B28'].number_format = CLP
eq['C28'] = '← completar con el dato del ERP'; eq['C28'].font = NOTA
eq['A29'] = 'Con el presupuesto comprometido, a 24 meses el plan…'; eq['A29'].font = NEGRO
eq['B29'] = '=IF(B28="","completar B28",IF(B28>=C24,"se paga","no se paga en este horizonte"))'
eq['B29'].font = Font(name=F, size=11, bold=True)
eq['A30'] = 'Con el presupuesto comprometido, a 12 meses el plan…'; eq['A30'].font = NEGRO
eq['B30'] = '=IF(B28="","completar B28",IF(B28>=C22,"se paga","no se paga en este horizonte"))'
eq['B30'].font = Font(name=F, size=11, bold=True)
eq.cell(31, 1, ('El dato vive en el ERP de Marley y el caso no lo entrega. Convertir la incógnita en una sola pregunta '
                'es el aporte de esta hoja: responde en minutos si el plan se justifica.')).font = NOTA
anchos(eq, [58, 22, 24])

for hoja in wb.worksheets:
    hoja.sheet_view.showGridLines = False

wb.save(OUT)
print('OK ->', OUT)
