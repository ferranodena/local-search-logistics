from .camions_parametres import ProblemParameters
from .camions_operadors import CamionsOperator
from typing import List, Set, Generator
from .abia_Gasolina import Gasolineres, Gasolinera
from .camions_operadors import swapCentres, mourePeticio, swapPeticions
import random


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
        for id_gas, gasolinera in enumerate(params.gasolineres.gasolineres): # Recorrem la llista de gasolineres retornant parelles, el índex i el objecte
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
        ingressos = 0.0
        for camio in self.camions:
            for viatge in camio:
                for i_peticio in viatge:
                    dies_pendents = self.peticions_info[i_peticio]
                    factor_preu = self._factor_de_preu(dies_pendents)
                    ingressos += self.params.valor * factor_preu
        return ingressos

    def _get_peticions_servides(self) -> Set[int]:
        """Retorna el conjunt de peticions servides"""
        servides = set()
        for camio in self.camions:
            for viatge in camio:
                for i_peticio in viatge:
                    servides.add(i_peticio)
        return servides


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
            gasolinera = self.params.gasolineres.gasolineres[id_gasolinera] # Obtenim l'objecte Gasolinera
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
        La penalització és la suma de les pèrdues de preu per cada petició no servida.
        """

        penalitzacio = 0.0
        peticions_servides = self._get_peticions_servides()  # Calculem-ho aquí
        peticions_totals = len(self.peticions_info)
        
        for i_peticio in range(peticions_totals):
            if i_peticio not in peticions_servides:
                dies_pendents = self.peticions_info[i_peticio]
                factor_preu = self._factor_de_preu(dies_pendents)
                penalitzacio += self.params.valor * (self._factor_de_preu(0) - factor_preu)
        
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
        new_state.camions = [[viatge.copy() for viatge in camio] for camio in self.camions]  # Còpia profunda
        return new_state

    

    def apply_action(self, action: CamionsOperator) -> 'StateRepresentation':
        """
        Aplica un operador a l'estat actual i retorna el nou estat resultant.
        :param action: operador a aplicar
        :return: nou estat després d'aplicar l'operador
        """
        
        new_state = self._copy()

        # Primer apliquem l'operador swapCentres, que intercanvia els centres de dos camions
        if isinstance(action, swapCentres):
            c1 = action.centre1
            c2 = action.centre2
            new_state.camions[c1], new_state.camions[c2] = new_state.camions[c2], new_state.camions[c1]

        elif isinstance(action, mourePeticio):
            id_peticio = action.id_peticio
            camio_origen = action.camio_origen
            camio_desti = action.camio_desti
            
            # Eliminar la petició del camió origen
            for viatge in new_state.camions[camio_origen]:
                if id_peticio in viatge:
                    viatge.remove(id_peticio)
                    break
            
            # Eliminar viatges buits
            new_state.camions[camio_origen] = [v for v in new_state.camions[camio_origen] if v]
            
            # Afegir al camió destí
            if new_state.camions[camio_desti]:
                if len(new_state.camions[camio_desti][-1]) < 2:
                    new_state.camions[camio_desti][-1].append(id_peticio)
                elif len(new_state.camions[camio_desti]) < self.params.n_viatges:
                    new_state.camions[camio_desti].append([id_peticio])
            else:
                new_state.camions[camio_desti].append([id_peticio])
        return new_state

    
    def generate_all_actions(self) -> Generator[CamionsOperator, None, None]:
        """
        Genera tots els possibles operadors aplicables a l'estat actual.
        :return: generador d'operadors
        """
        num_camions = len(self.camions)

        # Generar operadors swapCentres per cada parella de centres
        #for i in range(num_camions):
            #for j in range(i + 1, num_camions):
                #yield swapCentres(i, j)

        # Generar operadors mourePeticio per cada petició i camions diferents
        for id_camio_origen in range(num_camions):
            for viatge in self.camions[id_camio_origen]:
                for id_peticio in viatge:
                    for id_camio_desti in range(num_camions):
                        if id_camio_desti != id_camio_origen:
                            yield mourePeticio(id_peticio, id_camio_origen, id_camio_desti)

        # Generar operadors swapPeticions per cada parella de peticions en camions diferents
        # for id_camio1 in range(num_camions):
        #     for viatge1 in self.camions[id_camio1]:
        #         for id_peticio1 in viatge1:
        #             for id_camio2 in range(id_camio1 + 1, num_camions):
        #                 for viatge2 in self.camions[id_camio2]:
        #                     for id_peticio2 in viatge2:
        #                         yield swapPeticions(id_peticio1, id_camio1, id_peticio2, id_camio2)

        return self.generate_all_actions()

    def generate_actions_lazy(self) -> Generator['CamionsOperator', None, None]:
        """
        Genera un conjunt petit d'accions aleatòries (lazy) per a Simulated Annealing.
        Combina accions de tipus swapCentres i mourePeticio de manera equilibrada.
        """
        actions_generades = set() # set d'accions ja generades per evitar duplicats
        num_camions = len(self.camions) # Nombre de camions
        max_accions = 50  # Nombre màxim d'accions a generar

        for _ in range(max_accions): # Generem fins a max_accions accions
            tipus = random.choices(['swapCentres', 'mourePeticio'], weights=[0.3, 0.7])[0]

            # === Intercanviar centres entre dos camions ===
            if tipus == 'swapCentres': # Si el tipus d'acció és swapCentres
                c1, c2 = random.sample(range(num_camions), 2) # Seleccionem dos camions diferents aleatòriament
                if self.camions[c1] and self.camions[c2]: # Comprovem que ambdós camions tinguin viatges assignats
                    accio = ('swapCentres', c1, c2) # Creem una tupla representant l'acció
                    if accio not in actions_generades: # Si l'acció no ha estat generada abans
                        actions_generades.add(accio) # Afegim l'acció al set d'accions generades
                        yield swapCentres(c1, c2) # Retornem l'acció com a generador

            # === Moure una petició entre camions ===
            elif tipus == 'mourePeticio':  # Si el tipus d'acció és mourePeticio
                id_camio_origen = random.randint(0, num_camions - 1) # Seleccionem un camió origen aleatòriament
                if not self.camions[id_camio_origen]: # Si el camió origen no té viatges assignats, continuem al següent iteració
                    continue

                viatge_origen = random.choice(self.camions[id_camio_origen]) # Seleccionem un viatge aleatori del camió origen
                if not viatge_origen: # Si el viatge està buit, continuem
                    continue

                id_peticio = random.choice(viatge_origen) # Seleccionem una petició aleatòria del viatge origen
                id_camio_desti = random.choice([i for i in range(num_camions) if i != id_camio_origen]) # Seleccionem un camió destí diferent de l'origen

                # Comprovem si el camió destí pot rebre una nova petició
                camio_desti = self.camions[id_camio_desti] # Obtenim els viatges del camió destí
                pot_afegir = False # Variable per indicar si es pot afegir la petició

                if not camio_desti: # Si el camió destí no té viatges, es pot afegir la petició
                    pot_afegir = True
                else: # Si té viatges, comprovem l'últim viatge
                    ultim_viatge = camio_desti[-1] # Obtenim l'últim viatge del camió destí
                    if len(ultim_viatge) < 2: # Si l'últim viatge té menys de 2 peticions, es pot afegir la petició
                        pot_afegir = True
                    elif len(camio_desti) < self.params.n_viatges: # Si es poden afegir més viatges al camió destí, també es pot afegir la petició
                        pot_afegir = True 

                if pot_afegir: # Si es pot afegir la petició al camió destí
                    accio = ('mourePeticio', id_peticio, id_camio_origen, id_camio_desti) # Creem una tupla representant l'acció
                    if accio not in actions_generades: # Si l'acció no ha estat generada abans
                        actions_generades.add(accio) # Afegim l'acció al set d'accions generades
                        # yield mourePeticio(id_peticio, id_camio_origen, id_camio_desti) # Retornem l'acció com a generador
                        
            # elif tipus == 'swapPeticions':  # Si el tipus d'acció és swapPeticions
            #     id_camio1, id_camio2 = random.sample(range(num_camions), 2) # Seleccionem dos camions diferents aleatòriament
            #     if not self.camions[id_camio1] or not self.camions[id_camio2]: # Si algun dels camions no té viatges assignats, continuem
            #         continue

            #     viatge1 = random.choice(self.camions[id_camio1]) # Seleccionem un viatge aleatori del primer camió
            #     viatge2 = random.choice(self.camions[id_camio2]) # Seleccionem un viatge aleatori del segon camió

            #     if not viatge1 or not viatge2: # Si algun dels viatges està buit, continuem
            #         continue

            #     id_peticio1 = random.choice(viatge1) # Seleccionem una petició aleatòria del primer viatge
            #     id_peticio2 = random.choice(viatge2) # Seleccionem una petició aleatòria del segon viatge

            #     accio = ('swapPeticions', id_peticio1, id_camio1, id_peticio2, id_camio2) # Creem una tupla representant l'acció
            #     if accio not in actions_generades: # Si l'acció no ha estat generada abans
            #         actions_generades.add(accio) # Afegim l'acció al set d'accions generades
            #         yield swapPeticions(id_peticio1, id_camio1, id_peticio2, id_camio2) # Retornem l'acció com a generador
                
        return self.generate_actions_lazy() # Retornem el generador d'accions

    def __eq__(self, other):
        return isinstance(other, StateRepresentation) and self.params == other.params
    
    def __str__(self):
        output = []
        output.append("=" * 70)
        output.append("═══════════════════ ESTAT DELS CAMIONS ════════════════════")
        output.append("=" * 70)
        
        # Resum general
        benefici = -self.heuristica()
        ingressos = self.calcular_ingressos_servits()
        cost_km = self.calcular_cost_km()
        penalitzacio = self.calcular_penalitzacio_pendents()
        
        output.append(f"\n💰 BENEFICI TOTAL: {benefici:.2f}€")
        output.append(f"   ├─ Ingressos:    {ingressos:.2f}€")
        output.append(f"   ├─ Cost km:     -{cost_km:.2f}€")
        output.append(f"   └─ Penalització: -{penalitzacio:.2f}€")
        
        # Estadístiques globals
        peticions_servides_set = self._get_peticions_servides()
        km_totals = 0.0
        
        for id_camio, camio in enumerate(self.camions):
            for viatge in camio:
                km_totals += self._calcular_km_viatge(id_camio, viatge)
        
        output.append(f"\n📊 RESUM:")
        output.append(f"   ├─ Peticions servides: {len(peticions_servides_set)}/{len(self.peticions_info)}")
        output.append(f"   ├─ Peticions pendents: {len(self.peticions_info) - len(peticions_servides_set)}")
        output.append(f"   └─ Km totals recorreguts: {km_totals:.2f} km")
        
        output.append("\n" + "=" * 70)
        
        # Detall per cada camió
        for id_camio, camio in enumerate(self.camions):
            centre = self.params.centres.centres[id_camio]
            output.append(f"\n🚚 CAMIÓ {id_camio} | Centre de Distribució: ({centre.cx}, {centre.cy})")
            output.append("─" * 70)
            
            if not camio:
                output.append("   ⚠️  Cap viatge assignat")
                continue
            
            km_camio = 0.0
            cost_camio = 0.0
            ingressos_camio = 0.0
            
            for id_viatge, viatge in enumerate(camio):
                km_viatge = self._calcular_km_viatge(id_camio, viatge)
                cost_viatge = km_viatge * self.params.cost_km
                km_camio += km_viatge
                cost_camio += cost_viatge
                
                # Calcular ingressos del viatge
                ingressos_viatge = 0.0
                for id_peticio in viatge:
                    dies = self.peticions_info[id_peticio]
                    factor = self._factor_de_preu(dies)
                    ingressos_viatge += self.params.valor * factor
                
                ingressos_camio += ingressos_viatge
                benefici_viatge = ingressos_viatge - cost_viatge
                
                output.append(f"\n   📦 VIATGE {id_viatge} | {len(viatge)} petició(s)")
                output.append(f"      ├─ Km totals: {km_viatge:.2f} km")
                output.append(f"      ├─ Cost viatge: {cost_viatge:.2f}€")
                output.append(f"      ├─ Ingressos viatge: {ingressos_viatge:.2f}€")
                output.append(f"      └─ Benefici viatge: {benefici_viatge:.2f}€")
                
                # Desplaçaments detallats
                output.append(f"\n      🗺️  RUTA DEL VIATGE:")
                coords_actuals = (centre.cx, centre.cy)
                tram_num = 0
                
                for idx, id_peticio in enumerate(viatge):
                    id_gas = self.gasolinera_per_peticio[id_peticio]
                    gas = self.params.gasolineres.gasolineres[id_gas]
                    coords_gas = (gas.cx, gas.cy)
                    distancia_tram = self._manhattan(coords_actuals, coords_gas)
                    dies = self.peticions_info[id_peticio]
                    factor = self._factor_de_preu(dies)
                    preu = self.params.valor * factor
                    
                    output.append(f"         {tram_num}. Centre ({coords_actuals[0]}, {coords_actuals[1]}) "
                                f"→ Gasolinera {id_gas} ({coords_gas[0]}, {coords_gas[1]})")
                    output.append(f"            📏 Distància: {distancia_tram:.2f} km | "
                                f"💵 Cost: {distancia_tram * self.params.cost_km:.2f}€")
                    output.append(f"            📦 Petició {id_peticio}: {dies} dies pendents | "
                                f"Factor preu: {factor:.2f} | Ingressos: {preu:.2f}€")
                    
                    coords_actuals = coords_gas
                    tram_num += 1
                
                # Retorn al centre
                distancia_retorn = self._manhattan(coords_actuals, (centre.cx, centre.cy))
                output.append(f"         {tram_num}. Gasolinera ({coords_actuals[0]}, {coords_actuals[1]}) "
                            f"→ Centre ({centre.cx}, {centre.cy})")
                output.append(f"            📏 Distància: {distancia_retorn:.2f} km | "
                            f"💵 Cost: {distancia_retorn * self.params.cost_km:.2f}€")
            
            benefici_camio = ingressos_camio - cost_camio
            output.append(f"\n   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            output.append(f"   📊 RESUM CAMIÓ {id_camio}:")
            output.append(f"      ├─ Km totals: {km_camio:.2f} km")
            output.append(f"      ├─ Cost total: {cost_camio:.2f}€")
            output.append(f"      ├─ Ingressos totals: {ingressos_camio:.2f}€")
            output.append(f"      └─ Benefici camió: {benefici_camio:.2f}€")
        
        output.append("\n" + "=" * 70)
        return "\n".join(output)

    def _get_peticions_servides(self) -> Set[int]:
        """Retorna el conjunt de peticions servides"""
        servides = set()
        for camio in self.camions:
            for viatge in camio:
                for i_peticio in viatge:
                    servides.add(i_peticio)
        return servides


    
def generate_greedy_initial_state(params: ProblemParameters) -> StateRepresentation:
    """
    Assignar a cada camió les peticions més properes (de distància) fins a omplir la seva capacitat, 
    sense tenir en compte la penalització per peticions pendents.
    :param params: paràmetres del problema
    :return: estat inicial generat
    """
    estat = StateRepresentation(params)

    num_camions = len(params.centres.centres)
    num_peticions = len(estat.peticions_info)

    for i_peticio in range(num_peticions): # Recorrem totes les peticions pel seu índex
        id_gasolinera = estat.gasolinera_per_peticio[i_peticio] # Obtenim la gasolinera associada a la petició
        gasolinera = params.gasolineres.gasolineres[id_gasolinera] # Obtenim l'objecte Gasolinera
        coords_peticio = (gasolinera.cx, gasolinera.cy)

        min_distancia = float('inf')
        millor_camio = None

        for id_camio in range(num_camions): # Recorrem cada camió pel seu índex
            centre = params.centres.centres[id_camio] # Obtenim l'objecte Centre de distribució
            coords_centre = (centre.cx, centre.cy)
            distancia = estat._manhattan(coords_peticio, coords_centre) # calculem la distància entre la petició i el centre 
            if distancia < min_distancia : # Si la distància és menor que la mínima trobada fins ara
                min_distancia = distancia
                millor_camio = id_camio

        if millor_camio is not None: # si ja tenim un camió assignat
            camio_viatges = estat.camions[millor_camio]
            if not camio_viatges or len(camio_viatges[-1]) >= 2: # Si el camió no té viatges o l'últim viatge està ple
                if len(camio_viatges) < params.n_viatges: # Si el camió pot afegir un nou viatge
                    camio_viatges.append([i_peticio]) # Creem un nou viatge amb la petició
                else:
                    continue  # No es pot assignar aquesta petició
            else:
                camio_viatges[-1].append(i_peticio) # Afegim la petició a l'últim viatge existent
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
            camio_viatges = estat.camions[millor_camio]

            if not camio_viatges or len(camio_viatges[-1]) >= 2:
                if len(camio_viatges) < parametres.n_viatges:
                    camio_viatges.append([id_peticio])
                else:
                    continue  # No es pot assignar aquesta petició
            else:
                camio_viatges[-1].append(id_peticio)
    return estat


