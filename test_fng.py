"""Pruebas para conversión y validación FNG."""

import unittest

from FNG import GreibachGrammar, build_demo_grammar


class ValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar = GreibachGrammar(start_symbol="S")

    def test_readme_valid_productions(self) -> None:
        self.grammar.add_production("S", "aA")
        self.grammar.add_production("A", "bBC")
        self.grammar.add_production("B", "c")
        self.assertTrue(self.grammar._validate_production("S", self.grammar._tokenize("aA")))
        self.assertTrue(self.grammar._validate_production("A", self.grammar._tokenize("bBC")))
        self.assertTrue(self.grammar._validate_production("B", self.grammar._tokenize("c")))

    def test_readme_invalid_productions(self) -> None:
        self.assertFalse(self.grammar._validate_production("S", self.grammar._tokenize("AB")))
        self.assertFalse(self.grammar._validate_production("A", self.grammar._tokenize("Ba")))

    def test_start_symbol_epsilon_allowed(self) -> None:
        self.assertTrue(self.grammar._validate_production("S", []))
        self.assertFalse(self.grammar._validate_production("A", []))

    def test_numeric_terminals(self) -> None:
        self.assertTrue(self.grammar._validate_production("A", self.grammar._tokenize("2BC")))
        self.assertFalse(self.grammar._validate_production("A", self.grammar._tokenize("2B2")))

    def test_single_terminal_production(self) -> None:
        self.assertTrue(self.grammar._validate_production("S", self.grammar._tokenize("a")))

    def test_prime_nonterminal(self) -> None:
        self.assertTrue(self.grammar._validate_production("B'", self.grammar._tokenize("2B'")))

    def test_check_greibach_mixed_grammar(self) -> None:
        grammar = GreibachGrammar(start_symbol="S")
        grammar.add_production("S", "aA")
        grammar.add_production("A", "bBC")
        grammar.add_production("B", "AB")
        self.assertFalse(grammar.is_greibach())


class ConversionTests(unittest.TestCase):
    def test_left_recursion_elimination(self) -> None:
        grammar = GreibachGrammar(start_symbol="S")
        grammar.add_production("S", "Sa")
        grammar.add_production("S", "a")
        grammar.eliminate_left_recursion()

        self.assertIn("S'", grammar.productions)
        self.assertIn(["a", "S'"], grammar.productions["S"])
        self.assertIn(["a", "S'"], grammar.productions["S'"])
        self.assertIn([], grammar.productions["S'"])

    def test_substitution_makes_rules_start_with_terminal(self) -> None:
        grammar = GreibachGrammar(start_symbol="S")
        grammar.add_production("S", "AB")
        grammar.add_production("A", "a")
        grammar.add_production("B", "b")
        grammar.substitute_ordered(["A", "B", "S"])

        self.assertIn(["a", "B"], grammar.productions["S"])
        for rule in grammar.productions["S"]:
            self.assertTrue(grammar._is_terminal(rule[0]))

    def test_internal_terminal_elimination(self) -> None:
        grammar = GreibachGrammar(start_symbol="A")
        grammar.add_production("A", "2B2")
        grammar.add_production("C", "2")
        grammar.eliminate_internal_terminals()

        for rule in grammar.productions["A"]:
            self.assertTrue(grammar._validate_production("A", rule, start_symbol="A"))

    def test_full_conversion_demo(self) -> None:
        grammar = build_demo_grammar()
        grammar.to_greibach_normal_form(order=["C", "B", "B'", "A"])
        self.assertTrue(grammar.is_greibach())

    def test_idempotent_conversion(self) -> None:
        grammar = build_demo_grammar()
        order = ["C", "B", "B'", "A"]
        grammar.to_greibach_normal_form(order=order)
        first = grammar.copy()
        grammar.to_greibach_normal_form(order=order)
        self.assertEqual(first.productions, grammar.productions)

    def test_substitution_example_from_pdf(self) -> None:
        grammar = GreibachGrammar(start_symbol="A")
        grammar.add_production("A", "CB2")
        grammar.add_production("C", "2")
        grammar.substitute_ordered(["C", "A"])

        self.assertIn(["2", "B", "2"], grammar.productions["A"])


class CleanTests(unittest.TestCase):
    def test_remove_unreachable_symbols(self) -> None:
        grammar = GreibachGrammar(start_symbol="S")
        grammar.add_production("S", "a")
        grammar.add_production("X", "b")
        grammar.clean()
        self.assertNotIn("X", grammar.productions)

    def test_remove_non_generating_symbols(self) -> None:
        grammar = GreibachGrammar(start_symbol="S")
        grammar.add_production("S", "A")
        grammar.add_production("A", "B")
        grammar.add_production("B", "b")
        grammar.clean()
        self.assertIn("S", grammar.productions)
        self.assertIn("B", grammar.productions)


if __name__ == "__main__":
    unittest.main()
