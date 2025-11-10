from aima3.search import hill_climbing
from camions_problema import CamionsProblema
from camions_parametres import ProblemParameters
from camions_estat import generate_greedy_initial_state, generate_initial_state, generate_empty_initial_state
from abia_Gasolina import Gasolineres, CentresDistribucio
import time

# ========================================
# EXPERIMENT 6
# ========================================
# Configuració segons l'enunciat:
# - 10 centres de distribució
# - 1 camió per centre (multiplicitat = 1)
# - 100 gasolineres
# - Seed 1234 per gasolineres i centres

# Generar les dades del problema amb seed 1234
gasolineres = Gasolineres(num_gasolineres=100, seed=1234)
centres = CentresDistribucio(num_centres=10, multiplicitat=1, seed=1234)

# Paràmetres del problema (segons els  teus experiments)
params = ProblemParameters(
    km=640,           # Màxim km per camió
    n_viatges=5,      # Màxim viatges per camió
    valor=1000,       # Valor base del dipòsit (€)
    cost_km=2,        # Cost per km recorregut (€/km) --> Això és el que s'ha d'anar canviant
    gasolineres=gasolineres,
    centres=centres
)

# ============================================
# TRIAR LA MILLOR INICIALITZACIÓ DELS EXPERIMENTS 1 i 2
# ============================================
# Segons els teus resultats dels experiments, descomenta la línia adequada:

# Opció 1: Inicialització buida (empty)
# initial_state = generate_empty_initial_state(params)

# Opció 2: Inicialització ordenada per prioritat (random)
# initial_state = generate_initial_state(params)

# Opció 3: Inicialització greedy (la més comuna si va donar bons resultats)
initial_state = generate_greedy_initial_state(params)

# Crear el problema
problema = CamionsProblema(initial_state)

# Mesurar el temps d'execució en mil·lisegons
temps_inici = time.perf_counter()

# Executar Hill Climbing (segons els teus experiments)
solucio = hill_climbing(problema)

# Temps final
temps_final = time.perf_counter()
temps_ms = (temps_final - temps_inici) * 1000  # Convertir a mil·lisegonds

# Calcular el benefici de la solució
# Benefici = Ingressos - Cost dels km - Penalització
ingressos = solucio.calcular_ingressos_servits()
cost_km = solucio.calcular_cost_km()
penalitzacio = solucio.calcular_penalitzacio_pendents()

# Benefici total segons l'enunciat:
# "El beneficio lo mediremos como lo ganado con las peticiones que se sirven, 
#  menos el coste de los kilómetros recorridos"
benefici = ingressos - cost_km - penalitzacio

# Calcular altres mètriques útils
peticions_servides_set = solucio._get_peticions_servides()
peticions_servides = len(peticions_servides_set)
peticions_totals = len(solucio.peticions_info)
peticions_pendents = peticions_totals - peticions_servides

# Calcular km totals
km_totals = 0.0
for id_camio, camio in enumerate(solucio.camions):
    for viatge in camio:
        km_totals += solucio._calcular_km_viatge(id_camio, viatge)

# Mostrar els resultats per enviar al professor
print("=" * 70)
print("EXPERIMENT ESPECIAL - RESULTATS FINALS")
print("=" * 70)
print(f"\nConfiguració del problema:")
print(f"  - Centres de distribució: 10")
print(f"  - Camions per centre: 1")
print(f"  - Total camions: 10")
print(f"  - Gasolineres: 100")
print(f"  - Seed: 1234")
print(f"\n{'='*70}")
print(f"BENEFICI OBTINGUT: {benefici:.2f} €")
print(f"TEMPS D'EXECUCIÓ: {temps_ms:.2f} ms")
print(f"{'='*70}")
print(f"\nDetall del càlcul del benefici:")
print(f"  + Ingressos per peticions servides: {ingressos:.2f} €")
print(f"  - Cost dels km recorreguts: {cost_km:.2f} €")
print(f"  - Penalització per peticions pendents: {penalitzacio:.2f} €")
print(f"  {'─'*50}")
print(f"  = BENEFICI TOTAL: {benefici:.2f} €")
print("=" * 70)

# Informació addicional (opcional, per verificar)
print(f"\nInformació addicional de la solució:")
print(f"  - Peticions servides: {peticions_servides}/{peticions_totals}")
print(f"  - Peticions pendents: {peticions_pendents}")
print(f"  - Km totals recorreguts: {km_totals:.2f} km")

# Per verificar l'execució al laboratori
print(f"\n{'='*70}")
print("RESUM PER ENVIAR AL PROFESSOR:")
print(f"{'='*70}")
print(f"Benefici: {benefici:.2f} €")
print(f"Temps: {temps_ms:.2f} ms")
print(f"{'='*70}")

# Opcional: mostra la solució completa per debugar
# print("\n" + str(solucio))

