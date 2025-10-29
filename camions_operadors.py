class CamionsOperator(object):
    pass

class swapCentres(CamionsOperator): 

    def __init__(self, centre1: int, centre2: int):
        self.centre1 = centre1
        self.centre2 = centre2

    def __repr__(self):
        return f"swapCentres(centre1={self.centre1}, centre2={self.centre2})" 

    

class mourePeticio(CamionsOperator):

    def __init__(self, id_peticio: int, camio_origen: int, camio_desti: int):
        self.id_peticio = id_peticio
        self.camio_origen = camio_origen
        self.camio_desti = camio_desti

    def __repr__(self):
        return f"mourePeticio(id_peticio={self.id_peticio}, camio_origen={self.camio_origen}, camio_desti={self.camio_desti})"


