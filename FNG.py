"""Conversión básica a Forma Normal de Greibach (FNG)."""


class GreibachGrammar:
    """Representa una gramática y verifica producciones en FNG."""

    def __init__(self) -> None:
        self.productions = {}

    def add_production(self, variable: str, production: str) -> None:
        """
        Agrega una producción a la gramática.

        Ejemplo:
            S -> aA
        """
        if variable not in self.productions:
            self.productions[variable] = []

        self.productions[variable].append(production)

    def _is_terminal(self, symbol: str) -> bool:
        """
        Verifica si un símbolo es terminal.
        Convención:
            minúsculas = terminales
            mayúsculas = variables
        """
        return symbol.islower()

    def _validate_production(self, production: str) -> bool:
        """
        Verifica si una producción cumple FNG.

        Debe:
            comenzar con terminal
            seguido opcionalmente por variables.
        """

        if not production:
            return False

        # Primer símbolo debe ser terminal
        if not self._is_terminal(production[0]):
            return False

        # Los demás deben ser variables
        for symbol in production[1:]:
            if not symbol.isupper():
                return False

        return True

    def check_greibach(self) -> None:
        """Muestra si las producciones cumplen FNG."""

        print("\n--- Verificación FNG ---\n")

        for variable, rules in self.productions.items():

            for rule in rules:

                if self._validate_production(rule):
                    print(f"{variable} -> {rule}  ✔ Válida")
                else:
                    print(f"{variable} -> {rule}  ✘ No válida")

    def show_grammar(self) -> None:
        """Muestra la gramática completa."""

        print("\nGramática actual:\n")

        for variable, rules in self.productions.items():

            joined_rules = " | ".join(rules)
            print(f"{variable} -> {joined_rules}")


def interactive_session() -> None:
    """Permite ingresar una gramática desde terminal."""

    print("=== Forma Normal de Greibach ===\n")

    grammar = GreibachGrammar()

    try:

        total = int(input("¿Cuántas producciones desea ingresar?: "))

        for i in range(total):

            print(f"\nProducción #{i+1}")

            variable = input("Variable: ").strip().upper()

            production = input(
                "Producción (ejemplo: aAB): "
            ).strip()

            grammar.add_production(variable, production)

    except ValueError:
        print("Error: entrada inválida.")
        return

    grammar.show_grammar()
    grammar.check_greibach()


def main() -> None:
    interactive_session()
    print("\nFin del programa.")


if __name__ == "__main__":
    main()
