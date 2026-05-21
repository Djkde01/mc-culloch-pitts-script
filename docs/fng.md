# Forma Normal de Greibach (FNG)

Script en Python que **valida** y **convierte** gramáticas libres de contexto a **Forma Normal de Greibach (FNG)** desde la terminal.

> **Guía práctica:** entradas paso a paso, demostraciones y validación en [guias/FNG.md](guias/FNG.md).

## Ejecución

```bash
python3 FNG.py
```

Al iniciar se muestra un menú:

```
1. Validar gramática
2. Convertir a FNG
3. Demo con ejemplo del curso
```

## ¿Qué es la FNG?

Una gramática está en FNG si todas sus producciones tienen la forma:

```text
A → aα
```

Donde:

- `A` = no terminal (variable)
- `a` = terminal
- `α` = cadena de no terminales (puede ser vacía)

También se permite `S → ε` si el símbolo inicial puede generar la cadena vacía.

### Ejemplos válidos

```text
S -> aA
A -> bBC
B -> c
A -> 2BC
```

### Ejemplos inválidos

```text
S -> AB      (empieza con no terminal)
A -> Ba      (terminal interno)
A -> 2B2     (terminal interno)
```

## Algoritmo de conversión (4 pasos del curso)

El método `to_greibach_normal_form()` aplica estos pasos:

| Paso | Método | Descripción |
|------|--------|-------------|
| 1 | `remove_epsilon()` | Elimina producciones ε innecesarias |
| 2 | `eliminate_left_recursion()` | Sustituye `B → BC` por reglas con símbolo auxiliar `B'` |
| 3 | `substitute_ordered()` | Ordena NTs y sustituye apariciones iniciales hasta que todas empiecen con terminal |
| 4 | `eliminate_internal_terminals()` | Reemplaza terminales internos por NTs que los generan |

Pasos auxiliares internos: eliminar ε en auxiliares, quitar símbolos inalcanzables y una sustitución final.

### Ejemplo del material (demo opción 3)

Gramática original:

```text
A -> CB2
B -> BC
B' -> CB'
C -> 2
```

Tras la conversión (orden `C, B, B', A`):

```text
A -> 2BC
B -> 2B''
B'' -> 2B''
C -> 2
```

La regla `A -> CB2` se sustituye a `A -> 2B2` y luego a `A -> 2BC` porque `C → 2`.

## Convención de símbolos

| Tipo | Formato | Ejemplos |
|------|---------|----------|
| No terminales | Mayúsculas, opcional `'` | `S`, `A`, `B'` |
| Terminales | Minúsculas o dígitos | `a`, `b`, `2` |
| Cadena vacía | `ε`, `λ` o línea vacía | `S -> ε` |

## Modo validar (opción 1)

Ingresa el símbolo inicial y las producciones una a una. El programa indica cuáles cumplen FNG.

### Ejemplo de salida

```text
=== Forma Normal de Greibach ===

¿Cuántas producciones desea ingresar?: 3

Producción #1
Variable: S
Producción: aA

Producción #2
Variable: A
Producción: bBC

Producción #3
Variable: B
Producción: AB

--- Verificación FNG ---

S -> aA  ✔ Válida
A -> bBC  ✔ Válida
B -> AB  ✘ No válida
```

## Modo convertir (opción 2)

Además del símbolo inicial y las producciones, puedes indicar el **orden de no terminales** (separados por coma). Si lo dejas vacío, se infiere del orden de entrada y se insertan auxiliares (`B''`) antes de su variable base.

La gramática resultante se muestra **después de cada paso**, útil para exposiciones.

## Uso programático

```python
from FNG import GreibachGrammar

grammar = GreibachGrammar(start_symbol="A")
grammar.add_production("A", "CB2")
grammar.add_production("C", "2")

grammar.to_greibach_normal_form(order=["C", "A"], verbose=True)
print(grammar.is_greibach())  # True
```

### API principal

| Método | Descripción |
|--------|-------------|
| `add_production(variable, production)` | Agrega una regla |
| `check_greibach()` | Imprime validación por producción |
| `is_greibach()` | Devuelve `True` si toda la gramática cumple FNG |
| `to_greibach_normal_form(order, verbose)` | Ejecuta la conversión completa |
| `clean()` | Limpieza completa (ε, no generadores, inalcanzables) |

## Pruebas

```bash
python3 -m unittest test_fng.py -v
```

## Referencia

Material del curso: *Forma Normal de Greibach (FNG)* — UTP 2026-I.
