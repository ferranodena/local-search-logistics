class ProblemParameters(object):
    def __init__(self, km, viatges, valor, cost_km, gasolineres, centres):
        # límits i costos 
        self.km = km                    # Màxim km per camió al dia 
        self.viatges = viatges          # Màxim viatges per camió al dia 
        self.valor = valor              # Valor base del dipòsit (€)
        self.cost_km = cost_km          # Cost per km recorregut (€/km)
        
        # Dades del problema
        self.gasolineres = gasolineres  # Objecte Gasolineres amb llista de Gasolinera
        self.centres = centres          # Objecte CentresDistribucio amb llista de Distribucio
    def __repr__(self):
        return f"ProblemParameters(km={self.km}, viatges={self.viatges}, valor={self.valor}, cost_km={self.cost_km})"