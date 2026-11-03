
from src.LexicalAnalyzer import LexicalAnalyzer
from src.SymbolTable import SymbolTable
from src.Token import Token


def print_tokens(tokens: list[Token]):
  if len(tokens) == 0:
    print("No tokens found")
    return

  for token in tokens:
    line = token.attributes["line"]
    column = token.attributes["column"]
    print(
      f"{token.type:<15} {token.text!r:<20} "
      f"line={line}, column={column}"
    )

def print_symbol_table(symbol_table: SymbolTable):
  for name, entry in symbol_table.symbols.items():
    print(name, entry.occurrences)

def print_errors(errors):
  for error in errors:
    print(error)

if __name__ == "__main__":
  lexer = LexicalAnalyzer("data/main.mjava")
  tokens = lexer.tokenize("data/tokens.json")

  print("TOKENS:")
  print_tokens(tokens)

  if not lexer.symbol_table.is_empty():
    print("\nSYMBOL TABLE:")
    print_symbol_table(lexer.symbol_table)

  if len(lexer.errors) > 0:
    print("\nLEXICAL ERRORS:")
    print_errors(lexer.errors)
