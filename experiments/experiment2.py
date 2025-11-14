import random
import time
from implementacio.camions_estat import generate_initial_state, generate_greedy_initial_state, generate_empty_initial_state
from implementacio.camions_problema import CamionsProblema
from aima3.search import hill_climbing
import dataclasses
from implementacio.abia_Gasolina import Gasolineres, CentresDistribucio
import matplotlib.pyplot as plt
import numpy as np

# creem una classe de paràmetres per passar-los a les funcions d'estat inicial
@dataclasses.dataclass
class ProblemParameters:
    gasolineres: Gasolineres
    centres: CentresDistribucio
    n_viatges: int
    valor: float
    cost_km: float

seeds = [42, 123, 456, 789, 101112, 131415, 161718, 192021, 222324, 252627]
n_random_reps = 10
resultats = []

initial_states_funcs = {
    "ordenada": generate_initial_state,
    "greedy": generate_greedy_initial_state,
    "aleatoria": generate_initial_state  # això és important!
}

for estat_nom, func_estat in initial_states_funcs.items():
    for seed in seeds:
        gasolineres = Gasolineres(num_gasolineres=100, seed=seed)
        centres = CentresDistribucio(num_centres=5, multiplicitat=1, seed=seed+1)
        params = ProblemParameters(
            gasolineres=gasolineres,
            centres=centres,
            n_viatges=5,
            valor=100,
            cost_km=1
        )
        heuristiques_reps = []
        temps_reps = []
        ingressos_reps = []
        cost_reps = []
        penalitzacio_reps = []
        benefici_reps = []

        reps = n_random_reps if estat_nom == "aleatoria" else 1
        for _ in range(reps):
            estat = func_estat(params)
            problema = CamionsProblema(estat)
            inici = time.perf_counter_ns()
            solucio = hill_climbing(problema)
            temps = (time.perf_counter_ns() - inici) / 1e9
            ingressos = solucio.calcular_ingressos_servits()
            cost = solucio.calcular_cost_km()
            penalitzacio = solucio.calcular_penalitzacio_pendents()
            benefici = ingressos - (cost + penalitzacio)
            heuristiques_reps.append(solucio.heuristica())
            temps_reps.append(temps)
            ingressos_reps.append(ingressos)
            cost_reps.append(cost)
            penalitzacio_reps.append(penalitzacio)
            benefici_reps.append(benefici)

        resultats.append({
            "seed": seed,
            "inicialitzacio": estat_nom,
            "heuristica": np.mean(heuristiques_reps),
            "ingressos": np.mean(ingressos_reps),
            "cost": np.mean(cost_reps),
            "penalitzacio": np.mean(penalitzacio_reps),
            "benefici": np.mean(benefici_reps),
            "temps": np.mean(temps_reps),
        })

# Filtrar resultats per tipus d'inicialització
resultats_filtrats = {tipus: {k: [] for k in resultats[0].keys()} for tipus in initial_states_funcs.keys()}

for r in resultats:
    resultats_filtrats[r['inicialitzacio']]['seed'].append(r['seed'])
    resultats_filtrats[r['inicialitzacio']]['heuristica'].append(r['heuristica'])
    resultats_filtrats[r['inicialitzacio']]['ingressos'].append(r['ingressos'])
    resultats_filtrats[r['inicialitzacio']]['cost'].append(r['cost'])
    resultats_filtrats[r['inicialitzacio']]['penalitzacio'].append(r['penalitzacio'])
    resultats_filtrats[r['inicialitzacio']]['benefici'].append(r['benefici'])
    resultats_filtrats[r['inicialitzacio']]['temps'].append(r['temps'])

# Calcula les mitjanes per a cada tipus de solució inicial
mitjanes = []

for tipus in initial_states_funcs.keys():
    mitjanes.append({
        "inicialitzacio": tipus,
        "ingressos": np.mean(resultats_filtrats[tipus]["ingressos"]),
        "cost": np.mean(resultats_filtrats[tipus]["cost"]),
        "penalitzacio": np.mean(resultats_filtrats[tipus]["penalitzacio"]),
        "benefici": np.mean(resultats_filtrats[tipus]["benefici"]),
        "temps": np.mean(resultats_filtrats[tipus]["temps"]),
    })

# Imprimir taula amb mitjanes per cada solució inicial
print("RESULTATS EXPERIMENT: Influència de la solució inicial")
print("-" * 120)
print(f"{'Inicialitzacio':>15} | {'Ingressos':>10} | {'Cost':>10} | {'Penalitzacio':>12} | {'Benefici':>10} | {'Temps (s)':>10}")
print("-" * 120)
for r in mitjanes:
    print(f"{r['inicialitzacio']:>15} | "
          f"{r['ingressos']:>10.2f} | {r['cost']:>10.2f} | {r['penalitzacio']:>12.2f} | "
          f"{r['benefici']:>10.2f} | {r['temps']:>10.6f}")

# Generar gràfics de distribució de les variables
tipus = ['ordenada', 'greedy', 'aleatoria']
labels = ['Ordenada', 'Greedy', 'Aleatòria']

def extreu(atribut):
    return [ [r[atribut] for r in resultats if r['inicialitzacio'] == t] for t in tipus ]

atributs = [
    ('benefici', "Benefici (€)"),
    ('ingressos', "Ingressos (€)"),
    ('cost', "Cost (€)"),
    ('penalitzacio', "Penalització (€)"),
    ('temps', "Temps execució (s)")
]

for variable, ylabel in atributs:
    dades = extreu(variable)
    plt.figure(figsize=(8,5))
    plt.boxplot(dades, labels=labels)
    plt.ylabel(ylabel)
    plt.title(f"Distribució de {ylabel} per solució inicial")
    plt.grid(alpha=0.2)
    plt.show()
