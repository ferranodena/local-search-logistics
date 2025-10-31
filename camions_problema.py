from typing import Generator
from camions_operadors import CamionsOperator
from aima3.search import Problem
from camions_estat import StateRepresentation

class CamionsProblema(Problem):
    '''
    Definició del problema dels camions com a problema de cerca.
    '''

    def __init__(self, initial_state: StateRepresentation):
        super().__init__(initial_state)

    def actions(self, state: StateRepresentation) -> Generator[CamionsOperator, None, None]:
        return state.generate_actions()

    def result(self, state: StateRepresentation, action: CamionsOperator) -> StateRepresentation:
        return state.apply_action(action)

    def value(self, state: StateRepresentation) -> float:
        return -state.heuristica()

    def goal_test(self, state: StateRepresentation) -> bool:
        return False
