class State:
  def __init__(self, id: str, isStart: bool = False, isFinal: bool = False, transitions: list = None):
    self.id = id
    self.isStart = isStart
    self.isFinal = isFinal
    self.transitions = transitions if transitions is not None else []

class Transition:
  def __init__(self, from_state: State, to_state: State, symbol: str):
    self.from_state = from_state
    self.to_state = to_state
    self.symbol = symbol

class DFA:
  def __init__(self, start_state: State):
    self.start_state = start_state

  def from_transition_table(self, xlsx_path = "./dfa-transitions.xlsx"):
    from openpyxl import load_workbook

    wb = load_workbook(xlsx_path)
    ws = wb.active

    states = {}
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
      state =  State(id=row[1].value, isStart=row[0].value != None and row[0].value.startswith("->"), isFinal=row[0].value != None and row[0].value.startswith("*"))
      states[state.id] = state
      if state.isStart:
        self.start_state = state

    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
      state_id = row[1].value
      state = states[state_id]
      transitions = []
      for col in range(2, ws.max_column):
        symbol = ws.cell(row=1, column=col + 1).value
        to_state_id = row[col].value
        if to_state_id != '-' and to_state_id != '' and to_state_id is not None:
          to_state = states[to_state_id]
          transition = Transition(from_state=state, to_state=to_state, symbol=symbol)
          transitions.append(transition)
      state.transitions = transitions

# dfa = DFA(start_state=None)
# dfa.from_transition_table()
# print(f"Start State: {dfa.start_state.id}")
# print(f"Transitions from Start State: {[f'{t.symbol} -> {t.to_state.id}' for t in dfa.start_state.transitions]}")