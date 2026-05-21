"""Autómata McCulloch-Pitts y neurona extendida: implementación por terminal."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

# --- Activaciones ---

ACTIVATION_STEP = "step"
ACTIVATION_SIGMOID = "sigmoid"


def sigmoid(z: float) -> float:
    """Función sigmoide: 1 / (1 + e^-z)."""
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    exp_z = math.exp(z)
    return exp_z / (1.0 + exp_z)


def step_activation(z: float) -> float:
    """Escalón sobre z (dispara si z >= 0)."""
    return 1.0 if z >= 0.0 else 0.0


def get_activation_fn(name: str) -> Callable[[float], float]:
    if name == ACTIVATION_SIGMOID:
        return sigmoid
    if name == ACTIVATION_STEP:
        return step_activation
    raise ValueError(f"Activación desconocida: {name}. Use 'sigmoid' o 'step'.")


# --- MCP clásico ---


class McCullochPittsNeuron:
    """Neurona MCP: entradas binarias, pesos enteros, umbral, salida escalón."""

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

    def sum_activation(self, inputs: list[int]) -> int:
        self._validate_inputs(inputs)
        return sum(w * x for w, x in zip(self.weights, inputs))

    def _step(self, activation: int) -> int:
        return 1 if activation >= self.threshold else 0

    def predict(self, inputs: list[int]) -> int:
        return self._step(self.sum_activation(inputs))


# --- Neurona extendida (sesgo + sigmoide/escalón) ---


class ExtendedNeuron:
    """Neurona con pesos reales, sesgo y activación sigmoide o escalón."""

    def __init__(
        self,
        weights: list[float],
        bias: float,
        activation: str = ACTIVATION_SIGMOID,
    ) -> None:
        self.weights = weights
        self.bias = bias
        self.activation_name = activation
        self._activation_fn = get_activation_fn(activation)

    def _validate_inputs(self, inputs: list[float]) -> None:
        if len(inputs) != len(self.weights):
            raise ValueError(
                f"La longitud de las entradas ({len(inputs)}) "
                f"no coincide con la de los pesos ({len(self.weights)})."
            )

    def activate(self, inputs: list[float]) -> tuple[float, float]:
        """Devuelve (z, y): suma ponderada + sesgo y salida de activación."""
        self._validate_inputs(inputs)
        z = sum(w * x for w, x in zip(self.weights, inputs)) + self.bias
        y = self._activation_fn(z)
        return z, y

    def predict_binary(self, inputs: list[float], threshold: float = 0.5) -> int:
        _, y = self.activate(inputs)
        return 1 if y >= threshold else 0


# --- Red MCP para XOR ---


class MCPNetwork:
    """Red fija de 3 neuronas MCP que implementa XOR."""

    def __init__(self) -> None:
        self.n1 = McCullochPittsNeuron(weights=[1, -1], threshold=1)
        self.n2 = McCullochPittsNeuron(weights=[-1, 1], threshold=1)
        self.n3 = McCullochPittsNeuron(weights=[1, 1], threshold=1)

    def forward(self, inputs: list[int]) -> tuple[int, tuple[int, int]]:
        h1 = self.n1.predict(inputs)
        h2 = self.n2.predict(inputs)
        output = self.n3.predict([h1, h2])
        return output, (h1, h2)


def xor_network_predict(inputs: list[int]) -> int:
    return MCPNetwork().forward(inputs)[0]


# --- Presets de compuertas ---


@dataclass(frozen=True)
class GatePreset:
    name: str
    description: str
    mcp_weights: list[int]
    mcp_threshold: int
    extended_weights: list[float]
    extended_bias: float
    input_count: int = 2
    use_xor_network: bool = False

    def mcp_neuron(self) -> McCullochPittsNeuron:
        return McCullochPittsNeuron(self.mcp_weights, self.mcp_threshold)

    def extended_neuron(self, activation: str = ACTIVATION_SIGMOID) -> ExtendedNeuron:
        return ExtendedNeuron(
            self.extended_weights, self.extended_bias, activation=activation
        )


GATE_PRESETS: dict[str, GatePreset] = {
    "AND": GatePreset(
        name="AND",
        description="x1 AND x2",
        mcp_weights=[1, 1],
        mcp_threshold=2,
        extended_weights=[1.0, 1.0],
        extended_bias=-2.0,
    ),
    "OR": GatePreset(
        name="OR",
        description="x1 OR x2",
        mcp_weights=[1, 1],
        mcp_threshold=1,
        extended_weights=[1.0, 1.0],
        extended_bias=-1.0,
    ),
    "NOT": GatePreset(
        name="NOT",
        description="NOT x1 (x2 ignorada)",
        mcp_weights=[-1, 0],
        mcp_threshold=0,
        extended_weights=[-1.0, 0.0],
        extended_bias=0.0,
    ),
    "ANDNOT": GatePreset(
        name="ANDNOT",
        description="x1 AND NOT x2",
        mcp_weights=[1, -1],
        mcp_threshold=1,
        extended_weights=[1.0, -1.0],
        extended_bias=-1.0,
    ),
    "XOR": GatePreset(
        name="XOR",
        description="x1 XOR x2 (red de 3 neuronas MCP)",
        mcp_weights=[],
        mcp_threshold=0,
        extended_weights=[],
        extended_bias=0.0,
        use_xor_network=True,
    ),
}

BINARY_INPUTS_2 = [(0, 0), (0, 1), (1, 0), (1, 1)]


def _format_inputs(inputs: list[int]) -> str:
    labels = [f"x{i + 1}={v}" for i, v in enumerate(inputs)]
    return ", ".join(labels)


def _truth_table_rows(preset: GatePreset) -> list[list[int]]:
    n = preset.input_count
    if n == 1:
        return [[0], [1]]
    return [[a, b] for a, b in BINARY_INPUTS_2]


def run_gate_demo(name: str, mode: str = "mcp") -> None:
    """Imprime la tabla de verdad de una compuerta."""
    if name not in GATE_PRESETS:
        raise ValueError(f"Compuerta desconocida: {name}")

    preset = GATE_PRESETS[name]
    print(f"--- Compuerta {preset.name}: {preset.description} ---\n")

    if preset.use_xor_network:
        if mode == "mcp":
            _run_xor_demo_mcp()
        else:
            print("XOR en modo extendido usa la red MCP para la lógica binaria.")
            print("La sigmoide se muestra en las neuronas ocultas equivalentes.\n")
            _run_xor_demo_mcp(traced=False)
        return

    if mode == "mcp":
        neuron = preset.mcp_neuron()
        print(f"Pesos: {neuron.weights}  |  Umbral: {neuron.threshold}\n")
        print(f"{'Entradas':<20} | {'Suma':>4} | {'Salida':>6}")
        print("-" * 36)
        for row in _truth_table_rows(preset):
            s = neuron.sum_activation(row)
            out = neuron.predict(row)
            print(f"{_format_inputs(row):<20} | {s:>4} | {out:>6}")
    else:
        neuron = preset.extended_neuron(ACTIVATION_SIGMOID)
        print(
            f"Pesos: {neuron.weights}  |  Sesgo: {neuron.bias}  |  "
            f"Activación: sigmoide\n"
        )
        print(f"{'Entradas':<20} | {'z':>8} | {'y_sig':>8} | {'y_bin':>5}")
        print("-" * 48)
        for row in _truth_table_rows(preset):
            inputs_f = [float(x) for x in row]
            z, y = neuron.activate(inputs_f)
            y_bin = neuron.predict_binary(inputs_f)
            print(
                f"{_format_inputs(row):<20} | {z:>8.4f} | {y:>8.4f} | {y_bin:>5}"
            )
    print()


def _run_xor_demo_mcp(traced: bool = False) -> None:
    network = MCPNetwork()
    print("Red: N1 (x1 AND NOT x2) | N2 (NOT x1 AND x2) | N3 (N1 OR N2)\n")
    print(f"{'Entradas':<20} | {'N1':>3} | {'N2':>3} | {'XOR':>3}")
    print("-" * 36)
    for x1, x2 in BINARY_INPUTS_2:
        inputs = [x1, x2]
        out, (h1, h2) = network.forward(inputs)
        print(
            f"{_format_inputs(inputs):<20} | {h1:>3} | {h2:>3} | {out:>3}"
        )
    print()


def demo_xor_traced() -> None:
    """Tabla XOR con trazado paso a paso de la red."""
    print("--- XOR: red de 3 neuronas MCP ---\n")
    print("Topología:")
    print("  x1, x2 --> N1 [1,-1] θ=1  (x1 AND NOT x2)")
    print("  x1, x2 --> N2 [-1,1] θ=1  (NOT x1 AND x2)")
    print("  N1, N2 --> N3 [1,1]  θ=1  (OR)\n")

    network = MCPNetwork()
    for x1, x2 in BINARY_INPUTS_2:
        inputs = [x1, x2]
        s1 = network.n1.sum_activation(inputs)
        h1 = network.n1.predict(inputs)
        s2 = network.n2.sum_activation(inputs)
        h2 = network.n2.predict(inputs)
        s3 = network.n3.sum_activation([h1, h2])
        out = network.n3.predict([h1, h2])
        print(f"Entrada {_format_inputs(inputs)}")
        print(f"  N1: suma={s1}, umbral={network.n1.threshold} -> {h1}")
        print(f"  N2: suma={s2}, umbral={network.n2.threshold} -> {h2}")
        print(f"  N3: suma={s3}, umbral={network.n3.threshold} -> {out}")
        print(f"  Salida XOR: {out}\n")


def demo_and_gate() -> None:
    """Atajo: demo de la compuerta AND."""
    run_gate_demo("AND", mode="mcp")


def run_all_gate_demos(mode: str = "mcp") -> None:
    for name in ("AND", "OR", "NOT", "ANDNOT", "XOR"):
        run_gate_demo(name, mode=mode)


# --- Parsing y sesiones interactivas ---


def _parse_int_list(line: str) -> list[int]:
    parts = line.strip().split()
    if not parts:
        raise ValueError("Debe ingresar al menos un valor.")
    return [int(part) for part in parts]


def _parse_float_list(line: str) -> list[float]:
    parts = line.strip().split()
    if not parts:
        raise ValueError("Debe ingresar al menos un valor.")
    return [float(part) for part in parts]


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


def interactive_mcp_session() -> None:
    print("--- Neurona MCP (modo clásico) ---\n")
    try:
        weights = _parse_int_list(
            input("Pesos (enteros, ej. 1 1 o 1 -1): ")
        )
        threshold = int(input("Umbral (entero): ").strip())
    except ValueError as exc:
        print(f"Error de configuración: {exc}")
        return

    neuron = McCullochPittsNeuron(weights=weights, threshold=threshold)
    print(f"\nPesos={neuron.weights}, umbral={neuron.threshold}")
    print(f"Ingrese {len(weights)} entradas binarias (0/1). Vacío o 'salir' para terminar.\n")

    while True:
        line = input("Entradas> ").strip()
        if not line or line.lower() == "salir":
            break
        try:
            inputs = _parse_binary_vector(line, len(weights))
            s = neuron.sum_activation(inputs)
            out = neuron.predict(inputs)
            print(f"  {_format_inputs(inputs)} | suma={s} | salida={out}\n")
        except ValueError as exc:
            print(f"  Error: {exc}\n")


def interactive_extended_session() -> None:
    print("--- Neurona extendida (sesgo + activación) ---\n")
    try:
        weights = _parse_float_list(input("Pesos (reales, ej. 1.0 1.0): "))
        bias = float(input("Sesgo (real, ej. -2.0): ").strip())
        act = input("Activación (sigmoid/step) [sigmoid]: ").strip().lower()
        if not act:
            act = ACTIVATION_SIGMOID
        if act in ("escalon", "escalón"):
            act = ACTIVATION_STEP
    except ValueError as exc:
        print(f"Error de configuración: {exc}")
        return

    try:
        neuron = ExtendedNeuron(weights=weights, bias=bias, activation=act)
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    print(
        f"\nPesos={neuron.weights}, sesgo={neuron.bias}, "
        f"activación={neuron.activation_name}"
    )
    print(
        f"Ingrese {len(weights)} entradas (reales o 0/1). Vacío o 'salir' para terminar.\n"
    )

    while True:
        line = input("Entradas> ").strip()
        if not line or line.lower() == "salir":
            break
        try:
            inputs = _parse_float_list(line)
            if len(inputs) != len(weights):
                raise ValueError(
                    f"Se esperaban {len(weights)} entradas, se recibieron {len(inputs)}."
                )
            z, y = neuron.activate(inputs)
            y_bin = neuron.predict_binary(inputs)
            labels = ", ".join(f"x{i + 1}={v}" for i, v in enumerate(inputs))
            print(f"  {labels}")
            print(f"  z={z:.6f} | y={y:.6f} | y_binaria={y_bin}\n")
        except ValueError as exc:
            print(f"  Error: {exc}\n")


def _gate_submenu(mode: str) -> None:
    print("\nCompuertas: 1=AND  2=OR  3=NOT  4=ANDNOT  5=XOR  6=Todas  0=Volver")
    choice = input("Opción: ").strip()
    mapping = {
        "1": "AND",
        "2": "OR",
        "3": "NOT",
        "4": "ANDNOT",
        "5": "XOR",
    }
    if choice == "0":
        return
    if choice == "6":
        run_all_gate_demos(mode=mode)
        return
    if choice in mapping:
        run_gate_demo(mapping[choice], mode=mode)
    else:
        print("Opción no válida.")


def _print_main_menu() -> None:
    print("\n=== Autómata McCulloch-Pitts ===")
    print("1. Demos compuertas (MCP clásico)")
    print("2. Demos compuertas (neurona extendida + sigmoide)")
    print("3. Probar XOR (red de 3 neuronas + trazado)")
    print("4. Configurar neurona MCP manualmente")
    print("5. Configurar neurona extendida manualmente")
    print("0. Salir")


def main() -> None:
    while True:
        _print_main_menu()
        choice = input("\nOpción: ").strip()

        if choice == "0":
            print("Fin del programa.")
            break
        if choice == "1":
            _gate_submenu(mode="mcp")
        elif choice == "2":
            _gate_submenu(mode="extended")
        elif choice == "3":
            demo_xor_traced()
        elif choice == "4":
            interactive_mcp_session()
        elif choice == "5":
            interactive_extended_session()
        else:
            print("Opción no válida. Elija 0-5.")


if __name__ == "__main__":
    main()
