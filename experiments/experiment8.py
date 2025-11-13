from aima3.search import hill_climbing
from implementacio.camions_problema import CamionsProblema
from implementacio.camions_parametres import ProblemParameters
from implementacio.camions_estat import generate_greedy_initial_state, generate_initial_state, generate_empty_initial_state
from implementacio.abia_Gasolina import Gasolineres, CentresDistribucio
import time


# ========================================
# EXPERIMENT ESPECIAL
# ========================================
# Configuració segons l'enunciat:
# - 10 centres de distribució
# - 1 camió per centre (multiplicitat = 1)
# - 100 gasolineres
# - 10 execucions amb seeds diferents

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
    # Generar les dades del problema amb seed diferent per cada execució
    gasolineres = Gasolineres(num_gasolineres=100, seed=1234 + i)
    centres = CentresDistribucio(num_centres=10, multiplicitat=1, seed=1234 + i)
    
    # Paràmetres del problema
    params = ProblemParameters(
        km=640,           # Màxim km per camió
        n_viatges=5,      # Màxim viatges per camió
        valor=1000,       # Valor base del dipòsit (€)
        cost_km=2,        # Cost per km recorregut (€/km)
        gasolineres=gasolineres,
        centres=centres
    )
    
    # Generar l'estat inicial (greedy)
    initial_state = generate_greedy_initial_state(params)
    
    # Crear el problema
    problema = CamionsProblema(initial_state)
    
    # Mesurar el temps d'execució en mil·lisegons
    temps_inici = time.perf_counter()
    
    # Executar Hill Climbing
    solucio = hill_climbing(problema)
    
    # Temps final
    temps_final = time.perf_counter()
    temps_ms = (temps_final - temps_inici) * 1000  # Convertir a mil·lisegons
    
    # Calcular el benefici de la solució
    ingressos = solucio.calcular_ingressos_servits()
    cost_km = solucio.calcular_cost_km()
    penalitzacio = solucio.calcular_penalitzacio_pendents()
    benefici = ingressos - cost_km - penalitzacio
    
    # Calcular altres mètriques
    peticions_servides_set = solucio._get_peticions_servides()
    peticions_servides = len(peticions_servides_set)
    peticions_totals = len(solucio.peticions_info)
    peticions_pendents = peticions_totals - peticions_servides
    
    # Calcular km totals
    km_totals = 0.0
    for id_camio, camio in enumerate(solucio.camions):
        for viatge in camio:
            km_totals += solucio._calcular_km_viatge(id_camio, viatge)
    
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

# Mostrar els resultats
print("=" * 70)
print("EXPERIMENT ESPECIAL - RESULTATS FINALS")
print(f"(Mitjana de {NUM_EXECUCIONS} execucions)")
print("=" * 70)
print(f"\nConfiguració del problema:")
print(f"  - Centres de distribució: 10")
print(f"  - Camions per centre: 1")
print(f"  - Total camions: 10")
print(f"  - Gasolineres: 100")
print(f"  - Seeds: 1234-{1234 + NUM_EXECUCIONS - 1}")
print(f"\n{'='*70}")
print(f"BENEFICI OBTINGUT: {benefici_mitja:.2f} €")
print(f"TEMPS D'EXECUCIÓ: {temps_ms_mitja:.2f} ms")
print(f"{'='*70}")
print(f"\nDetall del càlcul del benefici:")
print(f"  + Ingressos per peticions servides: {ingressos_mitja:.2f} €")
print(f"  - Cost dels km recorreguts: {cost_km_mitja:.2f} €")
print(f"  - Penalització per peticions pendents: {penalitzacio_mitja:.2f} €")
print(f"  {'─'*50}")
print(f"  = BENEFICI TOTAL: {benefici_mitja:.2f} €")
print("=" * 70)

# Informació addicional
print(f"\nInformació addicional de la solució:")
print(f"  - Peticions servides: {peticions_servides_mitja:.1f}/{peticions_totals_mitja:.1f}")
print(f"  - Peticions pendents: {peticions_pendents_mitja:.1f}")
print(f"  - Km totals recorreguts: {km_totals_mitja:.2f} km")

# Resum
print(f"\n{'='*70}")
print("RESUM:")
print(f"{'='*70}")
print(f"Benefici: {benefici_mitja:.2f} €")
print(f"Temps: {temps_ms_mitja:.2f} ms")
print(f"{'='*70}")
