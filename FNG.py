"""Conversión y validación de gramáticas en Forma Normal de Greibach (FNG)."""

from __future__ import annotations

import copy
import re
from typing import Optional


EPSILON_ALIASES = frozenset({"ε", "λ", "epsilon", "e"})


class GreibachGrammar:
    """Representa una gramática libre de contexto y la convierte a FNG."""

    def __init__(self, start_symbol: str = "S") -> None:
        self.start_symbol = start_symbol
        self.productions: dict[str, list[list[str]]] = {}

    # ------------------------------------------------------------------
    # Entrada / salida
    # ------------------------------------------------------------------

    def add_production(self, variable: str, production: str) -> None:
        """Agrega una producción (p. ej. variable ``S``, producción ``aA``)."""
        variable = variable.strip()
        if variable not in self.productions:
            self.productions[variable] = []
        self.productions[variable].append(self._tokenize(production))

    def copy(self) -> GreibachGrammar:
        """Devuelve una copia profunda de la gramática."""
        other = GreibachGrammar(self.start_symbol)
        other.productions = copy.deepcopy(self.productions)
        return other

    def _format_rhs(self, rhs: list[str]) -> str:
        if not rhs:
            return "ε"
        return "".join(rhs)

    def show_grammar(self, title: str = "Gramática actual") -> None:
        """Muestra la gramática completa."""
        print(f"\n{title}:\n")
        for variable in self._sorted_nonterminals():
            rules = self.productions.get(variable, [])
            if not rules:
                continue
            joined = " | ".join(self._format_rhs(rule) for rule in rules)
            print(f"{variable} -> {joined}")

    # ------------------------------------------------------------------
    # Tokenización y clasificación de símbolos
    # ------------------------------------------------------------------

    def _tokenize(self, production: str) -> list[str]:
        text = production.strip()
        if text.lower() in EPSILON_ALIASES:
            return []

        tokens: list[str] = []
        index = 0
        while index < len(text):
            char = text[index]
            if char.isspace():
                index += 1
                continue
            if char.isupper():
                token = char
                index += 1
                if index < len(text) and text[index] == "'":
                    token += "'"
                    index += 1
                tokens.append(token)
                continue
            tokens.append(char)
            index += 1
        return tokens

    @staticmethod
    def _is_nonterminal(token: str) -> bool:
        return bool(re.fullmatch(r"[A-Z][A-Z0-9']*", token))

    @staticmethod
    def _is_terminal(token: str) -> bool:
        return bool(token) and not GreibachGrammar._is_nonterminal(token)

    def _symbols_in_rhs(self, rhs: list[str]) -> list[str]:
        return list(rhs)

    def _dedupe(self, rules: list[list[str]]) -> list[list[str]]:
        seen: set[tuple[str, ...]] = set()
        unique: list[list[str]] = []
        for rule in rules:
            key = tuple(rule)
            if key not in seen:
                seen.add(key)
                unique.append(rule)
        return unique

    def _sorted_nonterminals(self) -> list[str]:
        return sorted(self.productions.keys())

    def _default_order(self) -> list[str]:
        order: list[str] = []
        if self.start_symbol in self.productions:
            order.append(self.start_symbol)
        for nt in self._sorted_nonterminals():
            if nt not in order:
                order.append(nt)
        return order

    def _fresh_nonterminal(self, hint: str = "T") -> str:
        base = "T" if not hint else hint[0].upper()
        candidate = base
        suffix = 1
        while candidate in self.productions:
            candidate = f"{base}{suffix}"
            suffix += 1
        return candidate

    # ------------------------------------------------------------------
    # Validación FNG
    # ------------------------------------------------------------------

    def _validate_production(
        self, variable: str, rhs: list[str], start_symbol: Optional[str] = None
    ) -> bool:
        start = start_symbol or self.start_symbol
        if not rhs:
            return variable == start

        if not self._is_terminal(rhs[0]):
            return False

        return all(self._is_nonterminal(token) for token in rhs[1:])

    def is_greibach(self) -> bool:
        """Indica si todas las producciones cumplen FNG."""
        for variable, rules in self.productions.items():
            for rule in rules:
                if not self._validate_production(variable, rule):
                    return False
        return True

    def check_greibach(self) -> None:
        """Muestra si las producciones cumplen FNG."""
        print("\n--- Verificación FNG ---\n")
        for variable in self._sorted_nonterminals():
            for rule in self.productions.get(variable, []):
                formatted = self._format_rhs(rule)
                if self._validate_production(variable, rule):
                    print(f"{variable} -> {formatted}  ✔ Válida")
                else:
                    print(f"{variable} -> {formatted}  ✘ No válida")

    # ------------------------------------------------------------------
    # Paso 1: limpieza
    # ------------------------------------------------------------------

    def _nullable_symbols(self) -> set[str]:
        nullable: set[str] = set()
        changed = True
        while changed:
            changed = False
            for variable, rules in self.productions.items():
                if variable in nullable:
                    continue
                for rhs in rules:
                    if not rhs or all(
                        (self._is_nonterminal(sym) and sym in nullable)
                        or (not self._is_nonterminal(sym))
                        for sym in rhs
                    ):
                        if not rhs or all(
                            self._is_nonterminal(sym) and sym in nullable for sym in rhs
                        ):
                            nullable.add(variable)
                            changed = True
                            break
        return nullable

    def _remove_epsilon_productions(self) -> None:
        nullable = self._nullable_symbols()
        new_productions: dict[str, list[list[str]]] = {}

        for variable, rules in self.productions.items():
            expanded: list[list[str]] = []
            for rhs in rules:
                if not rhs:
                    if variable == self.start_symbol:
                        expanded.append([])
                    continue

                nullable_positions = [
                    index
                    for index, sym in enumerate(rhs)
                    if self._is_nonterminal(sym) and sym in nullable
                ]
                if not nullable_positions:
                    expanded.append(rhs)
                    continue

                count = 1 << len(nullable_positions)
                for mask in range(count):
                    new_rhs = list(rhs)
                    drop = [
                        nullable_positions[bit]
                        for bit in range(len(nullable_positions))
                        if mask & (1 << bit)
                    ]
                    for position in sorted(drop, reverse=True):
                        del new_rhs[position]
                    if new_rhs or variable == self.start_symbol:
                        expanded.append(new_rhs)

            if expanded:
                new_productions[variable] = self._dedupe(expanded)

        self.productions = new_productions

    def _generating_symbols(self) -> set[str]:
        generating: set[str] = set()
        changed = True
        while changed:
            changed = False
            for variable, rules in self.productions.items():
                if variable in generating:
                    continue
                for rhs in rules:
                    if all(
                        self._is_terminal(sym)
                        or (self._is_nonterminal(sym) and sym in generating)
                        for sym in rhs
                    ):
                        generating.add(variable)
                        changed = True
                        break
        return generating

    def _reachable_symbols(self) -> set[str]:
        if self.start_symbol not in self.productions:
            return set()
        reachable = {self.start_symbol}
        changed = True
        while changed:
            changed = False
            for variable in list(reachable):
                for rhs in self.productions.get(variable, []):
                    for sym in rhs:
                        if self._is_nonterminal(sym) and sym not in reachable:
                            reachable.add(sym)
                            changed = True
        return reachable

    def remove_epsilon(self) -> GreibachGrammar:
        """Elimina producciones ε excepto en el símbolo inicial."""
        self._remove_epsilon_productions()
        return self

    def remove_epsilon_from_auxiliaries(self) -> GreibachGrammar:
        """Elimina ε en no terminales distintos del símbolo inicial."""
        for variable, rules in self.productions.items():
            if variable == self.start_symbol:
                continue
            self.productions[variable] = [rule for rule in rules if rule]
        return self

    def remove_unreachable(self) -> GreibachGrammar:
        """Elimina no terminales inalcanzables desde el símbolo inicial."""
        reachable = self._reachable_symbols()
        self.productions = {
            variable: rules
            for variable, rules in self.productions.items()
            if variable in reachable
        }

        for variable in list(self.productions.keys()):
            self.productions[variable] = self._dedupe(
                [
                    [
                        sym
                        for sym in rhs
                        if self._is_terminal(sym)
                        or (self._is_nonterminal(sym) and sym in reachable)
                    ]
                    for rhs in self.productions[variable]
                ]
            )

        return self

    def clean(self) -> GreibachGrammar:
        """Elimina símbolos no generadores e inalcanzables."""
        self._remove_epsilon_productions()

        generating = self._generating_symbols()
        self.productions = {
            variable: rules
            for variable, rules in self.productions.items()
            if variable in generating
        }

        for variable in list(self.productions.keys()):
            self.productions[variable] = self._dedupe(
                [
                    [
                        sym
                        for sym in rhs
                        if self._is_terminal(sym)
                        or (self._is_nonterminal(sym) and sym in generating)
                    ]
                    for rhs in self.productions[variable]
                ]
            )

        reachable = self._reachable_symbols()
        self.productions = {
            variable: rules
            for variable, rules in self.productions.items()
            if variable in reachable
        }

        for variable in list(self.productions.keys()):
            self.productions[variable] = self._dedupe(
                [
                    [
                        sym
                        for sym in rhs
                        if self._is_terminal(sym)
                        or (self._is_nonterminal(sym) and sym in reachable)
                    ]
                    for rhs in self.productions[variable]
                ]
            )

        return self

    # ------------------------------------------------------------------
    # Paso 2: recursividad izquierda
    # ------------------------------------------------------------------

    def eliminate_left_recursion(self) -> GreibachGrammar:
        """Elimina recursividad izquierda directa en cada no terminal."""
        ordered = self._default_order()
        for variable in ordered:
            if variable not in self.productions:
                continue

            alpha_rules: list[list[str]] = []
            beta_rules: list[list[str]] = []

            for rhs in self.productions[variable]:
                if rhs and rhs[0] == variable:
                    alpha_rules.append(rhs[1:])
                else:
                    beta_rules.append(rhs)

            if not alpha_rules:
                continue

            prime = variable + "'"
            while prime in self.productions:
                prime += "'"

            if beta_rules:
                self.productions[variable] = [beta + [prime] for beta in beta_rules]
            else:
                self.productions[variable] = [[prime]]
            self.productions[prime] = [alpha + [prime] for alpha in alpha_rules] + [[]]

        return self

    # ------------------------------------------------------------------
    # Paso 3: sustitución ordenada
    # ------------------------------------------------------------------

    def _build_conversion_order(self, preferred: Optional[list[str]] = None) -> list[str]:
        order = list(preferred) if preferred else self._default_order()
        for nt in self._sorted_nonterminals():
            if nt in order:
                continue
            base = nt.replace("'", "")
            inserted = False
            for index, existing in enumerate(order):
                if existing.replace("'", "") == base:
                    order.insert(index, nt)
                    inserted = True
                    break
            if not inserted:
                order.append(nt)
        return order

    def substitute_ordered(self, order: Optional[list[str]] = None) -> GreibachGrammar:
        """Sustituye no terminales iniciales según el orden dado."""
        order = self._build_conversion_order(order)

        changed = True
        while changed:
            changed = False
            for index, ai in enumerate(order):
                if ai not in self.productions:
                    continue
                for prior in order[:index]:
                    if prior not in self.productions:
                        continue
                    updated: list[list[str]] = []
                    for rhs in self.productions[ai]:
                        if rhs and rhs[0] == prior:
                            for delta in self.productions[prior]:
                                updated.append(delta + rhs[1:])
                            changed = True
                        else:
                            updated.append(rhs)
                    deduped = self._dedupe(updated)
                    if deduped != self.productions[ai]:
                        self.productions[ai] = deduped
                        changed = True

        return self

    # ------------------------------------------------------------------
    # Paso 4: terminales internos
    # ------------------------------------------------------------------

    def _terminal_producers(self) -> dict[str, str]:
        mapping: dict[str, str] = {}
        for variable, rules in self.productions.items():
            for rhs in rules:
                if len(rhs) == 1 and self._is_terminal(rhs[0]):
                    terminal = rhs[0]
                    if terminal not in mapping:
                        mapping[terminal] = variable
        return mapping

    def eliminate_internal_terminals(self) -> GreibachGrammar:
        """Reemplaza terminales en posiciones internas por no terminales."""
        term_to_nt = self._terminal_producers()

        changed = True
        while changed:
            changed = False
            for variable in list(self.productions.keys()):
                updated: list[list[str]] = []
                for rhs in self.productions[variable]:
                    if len(rhs) <= 1:
                        updated.append(rhs)
                        continue

                    new_rhs = list(rhs)
                    for index in range(1, len(new_rhs)):
                        token = new_rhs[index]
                        if not self._is_terminal(token):
                            continue
                        if token not in term_to_nt:
                            fresh = self._fresh_nonterminal(token)
                            self.productions[fresh] = [[token]]
                            term_to_nt[token] = fresh
                            changed = True
                        new_rhs[index] = term_to_nt[token]
                        changed = True
                    updated.append(new_rhs)

                self.productions[variable] = self._dedupe(updated)

        return self

    # ------------------------------------------------------------------
    # Orquestador
    # ------------------------------------------------------------------

    def to_greibach_normal_form(
        self,
        order: Optional[list[str]] = None,
        verbose: bool = False,
    ) -> GreibachGrammar:
        """Ejecuta los pasos de conversión a FNG."""
        if self.is_greibach():
            if verbose:
                self.show_grammar("Gramática ya en FNG")
            return self

        steps = [
            ("Paso 1: eliminar producciones ε", self.remove_epsilon),
            ("Paso 2: eliminar recursividad izquierda", self.eliminate_left_recursion),
            (
                "Paso 3: eliminar ε en auxiliares",
                self.remove_epsilon_from_auxiliaries,
            ),
            ("Paso 4: eliminar símbolos inalcanzables", self.remove_unreachable),
            (
                "Paso 5: sustitución ordenada",
                lambda: self.substitute_ordered(order),
            ),
            ("Paso 6: eliminar terminales internos", self.eliminate_internal_terminals),
            (
                "Paso 7: sustitución final",
                lambda: self.substitute_ordered(order),
            ),
        ]

        for title, action in steps:
            action()
            if verbose:
                self.show_grammar(title)

        return self


# ----------------------------------------------------------------------
# Ejemplos y sesión interactiva
# ----------------------------------------------------------------------


def build_demo_grammar() -> GreibachGrammar:
    """Gramática de ejemplo alineada al material del curso."""
    grammar = GreibachGrammar(start_symbol="A")
    grammar.add_production("A", "CB2")
    grammar.add_production("B", "BC")
    grammar.add_production("B'", "CB'")
    grammar.add_production("C", "2")
    return grammar


def read_grammar_from_input(start_symbol: str = "S") -> Optional[GreibachGrammar]:
    """Lee producciones desde la terminal."""
    grammar = GreibachGrammar(start_symbol=start_symbol)
    try:
        total = int(input("¿Cuántas producciones desea ingresar?: "))
    except ValueError:
        print("Error: entrada inválida.")
        return None

    for index in range(total):
        print(f"\nProducción #{index + 1}")
        variable = input("Variable: ").strip()
        production = input("Producción (ejemplo: aAB o ε): ").strip()
        grammar.add_production(variable, production)

    return grammar


def interactive_validate() -> None:
    print("\n=== Validar gramática (FNG) ===\n")
    start = input("Símbolo inicial [S]: ").strip() or "S"
    grammar = read_grammar_from_input(start)
    if grammar is None:
        return
    grammar.show_grammar()
    grammar.check_greibach()


def interactive_convert() -> None:
    print("\n=== Convertir a FNG ===\n")
    start = input("Símbolo inicial [S]: ").strip() or "S"
    grammar = read_grammar_from_input(start)
    if grammar is None:
        return

    order_input = input(
        "Orden de no terminales (separados por coma, Enter = automático): "
    ).strip()
    order = (
        [item.strip() for item in order_input.split(",") if item.strip()]
        if order_input
        else None
    )

    print("\n--- Gramática original ---")
    grammar.show_grammar()
    grammar.to_greibach_normal_form(order=order, verbose=True)
    grammar.check_greibach()


def run_demo() -> None:
    print("\n=== Demo: conversión paso a paso ===\n")
    grammar = build_demo_grammar()
    grammar.show_grammar("Gramática original")
    grammar.to_greibach_normal_form(order=["C", "B", "B'", "A"], verbose=True)
    grammar.check_greibach()


def main() -> None:
    print("=== Forma Normal de Greibach (FNG) ===\n")
    print("1. Validar gramática")
    print("2. Convertir a FNG")
    print("3. Demo con ejemplo del curso")

    choice = input("\nOpción [1]: ").strip() or "1"

    if choice == "2":
        interactive_convert()
    elif choice == "3":
        run_demo()
    else:
        interactive_validate()

    print("\nFin del programa.")


if __name__ == "__main__":
    main()
