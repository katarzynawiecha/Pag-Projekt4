import math

class Vertex:
    def __init__(self, ident, wsp_x, wsp_y):
        self.id = ident
        self.x = wsp_x
        self.y = wsp_y
        self.edge_out = []
# funkcja liczaca odleglosc miedzy dwoma punktami
    def distance_to(self, v_to):
        a = (v_to.x - self.x)**2
        b = (v_to.y - self.y)**2
        return math.sqrt(a + b)

    def __repr__(self):
        return "ID: {} X: {} Y: {}".format(self.id, self.x, self.y)

class Edge:
    def __init__(self, v_from, v_to, ident, V, direction):
        self.vertex_from = v_from
        self.vertex_to = v_to
        self.id_jezdni = ident
        self.length = v_from.distance_to(v_to)
        self.time = self.length/V
        self.direction = direction  

    def weight(self):
        return self.time