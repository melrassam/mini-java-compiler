from src.LexicalAnalyzer import LexicalAnalyzer
from src.SemanticAnalyzer import SemanticAnalyzer
from src.SemanticAnalyzer import SemanticAnalyzer


if __name__ == "__main__":
  # read Mini Java file path (defaults to data/main.mjava)
  # pass the path to the lexical analyzer
  # pass the result to the syntax analyzer
  # pass the result to the semantic analyzer
  lexer = LexicalAnalyzer("data/main.mjava")
  lexer.tokenize()
