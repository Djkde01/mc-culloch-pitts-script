# Forma Normal de Greibach (FNG)

Este es un proyecto en Python que verifica producciones de una gramática formal utilizando la **Forma Normal de Greibach (FNG)**.

---

# Descripción

Este programa permite:

* Ingresar producciones de una gramática por terminal.
* Validar si las producciones cumplen la teoría de la Forma Normal de Greibach.
* Mostrar qué producciones son válidas o inválidas.
* Comprender cómo modelar gramáticas formales mediante programación orientada a objetos.

---

# ¿Qué es la Forma Normal de Greibach?

Una gramática está en Forma Normal de Greibach si todas sus producciones tienen la forma:

```text id="1z5f6w"
A → aα
```

Donde:

* `A` = variable o no terminal.
* `a` = terminal.
* `α` = secuencia de variables.

---

# Ejemplos

## Producciones válidas

```text id="1j0v6x"
S -> aA
A -> bBC
B -> c
```

## Producciones inválidas

```text id="c5du8u"
S -> AB
A -> Ba
```

---

# Cómo ejecutar el proyecto

## 1. Clonar el repositorio

```bash id="gk11ml"
git clone https://github.com/Djkde01/forma-normal-greibach.git
```

---

## 2. Entrar a la carpeta

```bash id="sgv13m"
cd forma-normal-greibach
```

---

## 3. Ejecutar el programa

```bash id="4k7ggv"
python forma_normal_greibach.py
```

---

# Ejemplo de ejecución

```text id="t1x9ib"
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

Gramática actual:

S -> aA
A -> bBC
B -> AB

--- Verificación FNG ---

S -> aA ✔ Válida
A -> bBC ✔ Válida
B -> AB ✘ No válida
```

---

# Explicación del código

El proyecto incluye un archivo adicional:

```text id="2lbqdb"
explicacion_forma_normal_greibach.md
```

que contiene:

* explicación teórica.
* análisis del código.
* relación entre teoría y programación.

---

# Conceptos implementados

| Concepto teórico | Implementación                  |
| ---------------- | ------------------------------- |
| Variables        | Letras mayúsculas               |
| Terminales       | Letras minúsculas               |
| Producciones     | Strings                         |
| Validación FNG   | Método `_validate_production()` |
| Gramática        | Diccionario                     |
