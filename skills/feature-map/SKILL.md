---
name: feature-map
description: Úsala al corregir bugs, optimizar rendimiento o implementar funcionalidades donde el cambio debe demostrarse ejecutando la app real (reproducir antes, verificar después con evidencia), al recibir reportes vagos ("va lento", capturas sin contexto), al crear o mantener un FEATURE_MAP.md, o al convertir errores recurrentes de agentes en guardrails duros (linters, checks de CI). Verificación de bucle cerrado basada en la arquitectura Pstack/Dune de Lauren Tan.
---

# Agent Verification Loop & Guardrails

Esta skill transforma al agente de un generador de código especulativo en un ingeniero autónomo capaz de **reproducir, verificar, demostrar y endurecer** cambios en el código base sin intervención humana constante (evitando que el usuario sea el cuello de botella).

---

## Principios Fundamentales

1. **Cero adivinanzas (Read Before Hypothesizing):** Prohibido afirmar cuál es la causa raíz de un problema sin haber leído previamente los archivos exactos involucrados y trazado el flujo real de ejecución.
2. **El camino más corto debe ser el mejor camino:** La estructura del código y los selectores deben estar documentados para que navegar y modificar una funcionalidad sea determinista.
3. **Verificación de bucle cerrado (Closed-Loop):** Un cambio no está terminado cuando compila; está terminado cuando el agente ejecuta la aplicación real (como lo haría un usuario), reproduce el escenario y captura evidencia objetiva del antes y después.
4. **Endurecimiento progresivo:** Las instrucciones en Markdown son *restricciones blandas* (el agente puede olvidarlas). Todo patrón de error recurrente debe convertirse en una *restricción dura* (regla de linter, verificación de dependencias o check en CI).

---

## Flujo de Trabajo 1: Creación y Mantenimiento del `FEATURE_MAP.md`

Busca `FEATURE_MAP.md` en la raíz del proyecto o en `.agent/` y aplica la primera regla que se cumpla:

| Situación observable | Acción |
|---|---|
| `FEATURE_MAP.md` existe | Consúltalo en la Fase 1 y actualiza las entradas que tu cambio afecte. |
| No existe **y** el proyecto tiene interfaz de usuario (web, móvil, escritorio, TUI) | Créalo antes de la Fase 2, como mínimo con la entrada de la funcionalidad que estás tocando. |
| No existe **y** el proyecto tiene más de 15 archivos de código fuente | Créalo antes de la Fase 2, como mínimo con la entrada de la funcionalidad que estás tocando. |
| Ninguna de las anteriores | No lo crees. En el Informe de Cierre escribe: "FEATURE_MAP.md omitido: proyecto sin UI y con ≤15 archivos fuente." |

Estructura de cada entrada:

```markdown
# Feature Map

## [Nombre de la Funcionalidad / Vista]
- **Ubicación del código:** `ruta/al/directorio/co-localizado/`
- **Ruta de navegación (Usuario):** Paso 1 -> Paso 2 -> Acción
- **Atajos de teclado / Comandos:** `Cmd+K` / `npm run dev`
- **Selectores deterministas (CDP / Playwright / Maestro):**
  - Contenedor principal: `[data-testid="..."]`
  - Acción disparadora: `button[aria-label="..."]`
- **Proceso / Hilo de ejecución:** Main thread / Renderer / Server Action / Worker
- **Invariantes críticos:** (ej. "No debe bloquear el hilo de renderizado > 16ms", "No importar módulos de servidor en cliente")
```

### Reglas de mantenimiento del mapa:
- Cada vez que crees una nueva funcionalidad o modifiques rutas/selectores, actualiza la entrada correspondiente en `FEATURE_MAP.md` dentro del mismo PR o conjunto de cambios.
- Mantén todo el código relacionado con una funcionalidad co-localizado en un mismo directorio siempre que la arquitectura lo permita.

---

## Flujo de Trabajo 2: Protocolo de Verificación en Bucle Cerrado

Ante cualquier tarea de corrección de bugs, optimización de rendimiento o nueva funcionalidad, ejecuta estrictamente estas 5 fases:

### Fase 1: Triaje y Localización Real
1. Consulta `FEATURE_MAP.md` para identificar la ubicación exacta de la funcionalidad.
2. Lee los archivos fuente relevantes y sus dependencias directas.
3. Si el reporte es ambiguo (ej. una captura de pantalla o descripción vaga), cruza los elementos visuales con los selectores del mapa antes de formular una hipótesis.

### Fase 2: Reproducción en Entorno Real
Levanta la aplicación localmente en modo desarrollo o pruebas utilizando la herramienta nativa correspondiente al stack:
- **Web / Electron:** Chrome DevTools Protocol (CDP), Playwright o Puppeteer (capturando logs de consola, errores de red, trazas de rendimiento/CPU y *heap snapshots*).
- **Móvil (iOS / Android / Flutter):** Simuladores nativos (`xcrun simctl`, `adb`, `flutter test` / integración) con captura de estado y métricas de frames.
- **Backend / CLI:** Ejecución directa del binario, endpoints reales o suites de integración contra entorno aislado.

*Requisito:* Captura evidencia del estado inicial (**Antes**) que demuestre el fallo o el comportamiento actual.

### Fase 3: Implementación Atómica
1. Aplica cambios pequeños, enfocados y fáciles de revertir.
2. Evita comentarios históricos o narrativos innecesarios en el código; el código debe ser autoexplicativo y el historial de Git debe describir el porqué del commit.
3. Respeta estrictamente el aislamiento de capas (ej. no mezclar lógica pesada de I/O en el hilo principal de renderizado UI).

### Fase 4: Verificación de Evidencia (Después)
1. Vuelve a ejecutar exactamente el mismo flujo de reproducción de la Fase 2.
2. Compara métricas y comportamiento (**Antes vs. Después**):
   - ¿Desaparecieron los errores de consola/excepciones?
   - ¿Se mantiene el presupuesto de rendimiento (ej. $< 16\text{ms}$ por frame para $60\text{fps}$)?
   - ¿Se mantuvieron intactas las funcionalidades adyacentes?
3. Si la verificación falla, **no entregues el código**. Analiza la traza real, ajusta e itera hasta que la prueba pase de forma determinista.

### Cuando el entorno bloquea la ejecución (Fases 2 y 4)
"La verificación falla" significa que la prueba se ejecutó y dio un resultado incorrecto. Si la prueba **no se puede ejecutar** (permiso denegado, servidor que no arranca, protocolo `file://` bloqueado, simulador ausente), recorre esta tabla en orden: la primera fila siempre aplica si hubo una denegación, y de las demás usa la primera que puedas ejecutar.

| Situación observable | Acción |
|---|---|
| Un permiso fue denegado (la herramienta respondió con denegación del usuario o del modo de permisos) | No repitas esa acción por otra vía (script, otra herramienta, primer plano en vez de segundo plano): la denegación es una decisión del usuario. Pasa a las filas siguientes solo con vías que no hagan lo denegado. |
| Fallo técnico (puerto ocupado, `file://` bloqueado, proceso que no arranca) y existe una vía alternativa con límite de tiempo (ej. otro puerto, un script que levanta el servidor, ejecuta Playwright/CDP headless y lo detiene, con `timeout 60`) | Úsala como reproducción y verificación. Registra en el informe qué vía alternativa usaste. |
| Existe una prueba más cercana al usuario que la lectura de código y que no requiere lo denegado (test de integración, ejecución del binario, `elementFromPoint` en un DOM cargado por script) | Ejecútala antes y después del cambio y entrégala como evidencia parcial. |
| Ninguna vía de ejecución funciona | Entrega el cambio marcado como **NO VERIFICADO**: escribe esas palabras en la primera línea del informe, indica qué vía falló y con qué error exacto, y da los pasos concretos (comando, URL, selector, resultado esperado antes y después) para que el usuario verifique. Si la causa fue un permiso, nombra el permiso que habría que conceder. |

### Fase 5: Informe de Cierre
Presenta al usuario un resumen conciso que incluya:
- Causa raíz verificada (con referencia a archivo y línea).
- Evidencia de reproducción inicial vs. verificación final, o el marcador **NO VERIFICADO** con los pasos de verificación pendientes.
- `FEATURE_MAP.md`: entradas creadas o actualizadas, o la línea de omisión del Flujo de Trabajo 1.

---

## Flujo de Trabajo 3: De Error Recurrente a Restricción Dura (Guardrails)

Cuando detectes que un agente (tú mismo o un subagente) comete un error estructural o viola una convención del proyecto:

1. **Identifica el patrón:** ¿Es un problema de arquitectura (ej. importar módulos prohibidos entre carpetas), un antipatrón del framework (ej. efectos secundarios descontrolados) o una regresión de rendimiento?
2. **Propón o implementa una restricción dura:**
   - Regla personalizada en ESLint / Biome / Analyzer / Clippy.
   - Verificación de grafo de dependencias en el pipeline de CI.
   - Tipado estricto que haga imposible representar estados inválidos.
3. **Objetivo:** Que el build o CI falle automáticamente en rojo si el patrón vuelve a introducirse, eliminando la necesidad de revisión humana para ese problema.

---

## Flujo de Trabajo 4: Autoevaluación de la Skill (Eval Loop)

Cuando modifiques esta skill o configures la verificación para un nuevo repositorio, valida su efectividad mediante aislamiento:

1. **Define una rúbrica objetiva (0 a 10):**
   - *Localización:* ¿Encontró el código correcto sin explorar archivos irrelevantes?
   - *Reproducción:* ¿Ejecutó la app real antes de editar código?
   - *Precisión:* ¿Resolvió la causa raíz sin introducir efectos secundarios?
   - *Evidencia:* ¿Entregó pruebas verificables del resultado?
2. **Prueba ciega con subagentes:** Ejecuta tareas de prueba en directorios o *worktrees* aislados con nombres neutros (sin indicar en el entorno que se trata de una evaluación, para evitar sesgos de comportamiento).
3. **Auditoría cruzada:** Revisa las llamadas a herramientas (*tool calls*) y bloques de razonamiento del subagente para detectar dónde dudó o adivinó, y refina `FEATURE_MAP.md` o los scripts de verificación hasta alcanzar una puntuación consistente.