# Fórmulas de revisión (baja tensión)

Símbolos: P potencia (W), U tensión (V), I intensidad (A), L longitud (m), S sección (mm²), γ conductividad (m/(Ω·mm²)), e caída de tensión (V), cos φ factor de potencia.

## Intensidad
- Monofásica: I = P / (U · cos φ)
- Trifásica: I = P / (√3 · U_L · cos φ)
- Corriente continua: I = P / U

## Caída de tensión
- Monofásica (ida y vuelta): e = 2 · L · I · cos φ / (γ · S)
- Trifásica: e = √3 · L · I · cos φ / (γ · S)
- Porcentual: e % = 100 · e / U

## Sección por caída de tensión (despejando)
- Monofásica: S = 2 · L · I · cos φ / (γ · e)
- Trifásica: S = √3 · L · I · cos φ / (γ · e)

## Coherencia de protección (criterio general)
- I_B ≤ I_n ≤ I_z (intensidad de empleo, calibre de la protección e intensidad admisible del conductor).
- Verificar además la condición de funcionamiento en la normativa vigente `[VERIFICAR: ITC-BT-22]`.

## Valores que NO se dan aquí
Conductividad según temperatura, intensidades admisibles por sección y sistema de instalación, caídas máximas permitidas y secciones mínimas: tomarlos de la ITC-BT vigente y marcar `[VERIFICAR]`.

## Ejemplo de comprobación en código
```python
import math
P, U, cosphi, L, S, gamma = 5750, 230, 1.0, 20, 6, 48  # gamma: [VERIFICAR] según temperatura
I = P / (U * cosphi)
e = 2 * L * I * cosphi / (gamma * S)
print(f"I = {I:.2f} A; e = {e:.2f} V; e% = {100*e/U:.2f} %")
```
