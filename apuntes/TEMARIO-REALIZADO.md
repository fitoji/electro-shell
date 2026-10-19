# Temario realizado

Registro de lo que **ya estudié**, en orden cronológico.

No es una copia del temario propuesto (`skills/tutor-electrotecnia/references/temario.md`): recoge lo que realmente se trabajó, incluidas consultas sueltas y dudas resueltas que no forman parte de ningún bloque cerrado.

**Convención de fecha**: día de la sesión de estudio, no del commit.
**Evidencia**: `apunte` = documento en `apuntes/`; `consulta` = resuelto en sesión sin apunte.

---

## Registro

| Fecha | Tema | Bloque propuesto | Evidencia | Pendiente |
| --- | --- | --- | --- | --- |
| 2026-10-18 | ITC-BT-14 — Línea General de Alimentación (LGA) | 8 | `apuntes/ITC-BT-14.md` | — |
| 2026-10-19 | ICP — Interruptor de Control de Potencia | 8 | `apuntes/ICP.md` | Tabla de intensidades normalizadas del ICP |
| 2026-10-19 | Cajas en instalaciones de enlace: CGP, caja de derivación, cajas de empalme | 8 | consulta en sesión | — |

---

## Cobertura por bloque

Comparación con los 12 bloques del temario propuesto.

| # | Bloque | Estado |
| --- | --- | --- |
| 1 | Magnitudes y unidades | sin tocar |
| 2 | Corriente continua | sin tocar |
| 3 | Potencia y energía | sin tocar |
| 4 | Corriente alterna monofásica | sin tocar |
| 5 | Potencias en CA | sin tocar |
| 6 | Sistemas trifásicos | sin tocar |
| 7 | Conductores y líneas | sin tocar |
| 8 | **Instalaciones de enlace** (ITC-BT-10 a ITC-BT-17) | **en curso** |
| 9 | Protecciones | sin tocar |
| 10 | Transformadores y máquinas | sin tocar |
| 11 | Automatismos cableados | sin tocar |
| 12 | Automatismos programables | sin tocar |

> Estudio no lineal: el bloque 8 se está trabajando antes que los bloques 1–7. Es válido como repaso aplicado, pero conviene volver a los prerrequisitos (bloques 7 y 9) cuando aparezcan cálculos de sección o protecciones.

---

## Notas de lo aprendido

- **"Caja de enlace" no es término del REBT.** El reglamento habla de CGP, caja de derivación, caja de empalme y caja para ICP. En obra se usa "caja de enlace" de forma coloquial, normalmente para la caja de derivación (ítem 6 del esquema de ITC-BT-12). `[FUENTE: md/ITC-BT-12.md §1.2 y §2]`
- **ICP ≠ IGA.** El ICP limita la potencia contratada y lo precinta la distribuidora; el IGA protege contra sobrecarga y cortocircuito y lo maneja el usuario. Nunca son el mismo dispositivo. `[FUENTE: md/ITC-BT-17.md §1.2]`

---

## Pendientes de verificación

- [ ] Tabla completa de intensidades normalizadas del ICP (ITC-BT-10 / ITC-BT-14) — el corpus no la incluye.
- [ ] Dimensiones exactas de cajas para derivaciones individuales (ITC-BT-15) — el corpus tiene la referencia pero no los valores completos.
- [ ] Correspondencia de cabecera de ITC-BT-19 Tabla 1 contra UNE 20.460-5-523.

---

## Siguiente tema

**Derivación Individual (DI)** — el tramo entre el contador y el ICP. Cierra la cadena de la instalación de enlace que empezó con la LGA.

---

## Cómo se mantiene este registro

**Automático.** La skill `tutor-electrotecnia` lo actualiza antes de cerrar cada turno, sin que haya que pedirlo. Las reglas están en el «Protocolo de registro» de `skills/tutor-electrotecnia/SKILL.md`.

Qué hace en cada sesión:

1. Añadir una fila a la tabla **Registro** con la fecha de la sesión.
2. Actualizar la fila correspondiente en **Cobertura por bloque**.
3. Si la duda generó un apunte en `apuntes/`, enlazarlo en la columna **Evidencia**.
4. Si quedó algo sin verificar, añadirlo a **Pendientes de verificación**.
5. Actualizar **Siguiente tema**.

Ajustes manuales permitidos: corregir una fecha, reclasificar un tema, marcar un bloque como `hecho`.
