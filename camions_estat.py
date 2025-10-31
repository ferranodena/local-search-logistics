from camions_parametres import ProblemParameters
from camions_operadors import CamionsOperator
from typing import List, Set, Generator
from abia_Gasolina import Gasolineres, Gasolinera
from camions_operadors import swapCentres, mourePeticio


class StateRepresentation(object):

    def __init__(self, params: ProblemParameters):
        '''
        Representació de l'estat del problema de camions, amb les següents propietats:
        - params: objecte ProblemParameters amb les dades del problema
        - camions: llista de llistes de viatges per camió, on cada viatge és una llista de peticions ateses
        '''
        self.params = params

        self.peticions_info = [] # dies pendents per cada petició, el índex de la llista indica el id de la petició, el valor associat a l'índex indica els dies que porta pendent la petició
        self.gasolinera_per_peticio = [] # gasolinera associada a cada petició, el índex de la llista indica el id de la petició, el valor de la llista indica la gasolinera associada
        
        i_global = 0
        for id_gas, gasolinera in enumerate(params.gasolineres): # Recorrem la llista de gasolineres retornant parelles, el índex i el objecte
            for dies in gasolinera.peticions: # Per cada gasolinera, iterem sobre totes les seves peticions pendents
                self.peticions_info.append(dies) # Afegim els dies pendents de la petició a la llista
                self.gasolinera_per_peticio.append(id_gas) # Afegim la gasolinera associada a la petició
                i_global += 1 # Incrementem el comptador global de peticions
        
        num_camions = len(params.centres.centres)
        self.camions = [[] for _ in range(num_camions)]  # Els índex de la primera llista són cada camió, les subllistes indiquen les peticions que ha de servir cada camió

        self.peticions_servides = set()

    def heuristica(self) -> float:
        """
        B_total = B - C - Pen
        On:
        - B = Ingressos dels dipòsits servits avui
        - C = Cost total dels km recorreguts
        - Pen = Penalització per peticions no servides avui
        
        Retorna: -B_total (per minimitzar, que equival a maximitzar B_total)
        """
        ingressos = self.calcular_ingressos_servits()
        cost_km = self.calcular_cost_km()
        penalitzacio = self.calcular_penalitzacio_pendents()
    
        benefici_total = ingressos - cost_km - penalitzacio
    
        return -benefici_total  # ha de ser negatiu
    
    def calcular_ingressos_servits(self) -> float:
        """
        Calcula el benefici perdut per les peticions no servides.
        Sumatori de les peticions servides avui pel seu factor de preu
        """
        ingressos = 0.0
        # Implementar càlcul del benefici perdut

        for camio in self.camions: # Recorrem cada camió
            for viatge in camio: # Recorrem cada viatge del camió
                for i_peticio in viatge: # Recorrem cada petició del viatge
                    dies_pendents = self.peticions_info[i_peticio] # Obtenim els dies pendents de la petició
                    factor_preu = self._factor_de_preu(dies_pendents) # Obtenim el factor de preu segons els dies pendents
                    ingressos += self.params.valor * factor_preu # Afegim als ingressos el valor de la petició multiplicat pel seu factor de preu
                    self.peticions_servides.add(i_peticio) # Afegim la petició a les peticions servides avui

        return ingressos

    def calcular_cost_km(self) -> float:
        """
        Calcula el cost total dels km recorreguts per tots els camions.
        És el cost per quilòmetre recorregut multiplicat pels km totals de tots els viatges
        """
        cost_km = 0.0
        # Implementar càlcul del cost de km totals

        for id_camio, camio in enumerate(self.camions): # Recorrem cada camió amb el seu índex
            for viatge in camio: # Recorrem cada viatge del camió
                km_viatge = self._calcular_km_viatge(id_camio, viatge) # Calculem els km del viatge
                cost_km += km_viatge * self.params.cost_km # Afegim al cost total els km del viatge multiplicat pel cost per km
        return cost_km
    
    def _calcular_km_viatge(self, id_camio: int, viatge: List[int]) -> float: # Els parametres són el id del camió i la llista de peticions del viatge
        """
        Calcula els km totals d'un viatge d'un camió donat.
        Un viatge comença al centre de distribució del camió, visita les gasolineres de les peticions i torna al centre.
        """
        coords_actuals = (self.params.centres.centres[id_camio].cx, self.params.centres.centres[id_camio].cy) # Les coordenades actuals del camió, comencem des del centre de distribució
        km_totals = 0.0

        for i_peticio in viatge:
            id_gasolinera = self.gasolinera_per_peticio[i_peticio] # Tenim el índex de la petició, obtenim la gasolinera associada
            gasolinera = self.params.gasolineres[id_gasolinera] # Obtenim l'objecte Gasolinera
            coords_gasolinera = (gasolinera.cx, gasolinera.cy)  # Obtenim les coordenades de la gasolinera asociada a la petició
            km_totals += self._manhattan(coords_actuals, coords_gasolinera) # Afegim als quilòmetres totals la distància que acabem de recórrer
            coords_actuals = coords_gasolinera  # Actualitzem les coordenades actuals del camió

        # Tornar al centre de distribució
        coords_centre = (self.params.centres.centres[id_camio].cx, self.params.centres.centres[id_camio].cy) # Coordenades del centre de distribució
        km_totals += self._manhattan(coords_actuals, coords_centre) # Afegim els quilòmetres per tornar al centre

        return km_totals # Retornem els quilòmetres totals del viatge
    
    def calcular_penalitzacio_pendents(self) -> float:
        """
        Calcula la penalització per les peticions no servides avui.
        És el sumatori de les penalitzacions no ateses el dia pel que porten pendent.
        Cada petició pendent afegeix una penalització segons els dies que porta pendent.
        """
        penalitzacio = 0.0
        # Implementar càlcul de la penalització per peticions pendents

        peticions_totals = len(self.peticions_info) # Nombre total de peticions
        for i_peticio in range(peticions_totals): # Recorrem totes les peticions pel seu índex
            if i_peticio not in self.peticions_servides: # Si la petició no ha estat servida avui
                dies_pendents = self.peticions_info[i_peticio] # Obtenim els dies pendents de la petició
                factor_preu = self._factor_de_preu(dies_pendents) # Obtenim el factor de preu segons els dies pendents
                penalitzacio += self.params.valor * (factor_preu(0) - factor_preu(dies_pendents)) # Afegim a la penalització el valor de la petició multiplicat per la diferència del factor de preu entre 0 dies i els dies pendents
        return penalitzacio
    
    def _factor_de_preu(self, dies: int) -> float: #f(d) del meu escrit :)
        """
        Factor de preu en funció dels dies que han passat per petició.
        Els dies són estrictament positius.
        """
        if dies == 0:
            return 1.02
        else: return max(0, 1-0.02 * dies)
        
    
    def _manhattan(self, c1, c2):
        """
        Distància Manhattan entre dues coordenades (x, y)
        """
        return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])
    
    def _copy(self) -> 'StateRepresentation':
        """
        Crea una còpia profunda de l'estat actual.
        :return: nova instància de StateRepresentation amb les mateixes dades
        """
        new_state = StateRepresentation(self.params)
        new_state.peticions_info = self.peticions_info.copy()
        new_state.gasolinera_per_peticio = self.gasolinera_per_peticio.copy()
        new_state.camions = [viatges.copy() for viatges in self.camions]
        new_state.peticions_servides = self.peticions_servides.copy()
        return new_state

    

    def apply_action(self, action: CamionsOperator) -> 'StateRepresentation':
        """
        Aplica un operador a l'estat actual i retorna el nou estat resultant.
        :param action: operador a aplicar
        :return: nou estat després d'aplicar l'operador
        """
        
        new_state = self._copy()

        if isinstance(action, swapCentres):
            c1 = action.centre1
            c2 = action.centre2
            new_state.camions[c1], new_state.camions[c2] = new_state.camions[c2], new_state.camions[c1]

        elif isinstance(action, mourePeticio):
            id_peticio = action.id_peticio
            camio_origen = action.camio_origen
            camio_desti = action.camio_desti

            for viatge in new_state.camions[camio_origen]: # Accedim a la llista de camions, i del camio origen, recorrem cada viatge (peticio)
                if id_peticio in viatge: # Si la petició està en aquest viatge
                    viatge.remove(id_peticio) # La esborrem del viatge
                    break

            if new_state.camions[camio_desti]: # Si el camió destí ja té viatges assignats
                new_state.camions[camio_desti][-1].append(id_peticio) # Afegim la petició al darrer viatge existent
            else:
                new_state.camions[camio_desti].append([id_peticio]) # Si no té viatges, creem un nou viatge amb la petició
        return new_state
    
    def generate_actions(self) -> Generator[CamionsOperator, None, None]:
        """
        Genera tots els possibles operadors aplicables a l'estat actual.
        :return: generador d'operadors
        """
        num_camions = len(self.camions)

        # Generar operadors swapCentres per cada parella de centres
        for i in range(num_camions):
            for j in range(i + 1, num_camions):
                yield swapCentres(i, j)

        # Generar operadors mourePeticio per cada petició i camions diferents
        for id_camio_origen in range(num_camions):
            for viatge in self.camions[id_camio_origen]:
                for id_peticio in viatge:
                    for id_camio_desti in range(num_camions):
                        if id_camio_desti != id_camio_origen:
                            yield mourePeticio(id_peticio, id_camio_origen, id_camio_desti)

    

    def __eq__(self, other):
        return isinstance(other, StateRepresentation) and self.params == other.params
    
def generate_greedy_initial_state(params: ProblemParameters) -> StateRepresentation:
    """
    Assignar a cada camió les peticions més properes (de distància) fins a omplir la seva capacitat, 
    sense tenir en compte la penalització per peticions pendents.
    :param params: paràmetres del problema
    :return: estat inicial generat
    """
    estat = StateRepresentation(params)

    num_camions = len(params.centres)
    num_peticions = len(estat.peticions_info)

    for i_peticio in range(num_peticions): # Recorrem totes les peticions pel seu índex
        id_gasolinera = estat.gasolinera_per_peticio[i_peticio] # Obtenim la gasolinera associada a la petició
        gasolinera = params.gasolineres[id_gasolinera] # Obtenim l'objecte Gasolinera
        coords_peticio = (gasolinera.cx, gasolinera.cy)

        min_distancia = float('inf')
        millor_camio = None

        for id_camio in range(num_camions): # Recorrem cada camió pel seu índex
            centre = params.centres[id_camio] # Obtenim l'objecte Centre de distribució
            coords_centre = (centre.cx, centre.cy)
            distancia = estat._manhattan(coords_peticio, coords_centre) # calculem la distància entre la petició i el centre 
            if distancia < min_distancia : # Si la distància és menor que la mínima trobada fins ara
                min_distancia = distancia
                millor_camio = id_camio
        if millor_camio is not None: # si ja tenim un camió assignat
            if estat.camions[millor_camio]: # Si el camió ja té viatges assignats
                estat.camions[millor_camio][-1].append(i_peticio) # Afegim la petició al darrer viatge existent
            else:
                estat.camions[millor_camio].append([i_peticio]) # Si no té viatges, creem un nou viatge amb la petició
    return estat

def generate_empty_initial_state(params: ProblemParameters) -> StateRepresentation:
    """
    Genera un estat inicial buit, sense cap petició assignada a cap camió.
    :param params: paràmetres del problema
    :return: estat inicial buit
    """
    estat = StateRepresentation(params) # Creem l'estat amb els paràmetres donats
    return estat

def generate_initial_state(parametres: ProblemParameters) -> StateRepresentation:
    """
    Les peticions es prioritzen segons la seva penalització potencial (pèrdua de preu per dia pendent). 
    El camió atén primer les peticions amb la penalització més alta, sempre que estiguin dins de
    la seva capacitat i distància. Després, si és compatible per distància i capacitat, 
    s'assigna la petició més propera geogràficament, i en cas d'empat, la que tingui més dies pendents, 
    i en cas d'empat, la que impliqui menys distància de retorn al centre assignat al camió. 
    :param parametres: paràmetres del problema
    :return: estat inicial generat
    """
    estat = StateRepresentation(parametres)

    nombre_camions = len(parametres.centres.centres)
    nombre_peticions = len(estat.peticions_info)

    peticions_ordenades = sorted( # ordenem les peticions segons el seu factor de preu, de més alt a més baix
        range(nombre_peticions),
        key=lambda i: (-estat._factor_de_preu(estat.peticions_info[i]), i)
    )

    for id_peticio in peticions_ordenades: #recorrem les peticions ordenades segons la seva prioritat
        id_gasolinera = estat.gasolinera_per_peticio[id_peticio]
        gasolinera = parametres.gasolineres.gasolineres[id_gasolinera]
        coordenades_peticio = (gasolinera.cx, gasolinera.cy)

        millor_camio = None
        millor_distancia = float('inf')
        millors_dies_pendents = -1
        millor_distancia_retor = float('inf')

        for id_camio in range(nombre_camions): # Recorrem cada camió pel seu índex
            centre = parametres.centres.centres[id_camio]
            coordenades_centre = (centre.cx, centre.cy)
            distancia = estat._manhattan(coordenades_peticio, coordenades_centre)
            dies_pendents = estat.peticions_info[id_peticio]
            distancia_retor = estat._manhattan(coordenades_peticio, coordenades_centre)

            # Prioritzem segons la distància, dies pendents i distància de retorn

            if (distancia < millor_distancia or
                (distancia == millor_distancia and dies_pendents > millors_dies_pendents) or
                (distancia == millor_distancia and dies_pendents == millors_dies_pendents and distancia_retor < millor_distancia_retor)):
                millor_distancia = distancia
                millors_dies_pendents = dies_pendents
                millor_distancia_retor = distancia_retor
                millor_camio = id_camio

        if millor_camio is not None:
            if estat.camions[millor_camio]:  # Si el camió ja té viatges assignats
                estat.camions[millor_camio][-1].append(id_peticio)  # Afegim la petició al darrer viatge existent
            else:
                estat.camions[millor_camio].append([id_peticio])  # Si no té viatges, creem un nou viatge amb la petició

    return estat
