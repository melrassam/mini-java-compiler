
import json
from pathlib import Path
from dataclasses import dataclass

from src.Token import Token
from src.DFA import DFA, DFAExecutor
from src.SymbolTable import SymbolTable, SymbolEntry


KEYWORDS = {
  "class": "CLASS",
  "public": "PUBLIC",
  "static": "STATIC",
  "void": "VOID",
  "int": "INT",
  "float": "FLOAT",
  "boolean": "BOOLEAN_TYPE",
  "char": "CHAR",
  "String": "STRING_TYPE",
  "if": "IF",
  "else": "ELSE",
  "while": "WHILE",
  "for": "FOR",
  "return": "RETURN",
  "true": "BOOLEAN",
  "false": "BOOLEAN",
}

PUNCTUATION = {
  "(": "LPAR",
  ")": "RPAR",
  "{": "LCUR",
  "}": "RCUR",
  "[": "LSQU",
  "]": "RSQU",
  ";": "SEMICOLON",
  ",": "COMMA",
  ".": "DOT",
}

OPERATORS = {
  "=": "ASSIGN",
  "==": "LOGOP",
  "!=": "LOGOP",
  ">": "LOGOP",
  "<": "LOGOP",
  ">=": "LOGOP",
  "<=": "LOGOP",
  "+": "ADDOP",
  "-": "ADDOP",
  "*": "MULOP",
  "/": "MULOP",
  "%": "MULOP",
  "&&": "ANDOP",
  "||": "OROP",
  "!": "NOTOP",
  "&": "BITANDOP",
  "|": "BITOROP",
  "~": "BITNOTOP",
  "^": "BITXOROP",
}


@dataclass(frozen=True)
class LexicalError:
  message: str
  line: int
  column: int
  def __str__(self):
    return f"Line {self.line}, column {self.column}: {self.message}"

class LexicalAnalyzer:
  def __init__(self, file_path: str = "data/main.mjava", dfa: DFA | None = None):
    self.file_path = file_path

    if dfa is None:
      dfa = DFA(None)
      root = Path(__file__).resolve().parents[1]
      dfa.from_transition_table(
        str(root / "dfa-transitions.xlsx")
      )

    self.executor = DFAExecutor(dfa)
    self.symbol_table = SymbolTable()
    self.errors: list[LexicalError] = []


  @staticmethod
  def classify(lexeme: str) -> str | None:
    """Accepts a lexeme and determines its token type. If it doesn't
    belong to any token type, it returns None

    Args:
      lexeme (str): lexeme string
    
    Returns:
      str | None: returns the token type as a string or None
    """

    if lexeme.startswith("//") or (lexeme.startswith("/*") and lexeme.endswith("*/")):
      return "COMMENT"

    if len(lexeme) > 0 and lexeme.strip() == "":
      return "SPACE"

    if lexeme in KEYWORDS:
      return KEYWORDS[lexeme]

    if lexeme in PUNCTUATION:
      return PUNCTUATION[lexeme]

    if lexeme in OPERATORS:
      return OPERATORS[lexeme]

    if (
      len(lexeme) >= 2
      and lexeme[0] in ('"', "'")
      and lexeme[-1] == lexeme[0]
    ):
      return "STRING"

    if lexeme[0].isdigit():
      return "NUMBER"

    if lexeme[0].isalpha() or lexeme[0] == "_":
      return "ID"

    return None


  @staticmethod
  def save_tokens(tokens: list[Token], file_path: str) -> None:
    """Saves a list of tokens in a file in JSON format

    Args:
      tokens (list[Token]): tokens to be saved
      file_path (str): output file path
    """

    output = [
      {
        "text": token.text,
        "type": token.type,
        "line": token.attributes["line"],
        "column": token.attributes["column"]
      }
      for token in tokens
    ]

    Path(file_path).write_text(
      json.dumps(output, indent=2),
      encoding="utf-8"
    )


  def tokenize(self, output_file_path = None) -> list[Token]:
    source = Path(self.file_path).read_text(encoding="utf-8")

    n = len(source)
    line = 1
    column = 1
    offset = 0
    tokens: list[Token] = []
    self.errors = []
    self.symbol_table = SymbolTable()

    def advance(end: int):
      nonlocal offset, line, column
      segment = source[offset:end]
      breaks = segment.count("\n")
      if breaks:
        line += breaks
        column = len(segment.rsplit("\n", 1)[-1]) + 1
      else:
        column += len(segment)
      offset = end

    def error(message: str):
      self.errors.append(LexicalError(message, line, column))

    while offset < n:
      char = source[offset]
      # if char.isspace():
      #   end = offset + 1
      #   while end < n and source[end].isspace():
      #     end += 1
      #   advance(end)
      #   continue

      # if source.startswith("//", offset):
      #   end = source.find("\n", offset + 2)
      #   advance(n if end == -1 else end)
      #   continue

      if source.startswith("/*", offset):
        end = source.find("*/", offset + 2)
        if end == -1:
          error("unterminated multi-line comment")
          advance(n)
        else:
          advance(end + 2)
        continue

      if char in ('"', "'"):
        newline = source.find("\n", offset + 1)
        closing_quote = source.find(char, offset + 1)
        if (
          closing_quote == -1
          or (newline != -1 and newline < closing_quote)
        ):
          error("unclosed string literal")
          advance(n if newline == -1 else newline)
          continue

      match = self.executor.match_longest(source, offset)
      if match is None or match.end == offset:
        error(f"invalid character {char!r}")
        advance(offset + 1)
        continue
      lexeme = source[offset:match.end]
      if (
        lexeme[0].isdigit()
        and match.end < n
        and (
          source[match.end].isalnum()
          or source[match.end] == "_"
        )
      ):
        end = match.end
        while end < n and (
          source[end].isalnum() or source[end] == "_"
        ):
          end += 1
        sequence = source[offset:end]
        if source[match.end].isdigit():
          error(
            f"numeric sequence not recognized by DFA {sequence!r}"
          )
        else:
          error(f"invalid identifier {sequence!r}")
        advance(end)
        continue

      token_type = self.classify(lexeme)
      if token_type is None:
        error(f"unrecognized lexeme {lexeme!r}")
        advance(match.end)
        continue
      attributes: dict[str, int | bool | SymbolEntry] = {
        "line": line,
        "column": column
      }

      if lexeme in ("true", "false"):
        attributes["value"] = (lexeme == "true")

      if token_type == "ID":
        attributes["symbol"] = self.symbol_table.add(
          lexeme, line, column
        )
      tokens.append(
        Token(lexeme, token_type, attributes)
      )
      advance(match.end)

    if output_file_path:
      self.save_tokens(tokens, output_file_path)

    return tokens
