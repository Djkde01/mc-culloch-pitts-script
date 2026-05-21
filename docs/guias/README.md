# Guías paso a paso

Guías prácticas para **demostrar y validar** cada script del repositorio desde la terminal. Incluyen el flujo interno del programa, entradas concretas y resultados esperados.

| Script | Guía | Teoría y API |
|--------|------|----------------|
| `FNG.py` | [FNG.md](FNG.md) | [../fng.md](../fng.md) |
| `mcp_neuron.py` | [mcp_neuron.md](mcp_neuron.md) | [../mcp_neuron.md](../mcp_neuron.md) |

## Validación automática (recomendado antes de exponer)

```bash
cd /ruta/al/proyecto/grammars
python3 -m unittest test_fng.py -v
python3 -m unittest test_mcp_neuron.py -v
```

Si todos los tests pasan, el núcleo lógico de cada script está correcto. Las guías siguientes complementan eso con demostración manual interactiva.
