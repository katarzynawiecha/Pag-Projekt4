import arcpy
from klasy import Vertex, Edge



#Ustawienie sciezek zapisu/odczytu
# infc = "C:/Users/Pietruszka/Desktop/PAg/2/dane.shp"
# arcpy.env.workspace = "C:/Users/Pietruszka/Desktop/PAg/2/wyniki"

def stworz_graf(vertexy, krawedzie):
    # arcpy.env.workspace = katalog
    #spatial join 
    # fieldmappings = arcpy.FieldMappings()
    # fieldmappings.addTable(outfc)
    # fieldmappings.addTable("vertex1.shp")

    # FieldIndex = fieldmappings.findFieldMapIndex("identJ")
    # fieldmap = fieldmappings.getFieldMap(FieldIndex)
    # fieldmap.mergeRule = "join"
    # fieldmappings.replaceFieldMap(FieldIndex, fieldmap)
    # arcpy.SpatialJoin_analysis("vertex.shp", "vertex1.shp", "spatialJoin.shp", "JOIN_ONE_TO_ONE","#",fieldmappings)

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
        edg = Edge(v_from, v_to, str(row.getValue("id_jezdni")), int(row.getValue("max_V")), 0)
        dictE[str(row.getValue("id_jezdni"))] = edg
        # uzupelnienie listy krawedzi
        v_from.edge_out.append(edg)
        v_to.edge_out.append(edg)

    # start, goal = list(dictW.values())[0:2]
    print("Liczba wiecholkow:", len(dictW), "Liczba krawedzi:", len(dictE))
    return dictW, dictE