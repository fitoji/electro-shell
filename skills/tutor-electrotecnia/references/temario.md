# Temario de electrotecnia (orden recomendado)

Cada bloque indica prerrequisitos. Ajustar al currículo real del ciclo del alumno.

| # | Bloque | Contenidos | Prerrequisitos |
| --- | --- | --- | --- |
| 1 | Magnitudes y unidades | Tensión, intensidad, resistencia, potencia, energía, SI | — |
| 2 | Corriente continua | Ley de Ohm, serie y paralelo, leyes de Kirchhoff, divisores | 1 |
| 3 | Potencia y energía | P = U·I, efecto Joule, rendimiento | 2 |
| 4 | Corriente alterna monofásica | Senoidal, valor eficaz, R, L, C, impedancia, fasores | 2 |
| 5 | Potencias en CA | Activa, reactiva, aparente, factor de potencia, compensación | 4 |
| 6 | Sistemas trifásicos | Estrella y triángulo, tensiones de fase y línea, potencia trifásica | 4, 5 |
| 7 | Conductores y líneas | Intensidad admisible, sección, caída de tensión | 3, 6 |
| 8 | Instalaciones de enlace | Previsión de cargas, acometidas, caja general de protección, línea general de alimentación, contadores, derivaciones individuales, dispositivos generales e individuales de mando y protección (ITC-BT-10 a ITC-BT-17) | 7 |
| 9 | Protecciones | Sobreintensidad, cortocircuito, contactos directos e indirectos, puesta a tierra | 7, 8 |
| 10 | Transformadores y máquinas | Transformador, motor asíncrono, placa de características | 5, 6 |
| 11 | Automatismos cableados | Contactores, relés, esquemas de mando y potencia, arranque de motores | 9, 10 |
| 12 | Automatismos programables | Lógica programada, PLC, GRAFCET | 11 |

> **Bloque 8 y el corpus.** Este bloque se estudia directamente contra el corpus del proyecto: `references/rebt_salida/md/ITC-BT-10.md` a `references/rebt_salida/md/ITC-BT-17.md`, con los valores numéricos en `references/rebt_salida/tablas/_v2/`. Citar siempre `[FUENTE: md/ITC-BT-XX.md §Y]`; lo que no esté en el corpus, `[VERIFICAR: ITC-BT-XX]`.

## Fórmulas base de referencia rápida
- Ley de Ohm: U = I · R
- Potencia (CC): P = U · I
- Monofásica CA: P = U · I · cos φ
- Trifásica: P = √3 · U_L · I_L · cos φ
- Energía: W = P · t

Los criterios normativos (secciones mínimas, caídas máximas, calibres) **no** están aquí: consultar la ITC-BT vigente y marcar `[VERIFICAR]`.
