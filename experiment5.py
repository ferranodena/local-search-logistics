from aima3.search import hill_climbing
from camions_problema import CamionsProblema
from camions_parametres import ProblemParameters
from camions_estat import generate_greedy_initial_state
from abia_Gasolina import Gasolineres, CentresDistribucio
import time

# ----------------------------------------
# ESCENARI: 5 centres, 10 camions, 100 gasolineres
# ----------------------------------------
gasolineres = Gasolineres(num_gasolineres=100, seed=1234)
centres = CentresDistribucio(num_centres=5, multiplicitat=2, seed=1234)

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

# Resultats
print("="*70)
print("EXPERIMENT: 5 CENTRES, 10 CAMIONS, 100 GASOLINERES")
print("="*70)
print(f"Benefici total: {benefici:.2f} €")
print(f"  + Ingressos: {ingressos:.2f} €")
print(f"  - Cost km: {cost_km:.2f} €")
print(f"  - Penalització: {penalitzacio:.2f} €")
print("-"*70)
print(f"Km totals recorreguts: {km_totals:.2f} km")
print(f"Peticions servides: {peticions_servides}/{peticions_totals}")
print(f"Peticions pendents: {peticions_pendents}")
print(f"Temps d'execució: {temps_ms:.2f} ms")
print("="*70)
