import random
import time
from camions_estat import generate_initial_state, generate_greedy_initial_state, generate_empty_initial_state
from camions_problema import CamionsProblema
from aima3.search import simulated_annealing, hill_climbing
import dataclasses
from abia_Gasolina import Gasolinera, Gasolineres, Distribucio, CentresDistribucio
import matplotlib.pyplot as plt
import numpy as np
from timeit import timeit
@dataclasses.dataclass


class ProblemParameters:
    gasolineres: Gasolineres
    centres: CentresDistribucio
    n_viatges: int
    valor: float
    cost_km: float
# --------------------------------------------
# Seeds per les rèpliques
seeds = [42, 123, 456, 789, 101112, 131415, 161718, 192021, 222324, 252627]

n_random_reps = 10

resultats = []

# Tipus d'estat inicial
initial_states_funcs = {
    "empty": generate_empty_initial_state,
    "random": generate_initial_state,
    "greedy": generate_greedy_initial_state
}

for estat_nom, func_estat in initial_states_funcs.items():
    print(f"=== Estat inicial: {estat_nom} ===")
    

    for i, seed in enumerate(seeds):
        # Generar gasolineres i centres amb seed diferent cada rèplica
        gasolineres = Gasolineres(num_gasolineres=100, seed=seed)
        centres = CentresDistribucio(num_centres=5, multiplicitat=1, seed=seed+1)

        # Paràmetres del problema
        params = ProblemParameters(
        gasolineres=gasolineres,
        centres=centres,
        n_viatges=5,
        valor=100,
        cost_km=1
)

        # Solució inicial ordenada
        estat_ordenat = generate_initial_state(params)
        problema_ordenat = CamionsProblema(estat_ordenat)

        inici = time.perf_counter_ns()
        solucio_ordenada = hill_climbing(problema_ordenat)
        temps_ordenat = (time.perf_counter_ns() - inici)/1e9

        resultats.append({
        'seed': seed,
        'inicialitzacio': 'ordenada',
        'heuristica': solucio_ordenada.heuristica(),
        'temps': temps_ordenat
        })

        # Solució inicial greedy
        estat_greedy = generate_greedy_initial_state(params)
        problema_greedy = CamionsProblema(estat_greedy)

        inici = time.perf_counter_ns()
        solucio_greedy = hill_climbing(problema_greedy)
        temps_greedy = (time.perf_counter_ns() - inici)/1e9

        resultats.append({
        "seed": seed,
        "inicialitzacio": "greedy",
        "heuristica": solucio_greedy.heuristica(),
        "temps": temps_greedy
        })

        # Solució inicial aleatòria
        heuristiques_aleatories = []
        temps_aleatori_list = []

        
        for _ in range(n_random_reps):
            estat_aleatori = generate_empty_initial_state(params)
            problema_aleatori = CamionsProblema(estat_aleatori)

            inici = time.perf_counter_ns()
            solucio_aleatoria = hill_climbing(problema_aleatori)
            temps_aleatori = (time.perf_counter_ns() - inici)/1e9

            heuristiques_aleatories.append(solucio_aleatoria.heuristica())
            temps_aleatori_list.append(temps_aleatori)

        # Mitjana dels resultats aleatoris
        heuristica_mitjana = sum(heuristiques_aleatories) / n_random_reps
        temps_mig = sum(temps_aleatori_list) / n_random_reps

        resultats.append({
            "seed": seed,
            "inicialitzacio": "aleatoria",
            "heuristica": heuristica_mitjana,
            "temps": temps_mig
        })
    
# --------------------------------------------
# Mostrar resultats
# --------------------------------------------
print("RESULTATS EXPERIMENT: Influència de la solució inicial")
print("-" * 80)
for r in resultats:
    print(f"Seed: {r['seed']:>8} | Inicialitzacio: {r['inicialitzacio']:>9} | "
          f"Heuristica final: {r['heuristica']:.2f} | Temps (s): {r['temps']:.9f}")

# Preparar dades pels gràfics
ordenat_times = [r['temps'] for r in resultats if r['inicialitzacio'] == 'ordenada']
greedy_times = [r['temps'] for r in resultats if r['inicialitzacio'] == 'greedy']
random_times = [r['temps'] for r in resultats if r['inicialitzacio'] == 'aleatoria']

ordenat_heur = [r['heuristica'] for r in resultats if r['inicialitzacio'] == 'ordenada']
greedy_heur = [r['heuristica'] for r in resultats if r['inicialitzacio'] == 'greedy']
random_heur = [r['heuristica'] for r in resultats if r['inicialitzacio'] == 'aleatoria']

# Gràfic de temps d'execució
plt.figure(figsize=(10, 6))
labels = ['Ordenat', 'Greedy', 'Aleatori']
times = [np.mean(ordenat_times), np.mean(greedy_times), np.mean(random_times)]
std_times = [np.std(ordenat_times), np.std(greedy_times), np.std(random_times)]

plt.bar(labels, times, yerr=std_times, capsize=5)
plt.title('Temps mitjà d\'execució per tipus d\'inicialització')
plt.ylabel('Temps (segons)')
plt.grid(True, alpha=0.3)
plt.show()

# Gràfic d'heurístiques
plt.figure(figsize=(10, 6))
heurs = [np.mean(ordenat_heur), np.mean(greedy_heur), np.mean(random_heur)]
std_heurs = [np.std(ordenat_heur), np.std(greedy_heur), np.std(random_heur)]

plt.bar(labels, heurs, yerr=std_heurs, capsize=5)
plt.title('Valor heurístic mitjà per tipus d\'inicialització')
plt.ylabel('Valor heurístic')
plt.grid(True, alpha=0.3)
plt.show()

# Box plot per comparar distribucions
plt.figure(figsize=(10, 6))
data = [ordenat_times, greedy_times, random_times]
plt.boxplot(data, labels=labels)
plt.title('Distribució dels temps d\'execució')
plt.ylabel('Temps (segons)')
plt.grid(True, alpha=0.3)
plt.show()
