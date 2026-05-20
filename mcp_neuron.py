"""Neurona de McCulloch-Pitts: implementación por terminal."""


class McCullochPittsNeuron:
    """Neurona MCP sin sesgo ni aprendizaje."""

    def __init__(self, weights: list[int], threshold: int) -> None:
        self.weights = weights
        self.threshold = threshold

    def _validate_inputs(self, inputs: list[int]) -> None:
        if len(inputs) != len(self.weights):
            raise ValueError(
                f"La longitud de las entradas ({len(inputs)}) "
                f"no coincide con la de los pesos ({len(self.weights)})."
            )
        for i, value in enumerate(inputs):
            if value not in (0, 1):
                raise ValueError(
                    f"Entrada no binaria en posición {i}: {value}. "
                    "Solo se permiten 0 y 1."
                )

    def _step(self, activation: int) -> int:
        return 1 if activation >= self.threshold else 0

    def predict(self, inputs: list[int]) -> int:
        self._validate_inputs(inputs)
        activation = sum(w * x for w, x in zip(self.weights, inputs))
        return self._step(activation)


def demo_and_gate() -> None:
    """Demuestra la compuerta lógica AND de 2 entradas."""
    print("--- Demo: compuerta lógica AND (2 entradas) ---")
    print("Pesos: [1, 1]  |  Umbral: 2\n")

    neuron = McCullochPittsNeuron(weights=[1, 1], threshold=2)
    combinations = [(0, 0), (0, 1), (1, 0), (1, 1)]

    for x1, x2 in combinations:
        inputs = [x1, x2]
        output = neuron.predict(inputs)
        activation = sum(w * x for w, x in zip(neuron.weights, inputs))
        print(f"Entrada {inputs}  |  Suma: {activation}  |  Salida: {output}")

    print()


def _parse_int_list(line: str) -> list[int]:
    parts = line.strip().split()
    if not parts:
        raise ValueError("Debe ingresar al menos un valor.")
    return [int(part) for part in parts]


def _parse_binary_vector(line: str, expected_len: int) -> list[int]:
    values = _parse_int_list(line)
    if len(values) != expected_len:
        raise ValueError(
            f"Se esperaban {expected_len} entradas binarias, se recibieron {len(values)}."
        )
    for i, value in enumerate(values):
        if value not in (0, 1):
            raise ValueError(
                f"Entrada no binaria en posición {i}: {value}. Solo se permiten 0 y 1."
            )
    return values


def interactive_session() -> None:
    """Permite configurar una neurona y probar entradas por terminal."""
    print("--- Modo interactivo ---\n")

    try:
        weights_line = input("Ingrese los pesos (enteros separados por espacio): ")
        weights = _parse_int_list(weights_line)

        threshold_line = input("Ingrese el umbral (entero): ")
        threshold = int(threshold_line.strip())
    except ValueError as exc:
        print(f"Error de configuración: {exc}")
        return

    neuron = McCullochPittsNeuron(weights=weights, threshold=threshold)
    print(f"\nNeurona configurada: pesos={neuron.weights}, umbral={neuron.threshold}")
    print(
        f"Ingrese {len(weights)} entradas binarias (0 o 1) separadas por espacio."
    )
    print("Línea vacía o 'salir' para terminar.\n")

    while True:
        line = input("Entradas> ").strip()
        if not line or line.lower() == "salir":
            break

        try:
            inputs = _parse_binary_vector(line, len(weights))
            activation = sum(w * x for w, x in zip(neuron.weights, inputs))
            output = neuron.predict(inputs)
            print(f"  Suma: {activation}  |  Salida: {output}\n")
        except ValueError as exc:
            print(f"  Error: {exc}\n")


def main() -> None:
    print("=== Neurona McCulloch-Pitts ===\n")
    demo_and_gate()

    answer = input("¿Desea probar otra neurona? (s/n): ").strip().lower()
    if answer in ("s", "si", "sí", "y", "yes"):
        interactive_session()

    print("Fin del programa.")


if __name__ == "__main__":
    main()
