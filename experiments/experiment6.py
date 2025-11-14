from aima3.search import hill_climbing
from implementacio.camions_problema import CamionsProblema
from implementacio.camions_parametres import ProblemParameters
from implementacio.abia_Gasolina import Gasolineres, CentresDistribucio
from implementacio.camions_estat import StateRepresentation
import numpy as np
import matplotlib.pyplot as plt

# Paràmetres escenari base
km_max = 640
n_viatges = 5
valor = 1000
num_camions = 10
num_gasolineres = 100
multiplicitat = 1

cost_kms = [2*(2**i) for i in range(6)]
seeds = [1234 + i for i in range(10)]

def generate_greedy_state_limit(params: ProblemParameters):
    estat = StateRepresentation(params)
    num_camions = len(params.centres.centres)
    num_peticions = len(estat.peticions_info)
    for i_peticio in range(num_peticions):
        id_gas = estat.gasolinera_per_peticio[i_peticio]
        gas = params.gasolineres.gasolineres[id_gas]
        coords_peticio = (gas.cx, gas.cy)
        dies_pendents = estat.peticions_info[i_peticio]
        factor = estat._factor_de_preu(dies_pendents)
        preu_peticio = params.valor * factor
        millor_camio = None
        millor_distancia = float("inf")
        millor_viatge_nou = False
        millor_cost_total = float("inf")
        for id_camio in range(num_camions):
            centre = params.centres.centres[id_camio]
            coords_centre = (centre.cx, centre.cy)
            distancia = estat._manhattan(coords_peticio, coords_centre)
            camio_viatges = estat.camions[id_camio]
            afegir_com_nou = (not camio_viatges or len(camio_viatges[-1]) >= 2)
            num_viatges = len(camio_viatges) + (1 if afegir_com_nou else 0)
            km_camio = sum(estat._calcular_km_viatge(id_camio, v) for v in camio_viatges)
            km_viatge_nou = estat._manhattan(coords_centre, coords_peticio) * 2 if afegir_com_nou else \
                estat._calcular_km_viatge(id_camio, camio_viatges[-1] + [i_peticio])
            cost_nou = params.cost_km * km_viatge_nou
            if num_viatges <= params.n_viatges and km_camio + km_viatge_nou <= params.km:
                if preu_peticio >= cost_nou:
                    if distancia < millor_distancia:
                        millor_camio = id_camio
                        millor_distancia = distancia
                        millor_viatge_nou = afegir_com_nou
                        millor_cost_total = cost_nou
        if millor_camio is not None:
            camio_viatges = estat.camions[millor_camio]
            if millor_viatge_nou:
                camio_viatges.append([i_peticio])
            else:
                camio_viatges[-1].append(i_peticio)
    return estat

resultats = {cost_km: [] for cost_km in cost_kms}
pendents_temps = {cost_km: [] for cost_km in cost_kms}
benefici = {cost_km: [] for cost_km in cost_kms}

for cost_km in cost_kms:
    for seed in seeds:
        gasolineres = Gasolineres(num_gasolineres=num_gasolineres, seed=seed)
        centres = CentresDistribucio(num_centres=num_camions, multiplicitat=multiplicitat, seed=seed)
        params = ProblemParameters(
            km=km_max,
            n_viatges=n_viatges,
            valor=valor,
            cost_km=cost_km,
            gasolineres=gasolineres,
            centres=centres,
        )
        initial_state = generate_greedy_state_limit(params)
        problema = CamionsProblema(initial_state)
        solucio = hill_climbing(problema)
        peticions_servides = sum([len([item for viatge in camio for item in viatge]) for camio in solucio.camions])
        peticions_totals = len(solucio.peticions_info)
        percentatge = 100 * peticions_servides / peticions_totals if peticions_totals > 0 else 0
        dies_pendents_servits = []
        for camio in solucio.camions:
            for viatge in camio:
                for idx in viatge:
                    dies_pendents_servits.append(solucio.peticions_info[idx])
        hist = np.histogram(dies_pendents_servits, bins=[-0.5,0.5,1.5,2.5,3.5,100], density=True)[0]
        resultats[cost_km].append(percentatge)
        pendents_temps[cost_km].append(hist)
        # Calcula benefici
        ingressos = solucio.calcular_ingressos_servits()
        cost = solucio.calcular_cost_km()
        penalitzacio = solucio.calcular_penalitzacio_pendents()
        penalitzacio_km = 0
        for id_camio, camio in enumerate(solucio.camions):
            km_camio = sum(solucio._calcular_km_viatge(id_camio, v) for v in camio)
            if km_camio > km_max:
                penalitzacio_km += (km_camio - km_max) * 10
        benefici_this = ingressos - cost - penalitzacio - penalitzacio_km
        benefici[cost_km].append(benefici_this)

print("Cost/km | %Servides |  Benefici")
print("-------------------------------")
for cost_km in cost_kms:
    pct = np.mean(resultats[cost_km])
    mitja_benefici = np.mean(benefici[cost_km])
    print(f"{cost_km:6}  | {pct:8.2f}  | {mitja_benefici:9.2f}")


cost_labels = [str(c) for c in cost_kms]
# Boxplot % servides
plt.figure(figsize=(8, 5))
dades_servides = [resultats[c] for c in cost_kms]
plt.boxplot(dades_servides, labels=cost_labels, patch_artist=True)
plt.title("% Peticions servides vs Cost/km")
plt.ylabel("% Peticions servides")
plt.xlabel("Cost/km")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.show()

# Boxplot benefici
plt.figure(figsize=(8, 5))
dades_benefici = [benefici[c] for c in cost_kms]
plt.boxplot(dades_benefici, labels=cost_labels, patch_artist=True)
plt.title("Benefici vs Cost/km")
plt.ylabel("Benefici (€)")
plt.xlabel("Cost/km")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.show()

