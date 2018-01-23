import arcpy
from klasy import Vertex, Edge

def stworz_graf(vertexy, krawedzie):


    #slownik wierzcholkow
    dictW={}

    rows = arcpy.SearchCursor(vertexy)
    for row in rows:
        # tworzenie obiektow Vertex i umieszczenie ich w slowniku
        vert = Vertex(str(row.getValue("ident")),row.getValue("X"),row.getValue("Y"))
        dictW[str(row.getValue("ident"))] = vert

    # slownik krawedzi
    dictE = {}

    rows = arcpy.SearchCursor(krawedzie)

    for row in rows:
        # tworzenie obiektow Edge i umieszczenie ich w slowniku
        v_from = dictW[str(row.getValue("id_from"))]
        v_to = dictW[str(row.getValue("id_to"))]
        edg = Edge(v_from, v_to, str(row.getValue("id_jezdni")), int(row.getValue("max_V")))
        dictE[str(row.getValue("id_jezdni"))] = edg
        # uzupelnienie listy krawedzi
        v_from.edge_out.append(edg)
        v_to.edge_out.append(edg)

    return dictW, dictE