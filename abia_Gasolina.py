import random
from typing import List


DISTRIBUCIO_PETICIONS = [0.05, 0.65, 0.25, 0.05]
DISTRIBUCIO_DIES = [0.60, 0.20, 0.15, 0.05]


class Gasolinera(object):
    """
    Estructura de dades d’una gasolinera
    """

    def __init__(self, cx: int, cy: int, peticions: List[int]):
        """
        Constructora
        :param cx: coordenada X
        :param cy: coordenada Y
        :param peticions: Llista d’enters amb els dies pendents de la petició (0 = avui)
        """
        self.cx = cx
        self.cy = cy
        self.peticions = peticions


class Gasolineres(object):
    """
    Llista de gasolineres
    """

    def __init__(self, num_gasolineres: int, seed: int):
        """
        Genera un nombre de gasolineres amb una llavor aleatòria
        :param num_gasolineres: Nombre de gasolineres
        :param seed: Llavor per al generador de nombres aleatoris
        """
        self.my_random = random.Random(seed)
        self.gasolineres = []
        for _ in range(num_gasolineres):
            gasolinera = Gasolinera(
                self.my_random.randint(0, 99),
                self.my_random.randint(0, 99),
                self.genera_peticions()
            )
            self.gasolineres.append(gasolinera)

    def genera_peticions(self) -> List[int]:
        """
        Generem un nombre de peticions entre 0 i 2 amb distribució esbiaixada.
        Generem el dia que porta la petició pendent amb una altra distribució esbiaixada.
        :return: Llista de peticions
        """
        pet = []
        dau = self.my_random.random()
        if dau < DISTRIBUCIO_PETICIONS[0]:
            num_peticions = 0
        elif dau < (DISTRIBUCIO_PETICIONS[0] + DISTRIBUCIO_PETICIONS[1]):
            num_peticions = 1
        else:
            num_peticions = 2

        for _ in range(num_peticions):
            dau = self.my_random.random()
            if dau < DISTRIBUCIO_DIES[0]:
                num_dies = 0
            elif dau < (DISTRIBUCIO_DIES[0] + DISTRIBUCIO_DIES[1]):
                num_dies = 1
            elif dau < (DISTRIBUCIO_DIES[0] + DISTRIBUCIO_DIES[1] + DISTRIBUCIO_DIES[2]):
                num_dies = 2
            else:
                num_dies = 3
            pet.append(num_dies)
        return pet


class Distribucio(object):
    """
    Centre de distribució
    """

    def __init__(self, cx: int, cy: int, diposit: int):
        """
        Constructora
        :param cx: coordenada X
        :param cy: coordenada Y
        :param diposit: capacitat del dipòsit
        """
        self.cx = cx
        self.cy = cy
        self.diposit = diposit


class CentresDistribucio(object):
    """
    Llista amb els centres de distribució
    """

    def __init__(self, num_centres: int, multiplicitat: int, seed: int):
        """
        Genera un nombre de centres amb una llavor aleatòria.
        Si la multiplicitat és diferent d’1, genera diversos centres a la mateixa posició
        per simular tenir més d’un camió en un centre.
        :param num_centres: Nombre de centres
        :param multiplicitat: Multiplicitat a la mateixa posició
        :param seed: Llavor per al generador de nombres aleatoris
        """
        self.centres = []
        self.my_random = random.Random(seed + 1)
        for _ in range(num_centres):
            # Nota: ara passem una capacitat de dipòsit d’exemple, p. ex. 1000
            centre_base = Distribucio(
                self.my_random.randint(0, 99),
                self.my_random.randint(0, 99),
                1000
            )
            for _ in range(multiplicitat):
                self.centres.append(centre_base)


if __name__ == "__main__":
    """
    Codi per provar les classes
    No té utilitat per a la pràctica
    """
    s = Gasolineres(100, 1234)
    c = CentresDistribucio(10, 1, 1234)
    histograma = [0, 0, 0, 0]

    for i in range(len(s.gasolineres)):
        print(f"Gasolinera {i}: {s.gasolineres[i].cx} {s.gasolineres[i].cy}")
        j = 0
        if not s.gasolineres[i].peticions:
            print("-> Sense peticions <-")
        for peticio in s.gasolineres[i].peticions:
            print(f"Petició {j}: Dies {peticio}")
            j += 1
            histograma[peticio] += 1

    print()
    for i in range(4):
        print(f"{histograma[i]} de {i} dies")
    print()
    for i in range(len(c.centres)):
        print(f"Centre {i}: {c.centres[i].cx} {c.centres[i].cy}")
