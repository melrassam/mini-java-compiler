
from dataclasses import dataclass, field

@dataclass
class SymbolEntry:
    name: str
    first_line: int
    first_column: int
    occurrences: list[tuple[int, int]] = field(default_factory=list)
    type: str | None = None
    scope: str | None = None

class SymbolTable:
    def __init__(self):
        self.symbols: dict[str, SymbolEntry] = {}
    def add(self, name: str, line: int, column: int) -> SymbolEntry:
        entry = self.symbols.get(name)
        if entry is None:
            entry = SymbolEntry(name, line, column)
            self.symbols[name] = entry
        entry.occurrences.append((line, column))
        return entry
    def lookup(self, name: str) -> SymbolEntry | None:
        return self.symbols.get(name)
