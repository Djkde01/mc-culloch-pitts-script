# Gramáticas y modelos formales

Colección de scripts en Python para **gramáticas libres de contexto** y **modelos de computación / IA**, orientados a uso didáctico desde la terminal. Cada script es independiente y usa solo la biblioteca estándar.

## Requisitos

- Python 3.8 o superior
- No se requieren dependencias externas (`pip install` no es necesario)

## Scripts disponibles

| Script | Descripción | Ejecución | Documentación |
|--------|-------------|-----------|---------------|
| [`FNG.py`](FNG.py) | Validación y conversión a **Forma Normal de Greibach** | `python3 FNG.py` | [docs/fng.md](docs/fng.md) |
| [`mcp_neuron.py`](mcp_neuron.py) | Neurona artificial **McCulloch-Pitts** (1943) | `python3 mcp_neuron.py` | [docs/mcp_neuron.md](docs/mcp_neuron.md) |

## Pruebas

Para ejecutar las pruebas del conversor FNG:

```bash
python3 -m unittest test_fng.py -v
```

## Estructura del repositorio

```
grammars/
├── README.md           # Este índice
├── docs/
│   ├── fng.md          # Teoría y uso de FNG.py
│   └── mcp_neuron.md   # Teoría y uso de mcp_neuron.py
├── FNG.py
├── mcp_neuron.py
└── test_fng.py
```
