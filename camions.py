from aima3.search import hill_climbing, simulated_annealing
from camions_problema import CamionsProblema
from camions_parametres import ProblemParameters
from camions_estat import generate_greedy_initial_state, generate_initial_state, generate_empty_initial_state
from abia_Gasolina import Gasolineres, CentresDistribucio

gasolineres = Gasolineres(num_gasolineres=100, seed=1234)
centres = CentresDistribucio(num_centres=5, multiplicitat=1, seed=5678)

params = ProblemParameters( km=640, n_viatges=5, valor=1000, cost_km=2, gasolineres=gasolineres, centres=centres)
initial_state = generate_initial_state(params)
n =simulated_annealing(CamionsProblema(initial_state))
n1 = hill_climbing(CamionsProblema(initial_state))
print(n1)
