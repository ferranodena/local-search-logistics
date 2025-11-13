from aima3.search import hill_climbing
from implementacio.camions_problema import CamionsProblema
from implementacio.camions_parametres import ProblemParameters
from implementacio.camions_estat import generate_greedy_initial_state
from implementacio.abia_Gasolina import Gasolineres, CentresDistribucio
import time


# ========================================================================
# EXPERIMENT 1: 5 centres, 10 camions (multiplicitat=2), 100 gasolineres
# ========================================================================

# Acumuladors per les mitjanes
benefici_total = 0
ingressos_total = 0
cost_km_total = 0
penalitzacio_total = 0
km_totals_acum = 0
peticions_servides_acum = 0
peticions_totals_acum = 0
peticions_pendents_acum = 0
temps_ms_acum = 0

NUM_EXECUCIONS = 10

for i in range(NUM_EXECUCIONS):
    gasolineres = Gasolineres(num_gasolineres=100, seed=1234 + i)
    centres = CentresDistribucio(num_centres=5, multiplicitat=2, seed=1234 + i)
    
    params = ProblemParameters(
        km=640,
        n_viatges=5,
        valor=1000,
        cost_km=2,
        gasolineres=gasolineres,
        centres=centres
    )
    
    # Generar estat inicial amb estratègia greedy
    initial_state = generate_greedy_initial_state(params)
    
    # Crear el problema
    problema = CamionsProblema(initial_state)
    
    # Mesurar el temps
    start = time.perf_counter()
    solucio = hill_climbing(problema)
    end = time.perf_counter()
    temps_ms = (end - start) * 1000
    
    # Calcular mètriques
    ingressos = solucio.calcular_ingressos_servits()
    cost_km = solucio.calcular_cost_km()
    penalitzacio = solucio.calcular_penalitzacio_pendents()
    benefici = ingressos - cost_km - penalitzacio
    
    # Peticions
    peticions_servides = len(solucio._get_peticions_servides())
    peticions_totals = len(solucio.peticions_info)
    peticions_pendents = peticions_totals - peticions_servides
    
    # Km totals recorreguts
    km_totals = sum(solucio._calcular_km_viatge(id_camio, viatge)
                    for id_camio, camio in enumerate(solucio.camions)
                    for viatge in camio)
    
    # Acumular
    benefici_total += benefici
    ingressos_total += ingressos
    cost_km_total += cost_km
    penalitzacio_total += penalitzacio
    km_totals_acum += km_totals
    peticions_servides_acum += peticions_servides
    peticions_totals_acum += peticions_totals
    peticions_pendents_acum += peticions_pendents
    temps_ms_acum += temps_ms

# Calcular mitjanes
benefici_mitja = benefici_total / NUM_EXECUCIONS
ingressos_mitja = ingressos_total / NUM_EXECUCIONS
cost_km_mitja = cost_km_total / NUM_EXECUCIONS
penalitzacio_mitja = penalitzacio_total / NUM_EXECUCIONS
km_totals_mitja = km_totals_acum / NUM_EXECUCIONS
peticions_servides_mitja = peticions_servides_acum / NUM_EXECUCIONS
peticions_totals_mitja = peticions_totals_acum / NUM_EXECUCIONS
peticions_pendents_mitja = peticions_pendents_acum / NUM_EXECUCIONS
temps_ms_mitja = temps_ms_acum / NUM_EXECUCIONS

# Resultats
print("="*70)
print("EXPERIMENT 1: 5 CENTRES, 10 CAMIONS, 100 GASOLINERES")
print(f"(Mitjana de {NUM_EXECUCIONS} execucions)")
print("="*70)
print(f"Benefici total: {benefici_mitja:.2f} €")
print(f"  + Ingressos: {ingressos_mitja:.2f} €")
print(f"  - Cost km: {cost_km_mitja:.2f} €")
print(f"  - Penalització: {penalitzacio_mitja:.2f} €")
print("-"*70)
print(f"Km totals recorreguts: {km_totals_mitja:.2f} km")
print(f"Peticions servides: {peticions_servides_mitja:.1f}/{peticions_totals_mitja:.1f}")
print(f"Peticions pendents: {peticions_pendents_mitja:.1f}")
print(f"Temps d'execució: {temps_ms_mitja:.2f} ms")
print("="*70)
print()


# ========================================================================
# EXPERIMENT 2: 10 centres, 10 camions (multiplicitat=1), 100 gasolineres
# ========================================================================

# Acumuladors per les mitjanes
benefici_total = 0
ingressos_total = 0
cost_km_total = 0
penalitzacio_total = 0
km_totals_acum = 0
peticions_servides_acum = 0
peticions_totals_acum = 0
peticions_pendents_acum = 0
temps_ms_acum = 0

for i in range(NUM_EXECUCIONS):
    gasolineres = Gasolineres(num_gasolineres=100, seed=1234 + i)
    centres = CentresDistribucio(num_centres=10, multiplicitat=1, seed=1234 + i)
    
    params = ProblemParameters(
        km=640,
        n_viatges=5,
        valor=1000,
        cost_km=2,
        gasolineres=gasolineres,
        centres=centres
    )
    
    # Generar estat inicial amb estratègia greedy
    initial_state = generate_greedy_initial_state(params)
    
    # Crear el problema
    problema = CamionsProblema(initial_state)
    
    # Mesurar el temps
    start = time.perf_counter()
    solucio = hill_climbing(problema)
    end = time.perf_counter()
    temps_ms = (end - start) * 1000
    
    # Calcular mètriques
    ingressos = solucio.calcular_ingressos_servits()
    cost_km = solucio.calcular_cost_km()
    penalitzacio = solucio.calcular_penalitzacio_pendents()
    benefici = ingressos - cost_km - penalitzacio
    
    # Peticions
    peticions_servides = len(solucio._get_peticions_servides())
    peticions_totals = len(solucio.peticions_info)
    peticions_pendents = peticions_totals - peticions_servides
    
    # Km totals recorreguts
    km_totals = sum(solucio._calcular_km_viatge(id_camio, viatge)
                    for id_camio, camio in enumerate(solucio.camions)
                    for viatge in camio)
    
    # Acumular
    benefici_total += benefici
    ingressos_total += ingressos
    cost_km_total += cost_km
    penalitzacio_total += penalitzacio
    km_totals_acum += km_totals
    peticions_servides_acum += peticions_servides
    peticions_totals_acum += peticions_totals
    peticions_pendents_acum += peticions_pendents
    temps_ms_acum += temps_ms

# Calcular mitjanes
benefici_mitja = benefici_total / NUM_EXECUCIONS
ingressos_mitja = ingressos_total / NUM_EXECUCIONS
cost_km_mitja = cost_km_total / NUM_EXECUCIONS
penalitzacio_mitja = penalitzacio_total / NUM_EXECUCIONS
km_totals_mitja = km_totals_acum / NUM_EXECUCIONS
peticions_servides_mitja = peticions_servides_acum / NUM_EXECUCIONS
peticions_totals_mitja = peticions_totals_acum / NUM_EXECUCIONS
peticions_pendents_mitja = peticions_pendents_acum / NUM_EXECUCIONS
temps_ms_mitja = temps_ms_acum / NUM_EXECUCIONS

# Resultats
print("="*70)
print("EXPERIMENT 2: 10 CENTRES, 10 CAMIONS, 100 GASOLINERES")
print(f"(Mitjana de {NUM_EXECUCIONS} execucions)")
print("="*70)
print(f"Benefici total: {benefici_mitja:.2f} €")
print(f"  + Ingressos: {ingressos_mitja:.2f} €")
print(f"  - Cost km: {cost_km_mitja:.2f} €")
print(f"  - Penalització: {penalitzacio_mitja:.2f} €")
print("-"*70)
print(f"Km totals recorreguts: {km_totals_mitja:.2f} km")
print(f"Peticions servides: {peticions_servides_mitja:.1f}/{peticions_totals_mitja:.1f}")
print(f"Peticions pendents: {peticions_pendents_mitja:.1f}")
print(f"Temps d'execució: {temps_ms_mitja:.2f} ms")
print("="*70)
