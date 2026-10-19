# ICP — Interruptor de Control de Potencia

## En una frase
El **ICP** es un interruptor **precintable** que limita la potencia máxima que puedes consumir según el contrato con la compañía, y lo instala la empresa distribuidora (no el cliente).

## Prerrequisitos
- Bloque 7 del temario: Conductores y líneas
- Bloque 8 del temario: Instalaciones de enlace (ITC-BT-10 a ITC-BT-17)

## Desarrollo

### ¿Qué es?
Es un dispositivo de **control contractual**: limita tu potencia máxima contratada. No protege contra cortocircuitos ni sobrecargas — esa función la tiene el **Interruptor General Automático (IGA)**, que es un dispositivo independiente.

El ICP va en su **propia caja**, independiente y **precintable**, dentro del cuadro de mando y protección. Solo la compañía distribuidora puede abrirlo o manipularlo.

> *"Se colocará una caja para el interruptor de control de potencia, inmediatamente antes de los demás dispositivos, en compartimento independiente y precintable."*  
> [FUENTE: references/rebt_salida/md/ITC-BT-17.md §1.1]

### Ubicación en la instalación de enlace

```
Derivación Individual (DI)
    │
    ▼
┌─────────────────────────┐
│  CAJA PARA ICP          │ ← Compartimento INDEPENDIENTE
│  (precintable, compañía) │   y PRECINTABLE
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ DISPOSITIVOS GENERALES   │
│ DE MANDO Y PROTECCIÓN   │ ← IGA + diferencial general + PIA
│ (usuario)               │
└─────────────────────────┘
```

### Diferencia clave: ICP vs. Interruptor General Automático (IGA)

| Característica | ICP | IGA |
|---|---|---|
| **Función** | Limitar potencia contratada | Protección contra sobrecarga y cortocircuito |
| **¿Quién lo precinta?** | Empresa distribuidora | Usuario |
| **¿Quién lo manipula?** | Solo la distribuidora | Usuario |
| **Norma** | Modelo oficialmente aprobado | UNE 20.451 / UNE-EN 60.439-3 |
| **Corte omnipolar** | Sí | Sí |
| **Mismo dispositivo** | Nunca pueden ser el mismo | — |

> *"Este interruptor será independiente del interruptor de control de potencia."*  
> [FUENTE: references/rebt_salida/md/ITC-BT-17.md §1.2]

### Cuadro general de mando y protección — composición mínima

Según ITC-BT-17 §1.2, el cuadro debe contener como mínimo:

1. **Interruptor General Automático (IGA)** — corte omnipolar, con protección sobrecarga/cortocircuito, poder de corte ≥ 4.500 A
2. **Interruptor diferencial general** — protección contra contactos indirectos
3. **PIA (Pequeños Interruptores Automáticos)** — uno por circuito interior
4. **ICP** — en su propia caja precintable e independiente
5. **Protección contra sobretensiones** — si procede (ITC-BT-23)

### Criterios de ubicación

| Parámetro | Valor |
|---|---|
| **Altura (viviendas)** | 1,4 m – 2,0 m desde el suelo |
| **Altura (locales comerciales)** | ≥ 1,0 m desde el suelo |
| **¿Dónde?** | Junto a la puerta de entrada, nunca en dormitorios, baños ni aseos |
| **Grado de protección envolvente** | IP 30 / IK 07 [FUENTE: references/rebt_salida/md/ITC-BT-17.md §1.2] |

### Potencias normalizadas de ICP

[VERIFICAR: ITC-BT-10 / ITC-BT-14] — Las más habituales en viviendas son:

| Potencia contratada | Intensidad ICP |
|---|---|
| 3,3 kW | 15 A |
| 4,4 kW | 20 A |
| 5,5 kW | 25 A |
| 6,9 kW | 32 A |
| 9,2 kW | 40 A |
| 11,4 kW | 50 A |

---

## Ejemplo resuelto

**Enunciado**: Una vivienda tiene potencia contratada de 5,5 kW en monofásico a 230 V. ¿De cuántos amperios debe ser el ICP?

**Fórmula**: I = P / U

**Datos**:
- P = 5.500 W
- U = 230 V

**Sustitución**: I = 5.500 W / 230 V

**Resultado**: I = **23,9 A → ICP de 25 A**

---

## Ejercicios

1. **(Básico)** Una vivienda tiene contratada una potencia de 4,4 kW en monofásico a 230 V. ¿De cuántos amperios debe ser el ICP?

2. **(Medio)** Indica qué dispositivos forman el cuadro general de mando y protección mínimo según ITC-BT-17 y explica la diferencia entre el ICP y el IGA.

3. **(Aplicado)** Un local comercial tiene ICP de 32 A. La compañía distribuidora le quiere subir la potencia a 9,2 kW. ¿Es posible sin cambiar el ICP? Justifícalo.

---

## Resumen
- El **ICP** controla la **potencia máxima contratada**, lo precinta la distribuidora y es **independiente** del IGA.
- El **cuadro de mando y protección** mínimo lleva: ICP (precintado), IGA, diferencial general y PIA por circuito.
- Se coloca **junto a la entrada**, entre la derivación individual y el resto del cuadro.
- El **ICP nunca puede ser el mismo dispositivo que el IGA**.

---

## Siguiente tema
Derivación Individual (DI) — el tramo entre el contador y el ICP → Bloque 8 del temario (Instalaciones de enlace, ITC-BT-12/ITC-BT-15).

## Verificaciones pendientes
- [ ] Tabla completa de intensidades normalizadas del ICP (ITC-BT-10 / ITC-BT-14)
- [ ] ITC-BT-15: dimensiones exactas de cajas para derivaciones individuales
