import time
import random
import matplotlib.pyplot as plt
import pandas as pd

from aima3.search import hill_climbing, simulated_annealing, exp_schedule
from implementacio.camions_problema import CamionsProblema
from implementacio.camions_parametres import ProblemParameters
from implementacio.camions_estat import generate_greedy_initial_state
from implementacio.abia_Gasolina import Gasolineres, CentresDistribucio


# ---------------- Paràmetres generals ----------------

NUM_EXECUCIONS = 10
NUM_GASOLINERES = 100
NUM_CENTRES = 10

SA_K = 0.005
SA_LAM = 0.0005
SA_LIMIT = 1000

# Límits comuns per als gràfics
X_MIN, X_MAX = 1, NUM_EXECUCIONS
Y_MIN, Y_MAX = 0, 40000  # 0 .. 40000 ms


# ---------------- Helpers per crear problema ----------------

def crea_problema(seed: int, use_lazy: bool) -> CamionsProblema:
    """Crea una instància de CamionsProblema amb estat greedy i flag per triar el generador d'accions."""
    random.seed(seed)

    gas = Gasolineres(num_gasolineres=NUM_GASOLINERES, seed=seed)
    centres = CentresDistribucio(num_centres=NUM_CENTRES, multiplicitat=1, seed=seed)

    params = ProblemParameters(
        km=640,
        n_viatges=5,
        valor=1000,
        cost_km=2,
        gasolineres=gas,
        centres=centres,
    )

    initial_state = generate_greedy_initial_state(params)
    problema = CamionsProblema(initial_state)

    # Dins CamionsProblema.actions(state) has de mirar aquest flag:
    # if getattr(self, "use_lazy_actions", False):
    #     return state.generate_actions_lazy()
    # else:
    #     return state.generate_all_actions()
    problema.use_lazy_actions = use_lazy

    return problema


def benefici(state):
    return (
        state.calcular_ingressos_servits()
        - state.calcular_cost_km()
        - state.calcular_penalitzacio_pendents()
    )


def executa_bloc(use_lazy: bool):
    """Executa 10 rèpliques amb HC i SA, usant all o lazy segons use_lazy."""
    registres = []

    for i in range(NUM_EXECUCIONS):
        seed = 1234 + i

        # ---------- HC ----------
        problema_hc = crea_problema(seed, use_lazy=use_lazy)
        t0 = time.perf_counter()
        sol_hc = hill_climbing(problema_hc)
        t1 = time.perf_counter()
        temps_hc = (t1 - t0) * 1000.0
        ben_hc = benefici(sol_hc)

        # ---------- SA ----------
        problema_sa = crea_problema(seed, use_lazy=use_lazy)
        schedule = exp_schedule(k=SA_K, lam=SA_LAM, limit=SA_LIMIT)
        t0 = time.perf_counter()
        sol_sa = simulated_annealing(problema_sa, schedule)
        t1 = time.perf_counter()
        temps_sa = (t1 - t0) * 1000.0
        ben_sa = benefici(sol_sa)

        registres.append({
            "Execució": i + 1,
            "HC_Benefici": ben_hc,
            "HC_Temps_ms": temps_hc,
            "SA_Benefici": ben_sa,
            "SA_Temps_ms": temps_sa,
        })

    df = pd.DataFrame(registres)
    mitjanes = df[["HC_Benefici", "HC_Temps_ms", "SA_Benefici", "SA_Temps_ms"]].mean()
    return df, mitjanes


def dibuixa_grafic_temps(df, title, filename):
    """Dibuixa el gràfic de temps per rèplica amb escala comuna."""
    x = df["Execució"]

    plt.figure(figsize=(10, 5))
    plt.plot(x, df["HC_Temps_ms"], marker="o", label="HC")
    plt.plot(x, df["SA_Temps_ms"], marker="s", label="SA")
    plt.title(title)
    plt.xlabel("Rèplica")
    plt.ylabel("Temps (ms)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)

    # Escala comuna
    plt.xlim(X_MIN, X_MAX)
    plt.ylim(Y_MIN, Y_MAX)

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()


# ---------------- Experiment complet ----------------

def experiment_all_vs_lazy():
    # Bloc 1: generate_all_actions
    df_all, mitjanes_all = executa_bloc(use_lazy=False)
    print("\n=== Resultats amb generate_all_actions ===")
    print(df_all)
    print("\nMitjanes all:")
    print(mitjanes_all)

    dibuixa_grafic_temps(
        df_all,
        "Temps d'execució per rèplica (HC vs SA) amb generate_all_actions",
        "temps_all.png",
    )

    # Bloc 2: generate_actions_lazy
    df_lazy, mitjanes_lazy = executa_bloc(use_lazy=True)
    print("\n=== Resultats amb generate_actions_lazy ===")
    print(df_lazy)
    print("\nMitjanes lazy:")
    print(mitjanes_lazy)

    dibuixa_grafic_temps(
        df_lazy,
        "Temps d'execució per rèplica (HC vs SA) amb generate_actions_lazy",
        "temps_lazy.png",
    )


if __name__ == "__main__":
    experiment_all_vs_lazy()