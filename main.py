
from src.LexicalAnalyzer import LexicalAnalyzer

if __name__ == "__main__":
    lexer = LexicalAnalyzer("data/main.mjava")
    tokens = lexer.tokenize("data/tokens.json")
    print("\nTOKENS:")
    for token in tokens:
        line = token.attributes["line"]
        column = token.attributes["column"]
        print(
            f"{token.type:<15} {token.text!r:<20} "
            f"line={line}, column={column}"
        )
    print("\nSYMBOL TABLE:")
    for name, entry in lexer.symbol_table.symbols.items():
        print(name, entry.occurrences)
    print("\nLEXICAL ERRORS:")
    for error in lexer.errors:
        print(error)
