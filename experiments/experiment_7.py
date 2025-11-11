# ============================================================
# EXPERIMENT DEFINITIU: efecte del límit de km (horari) sobre el benefici
# ============================================================

from aima3.search import hill_climbing
from camions_problema import CamionsProblema
from camions_parametres import ProblemParameters
from camions_operadors import swapCentres, mourePeticio
from abia_Gasolina import Gasolineres, CentresDistribucio
from camions_estat import StateRepresentation
import time
import matplotlib.pyplot as plt


# ============================================================
# 1️⃣ PATCH: nova heurística amb límit de km
# ============================================================

def heuristica_limit_km(self):
    ingressos = self.calcular_ingressos_servits()
    cost_km = self.calcular_cost_km()
    penalitzacio = self.calcular_penalitzacio_pendents()

    penalitzacio_km = 0
    for id_camio, camio in enumerate(self.camions):
        km_camio = sum(self._calcular_km_viatge(id_camio, v) for v in camio)
        if km_camio > self.params.km:
            penalitzacio_km += (km_camio - self.params.km) * 10

    benefici_total = ingressos - cost_km - penalitzacio - penalitzacio_km
    return -benefici_total


# ============================================================
# 2️⃣ NOVA FUNCIÓ: generar estat greedy respectant límit de km
# ============================================================

def generate_greedy_state_limit(params: ProblemParameters) -> StateRepresentation:
    estat = StateRepresentation(params)
    num_camions = len(params.centres.centres)
    num_peticions = len(estat.peticions_info)

    for i_peticio in range(num_peticions):
        id_gas = estat.gasolinera_per_peticio[i_peticio]
        gas = params.gasolineres.gasolineres[id_gas]
        coords_peticio = (gas.cx, gas.cy)

        millor_camio = None
        millor_distancia = float("inf")

        for id_camio in range(num_camions):
            centre = params.centres.centres[id_camio]
            coords_centre = (centre.cx, centre.cy)
            distancia = estat._manhattan(coords_peticio, coords_centre)
            # Calculem km actuals del camió
            km_camio = sum(estat._calcular_km_viatge(id_camio, v) for v in estat.camions[id_camio])
            # Només considerar si pot assumir aquest viatge dins del límit
            km_viatge_nou = estat._manhattan(coords_centre, coords_peticio) * 2
            if km_camio + km_viatge_nou <= params.km and distancia < millor_distancia:
                millor_camio = id_camio
                millor_distancia = distancia

        if millor_camio is not None:
            camio_viatges = estat.camions[millor_camio]
            if not camio_viatges or len(camio_viatges[-1]) >= 2:
                if len(camio_viatges) < params.n_viatges:
                    camio_viatges.append([i_peticio])
            else:
                camio_viatges[-1].append(i_peticio)
    return estat


# ============================================================
# Apliquem el patch a l'estat
# ============================================================
StateRepresentation.heuristica = heuristica_limit_km


# ============================================================
# 3️⃣ CONFIGURACIÓ DE L'EXPERIMENT
# ============================================================

gasolineres = Gasolineres(num_gasolineres=100, seed=1234)
centres = CentresDistribucio(num_centres=10, multiplicitat=1, seed=1234)

valor = 1000
cost_km = 2
n_viatges = 5

escenaris = {
    "Jornada reduïda (-1h)": 560,
    "Base (640 km)": 640,
    "Jornada ampliada (+1h)": 720,
}

resultats = []

# ============================================================
# 4️⃣ EXECUCIÓ
# ============================================================

for nom, km_max in escenaris.items():
    params = ProblemParameters(
        km=km_max,
        n_viatges=n_viatges,
        valor=valor,
        cost_km=cost_km,
        gasolineres=gasolineres,
        centres=centres,
    )

    # ✅ nova inicialització que respecta límit de km
    initial_state = generate_greedy_state_limit(params)
    problema = CamionsProblema(initial_state)

    start = time.time()
    solucio = hill_climbing(problema)
    temps = time.time() - start

    ingressos = solucio.calcular_ingressos_servits()
    cost = solucio.calcular_cost_km()
    penalitzacio = solucio.calcular_penalitzacio_pendents()
    penalitzacio_km = 0

    for id_camio, camio in enumerate(solucio.camions):
        km_camio = sum(solucio._calcular_km_viatge(id_camio, v) for v in camio)
        if km_camio > km_max:
            penalitzacio_km += (km_camio - km_max) * 10

    benefici = ingressos - cost - penalitzacio - penalitzacio_km

    resultats.append((nom, benefici, ingressos, cost, penalitzacio, penalitzacio_km, temps))


# ============================================================
# 5️⃣ MOSTRAR RESULTATS
# ============================================================

print("=" * 75)
print("EFECTE DE L'HORARI DE LES CISTERNE SOBRE EL BENEFICI (Hill Climbing)")
print("=" * 75)
for nom, b, i, c, p, pk, t in resultats:
    print(f"{nom:25} | Benefici: {b:10.2f} € | Temps: {t:6.2f}s")
    print(f"   Ingressos: {i:10.2f} €  | Cost km: {c:10.2f} €  "
          f"| Penalització: {p:8.2f} €  | Penalització km: {pk:8.2f} €")
print("=" * 75)

print("\nInterpretació:")
print(" - Si augmentem els km màxims, els camions poden fer més viatges → benefici ↑")
print(" - Si reduïm els km màxims, es limiten els viatges → benefici ↓")
print(" - Ara el límit de km s'aplica realment en l'assignació inicial.")
print("=" * 75)
# ============================================================
# 6️⃣ Gràfics comparatius 
# ============================================================

labels = [r["nom"] for r in resultats]

# --- Gràfic de benefici
beneficis = [r["benefici"] for r in resultats]
plt.figure(figsize=(8, 5))
plt.bar(labels, beneficis, color=["#e74c3c", "#f1c40f", "#2ecc71"])
plt.title("Impacte del límit de km sobre el benefici")
plt.ylabel("Benefici (€)")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.show()

# --- Gràfic de costos
costos = [r["cost"] for r in resultats]
plt.figure(figsize=(8, 5))
plt.bar(labels, costos, color=["#3498db", "#9b59b6", "#95a5a6"])
plt.title("Cost total dels km recorreguts segons el límit")
plt.ylabel("Cost (€)")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.show()

# --- Gràfic de peticions servides
peticions_percent = [100 * r["peticions_servides"] / r["peticions_totals"] for r in resultats]
plt.figure(figsize=(8, 5))
plt.bar(labels, peticions_percent, color=["#1abc9c", "#f39c12", "#e67e22"])
plt.title("Percentatge de peticions servides segons el límit de km")
plt.ylabel("% Peticions servides")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.show()