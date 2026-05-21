"""Pruebas para mcp_neuron.py."""

import unittest

from mcp_neuron import (
    ACTIVATION_SIGMOID,
    GATE_PRESETS,
    ExtendedNeuron,
    McCullochPittsNeuron,
    MCPNetwork,
    sigmoid,
    xor_network_predict,
)


def _truth_tables_2() -> list[tuple[list[int], str]]:
    return [
        ([0, 0], "00"),
        ([0, 1], "01"),
        ([1, 0], "10"),
        ([1, 1], "11"),
    ]


class TestMcCullochPittsNeuron(unittest.TestCase):
    def test_and_gate(self) -> None:
        neuron = McCullochPittsNeuron([1, 1], 2)
        expected = {"00": 0, "01": 0, "10": 0, "11": 1}
        for inputs, key in _truth_tables_2():
            with self.subTest(inputs=inputs):
                self.assertEqual(neuron.predict(inputs), expected[key])

    def test_or_gate(self) -> None:
        neuron = McCullochPittsNeuron([1, 1], 1)
        expected = {"00": 0, "01": 1, "10": 1, "11": 1}
        for inputs, key in _truth_tables_2():
            with self.subTest(inputs=inputs):
                self.assertEqual(neuron.predict(inputs), expected[key])

    def test_andnot_gate(self) -> None:
        neuron = McCullochPittsNeuron([1, -1], 1)
        expected = {"00": 0, "01": 0, "10": 1, "11": 0}
        for inputs, key in _truth_tables_2():
            with self.subTest(inputs=inputs):
                self.assertEqual(neuron.predict(inputs), expected[key])

    def test_not_x1(self) -> None:
        neuron = McCullochPittsNeuron([-1, 0], 0)
        expected = {"00": 1, "01": 1, "10": 0, "11": 0}
        for inputs, key in _truth_tables_2():
            with self.subTest(inputs=inputs):
                self.assertEqual(neuron.predict(inputs), expected[key])

    def test_invalid_binary_input(self) -> None:
        neuron = McCullochPittsNeuron([1, 1], 1)
        with self.assertRaises(ValueError):
            neuron.predict([0, 2])

    def test_length_mismatch(self) -> None:
        neuron = McCullochPittsNeuron([1, 1], 1)
        with self.assertRaises(ValueError):
            neuron.predict([1])


class TestXORNetwork(unittest.TestCase):
    def test_xor_truth_table(self) -> None:
        expected = {"00": 0, "01": 1, "10": 1, "11": 0}
        network = MCPNetwork()
        for inputs, key in _truth_tables_2():
            with self.subTest(inputs=inputs):
                out, hidden = network.forward(inputs)
                self.assertEqual(out, expected[key])
                self.assertEqual(xor_network_predict(inputs), expected[key])
                self.assertIsInstance(hidden, tuple)

    def test_xor_preset_flag(self) -> None:
        self.assertTrue(GATE_PRESETS["XOR"].use_xor_network)


class TestExtendedNeuron(unittest.TestCase):
    def test_sigmoid_monotonic(self) -> None:
        self.assertLess(sigmoid(-5), sigmoid(0))
        self.assertLess(sigmoid(0), sigmoid(5))

    def test_extended_matches_mcp_presets(self) -> None:
        for name in ("AND", "OR", "NOT", "ANDNOT"):
            preset = GATE_PRESETS[name]
            mcp = preset.mcp_neuron()
            ext = preset.extended_neuron(ACTIVATION_SIGMOID)
            for inputs, _ in _truth_tables_2():
                with self.subTest(gate=name, inputs=inputs):
                    mcp_out = mcp.predict(inputs)
                    ext_out = ext.predict_binary([float(x) for x in inputs])
                    self.assertEqual(mcp_out, ext_out)

    def test_activate_returns_z_and_y(self) -> None:
        neuron = ExtendedNeuron([1.0, 1.0], -2.0, activation=ACTIVATION_SIGMOID)
        z, y = neuron.activate([1.0, 1.0])
        self.assertEqual(z, 0.0)
        self.assertAlmostEqual(y, 0.5, places=5)


class TestGatePresets(unittest.TestCase):
    def test_all_presets_defined(self) -> None:
        self.assertEqual(
            set(GATE_PRESETS.keys()), {"AND", "OR", "NOT", "ANDNOT", "XOR"}
        )


if __name__ == "__main__":
    unittest.main()
