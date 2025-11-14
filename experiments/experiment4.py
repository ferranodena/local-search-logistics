from aima3.search import hill_climbing, simulated_annealing
from implementacio.camions_problema import CamionsProblema
from implementacio.camions_parametres import ProblemParameters
from implementacio.camions_estat import generate_greedy_initial_state 
from implementacio.abia_Gasolina import Gasolineres, CentresDistribucio
import time
import matplotlib.pyplot as plt
import copy



# Configuració de l'experiment
seed = 1234  # Seed fix per reproducibilitat
n_repliques = 3  # Nombre de rèpliques per cada mida 


# Paràmetres del problema (constants)
KM_MAX = 640
N_VIATGES = 5
VALOR_DIPOSITIT = 1000
COST_KM = 2
MULTIPLICITAT = 1  # Camions per centre


# Paràmetres òptims de Simulated Annealing (obtinguts de l'Experiment 3)
SA_LIMIT = 1000
SA_K = 1
SA_LAMBDA = 0.001


# Mides del problema a provar (centres:gasolineres en proporció 10:100)
mides = [
    (10, 100),
    (20, 200),
    (30, 300),
    (40, 400),
    (50, 500),
]


resultats = []


print("=" * 80)
print("EXPERIMENT 4: ESCALABILITAT - TEMPS D'EXECUCIÓ vs MIDA DEL PROBLEMA")
print("=" * 80)
print(f"Proporció centres:gasolineres = 10:100")
print(f"Nombre de rèpliques per mida: {n_repliques}")
print(f"Seed: {seed}")
print(f"Paràmetres SA: limit={SA_LIMIT}, k={SA_K}, lambda={SA_LAMBDA}")
print("=" * 80)


for num_centres, num_gasolineres in mides:
    print(f"\nProcessant mida: {num_centres} centres, {num_gasolineres} gasolineres...")
    
    temps_hc_list = []
    temps_sa_list = []
    benefici_hc_list = []
    benefici_sa_list = []
    
    for replica in range(n_repliques):
        # Generar dades amb seed diferent per cada rèplica
        seed_replica = seed + replica
        gasolineres = Gasolineres(num_gasolineres=num_gasolineres, seed=seed_replica)
        centres = CentresDistribucio(num_centres=num_centres, multiplicitat=MULTIPLICITAT, seed=seed_replica)
        
        params = ProblemParameters(
            km=KM_MAX,
            n_viatges=N_VIATGES,
            valor=VALOR_DIPOSITIT,
            cost_km=COST_KM,
            gasolineres=gasolineres,
            centres=centres
        )
        
        # Generar estat inicial BASE
        initial_state_base = generate_greedy_initial_state(params)
        

        initial_state_hc = copy.deepcopy(initial_state_base)
        initial_state_sa = copy.deepcopy(initial_state_base)
        
        # HILL CLIMBING
        problema_hc = CamionsProblema(initial_state_hc)
        temps_inici_hc = time.perf_counter()
        solucio_hc = hill_climbing(problema_hc)
        temps_final_hc = time.perf_counter()
        temps_hc = (temps_final_hc - temps_inici_hc) * 1000  # ms
        
        # Calcular benefici
        ingressos_hc = solucio_hc.calcular_ingressos_servits()
        cost_km_hc = solucio_hc.calcular_cost_km()
        penalitzacio_hc = solucio_hc.calcular_penalitzacio_pendents()
        benefici_hc = ingressos_hc - cost_km_hc - penalitzacio_hc
        
        temps_hc_list.append(temps_hc)
        benefici_hc_list.append(benefici_hc)
        
        # SIMULATED ANNEALING
        problema_sa = CamionsProblema(initial_state_sa)

        # Crear funció de schedule que retorna 0 després de SA_LIMIT iteracions
        def sa_schedule(t):
            if t > SA_LIMIT:
                return 0  # Això farà que l'algorisme s'aturi
            temp = SA_K * (SA_LAMBDA ** t)
            return temp if temp > 0.01 else 0

        temps_inici_sa = time.perf_counter()
        solucio_sa = simulated_annealing(problema_sa, schedule=sa_schedule)
        temps_final_sa = time.perf_counter()
        temps_sa = (temps_final_sa - temps_inici_sa) * 1000  # ms
        
        # Calcular benefici
        ingressos_sa = solucio_sa.calcular_ingressos_servits()
        cost_km_sa = solucio_sa.calcular_cost_km()
        penalitzacio_sa = solucio_sa.calcular_penalitzacio_pendents()
        benefici_sa = ingressos_sa - cost_km_sa - penalitzacio_sa
        
        temps_sa_list.append(temps_sa)
        benefici_sa_list.append(benefici_sa)
        
        print(f"  Rèplica {replica + 1}/{n_repliques} completada")
    
    # Calcular mitjanes i desviacions estàndard
    temps_hc_mitjana = sum(temps_hc_list) / len(temps_hc_list)
    temps_sa_mitjana = sum(temps_sa_list) / len(temps_sa_list)
    benefici_hc_mitjana = sum(benefici_hc_list) / len(benefici_hc_list)
    benefici_sa_mitjana = sum(benefici_sa_list) / len(benefici_sa_list)
    
    # Calcular desviacions estàndard
    import math
    temps_hc_std = math.sqrt(sum((x - temps_hc_mitjana)**2 for x in temps_hc_list) / len(temps_hc_list))
    temps_sa_std = math.sqrt(sum((x - temps_sa_mitjana)**2 for x in temps_sa_list) / len(temps_sa_list))
    benefici_hc_std = math.sqrt(sum((x - benefici_hc_mitjana)**2 for x in benefici_hc_list) / len(benefici_hc_list))
    benefici_sa_std = math.sqrt(sum((x - benefici_sa_mitjana)**2 for x in benefici_sa_list) / len(benefici_sa_list))
    
    # Emmagatzemar resultats
    resultats.append({
        'num_centres': num_centres,
        'num_gasolineres': num_gasolineres,
        'temps_hc_ms': temps_hc_mitjana,
        'temps_hc_std': temps_hc_std,
        'temps_sa_ms': temps_sa_mitjana,
        'temps_sa_std': temps_sa_std,
        'benefici_hc': benefici_hc_mitjana,
        'benefici_hc_std': benefici_hc_std,
        'benefici_sa': benefici_sa_mitjana,
        'benefici_sa_std': benefici_sa_std
    })
    
    print(f"  -> HC: {temps_hc_mitjana:.2f} ± {temps_hc_std:.2f} ms, Benefici: {benefici_hc_mitjana:.2f} ± {benefici_hc_std:.2f} €")
    print(f"  -> SA: {temps_sa_mitjana:.2f} ± {temps_sa_std:.2f} ms, Benefici: {benefici_sa_mitjana:.2f} ± {benefici_sa_std:.2f} €")


# ========================================
# MOSTRAR RESULTATS FINALS
# ========================================
print("\n" + "=" * 80)
print("RESULTATS FINALS - TAULA RESUM")
print("=" * 80)
print(f"{'Centres':<10} {'Gasolineres':<12} {'HC Temps (ms)':<18} {'SA Temps (ms)':<18} {'HC Benefici (€)':<20} {'SA Benefici (€)':<20}")
print("-" * 80)


for r in resultats:
    print(f"{r['num_centres']:<10} {r['num_gasolineres']:<12} "
          f"{r['temps_hc_ms']:<10.2f}±{r['temps_hc_std']:<6.2f} "
          f"{r['temps_sa_ms']:<10.2f}±{r['temps_sa_std']:<6.2f} "
          f"{r['benefici_hc']:<10.2f}±{r['benefici_hc_std']:<8.2f} "
          f"{r['benefici_sa']:<10.2f}±{r['benefici_sa_std']:<8.2f}")




# gràfics


# Extreure dades per graficar
centres_list = [r['num_centres'] for r in resultats]
temps_hc_list = [r['temps_hc_ms'] for r in resultats]
temps_hc_std_list = [r['temps_hc_std'] for r in resultats]
temps_sa_list = [r['temps_sa_ms'] for r in resultats]
temps_sa_std_list = [r['temps_sa_std'] for r in resultats]
benefici_hc_list = [r['benefici_hc'] for r in resultats]
benefici_hc_std_list = [r['benefici_hc_std'] for r in resultats]
benefici_sa_list = [r['benefici_sa'] for r in resultats]
benefici_sa_std_list = [r['benefici_sa_std'] for r in resultats]


# Crear figura amb 4 subgràfics
fig, axes = plt.subplots(2, 2, figsize=(14, 11))


# Gràfic 1: Temps d'execució
ax1 = axes[0, 0]
ax1.errorbar(centres_list, temps_hc_list, yerr=temps_hc_std_list, 
             marker='o', label='Hill Climbing', linewidth=2, capsize=5)
ax1.errorbar(centres_list, temps_sa_list, yerr=temps_sa_std_list,
             marker='s', label='Simulated Annealing', linewidth=2, capsize=5)
ax1.set_xlabel('Nombre de centres de distribució', fontsize=12)
ax1.set_ylabel('Temps d\'execució (ms)', fontsize=12)
ax1.set_title('Escalabilitat: Temps d\'execució vs Mida del problema', fontsize=14, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)


# Gràfic 2: Benefici
ax2 = axes[0, 1]
ax2.errorbar(centres_list, benefici_hc_list, yerr=benefici_hc_std_list,
             marker='o', label='Hill Climbing', linewidth=2, capsize=5)
ax2.errorbar(centres_list, benefici_sa_list, yerr=benefici_sa_std_list,
             marker='s', label='Simulated Annealing', linewidth=2, capsize=5)
ax2.set_xlabel('Nombre de centres de distribució', fontsize=12)
ax2.set_ylabel('Benefici (€)', fontsize=12)
ax2.set_title('Escalabilitat: Benefici vs Mida del problema', fontsize=14, fontweight='bold')
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)


# Gràfic 3: Ràtio SA/HC en temps
ax3 = axes[1, 0]
ratio_temps = [sa / hc for sa, hc in zip(temps_sa_list, temps_hc_list)]
ax3.plot(centres_list, ratio_temps, marker='D', linewidth=2, color='purple')
ax3.axhline(y=1, color='r', linestyle='--', label='Igualtat (SA = HC)')
ax3.set_xlabel('Nombre de centres de distribució', fontsize=12)
ax3.set_ylabel('Ràtio SA/HC', fontsize=12)
ax3.set_title('Ràtio de temps SA/HC', fontsize=14, fontweight='bold')
ax3.legend(fontsize=11)
ax3.grid(True, alpha=0.3)


# Gràfic 4: Diferència de benefici SA - HC
ax4 = axes[1, 1]
diff_benefici = [sa - hc for sa, hc in zip(benefici_sa_list, benefici_hc_list)]
colors = ['green' if d > 0 else 'red' for d in diff_benefici]
ax4.bar(centres_list, diff_benefici, color=colors, alpha=0.7)
ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
ax4.set_xlabel('Nombre de centres de distribució', fontsize=12)
ax4.set_ylabel('Diferència de benefici (SA - HC) en €', fontsize=12)
ax4.set_title('Diferència de benefici: SA vs HC', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')


plt.tight_layout()
plt.savefig('experiment_escalabilitat.png', dpi=300, bbox_inches='tight')
print("Gràfics guardats a: experiment_escalabilitat.png")


# Gràfic addicional: Temps en escala logarítmica (per veure millor la tendència)
plt.figure(figsize=(10, 6))
plt.semilogy(centres_list, temps_hc_list, 'o-', label='Hill Climbing', linewidth=2)
plt.semilogy(centres_list, temps_sa_list, 's-', label='Simulated Annealing', linewidth=2)
plt.xlabel('Nombre de centres de distribució', fontsize=12)
plt.ylabel('Temps d\'execució (ms) - Escala log', fontsize=12)
plt.title('Escalabilitat: Temps en escala logarítmica', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.savefig('experiment_escalabilitat_log.png', dpi=300, bbox_inches='tight')
print("Gràfic logarítmic guardat a: experiment_escalabilitat_log.png")


plt.show()


print("\n" + "=" * 80)
print("EXPERIMENT COMPLETAT!")
print("=" * 80)
print("Fitxers generats:")
print("  - experiment_escalabilitat.csv")
print("  - experiment_escalabilitat.png")
print("  - experiment_escalabilitat_log.png")
print("=" * 80)
