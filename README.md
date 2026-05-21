# Gramáticas y modelos formales

Colección de scripts en Python para **gramáticas libres de contexto** y **modelos de computación / IA**, orientados a uso didáctico desde la terminal. Cada script es independiente y usa solo la biblioteca estándar.

## Requisitos

- Python 3.8 o superior
- No se requieren dependencias externas (`pip install` no es necesario)

## Scripts disponibles

| Script | Descripción | Ejecución | Documentación |
|--------|-------------|-----------|---------------|
| [`FNG.py`](FNG.py) | Validación y conversión a **Forma Normal de Greibach** | `python3 FNG.py` | [Teoría](docs/fng.md) · [Guía paso a paso](docs/guias/FNG.md) |
| [`mcp_neuron.py`](mcp_neuron.py) | **McCulloch-Pitts** + neurona extendida (sigmoide, sesgo), compuertas AND/OR/NOT/ANDNOT/XOR | `python3 mcp_neuron.py` | [Teoría](docs/mcp_neuron.md) · [Guía paso a paso](docs/guias/mcp_neuron.md) |

## Pruebas

Para ejecutar las pruebas:

```bash
python3 -m unittest test_fng.py -v
python3 -m unittest test_mcp_neuron.py -v
```

## Estructura del repositorio

```
grammars/
├── README.md           # Este índice
├── docs/
│   ├── fng.md          # Teoría y API de FNG.py
│   ├── mcp_neuron.md   # Teoría y API de mcp_neuron.py
│   └── guias/          # Demostración y validación paso a paso
│       ├── README.md
│       ├── FNG.md
│       └── mcp_neuron.md
├── FNG.py
├── mcp_neuron.py
├── test_fng.py
└── test_mcp_neuron.py
```
