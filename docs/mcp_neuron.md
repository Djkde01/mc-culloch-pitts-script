# Neurona McCulloch-Pitts y modelo extendido

Script en Python que implementa el **autómata de McCulloch y Pitts** (1943) y una **neurona extendida** con sesgo y función sigmoide, orientada a compuertas lógicas y uso didáctico desde la terminal.

> **Guía práctica:** entradas paso a paso, demostraciones y validación en [guias/mcp_neuron.md](guias/mcp_neuron.md).

## Ejecución

```bash
python3 mcp_neuron.py
```

Al iniciar aparece un menú con demos de compuertas, prueba de XOR en red, y modos de configuración manual.

## Modelo biológico-computacional

### Entrada de señales (dendritas)

Las entradas `x1`, `x2`, `x3` representan la estimulación del entorno. En modo **MCP clásico** solo se aceptan valores binarios (`0` o `1`). En modo **extendido** pueden usarse valores reales (por ejemplo intensidades de estímulo).

### Sumatoria y umbral / sesgo

La neurona agrega las señales ponderadas:

- **MCP clásico:** `suma = Σ (w_i · x_i)`. Si `suma ≥ θ` (umbral), la neurona dispara (`salida = 1`).
- **Neurona extendida:** `z = Σ (w_i · x_i) + b` (sesgo `b`). El valor `z` modela la intensidad de estimulación antes de la activación.

Equivalencia didáctica:

```
MCP:       dispara si  Σ(w_i · x_i) ≥ θ
Extendida: dispara si  z = Σ(w_i · x_i) + b ≥ 0   ⟺   θ = -b
```

Ejemplo AND: pesos `[1, 1]`, umbral `2` ⟺ pesos `[1.0, 1.0]`, sesgo `-2.0`.

### Función de activación

| Modo | Función | Salida |
|------|---------|--------|
| MCP clásico | Escalón con umbral θ | `0` o `1` |
| Extendida (sigmoide) | `y = 1 / (1 + e^-z)` | Continua en `(0, 1)` |
| Extendida (escalón) | `y = 1` si `z ≥ 0` | `0.0` o `1.0` |

La sigmoide modela un disparo gradual (señal eléctrica por el axón). Para comparar con lógica binaria se usa **binarización**: `y_binaria = 1` si `y ≥ 0.5`.

### Pesos

| Valor | Rol habitual |
|-------|----------------|
| `1` / `1.0` | Conexión excitatoria |
| `-1` / `-1.0` | Conexión inhibitoria |

## Compuertas implementadas

| Compuerta | MCP (pesos, umbral) | ¿Una neurona? |
|-----------|---------------------|---------------|
| AND | `[1, 1]`, θ=2 | Sí |
| OR | `[1, 1]`, θ=1 | Sí |
| NOT x1 | `[-1, 0]`, θ=0 | Sí (x2 ignorada) |
| ANDNOT | `[1, -1]`, θ=1 | Sí |
| XOR | Red de 3 neuronas | **No** |

### ANDNOT

`x1 AND NOT x2`: pesos `[1, -1]`, umbral `1`.

| x1 | x2 | Suma | Salida |
|----|----|------|--------|
| 0 | 0 | 0 | 0 |
| 0 | 1 | -1 | 0 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 0 |

### XOR (red de 3 neuronas)

XOR no es linealmente separable: **una sola neurona MCP no puede implementarla**. El script usa esta red:

```
x1, x2 ──► N1 [1,-1] θ=1   (x1 AND NOT x2)
x1, x2 ──► N2 [-1,1] θ=1   (NOT x1 AND x2)
N1, N2 ──► N3 [1,1]  θ=1   (OR)
```

| x1 | x2 | N1 | N2 | XOR |
|----|----|----|----|-----|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 0 |

Use la opción **3** del menú para ver el trazado paso a paso.

## Menú principal

```
=== Autómata McCulloch-Pitts ===
1. Demos compuertas (MCP clásico)
2. Demos compuertas (neurona extendida + sigmoide)
3. Probar XOR (red de 3 neuronas + trazado)
4. Configurar neurona MCP manualmente
5. Configurar neurona extendida manualmente
0. Salir
```

En las opciones 1 y 2, submenú: AND, OR, NOT, ANDNOT, XOR o todas.

### Salida modo MCP (ejemplo AND)

```
Entradas             | Suma | Salida
x1=0, x2=0           |    0 |      0
x1=0, x2=1           |    1 |      0
x1=1, x2=0           |    1 |      0
x1=1, x2=1           |    2 |      1
```

### Salida modo extendido (ejemplo AND)

```
Entradas             |        z |    y_sig | y_bin
x1=1, x2=1           |   0.0000 |   0.5000 |     1
```

## Uso programático

```python
from mcp_neuron import (
    McCullochPittsNeuron,
    ExtendedNeuron,
    MCPNetwork,
    GATE_PRESETS,
    xor_network_predict,
)

# MCP clásico
and_gate = McCullochPittsNeuron([1, 1], 2)
and_gate.predict([1, 1])  # 1

# Extendida
neuron = ExtendedNeuron([1.0, 1.0], -2.0, activation="sigmoid")
z, y = neuron.activate([1.0, 1.0])

# XOR
xor_network_predict([1, 0])  # 1
network = MCPNetwork()
out, (h1, h2) = network.forward([1, 1])

# Presets
preset = GATE_PRESETS["ANDNOT"]
preset.mcp_neuron().predict([1, 0])  # 1
```

## API principal

| Clase / función | Descripción |
|-----------------|-------------|
| `McCullochPittsNeuron` | Pesos enteros, umbral, entradas binarias, salida 0/1 |
| `ExtendedNeuron` | Pesos reales, sesgo, activación `sigmoid` o `step` |
| `MCPNetwork` | Red fija de 3 neuronas para XOR |
| `GATE_PRESETS` | Configuraciones AND, OR, NOT, ANDNOT, XOR |
| `run_gate_demo(name, mode)` | Imprime tabla de verdad (`mcp` o `extended`) |

## Pruebas

```bash
python3 -m unittest test_mcp_neuron.py -v
```

## Referencia

McCulloch y Pitts (1943) modelaron neuronas binarias con umbral. La neurona extendida con sigmoide y sesgo aproxima el comportamiento de unidades posteriores en redes feedforward, manteniendo el MCP clásico como caso didáctico separado.
