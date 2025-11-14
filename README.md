# 🔍 Pràctica de Cerca Local — ABIA (UPC 2025/2026)

Aquest projecte correspon a la **Pràctica de Búsqueda Local** de l’assignatura *Algorismes Bàsics per la Intel·ligència Artificial (ABIA)* del grau en Intel·ligència Artificial de la UPC. L’objectiu és aplicar tècniques de **cerca local** per resoldre un problema de **planificació de rutes de distribució de combustible**, on diverses cisternes han d’abastir un conjunt de gasolineres de manera eficient.

## 🧠 Objectius

L'objectiu principal d'aquest treball és resoldre un problema de distribució logística de combustible mitjançant algorismes de cerca local, implementant i avaluant tots els components necessaris per obtenir solucions òptimes en termes de benefici econòmic i eficiència operativa. En concret, els objectius específics són:

1. **Dissenyar i implementar la representació del problema**, definint una estructura de dades eficient per a l'estat que tingui en compte les restriccions de capacitat, distància i nombre de viatges dels vehicles.

2. **Desenvolupar estratègies de generació de solucions inicials i operadors de transformació**, implementant múltiples alternatives per a la inicialització i definint un conjunt d'operadors que permetin explorar eficientment l'espai de solucions.

3. **Definir i justificar funcions heurístiques** que permetin avaluar la qualitat de les solucions considerant ingressos, costos de desplaçament i penalitzacions per peticions pendents, analitzant el seu impacte en la cerca.

4. **Experimentar amb els algorismes Hill Climbing i Simulated Annealing**, comparant el rendiment dels diferents components implementats (solució inicial, operadors, heurística) i ajustant els paràmetres per obtenir solucions òptimes.

5. **Analitzar l'escalabilitat i la sensibilitat del sistema** davant variacions en els paràmetres operatius (nombre de centres, camions, cost per km, horari de treball), extraient conclusions rellevants per a futures aplicacions pràctiques.

---

## 🧩 Descripció del problema

La pràctica aborda el **problema de planificació de rutes per a la distribució de combustible** a una xarxa de gasolineres, utilitzant **algoritmes de cerca local** per trobar solucions eficients dins d’un espai de possibilitats molt ampli. L’objectiu és **optimitzar el conjunt de viatges realitzats per les cisternes**, de manera que es **maximitzi el benefici global de l’empresa** i alhora es **minimitzi la distància total recorreguda** i, per tant, el cost associat.

El sistema ha de decidir **quines peticions de subministrament s’han d’atendre cada dia**, **com s’han d’assignar als camions** i **en quin ordre s’han de servir** per complir amb les limitacions de capacitat, temps i distància. Cada cisterna només pot fer un nombre màxim de viatges i quilòmetres diaris, i cada gasolinera pot tenir diverses peticions pendents amb prioritats diferents segons el temps d’espera.

A més de trobar una distribució factible, la pràctica busca **avaluar diferents estratègies heurístiques**, **formes d’inicialització de la solució** i **tipus d’operadors**, comparant-ne els resultats tant en qualitat com en temps d’execució. Per això, s’apliquen i analitzen els algoritmes **Hill Climbing** i **Simulated Annealing**, observant com responen davant canvis en els paràmetres del problema (nombre de centres, gasolineres, costos o restriccions).

En conjunt, el treball combina la **formulació formal d’un problema d’optimització** amb la seva **resolució experimental**, oferint una visió pràctica de com els mètodes de cerca local poden aplicar-se a casos reals de logística i planificació de recursos.

---

## 🧱 Estructura del projecte

- `README.md` — Resum del projecte i instruccions d’ús.
- `INFORME.md` — Arxiu de generació de l'informe
- `INFORME.pdf` — Informe final amb resultats i conclusions.
- `documentacio/` — Documents de referència i explicacions addicionals. Conté l’enunciat oficial i la descripció de la implementació de l’estat.
- `implementacio/` — Codi font principal del problema i la seva resolució.
  - `abia_Gasolina.py` — Llibreria base facilitada amb les classes del laboratori.
  - `camions.py` — Gestió general de camions i centres de distribució.
  - `camions_estat.py` — Representació de l’estat del problema (assignacions, peticions, etc.).
  - `camions_operadors.py` — Definició dels operadors per generar estats successors.
  - `camions_parametres.py` — Paràmetres globals del problema (costos, límits, constants...).
  - `camions_problema.py` — Integració de totes les parts amb els algorismes de cerca.
  - `__init__.py` — Fitxer d’inicialització del mòdul Python.
- `experiments/` — Scripts per executar els experiments i generar resultats: Inclou proves amb *Hill Climbing*, *Simulated Annealing* i escalabilitat.
  - `resultats/` — Fitxers i gràfics generats pels experiments.

---

## 📦 Dependències

Aquest projecte s’ha desenvolupat en **Python 3.12+** i requereix les següents llibreries:

- `numpy` — Operacions numèriques i càlculs de mitjanes i distàncies.  
- `matplotlib` — Generació de gràfics per a l’anàlisi d’experiments.  
- `pandas` — Gestió de dades i resultats experimentals en taules.  
- `time` — Mesura del temps d’execució dels algorismes.  
- `random` — Generació d’escenaris i inicialitzacions aleatòries.  
- `json` — Emmagatzematge i lectura de resultats d’experiments.  
- `math` — Funcions matemàtiques per al càlcul de costos i heurístiques.  
- `aima3` — Implementació dels algorismes de cerca local (Hill Climbing, Simulated Annealing).

Per instal·lar totes les dependències necessàries:

```bash
pip install numpy matplotlib pandas aima3
```

---

## 🚀 Ús

**ATENCIÓ**: En favor de l'organització del projecte, tot el codi d'implementació i els experiments es troben a la carpeta `implementacio/` i `experiments/` respectivament com a __paquets de Python__. Assegureu-vos d'executar els scripts des de la carpeta arrel i seguint la següent comanda:

```bash
python -m paquet.script
```

Per exemple, per executar l'script de l'experiment 3:

```bash
python -m experiments.experiments3
```

O per executar el problema principal:

```bash
python -m implementacio.camions
```

---

## 👥 Autors

- Ferran Òdena
- Carlos Palazón  
- Pol Riera
