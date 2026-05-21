# Neurona McCulloch-Pitts (terminal)

Script en Python que implementa una **neurona artificial de McCulloch y Pitts** (1943): el modelo más simple de unidad de procesamiento con entradas binarias, pesos enteros y una función de activación escalón. Todo el programa se ejecuta, configura y consulta **desde la terminal** (sin interfaz gráfica ni dependencias externas).

## Ejecución rápida

```bash
cd /ruta/al/proyecto
python3 mcp_neuron.py
```

Al iniciar, el script muestra automáticamente la **demo de la compuerta AND** y luego pregunta si deseas entrar al **modo interactivo** para probar otras configuraciones.

## ¿Qué es una neurona McCulloch-Pitts?

Es un modelo binario que:

1. Recibe un vector de entradas **estrictamente binarias** (solo `0` o `1`).
2. Calcula la **suma ponderada** (producto punto) entre entradas y pesos.
3. Compara esa suma con un **umbral** entero.
4. Devuelve `1` si la suma es **mayor o igual** al umbral; en caso contrario, `0`.

No incluye **sesgo (bias)** ni **aprendizaje**: los pesos y el umbral se fijan a mano al diseñar la neurona para una función lógica concreta.

### Fórmula

```
activación = Σ (peso_i × entrada_i)
salida     = 1  si activación ≥ umbral
           = 0  en caso contrario
```

### Pesos

| Valor | Significado habitual |
|-------|----------------------|
| `1`   | Conexión excitatoria |
| `-1`  | Conexión inhibitoria |

## Flujo del programa

```
Inicio
  → Demo compuerta AND (4 combinaciones)
  → ¿Probar otra neurona? (s/n)
       → s: modo interactivo (pesos, umbral, entradas)
       → n: fin
```

## Demo: compuerta AND

La neurona se configura así para una AND de 2 entradas:

| Parámetro | Valor   | Motivo |
|-----------|---------|--------|
| Pesos     | `[1, 1]` | Ambas entradas suman cuando están activas |
| Umbral    | `2`      | Solo con las dos entradas en `1` la suma alcanza 2 |

| x1 | x2 | Suma | Salida |
|----|----|------|--------|
| 0  | 0  | 0    | 0      |
| 0  | 1  | 1    | 0      |
| 1  | 0  | 1    | 0      |
| 1  | 1  | 2    | 1      |

Salida esperada en terminal:

```
--- Demo: compuerta lógica AND (2 entradas) ---
Pesos: [1, 1]  |  Umbral: 2

Entrada [0, 0]  |  Suma: 0  |  Salida: 0
Entrada [0, 1]  |  Suma: 1  |  Salida: 0
Entrada [1, 0]  |  Suma: 1  |  Salida: 0
Entrada [1, 1]  |  Suma: 2  |  Salida: 1
```

## Modo interactivo

Responde `s`, `si` o `sí` cuando el programa lo pregunte. Luego:

1. **Pesos:** enteros separados por espacios, por ejemplo `1 1` o `1 1 -1`.
2. **Umbral:** un entero, por ejemplo `2`.
3. **Entradas:** en cada prompt `Entradas>`, escribe tantos `0` o `1` como pesos definiste, separados por espacio.

Para salir del bucle de entradas: línea vacía (Enter) o la palabra `salir`.

### Ejemplo: compuerta OR (2 entradas)

```
¿Desea probar otra neurona? (s/n): s
Ingrese los pesos (enteros separados por espacio): 1 1
Ingrese el umbral (entero): 1

Entradas> 0 0
  Suma: 0  |  Salida: 0

Entradas> 1 1
  Suma: 2  |  Salida: 1
```

Con umbral `1`, basta que una entrada esté en `1` para que la salida sea `1`.

### Errores habituales

El programa no se cierra ante un error de entrada; muestra el mensaje y vuelve a pedir datos:

- Entradas con longitud distinta a la de los pesos.
- Valores distintos de `0` o `1`.
- Línea de pesos vacía o umbral no numérico (en la configuración inicial).

## Uso programático (clase)

Puedes importar la neurona desde otro módulo Python:

```python
from mcp_neuron import McCullochPittsNeuron

neuron = McCullochPittsNeuron(weights=[1, 1], threshold=2)
print(neuron.predict([1, 1]))  # 1
print(neuron.predict([0, 1]))  # 0
```

### API

| Método | Descripción |
|--------|-------------|
| `__init__(weights, threshold)` | Guarda la lista de pesos enteros y el umbral entero. |
| `predict(inputs)` | Valida entradas binarias, calcula el producto punto y devuelve `0` o `1`. |

## Referencia histórica

McCulloch y Pitts (1943) demostraron que redes de estas neuronas binarias pueden representar funciones lógicas y, en principio, comportamiento similar al razonamiento formal. Este script es una implementación didáctica de **una sola neurona**, no de una red completa.
