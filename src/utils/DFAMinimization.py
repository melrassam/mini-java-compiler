import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.DFA import DFA, State, Transition

class StateGroup:
  def __init__(self, id: str, states: list):
    self.id = id
    self.states = states
  def __str__(self):
    return f"StateGroup(id={self.id}, states={self.states})"

class MinimizationLoop:
  def __init__(self, stateGroups: list = None):
    self.stateGroups = stateGroups
  def __str__(self):
    return f"MinimizationLoop(stateGroups={self.stateGroups})"
  def create_initial_groups(self, dfa: DFA):
    final_states = []
    non_final_states = []
    def recursive_grouping(state: State):
      if state.isFinal:
        final_states.append(state)
      else:
        non_final_states.append(state)
      for transition in state.transitions:
        if transition.to_state not in final_states and transition.to_state not in non_final_states:
          recursive_grouping(transition.to_state)
    recursive_grouping(dfa.start_state)
    self.stateGroups = [StateGroup("Final States", final_states), StateGroup("Non-Final States", non_final_states)]

  def get_containing_group(self, state: State):
    for group in self.stateGroups:
      if state in group.states:
        return group
    return None

  def rebuild_groups(self, alphabet):
    group_of = {
      state: i
      for i, group in enumerate(self.stateGroups)
      for state in group.states
    }
    new_groups = []
    for group in self.stateGroups:
      buckets = {}
      for state in group.states:
        destinations = {t.symbol: t.to_state for t in state.transitions}
        signature = tuple(group_of[destinations[symbol]] for symbol in alphabet)
        buckets.setdefault(signature, []).append(state)
      for states in buckets.values():
          new_groups.append(StateGroup(f"G{len(new_groups)}", states))
    self.stateGroups = new_groups


  def minimize(self, alphabet):
    while True:
      previous_count = len(self.stateGroups)
      self.rebuild_groups(alphabet)
      if len(self.stateGroups) == previous_count:
        break
    return self.stateGroups

  def build_minimized_dfa(self, original_dfa: DFA):
    state_to_group = {
      state: i
      for i, group in enumerate(self.stateGroups)
      for state in group.states
    }
    new_states = []
    for group in self.stateGroups:
      new_state = State(id=group.id, isStart=original_dfa.start_state in group.states, isFinal=any(s.isFinal for s in group.states))
      new_states.append(new_state)
    for i, group in enumerate(self.stateGroups):
      representative = group.states[0]
      from_state = new_states[i]
      for transition in representative.transitions:
        destination_group = state_to_group[transition.to_state]
        to_state = new_states[destination_group]
        from_state.transitions.append(Transition(from_state, to_state, transition.symbol))
    start_state = next(s for s in new_states if s.isStart)
    minimized_dfa = DFA(start_state)
    minimized_dfa.alphabet = original_dfa.alphabet.copy()
    return minimized_dfa

if __name__ == "__main__":
  dfa = DFA(None)
  dfa.from_transition_table()
  ml = MinimizationLoop()
  ml.create_initial_groups(dfa)
  ml.minimize(dfa.alphabet)
  minimized_dfa = ml.build_minimized_dfa(dfa)
  print("Equivalence classes:")
  for group in ml.stateGroups:
      print(f"{group.id}: {[s.id for s in group.states]}")
  print(f"Minimized start state: {minimized_dfa.start_state.id}")