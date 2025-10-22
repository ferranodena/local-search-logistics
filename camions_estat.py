from camions_parametres import ProblemParameters
from camions_operadors import CamionsOperator
from typing import List, Set, Generator


class StateRepresentation(object):

    def __init__(self, params: ProblemParameters):
        '''
        Representació de l'estat del problema de camions, amb les següents propietats:
        - params: objecte ProblemParameters amb les dades del problema
        - camions: llista de llistes de viatges per camió, on cada viatge és una llista de peticions ateses
        '''
        self.params = params
        self.camions = []  #CALDRÀ FER-HO MÉS EFICIENT !!¡!¡

    def es_possible(self) -> bool:
        """
        Comprova si l'estat actual compleix totes les restriccions:
        - Cap camió supera els km màxims diaris (self.params.km_max)
        - Cap camió supera el nombre màxim de viatges diaris (self.params.viatges_max)
        - Cap viatge porta més de 2 peticions
        - Cap petició s'atén més d'una vegada
        """
        peticions_atendides: Set[int] = set()

        for camio in self.camions:
        #CALDRÀ FER-HO MÉS EFICIENT !!¡!¡
            km_total = 0
            viatges_count = 0

            for viatge in camio:
                viatges_count += 1
                if viatges_count > self.params.viatges:
                    return False  # Supera el nombre màxim de viatges

                if len(viatge) > 2:
                    return False  # Supera el nombre màxim de peticions per viatge

                # Calcular km del viatge (suposant que tenim una funció per això)
                km_viatge = self.calcula_km_viatge(viatge)
                km_total += km_viatge

                if km_total > self.params.km:
                    return False  # Supera els km màxims diaris

                for peticio in viatge:
                    if peticio in peticions_atendides:
                        return False  # Petició ja atesa
                    peticions_atendides.add(peticio)

        return True 

    
    def manhattan(self, c1, c2):
        """
        Distància Manhattan entre dues coordenades (x, y)
        """
        return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])
    
    def apply_action(self, action: CamionsOperator) -> 'StateRepresentation':
        pass

    def __eq__(self, other):
        return isinstance(other, StateRepresentation) and self.params == other.params
    
def generate_initial_state(params: ProblemParameters) -> StateRepresentation:
    pass