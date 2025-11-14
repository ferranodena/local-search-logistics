from aima3.search import hill_climbing
from implementacio.camions_problema import CamionsProblema
from implementacio.camions_parametres import ProblemParameters
from implementacio.camions_estat import generate_greedy_initial_state
from implementacio.abia_Gasolina import Gasolineres, CentresDistribucio
import time

# Configuració bàsica del problema
num_gasolineres = 100
num_centres = 10
km_max = 640
n_viatges = 5
valor_diposits = 1000
cost_km = 2
num_repliques = 10  # Nombre de rèpliques per experiment

# Definició de conjunts d'operadors a provar
conjunts_operadors = {
    "swapCentres": ["swapCentres"],
    "mourePeticio": ["mourePeticio"],
    "swap+moure": ["swapCentres", "mourePeticio"],
    "swap+moure+intercanvia": ["swapCentres", "mourePeticio", "intercanviaPeticio"]
}

# Experiments amb rèpliques
for nom_conjunt, operadors in conjunts_operadors.items():
    print(f"\n=== Experiment amb operadors: {nom_conjunt} ===")
    
    for replica in range(num_repliques):
        seed = 1234 + replica  # Diferent seed per rèplica
        print(f"\n--- Rèplica {replica + 1} | seed={seed} ---")
        
        # Crear gasolineres i centres amb seed diferent
        gasolineres = Gasolineres(num_gasolineres=num_gasolineres, seed=seed)
        centres = CentresDistribucio(num_centres=num_centres, multiplicitat=1, seed=seed)
        
        # Paràmetres del problema
        params = ProblemParameters(
            km=km_max,
            n_viatges=n_viatges,
            valor=valor_diposits,
            cost_km=cost_km,
            gasolineres=gasolineres,
            centres=centres
        )
        
        # Estat inicial greedy
        initial_state = generate_greedy_initial_state(params)
        
        # Crear instància del problema i assignar operadors
        problema = CamionsProblema(initial_state)
        problema.operadors = operadors
        
        # Executar Hill Climbing
        start = time.perf_counter()
        solucio = hill_climbing(problema)
        end = time.perf_counter()
        temps_ms = (end - start) * 1000
        
        # Calcular beneficis
        ingressos = solucio.calcular_ingressos_servits()
        cost_total_km = solucio.calcular_cost_km()
        penalitzacio = solucio.calcular_penalitzacio_pendents()
        benefici = ingressos - cost_total_km - penalitzacio
        
        peticions_servides = len(solucio._get_peticions_servides())
        peticions_totals = len(solucio.peticions_info)
        peticions_pendents = peticions_totals - peticions_servides
        
        km_totals = sum(solucio._calcular_km_viatge(id_camio, viatge)
                        for id_camio, camio in enumerate(solucio.camions)
                        for viatge in camio)
        
        # Mostrar resultats
        print(f"Benefici obtingut: {benefici:.2f} €")
        print(f"Temps d'execució: {temps_ms:.2f} ms")
        print(f"Peticions servides: {peticions_servides}/{peticions_totals}")
        print(f"Peticions pendents: {peticions_pendents}")
        print(f"Km totals recorreguts: {km_totals:.2f} km")
        print("-" * 70)
