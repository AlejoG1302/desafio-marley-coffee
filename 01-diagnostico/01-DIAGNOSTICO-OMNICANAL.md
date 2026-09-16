# Diagnóstico omnicanal — Desafío Marley Coffee

Entregable 1 de 13 · Taller Aplicado de Marketing III · Duoc UC 2026
Base: documento de bajada, PPT kickoff, rúbrica de comisión y video de bajada.

---

## 0. Régimen de datos — cómo leer este documento

La comisión exige distinguir dato público, supuesto del caso y hallazgo propio (criterio #1),
y el diseñador del desafío agregó una regla dura: *se pueden hacer supuestos, siempre que no
contradigan los números concretos del diseño*. Cada afirmación de este diagnóstico va marcada:

| Marca | Significado |
|---|---|
| **[P]** | Dato público verificable (FNE ago-2025, prensa especializada, GPS Property) |
| **[C]** | Supuesto académico del caso — entregado en el brief, se toma como dado |
| **[D]** | Derivado — cálculo propio del equipo sobre datos [P] o [C]. Fórmula explícita |
| **[H]** | Hipótesis del equipo — **no confirmada**, requiere levantamiento primario |

Nada marcado **[C]** se contradice en este documento. Donde el equipo cuestiona una cifra del
caso (§9.2), lo hace con aritmética explícita y sin reemplazar el dato original.

---

## 1. Qué se está diagnosticando

El objeto del diagnóstico **no es el café ni la marca**: es la **red física de 3.390 puntos y
4.000 máquinas** que Marley Coffee opera en Chile [C], y la experiencia que esa red entrega a dos
clientes distintos que hoy se tratan como uno solo.

### 1.1. El modelo de dos capas

Un error frecuente en este tipo de desafío es hablar de "el cliente" sin decir cuál. En food
service hay **dos** y sus journeys no coinciden:

| | **Capa 1 — Cliente B2B (contractual)** | **Capa 2 — Consumidor final (la taza)** |
|---|---|---|
| **Horeca** | Dueño/administrador de cafetería o restaurante | Comensal del local |
| **OCS** | Facilities, RRHH o adquisiciones — o **XYZ SPA intermediando** | Colaborador de la oficina o faena |
| **Estaciones de servicio** | Gerente de categoría del operador (Arcoprime, Enex, FEMSA) o el franquiciado | Conductor en tránsito |
| **Panaderías** | Dueño independiente o jefe de compras de cadena | Comprador de barrio, frecuencia diaria |

**Quién paga** está en la capa 1. **Quién juzga la marca** está en la capa 2. Marley factura a la
capa 1 y **no tiene relación directa con ninguna de las dos en tres de los cuatro canales** —
porque el punto es operado por un tercero.

Esta asimetría es la que genera el problema central: *la experiencia que decide la renovación del
contrato no es la que Marley puede observar*.

### 1.2. Grado de control real por canal [D]

Criterio del brief §3.4: "quién controla la experiencia y qué implica eso para la capacidad real
de intervenir".

| Canal | Controla el punto | Controla el precio al consumidor | Entrega dato de venta | **Margen de intervención de Marley** |
|---|---|---|---|---|
| **Horeca** | Cliente B2B directo | Cliente | Pedidos (ERP) | **Alto** — relación directa, sin intermediario |
| **OCS directo** (950 pts) | Empresa cliente | N/A (consumo interno) | Pedidos + tickets | **Alto** |
| **OCS vía XYZ SPA** (310 pts) | Partner | N/A | Reporte mensual agregado | **Bajo** — el partner es el muro |
| **Panaderías cadena** (350 pts) | Cadena | Cadena | Info agregada | **Medio** |
| **Panaderías independientes** (270 pts) | Dueño | Dueño | Solo pedidos y facturación | **Medio-bajo** |
| **EESS** (360 pts) | Operador tercero | **Operador** | Solo 55% de los puntos | **Bajo** — todo requiere autorización |

*Derivación: composición de puntos de §2 del brief [C]. Los porcentajes de dato provienen de las
líneas base declaradas por canal [C].*

**Lectura:** Marley tiene control alto sobre **2.100 puntos (62%)** y control bajo o nulo sobre
**1.290 puntos (38%)** [D]. Cualquier iniciativa que asuma control uniforme sobre los 3.390
puntos es inviable por diseño, no por presupuesto.

---

## 2. Journey del cliente B2B — estructura común y momentos de verdad

Las siete etapas se repiten en los cuatro canales; lo que cambia es quién las ejecuta y cuánta
evidencia deja.

```
DESCUBRIMIENTO → EVALUACIÓN → ALTA Y ONBOARDING → USO RECURRENTE → INCIDENTE → RENOVACIÓN → RECOMENDACIÓN
                                   ▲                    ▲              ▲
                              MOMENTO DE          MOMENTO DE      MOMENTO DE
                               VERDAD 1            VERDAD 2        VERDAD 3
                          Instalación y        Primera            Primera falla
                          capacitación         reposición         de máquina
```

### Los tres momentos de verdad

**MV1 — Instalación y primera capacitación.** Define si el producto se prepara bien durante toda
la vida del contrato. La capacitación aparece declarada como fricción principal en Horeca [C] y su
consecuencia se ve en panaderías: **76% de cumplimiento de estándares de limpieza y preparación**
en visitas de control [C] — **1 de cada 4 visitas de control encuentra el punto fuera de estandar** [D]. *(El caso mide cumplimiento por visita, no por punto: no equivale a que un cuarto de los puntos falle siempre.)*

**MV2 — Primera reposición.** Define si el cliente confía en el abastecimiento. Es el momento donde
Marley es peor: 82% de las reposiciones Horeca se gestionan por ejecutivo, correo o mensajería [C],
sin visibilidad de estado del pedido — declarada como fricción principal del canal [C].

**MV3 — Primera falla de máquina.** Es el momento de verdad más destructivo y el peor cubierto:
respuesta técnica promedio de **31 horas** en OCS [C] —más de una jornada laboral completa con la
máquina caída frente a los colaboradores— y un sistema de tickets que identifica la máquina solo en
75% de los casos y **no está integrado con CRM ni con ventas** [C].

### 2.1. Las etapas sin dueño

| Etapa | Quién la ejecuta hoy | Evidencia que deja |
|---|---|---|
| Descubrimiento | Prospección del ejecutivo + formulario web pasivo [C] | Ninguna trazable |
| Evaluación | Ejecutivo comercial | CRM (65% de cobertura) [C] |
| Alta y onboarding | Instalador + ejecutivo | ERP; sin registro de capacitación |
| Uso recurrente | **Ejecutivo tomando el pedido** [C] | ERP (transacción, no experiencia) |
| Incidente | Servicio técnico | Ticket (75% identifica máquina) [C] |
| Renovación | Ejecutivo | ERP |
| Recomendación | **Nadie** | **Ninguna — no existe programa de referidos** [C] |

**Hallazgo:** dos de las siete etapas —descubrimiento y recomendación, las dos que generan
crecimiento— **no tienen dueño ni instrumentación**. El sistema está construido para atender
clientes que ya existen, no para conseguir nuevos.

---

## 3. Diagnóstico canal por canal

### 3.1. HORECA — el motor caro

**Línea base [C]:** 1.150 puntos · 1.320 máquinas · 36% de las ventas · NPS **46** · CSAT 4,2/5 ·
retención 86% · 2,8 reclamos por 100 pedidos · OTIF 92% · 68% RM.

| Fricción | Evidencia | Severidad |
|---|---|---|
| Reposición manual | 82% por ejecutivo/correo/mensajería [C] | **Crítica** |
| Sin visibilidad del pedido | 1ª de las tres fricciones declaradas del canal [C] | **Crítica** |
| Fallas de máquina | 2ª de las tres declaradas [C] | Alta |
| Capacitación del personal | 3ª de las tres declaradas [C] | Alta |
| Asimetría de servicio regional | 48h RM vs. 72–96h regiones [C]; **32% de los puntos está fuera de RM** [D] | Media |
| Captación pasiva | Solo formulario web manual [C] | Alta |

*El caso declara las tres fricciones de Horeca pero **no las jerarquiza**: el orden es el de mención en el documento, y la columna Severidad es evaluación propia del equipo [D].*

**Dimensionamiento del costo oculto [D]:** asumiendo una reposición mensual por punto activo
—supuesto propio, a validar [H]— el canal genera ~1.150 pedidos/mes, de los cuales **~943 se
tramitan a mano** (82%). A 2,8 reclamos por 100 pedidos, son **~32 reclamos mensuales** solo en
Horeca. Cada uno de esos 943 pedidos consume tiempo de un ejecutivo comercial que **no está
vendiendo**.

**Diagnóstico:** es el canal **más sano en percepción (NPS 46, el mejor de los cuatro) y el más
caro de operar por transacción**. El problema de Horeca no es la satisfacción: es que su modelo de
servicio no escala. Crecer 8% en puntos activos [C] con este proceso significa contratar
proporcionalmente más ejecutivos para tomar pedidos.

> **La oportunidad de Horeca no es mejorar la experiencia, es liberar capacidad comercial.**

---

### 3.2. OCS — la retención frágil

**Línea base [C]:** 1.260 puntos · 1.550 máquinas · 12% de las ventas · NPS **38** ·
retención **90%** · disponibilidad de máquinas 94% · quiebres de stock en **6,8% de los puntos/mes**
· respuesta técnica **31 h** · 62% RM.
**Posición competitiva [P]:** 2º lugar con 10–20%, contra Nestlé (Nescafé/Nespresso) con 60–70%.

| Fricción | Evidencia | Severidad |
|---|---|---|
| Quiebre de stock | 6,8% de los puntos/mes = **~86 puntos con quiebre cada mes**, ~1.030 eventos-punto/año [D] | **Crítica** |
| Respuesta técnica lenta | 31 h promedio [C] — más de una jornada con la máquina caída | **Crítica** |
| Ceguera sobre 310 puntos | XYZ SPA reporta mensual agregado, sin identificación del consumidor final ni acceso en tiempo real [C] = **25% del canal es una caja negra** [D] | **Crítica** |
| Sin voz del consumidor | No hay medición del colaborador que usa la máquina [C] | Alta |

**El hallazgo central del canal [D+H]:** OCS tiene **la retención más alta de los cuatro canales
(90%) y el segundo NPS más bajo (38)**. Esa combinación no es virtuosa, es sospechosa: sugiere
**retención contractual o por inercia, no por satisfacción** [H]. Un cliente que se queda sin
recomendar es un cliente que se irá en cuanto un competidor con más músculo —Nestlé, 60–70% del
canal [P]— le toque la puerta con una oferta de servicio.

> **La retención de 90% en OCS no es un activo, es un riesgo con fecha de vencimiento.**

Esta es la hipótesis más importante del diagnóstico y es verificable: cruzar fecha de renovación
contra NPS, y preguntar intención de recompra en ausencia de contrato (H1, §10).

---

### 3.3. ESTACIONES DE SERVICIO Y CONVENIENCIA — máxima exposición, mínimo control

**Línea base [C]:** 360 puntos · 430 máquinas · 9% de las ventas · NPS **34 (el más bajo)** ·
disponibilidad de producto **91% (la más baja)** · datos de venta semanal solo en **55%** de los puntos.
Composición: 95 puntos piloto nacional + 85 en dos operadores regionales + 180 independientes [C].
**Contexto [P]:** 1.710 tiendas de conveniencia en Chile (+25% en dos años), 78,3% dentro de una
estación de servicio. Arcoprime/Copec 30,6% · FEMSA/Oxxo 16,8% · Enex/Shell 13,2%. Copec vende
**>22 millones de tazas al año** y recibe ~1 millón de personas diarias. Marley: **0–5%** en el
submercado. En agosto 2025 la FNE aprueba la compra del 70% de Juan Valdez Chile por Copec.

| Fricción | Evidencia | Severidad |
|---|---|---|
| Producto agotado | Disponibilidad 91%, la peor del sistema [C] | **Crítica** |
| Ceguera comercial | 45% de los puntos = **162 puntos sin dato de venta** [D] | **Crítica** |
| Sin control de precio ni promoción | Dependen del operador [C] | Alta (estructural) |
| Tres modelos de relación distintos | Piloto nacional / regionales / independientes, con tres niveles de dato [C] | Alta |
| Toda intervención requiere autorización | Señalética, QR, activaciones [C] | Alta (estructural) |

**El desbalance que define el canal [D]:** EESS representa **9% de las ventas** pero, por el tráfico
del formato, concentra probablemente la **mayor exposición diaria de marca de toda la red** [H]. Una
máquina sucia o sin producto en una estación de servicio no daña un 9% del negocio: daña la
percepción de marca ante un público que después decide en la oficina, en la panadería y en el
supermercado.

El video lo confirma en palabras del diseñador: *"Marley Coffee tiene una deuda y lo declaran ellos
mismos... hoy no está haciendo foco y lo debe hacer, justamente por el volumen brutal que tienen"*.

> **EESS es el canal donde Marley arriesga más marca por peso de venta. Es el pasivo reputacional
> de la red.**

---

### 3.4. PANADERÍAS — la mejor frecuencia, la peor taza

**Línea base [C]:** 620 puntos · 700 máquinas · 6% de las ventas · NPS **39** · disponibilidad 93% ·
**cumplimiento de estándares de limpieza y preparación: 76%** en visitas de control.
Composición: 140 en una cadena regional + 210 en seis cadenas medianas + **270 independientes** [C].
**Contexto [P]:** Castaño lidera comida envasada para cafeterías y conveniencia con 30–40%.
No existe información pública de estrategia de Marley en este canal.

| Fricción | Evidencia | Severidad |
|---|---|---|
| Calidad de preparación fuera de estándar | **24% de incumplimiento** = ~149 puntos por debajo de norma [D] | **Crítica** |
| Cero visibilidad de experiencia | 270 independientes reportan solo pedidos y facturación [C] | **Crítica** |
| Sin estrategia declarada de canal | No hay información pública [P] | Alta |
| Capacitación no gobernada | "Capacitación básica" en el modelo comercial [C] | Alta |

**Por qué el 76% es la métrica más grave del diagnóstico [D]:** la panadería en Chile es un ritual
de **frecuencia diaria**. Un café mal preparado en un local que el consumidor visita todos los días
no es un mal momento aislado: es un mal momento **repetido 250 veces al año** sobre el mismo
consumidor. En términos de daño acumulado de marca, 24% de incumplimiento en panaderías pesa más
que 9% de indisponibilidad en estaciones de servicio.

Y la lectura del diseñador acota el objetivo: *"no significa salir a buscar Castaños, sino ver cómo
competimos en esa industria para ganar share, y que a su vez converse con los otros tres canales"*.

> **Panaderías es el canal con mejor economía de frecuencia y peor control de calidad. Es una
> palanca de marca desperdiciada.**

---

### 3.5. Cuadro comparativo — los cuatro canales en una vista

| | **Horeca** | **OCS** | **EESS** | **Panaderías** |
|---|---|---|---|---|
| % ventas [C] | 36% | 12% | 9% | 6% |
| Puntos [C] | 1.150 | 1.260 | 360 | 620 |
| NPS [C] | **46** ✅ | 38 | **34** ❌ | 39 |
| Retención [C] | 86% | **90%** | n/d | n/d |
| Disponibilidad [C] | OTIF 92% | 94% máq. · 6,8% quiebres | **91%** ❌ | 93% |
| Calidad de servicio [C] | 2,8 recl./100 ped. | 31 h respuesta | n/d | **76% estándar** ❌ |
| Cobertura de datos [D] | Pedidos, sin experiencia | 75% del canal | **55%** ❌ | Solo cadenas |
| Control de Marley [D] | **Alto** | Mixto (75/25) | **Bajo** | Medio-bajo |
| Posición competitiva [P] | Base del negocio | 2º (Nestlé 60–70%) | 0–5% | Menor (Castaño 30–40%) |
| **Patología dominante** | **No escala** | **Retención frágil** | **Riesgo de marca** | **Calidad no gobernada** |

---

## 4. Fricciones transversales — lo que se repite en 2 o más canales

El brief pregunta explícitamente cuáles fricciones son comunes a varios canales. Son seis, y están
ordenadas por causalidad: la primera causa a las demás.

**F1 · Ceguera de punto — la raíz de todo.**
El ERP no identifica de forma homogénea cada punto físico y **no existe un identificador único de
cliente ni de punto** [C]. Afecta a los 4 canales. Consecuencia: es imposible unir lo que se
factura, lo que se repara y lo que se percibe sobre un mismo local. *Todo el resto del diagnóstico
es sintomático de esto.*

**F2 · Reposición reactiva.**
El sistema espera a que el cliente pida o reclame. Horeca 82% manual, OCS 6,8% de quiebres,
disponibilidad 91–93% en EESS y panaderías [C]. Nadie sabe cuándo se va a acabar el café en un punto
antes de que se acabe.

**F3 · Calidad de preparación fuera de control.**
Capacitación declarada como fricción en Horeca; 76% de cumplimiento en panaderías [C]. En 3 de 4
canales la taza la prepara un tercero con rotación de personal alta [H]. El producto que Marley
controla (el grano) es excelente —lo prueba el liderazgo 50–60% en retail [P]—; el producto que el
consumidor recibe (la taza) no lo controla nadie.

**F4 · Servicio técnico desacoplado.**
Tickets identifican la máquina en 75% de los casos y no se integran con CRM ni ventas [C];
31 h de respuesta en OCS. El momento de verdad más destructivo es justo donde hay menos dato.

**F5 · Voz del cliente inexistente.**
Encuestas esporádicas, sin medición unificada de NPS, CSAT o CES entre canales [C]. Los NPS de
34–46 del caso son **estimaciones, no un sistema de medición**. Hoy Marley no puede saber si mejora.

**F6 · El tercero como muro.**
XYZ SPA en OCS, operadores en EESS, cadenas en panaderías: intermedian **la experiencia y el dato**
a la vez [C]. 38% de los puntos está detrás de este muro [D].

### 4.1. Cómo se encadenan

```
        F1 · CEGUERA DE PUNTO  (no hay ID único)
                    │
        ┌───────────┼───────────┬───────────┐
        ▼           ▼           ▼           ▼
   F2 Reposición  F4 Servicio  F3 Calidad  F6 Muro
     reactiva      desacoplado  sin gobierno  del tercero
        │           │           │           │
        └───────────┴─────┬─────┴───────────┘
                          ▼
                F5 · SIN VOZ DEL CLIENTE
                          ▼
        No se puede saber si algo de esto mejora
```

**Consecuencia metodológica y no negociable:** *no se puede medir una experiencia omnicanal sobre
una red cuyos puntos no tienen identidad*. Cualquier marco de medición que no empiece por resolver
F1 es voluntarista. Esto condiciona la hoja de ruta: el primer movimiento no es una campaña ni un
piloto de experiencia, es un **maestro único de puntos**.

---

## 5. Influencia cruzada (halo) — el sistema que hoy es invisible

El brief y el video insisten: **omnicanalidad, no multicanalidad** — el cliente al centro y los
canales alrededor. El diagnóstico identifica **tres flujos de influencia cruzada**, ninguno de los
cuales es observable hoy.

### Flujo A — Consumidor → B2B (demanda inducida)
El colaborador que toma Marley todos los días en su oficina (OCS) es también el dueño de una
cafetería, el comprador de la panadería de su barrio y el conductor que para en una estación de
servicio. La prueba de marca ocurre en un canal y la decisión de compra B2B ocurre en otro.
**Instrumentación actual: ninguna.** No hay QR, ni código, ni la pregunta "¿dónde probó Marley
Coffee por primera vez?" que el propio brief sugiere como indicador [C].

### Flujo B — B2B → B2B (referido entre pares)
Los decisores de un mismo canal se conocen: dueños de cafeterías entre sí, jefes de compras de
cadenas de panadería, gerentes de facilities en el circuito corporativo. **Instrumentación actual:
ninguna.** No existe programa de referidos B2B [C] y la captación es un formulario web pasivo.

### Flujo C — Contaminación negativa (el halo inverso)
Es el flujo que hoy opera **con más fuerza y sin control**: una máquina sucia en una estación de
servicio o una taza fuera de estándar en una panadería daña la percepción de marca ante el mismo
público que después decide una compra OCS o Horeca. El brief lo nombra explícitamente: *"una mala
experiencia en un canal puede dañar la percepción de marca en todos los demás puntos de contacto,
incluso si esos otros canales funcionan bien"* [C].

### 5.1. Matriz de influencia cruzada [D+H]

Rol propuesto de cada canal dentro del sistema, según su tráfico, frecuencia y control:

| Canal | Rol en el sistema | Frecuencia de contacto | Dirección dominante |
|---|---|---|---|
| **OCS** | **Puerta de entrada** — prueba diaria, cautiva, gratuita para el consumidor | Diaria, 5 días/semana | Alimenta a los otros 3 |
| **EESS** | **Alcance y recuerdo** — máximo tráfico, mínimo control | Esporádica, alto volumen | Alimenta y contamina |
| **Panaderías** | **Refuerzo de hábito** — ritual diario de barrio | Diaria | Refuerza o erosiona |
| **Horeca** | **Consumo aspiracional y recompra** — donde la marca se elige | Ocasional, alta intención | Recibe de los tres |

**Hipótesis estructural del sistema [H]:** *OCS es la principal puerta de entrada de prueba de marca
del consumidor chileno y Horeca es donde esa prueba se convierte en preferencia*. Si se confirma,
reordena la priorización: invertir en OCS no se justifica por su 12% de ventas sino por su rol de
**generador de demanda para el otro 51%**.

Es verificable con una sola pregunta en encuesta segmentada (H3, §10), y es exactamente la
"metodología para medir el efecto de un canal sobre otro" que el brief pide [C].

---

## 6. Diagnóstico de capacidades de datos — por qué hoy nada de esto se puede medir

**Estado declarado [C]:**

| Sistema | Cobertura | Brecha crítica |
|---|---|---|
| ERP | 95% de las transacciones | **No identifica homogéneamente el punto físico** |
| CRM comercial | 65% de las cuentas B2B activas · 40% de campos completos | Sin canal, ubicación, tamaño ni potencial en la mayoría |
| Servicio técnico | Identifica la máquina en 75% de los tickets | **No integrado con CRM ni con ventas** |
| Partners | XLS/CSV mensuales, detalle heterogéneo | Sin POS en tiempo real |
| Voz del cliente | Encuestas esporádicas | Sin NPS/CSAT/CES unificado |
| Integración | ~30% automática | 70% carga manual |
| **Identificador único** | **No existe** | **El journey omnicanal es inobservable** |

### 6.1. El número que resume la brecha [D]

Si el 40% de completitud se mide sobre el 65% de cuentas registradas:

```
0,65 × 0,40 = 0,26
```

> **Solo 1 de cada 4 cuentas B2B de Marley Coffee es plenamente analizable hoy.**
> *(Supuesto de la derivación: la completitud de 40% se mide sobre los registros existentes del CRM,
> no sobre el universo total. Si se midiera sobre el universo, la cifra sería aún peor.)*

Con 26% de cuentas analizables no se puede hacer segmentación por canal, ni análisis de cartera, ni
lead scoring, ni atribución cruzada, ni un modelo de churn. **Las cinco cosas que el desafío pide
construir dependen de un dato que hoy no existe.**

---

## 7. Análisis complementarios (rúbrica, criterio #11)

### 7.1. FODA

| **FORTALEZAS** | **DEBILIDADES** |
|---|---|
| Líder absoluto en café de grano envasado retail: 50–60% [P] | Sin identificador único de cliente ni punto [C] |
| Red instalada de 4.000 máquinas — activo difícil de replicar [C] | 82% de reposiciones Horeca manuales [C] |
| Marca con capital cultural genuino y no imitable (familia Marley, reggae, sustentabilidad) | Solo 26% de cuentas B2B analizables [D] |
| Crecimiento sostenido: +26,5% en 2024 [P] | NPS bajo y disperso (34–46), sin sistema de medición [C] |
| Retención B2B de 86–90% [C] | 24% de incumplimiento de estándar en panaderías [C] |
| Licencia exclusiva LatAm desde 2017 [P] | Sin e-commerce B2B ni inbound [C] |
| Relación directa con 62% de los puntos [D] | Dependencia de terceros en 38% de los puntos [D] |

| **OPORTUNIDADES** | **AMENAZAS** |
|---|---|
| Conveniencia creciendo +25% en dos años [P] | Copec + Juan Valdez integrados en Pronto, con máquinas propias y 22M tazas/año [P] |
| Digitalización B2B como terreno virgen de la categoría | Nestlé 60–70% en institucional, con capacidad de inversión superior [P] |
| Panaderías sin proveedor de café dominante [P] | Castaño 30–40% con máquinas propias en el canal panadería [P] |
| Nestlé domina OCS con un modelo de alto costo por taza — espacio para otra propuesta de valor [H] | Concentración del canal conveniencia en 5 operadores → alto poder de negociación del comprador [P] |
| Ley 21.719 obliga a formalizar consentimiento: convertible en activo de confianza B2B | Retención OCS de 90% con NPS 38: frágil ante una oferta de servicio superior [H] |
| Frecuencia diaria de panaderías = plataforma de hábito de bajo costo | Food service proyectado a bajar de 63% a ~50% en 3 años [C] |

### 7.2. PESTEL — solo los factores que mueven la aguja

*Verificado con research el 17-08-2026. Fuentes al pie de la sección.*

| | Factor | Implicancia directa en el desafío |
|---|---|---|
| **P** | La FNE está observando activamente el mercado del café (informe ago-2025) [P] | Cautela con acuerdos de exclusividad con operadores de EESS |
| **E** | **Ventana de alivio de costo** — el arábica cerró en **321,45 ¢/lb el 17-08-2026**, −3,9% en 30 días, tras el récord histórico de **437,95 ¢/lb a fines de 2025**. Brasil proyecta cosecha récord 2026/27 de **75,3–75,9 M de sacos (+15,5%)**, presionando a la baja [P] | **Cambia el argumento del business case — ver §7.2.1** |
| **S** | Consumo de café fuera del hogar en alza; panadería como ritual diario en Chile | Sostiene la tesis de frecuencia del canal panaderías |
| **T** | **Telemetría en máquinas de café es estándar internacional confirmado**: Costa Express opera ~13.500 máquinas en 17 mercados con monitoreo centralizado, diagnóstico remoto y configuración OTA [P]. La telemetria permite reposicion predictiva; los proveedores del sector declaran reducciones de downtime de hasta 30% (cifra de proveedor, sin verificacion independiente) | Habilita reposición predictiva sin renovar flota — la restricción dura del caso |
| **E** | Sustentabilidad en el ADN de la marca — *"lo cuidan mucho"* (video) | Palanca diferencial frente a Nespresso en residuos y trazabilidad |
| **L** | **Ley 21.719 — publicada el 13-12-2024, entra en vigencia el 1 de diciembre de 2026** [P] | **Es el factor más urgente del PESTEL — ver §7.2.2** |

#### 7.2.1. El precio del café cambia el argumento del business case [D]

La lectura intuitiva —"el café está caro, hay presión de margen"— **ya no es correcta a agosto 2026**.
El mercado viene **bajando** desde un récord histórico:

| Hito | Nivel |
|---|---|
| Récord histórico (fines 2025) | 437,95 ¢/lb |
| **Hoy (17-08-2026)** | **321,45 ¢/lb** (−3,9% en 30 días) |
| Rango 52 semanas | 244 – 432 ¢/lb |
| Driver | Cosecha récord de Brasil 2026/27: 75,3–75,9 M sacos, +15,5% |

**Tres consecuencias para la propuesta:**

1. **Hay una ventana de financiamiento.** La normalización del costo del grano libera margen que puede
   financiar parte de los $220M **sin tocar el precio al cliente B2B ni el P&L operativo**. Es un
   argumento de business case mucho más fuerte que "invertir y esperar retorno". *Cuantificar el
   tamaño de la ventana requiere el costo de venta real de Marley — brecha abierta (§12).*
2. **Hay un riesgo competitivo simétrico.** Si el costo baja para Marley, baja para **Nestlé**, que
   tiene 60–70% del canal institucional [P] y más músculo financiero. Un competidor con costo
   aliviado puede atacar OCS por precio justo donde Marley es 2º con retención frágil (§3.2).
   **La ventana de alivio no es una ventaja: es una carrera.**
3. **El anclaje de precio del cliente B2B quedó alto.** La base contractual absorbió alzas durante el
   shock 2024-2025. Sostener precio mientras el costo baja es posible, pero **solo si la experiencia
   lo justifica** — que es exactamente lo que este desafío construye.

> **Reencuadre:** la digitalización de la experiencia no es un gasto que compite con el margen. Es lo
> que permite **defender el precio** cuando el costo del insumo se normaliza y el competidor grande
> tiene más espacio para atacar.

#### 7.2.2. Ley 21.719 — el factor más urgente del PESTEL [P]

**No es un marco de referencia lejano: entra en vigencia el 1 de diciembre de 2026, dentro del
horizonte de 12 meses de esta hoja de ruta.** Los pilotos de 90 días cruzan esa fecha.

| Exigencia | Qué implica para este desafío |
|---|---|
| **Base de licitud obligatoria** — consentimiento explícito, necesidad contractual, obligación legal o interés legítimo bien definido | Ningún QR, formulario ni encuesta puede capturar dato "por si acaso". Cada mecanismo necesita finalidad declarada **antes** de diseñarse |
| **Derechos ARCO + portabilidad + bloqueo** (seis derechos exigibles) | El portal transaccional B2B y el CRM deben nacer con capacidad de exportar, rectificar y eliminar datos del titular |
| **Notificación obligatoria de brechas** a la nueva **Agencia de Protección de Datos Personales (APDP)** | Requisito de gobierno de datos, no solo técnico. Entra en el marco de gobernanza (entregable 8) |
| **Multas hasta 20.000 UTM**, o entre **2% y 4% de los ingresos anuales** para grandes empresas | Convierte el cumplimiento en tema de comité ejecutivo, no de área legal |
| **Delegado de Protección de Datos (DPO)** | Un rol nuevo que la propuesta de gobierno de datos debe nombrar |

**Cómo esto se convierte en ventaja competitiva, no solo en restricción:**

Marley debe construir su captura de datos **desde cero** (hoy no hay ID único, ni portal, ni programa
de captura). Un competidor con sistemas legacy tiene que **remediar**; Marley puede nacer conforme.
El **"compliance by design"** es defendible ante la comisión como decisión de diseño deliberada y es
un argumento de venta real frente a clientes corporativos de OCS —que en diciembre de 2026 estarán
exigiendo lo mismo a *sus* proveedores.

**Y es un riesgo de primer orden para el registro de riesgos (entregable 12):** un mecanismo de
captura físico-digital diseñado sin base de licitud es una iniciativa que **habrá que apagar** el
1 de diciembre de 2026, con el presupuesto ya gastado.

### 7.3. Cadena de valor — dónde se pierde el valor

| Eslabón | Estado | Diagnóstico |
|---|---|---|
| Logística de entrada · tostado · envasado | Sano | Lo prueba el liderazgo 50–60% en retail [P] |
| **Logística de salida** | **Deficiente** | OTIF 92%, 48–96 h, 6,8% de quiebres [C] |
| **Marketing y ventas** | **Deficiente** | Captación manual, CRM al 65%, sin inbound [C] |
| **Servicio postventa** | **El eslabón más débil** | 31 h de respuesta, tickets sin integrar, capacitación no gobernada [C] |
| Infraestructura (ERP) | Insuficiente | Sin ID de punto [C] |
| Desarrollo tecnológico | Insuficiente | 30% de integración automática [C] |

> **El valor no se pierde en el producto: se pierde en salida, servicio y datos.** Marley tiene un
> producto ganador con una operación de servicio que no escala. Esto explica la paradoja de fondo
> del caso: líder en el canal donde solo hay que poner el producto en la góndola (retail), actor
> menor en los canales donde hay que **servir**.

### 7.4. Benchmark y revisión de mercados extranjeros

*Verificado con research el 17-08-2026. Se marca explícitamente qué quedó confirmado y qué no.*

| Referente | Hallazgo verificado | Aplica a | Estado |
|---|---|---|---|
| **Costa Express** (Reino Unido, 17 mercados) | **~13.500 maquinas self-serve** en total, mayor proveedor de cafe a estaciones de servicio del Reino Unido *(una fuente cita ~11.000 efectivamente conectadas en red; la cifra de flota con telemetria varia segun fuente)*. Telemetría con **monitoreo centralizado, diagnóstico remoto y actualización de configuración OTA** sobre conectividad celular gestionada — sin depender de la red fija del punto | **EESS** | ✅ Confirmado |
| **Telemetría en OCS** (estándar de industria) | Los módulos registran tazas por día, tipo de bebida, temperatura, presión de bomba y tiempo de extracción. Habilita **reposición predictiva** y mantenimiento proactivo, con **reduccion de downtime de hasta 30% segun publicaciones del sector** (cifra declarada por proveedores, no verificada de forma independiente). Existen datasets de +75 M de bebidas sobre ~6.500 maquinas IoT B2B | **OCS, Horeca** | Capacidad confirmada; magnitud no |
| **Nespresso Pro / Nestlé Professional Chile** | Portal de pedidos online con corte horario declarado (15:00 días hábiles), centro de servicios profesional, comodato de máquinas y paquete de servicios técnicos y comerciales para foodservice. **Es el estándar competitivo local que Marley debe igualar** | **OCS** | ✅ Confirmado |
| **Nescafé Alegria** (Nestlé, global) | Solución diseñada explícitamente **para entornos sin operador capacitado**, donde el cliente se autoatiende. Tres niveles de máquina por volumen (30–50, 60–80, 120–140 tazas/día), pensadas para operar, limpiar y mantener sin barista | **Panaderías, EESS** | ✅ Confirmado |
| **3corações / TRES InCompany** (Brasil) | Modelo OCS LatAm de escala comparable: instalación **en comodato con asistencia técnica garantizada** y **pedido mínimo mensual** (300 cápsulas) como contrapartida — sin costo de mantención ni transporte para el cliente | **OCS** | ⚠️ Modelo comercial confirmado; **telemetría no verificada** |
| **Arcoprime / Copec** | Control total: dueño del punto, de la máquina y del dato. Marley **no puede igualarlo** en EESS → debe competir con otra lógica | EESS | ✅ Estructural (FNE) |
| ~~"Coffee corner" estandarizado (España)~~ | **Descartado.** El research devuelve una cadena de franquicias de cafetería de 100–120 m², no un kit de canal para panadería independiente. **La referencia no aplica** y se reemplaza por Nescafé Alegria | — | ❌ Descartado |

#### 7.4.1. Las dos lecciones de benchmark que reordenan el diagnóstico

**Lección 1 — La reposición predictiva no exige renovar la flota.**
Era la pregunta de benchmark que ordenaba todo, porque el presupuesto **no cubre renovación de
máquinas** [C]. Respuesta: los líderes resuelven con **módulos de telemetría y conectividad celular
gestionada**, no con máquinas nuevas. Costa Express lo hace sobre 13.500 equipos sin depender de la
red fija del local — exactamente la restricción de un punto operado por un tercero, donde Marley no
controla el WiFi. Esto convierte F2 (reposición reactiva) de "problema estructural" a
**problema con solución conocida y compatible con la restricción presupuestaria**.

**Lección 2 — Nestlé no resuelve la calidad de preparación capacitando: la resuelve diseñando.**
Nescafé Alegria está construido explícitamente *para entornos donde no hay un operador capacitado*.
Es la respuesta directa al hallazgo más grave del diagnóstico: el **76% de cumplimiento de estándar
en panaderías** (§3.4).

> **Implicancia contraintuitiva:** el líder del mercado comercializa una solución **diseñada para
> operar sin personal capacitado**. Eso es dato público. **Por qué llegó a ese diseño no lo sabemos**
> —no hay declaración de Nestlé al respecto y la inferencia es nuestra—, pero el producto existe y es
> su respuesta a ese escenario.
>
> Si la lectura es correcta, **la propuesta para panaderías no debería ser un programa de
> capacitación**: debe ser un rediseño del proceso que haga difícil preparar mal la taza. Contradice
> la solución obvia, y es el tipo de decisión no obvia que la rúbrica premia en creatividad aplicada
> (criterio #4) — pero se presenta como hipótesis de diseño, no como conclusión de benchmark.

---

### Fuentes del research (verificado 17-08-2026)

- Precio del café: [Barchart — Coffee C ICE](https://www.barchart.com/story/news/34701320/why-is-coffee-back-in-bullish-mode) · [Bloomberg Línea — de su mayor alza en 26 años a su mayor caída](https://www.bloomberglinea.com/mercados/de-su-mayor-alza-en-26-anos-a-su-mayor-caida-en-2026-que-pasa-con-el-precio-del-cafe/) · [Noticias Agropecuarias — cosecha récord de Brasil](https://www.noticiasagropecuarias.com/2026/06/07/la-cosecha-record-de-brasil-aumenta-la-presion-sobre-los-precios-del-cafe/)
- Ley 21.719: [Asentic — la ley explicada sin tecnicismos](https://www.asentic.cl/blog/ley-21719-datos-personales/) · [Araya & Cía.](https://www.araya.cl/2026/06/nueva-ley-de-proteccion-de-datos-personales-en-chile-que-es-por-que-es-clave-y-como-deben-prepararse-las-empresas/) · [Prey — guía 2026](https://preyproject.com/es/blog/ley-de-proteccion-de-datos-en-chile)
- Costa Express y telemetría: [Eseye — caso Costa Express](https://www.eseye.com/resources/case-studies/costa-express/) · [Device Insight](https://device-insight.com/en/coffee-goes-smart-with-device-insight/) · [Vendon — telemetría en estaciones de servicio](https://vendon.net/blog/how-telemetry-can-boost-your-petrol-station-coffee-sales/)
- Telemetría OCS: [CoffeeClick — connected machines 2026](https://coffeeclick.nl/en/connected-koffiemachine-telemetrie-2026/) · [Professional Coffee Machines — mantenimiento predictivo](https://www.professionalcoffeemachines.com/the-machine-speaks-connected-machines-remote-diagnostics-and-iot-the-future-of-predictive-maintenance/)
- Competencia local: [Nespresso Pro Chile](https://www.nespresso.com/pro/cl/es/order/machines/pro) · [Nestlé Professional LATAM Chile](https://www.nestleprofessional-latam.com/cl/bebidas/maquinas)
- Nescafé Alegria: [Foodservice REP — máquinas sin barista](https://www.foodservicerep.com.au/coffee-machines-deliver-on-quality-without-the-need-for-a-barista) · [Nestlé — Alegria](https://www.nestle.in/brands/vfs/beveragesystem/nescafealegria)
- 3corações: [TRES InCompany](https://www.escolhatres.com.br/incompany-home/) · [3corações PRO](https://www.3cpro.com.br/)
- Marley Coffee: [La Tercera — inversión US$7 M y expansión](https://www.latercera.com/pulso/noticia/marley-coffee-sigue-con-su-expansion-en-chile-y-latinoamerica-invertira-us7-millones-en-apertura-de-nuevos-locales-y-productos/RZHP5WRBCVBNJFBDAVN3LYRXJY/) · [La Tercera — duplicar cafeterías vía franquicias](https://www.latercera.com/pulso/noticia/marley-coffee-quiere-duplicar-sus-cafeterias-en-dos-anos-bajo-el-modelo-de-franquicias/)

---

## 8. Brechas priorizadas

Cruce de **severidad** (impacto en experiencia y negocio) contra **grado de control de Marley**
(§1.2). Determina qué se ataca directo y qué requiere negociación con un tercero.

```
   ALTA │  F3 Calidad de preparación      │  F1 ID único de punto        
SEVERI- │     (panaderías, EESS)          │  F2 Reposición reactiva      
  DAD   │  F6 Muro del tercero            │  F4 Servicio técnico         
        │  Datos POS de operadores        │  F5 Voz del cliente          
        │                                 │  Captación B2B pasiva        
        ├─────────────────────────────────┼──────────────────────────────
        │  Precio y promoción en EESS     │  Asimetría de servicio       
   BAJA │  (fuera de alcance por brief)   │  regional                    
        │                                 │                              
        └─────────────────────────────────┴──────────────────────────────
              BAJO CONTROL                      ALTO CONTROL
         (requiere negociación)            (ejecutable por Marley)
```

**Cuadrante superior derecho — se ataca primero, no requiere permiso de nadie:**
F1 (ID único de punto), F2 (reposición reactiva), F4 (servicio técnico), F5 (voz del cliente) y la
captación B2B. Cubre los dos canales con 48% de las ventas [D] y **62% de los puntos**.

**Cuadrante superior izquierdo — se negocia, no se asume:**
Calidad de preparación en panaderías y EESS, y acceso a datos POS. Requieren contrapartida de valor
para el tercero, no solo una solicitud. Aquí es donde una propuesta ingenua se cae en la comisión:
el brief es explícito en que **todo cambio en un punto operado por un partner requiere su
autorización** [C].

---

## 9. Cuestionamiento cuantitativo de la línea base

El brief autoriza a cuestionar las metas "siempre que presenten una justificación cuantitativa" [C],
y el video acota: los supuestos no pueden contradecir los números del diseño. Lo que sigue **no
cambia ninguna cifra**: reconstruye la aritmética que hay detrás de una de ellas.

### 9.1. Reconstrucción del NPS ponderado base [D]

El brief fija una base de **42** para el "NPS ponderado de los cuatro canales" sin explicitar el
criterio de ponderación. Probando las tres alternativas posibles:

| Criterio de ponderación | Resultado |
|---|---|
| Promedio simple | 39,3 |
| Por puntos activos | 40,5 |
| Por máquinas | 40,4 |
| **Por participación de ventas** | **42,1** ✅ |

*Cálculo: pesos relativos dentro del 63% de food service → Horeca 57,1%, OCS 19,0%, EESS 14,3%,
Panaderías 9,5%.*
`46(0,571) + 38(0,190) + 34(0,143) + 39(0,095) = 42,1`

**Inferencia del equipo: la ponderacion por participacion de ventas es la unica de las cuatro que reproduce el 42 declarado.** El documento del desafio no explicita el criterio, de modo que es una reconstruccion propia y **debe confirmarse con el docente o el tutor** antes de apoyarse en ella. Es coherente con el dato
del caso y permite proyectar la meta con precisión en vez de a ojo.

### 9.2. La consecuencia estratégica que esto revela

Si la ponderación es por ventas, **Horeca concentra el 57% del peso de la métrica**. Entonces:

| Escenario de mejora | Efecto en el NPS ponderado |
|---|---|
| EESS de 34 → 52 (+18 puntos, el canal más deficitario) | **+2,6** → llega a 44,7. **Insuficiente** |
| Los cuatro canales +10 puntos | +10,0 → llega a 52,1 ✅ pero exige mover todo a la vez |
| **Horeca 46 → 60 y OCS 38 → 48** | **+9,9 → llega a 52,0** ✅ con solo dos canales |

> **Hallazgo:** la meta de 42 → 52 es, aritméticamente, **una meta de Horeca y OCS** (76% del peso
> combinado), no una meta de los cuatro canales por igual.

**Y aquí aparece la tensión de fondo del desafío**, que el equipo debe resolver explícitamente:

- La **métrica de NPS** premia invertir en Horeca y OCS.
- La **lectura competitiva** (Copec+Juan Valdez avanzando, Castaño consolidado, *"tenemos una
  deuda"* según la propia empresa) exige invertir en EESS y panaderías.
- La **exposición de marca** está donde la métrica pesa menos.

Un diagnóstico que no nombre esta contradicción está incompleto. La propuesta de medición tendrá
que **decidir** si mantiene la ponderación por ventas —y asume que EESS quedará subrepresentado— o
propone una ponderación alternativa por exposición de marca, con justificación.

---

## 10. Hipótesis a verificar y diseño de levantamiento

Cada hipótesis nace de una tensión del diagnóstico y tiene un método de verificación acotado a los
recursos del caso.

| # | Hipótesis | Origen | Cómo se verifica |
|---|---|---|---|
| **H1** | La retención de 90% en OCS es contractual, no por satisfacción | §3.2 · retención alta + NPS 38 | Cruzar fecha de renovación vs. NPS · preguntar intención de recompra sin contrato de por medio · entrevistas a facilities |
| **H2** | Entre las tres fricciones declaradas de Horeca, la que más pesa en la no-recompra es la incertidumbre de la entrega, no el precio | §3.1 · el caso declara las tres pero no las rankea | **CES** medido en el momento de la reposición · entrevistas a dueños de cafeterías |
| **H3** | OCS es la principal puerta de entrada de prueba de marca del consumidor chileno | §5.1 · matriz de influencia cruzada | Pregunta *"¿dónde probó Marley Coffee por primera vez?"* en encuesta segmentada por canal |
| **H4** | El 24% de incumplimiento en panaderías correlaciona con rotación de personal del punto, no con desinterés del dueño | §3.4 · 76% de cumplimiento | Registrar antigüedad del personal en las visitas de control · mystery shopping |
| **H5** | Los puntos EESS sin dato POS tienen peor disponibilidad que los que sí reportan | §3.3 · 55% con dato | Comparar disponibilidad de los dos grupos (162 vs. 198 puntos) |
| **H6** | Una parte relevante de los leads B2B se pierde por tiempo de respuesta, no por precio | §2.1 · captación pasiva | Medir el tiempo entre envío del formulario y primer contacto comercial |
| **H7** | El consumidor no distingue si la mala experiencia ocurrió en un punto operado por Marley o por un tercero | §5 · flujo C | Encuesta de atribución de responsabilidad tras una experiencia negativa |

### 10.1. Instrumentos, alcance y secuencia

| Instrumento | Alcance | Hipótesis que resuelve |
|---|---|---|
| Encuesta segmentada por canal (consumidor final) | Muestra por canal, anonimizada [C] | H3, H7 |
| Entrevistas a decisores B2B | Dueños Horeca · facilities OCS · administradores EESS y panaderías | H1, H2, H6 |
| **Mystery shopping / visitas de observación** | Muestra de los 4 canales: estado de máquina, disponibilidad, calidad de servicio | H4, H5 |
| Análisis de datos internos | ERP + CRM + tickets, con las brechas de §6 declaradas | H5, H6 |
| Social listening y reseñas | Marley y competidores por canal (Nestlé, Copec/Pronto, Starbucks, Dunkin', Castaño) [C] | H7 · estándares esperados |

**Restricción legal transversal [C]:** solo información agregada, anonimizada o sintética; todo
mecanismo de captura debe informar su finalidad y solicitar consentimiento.

---

## 11. El problema central — en una frase

La comisión exige una idea central jerarquizada: *"si el grupo no puede resumir su propuesta en una
frase, no está lista"* (criterio #2). El video lo repite: *"debemos ser capaces de entregar la idea
de resolución del desafío en una frase"*.

> ## Marley Coffee no tiene un problema de café: tiene **3.390 puntos que no puede ver**.
>
> Sin identidad única de punto, su experiencia se gestiona **por reclamo** y no por diseño, su
> reposición **por memoria** y no por dato, y su crecimiento **por esfuerzo comercial** y no por
> sistema — de modo que el mal momento de un canal se paga en todos los demás, y nadie se entera.

### Por qué esta formulación resiste a la comisión

| Criterio | Cómo lo cumple |
|---|---|
| **Fundamentado** (#1) | Se sostiene en dato del caso: sin ID único [C], 82% manual [C], 26% de cuentas analizables [D] |
| **Uno, no una lista** (#2) | Una sola causa raíz (F1) de la que cuelgan las cinco fricciones restantes (§4.1) |
| **Específico de Marley** (#3) | No aplica a Nescafé ni a Starbucks: ellos **sí** ven su red. La ceguera es consecuencia directa del modelo de Marley —crecer rápido apoyado en terceros que operan el punto— y esa es su historia, no la de un competidor |
| **Sistémico** (rúbrica) | La última cláusula es literalmente la definición de omnicanalidad: *el mal momento de un canal se paga en todos los demás* |
| **Medible** (#8) | La solución tiene KPI natural: % de puntos con identidad única y trazabilidad completa — no es métrica de vanidad |

### Hacia dónde apunta (fuera del alcance de este entregable)

El diagnóstico condiciona la secuencia de la propuesta, no la propuesta misma:

1. **Primero ver** — identidad única de punto. Habilitador de todo lo demás; sin esto, ninguna
   medición es real.
2. **Después servir sin que lo pidan** — reposición predictiva y portal transaccional Horeca:
   convertir 943 pedidos manuales/mes [D] en capacidad comercial liberada.
3. **Después conectar** — mecanismos físico-digitales que hagan visibles los flujos A y B del halo
   (§5) y conviertan la prueba en OCS en demanda B2B.
4. **En paralelo, negociar** — el cuadrante de bajo control (§8) requiere contrapartida de valor
   para el tercero, no una solicitud.

---

## 12. Supuestos propios del equipo — declaración explícita

Además de los supuestos académicos del caso [C], este diagnóstico introduce los siguientes
supuestos propios. Ninguno contradice una cifra del brief; todos son verificables:

1. **Frecuencia de reposición Horeca:** se asume una reposición mensual por punto activo para
   dimensionar la carga operativa (§3.1). El brief no entrega frecuencia de pedido. **Si la
   frecuencia real es quincenal, la carga manual se duplica** — el argumento se refuerza, no se
   debilita.
2. **Base de cálculo del CRM (§6.1):** se asume que el 40% de completitud se mide sobre el 65% de
   cuentas registradas. Si se midiera sobre el universo total, la cifra de analizabilidad sería
   peor que 26%.
3. **Exposición de marca de EESS:** se asume que el canal concentra la mayor exposición diaria de
   marca por el tráfico del formato (~1 millón de personas/día solo en Copec [P]), pese a ser 9% de
   las ventas. **Pendiente de dimensionar** con datos de tráfico de los operadores.
4. **Rotación de personal en los puntos de terceros:** se asume alta en Horeca y panaderías como
   explicación de la brecha de capacitación. **Es H4, no un hecho.**
5. **Ponderación del NPS base:** se infiere ponderación por participación de ventas por
   coincidencia aritmética con el 42 declarado (§9.1). Debe confirmarse con el docente o el tutor.

### Brechas de información que siguen abiertas

- Frecuencia y ticket promedio de pedido por canal.
- Costo de servir por punto y por canal (necesario para el business case).
- Tráfico real de consumidores en los puntos EESS y panaderías.
- Antigüedad de contratos OCS y calendario de renovaciones (crítico para H1).
- Detalle del contrato con XYZ SPA: qué se puede exigir contractualmente hoy y qué en la renovación.

---

## Trazabilidad — de dónde sale cada pieza

| Sección | Exigencia que responde |
|---|---|
| §1–§3 | Entregable 1: mapa de journey por los 4 canales, momentos de verdad, fricciones y brechas |
| §4 | Pregunta guía del brief: *"¿cuáles fricciones son comunes a varios canales?"* |
| §5 | Brief §2.3 y §3.4: influencia cruzada y puntos de conexión · criterio "pensamiento sistémico" |
| §6 | Brief §3.5: punto de partida tecnológico y de datos · habilita el gobierno de datos |
| §7 | Rúbrica criterio #11: FODA, PESTEL, Benchmark, Cadena de Valor, mercados extranjeros |
| §8 | Brief §3.4: priorización según control real y contexto competitivo |
| §9 | Brief §2.4: *"pueden cuestionar las metas con justificación cuantitativa"* |
| §10 | Brief §5.2 y §5.3: investigación primaria y tensiones convertidas en hipótesis |
| §11 | Rúbrica criterios #2 y #3 · exigencia del video: la idea en una frase |
| §12 | Rúbrica criterio #1 · regla de supuestos del video |

✅ **Pendientes cerrados con research el 17-08-2026:** precio internacional del café (§7.2.1),
vigencia de la Ley 21.719 (§7.2.2) y referentes de benchmark (§7.4). Fuentes al pie de §7.4.
Un referente fue **descartado** ("coffee corner" España) y uno quedó **parcialmente verificado**
(telemetría de 3corações). Ambos marcados en la tabla.

⚠️ **Sigue abierto:** el costo de venta real de Marley, necesario para dimensionar la ventana de
alivio de margen de §7.2.1, y el tráfico de consumidores en puntos EESS y panaderías (§12).
