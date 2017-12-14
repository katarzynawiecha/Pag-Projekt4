import arcpy

class Vertex:
    def __init__(self, ident, wsp_x, wsp_y):
        self.id = ident
        self.x = wsp_x
        self.y = wsp_y
        self.edge_out = []

class Edge:
    def __init__(self, v_from, v_to, ident, l, t, direction):
        self.vertex_from = v_from
        self.vertex_to = v_to
        self.id_jezdni = ident
        self.length = l
        self.time = t
        self.direction = direction  

#Ustawienie sciezek zapisu/odczytu
infc = "C:/Users/Pietruszka/Desktop/PAg/2/dane.shp"
arcpy.env.workspace = "C:/Users/Pietruszka/Desktop/PAg/2/wyniki"

#spatial join 
fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable("vertex.shp")
fieldmappings.addTable("vertex1.shp")

FieldIndex = fieldmappings.findFieldMapIndex("identJ")
fieldmap = fieldmappings.getFieldMap(FieldIndex)
fieldmap.mergeRule = "join"
fieldmappings.replaceFieldMap(FieldIndex, fieldmap)
arcpy.SpatialJoin_analysis("vertex.shp", "vertex1.shp", "spatialJoin.shp", "JOIN_ONE_TO_ONE","#",fieldmappings)

#slownik wierzcholkow
dictW={}

rows = arcpy.SearchCursor("spatialJoin.shp")
for row in rows:
    # tworzenie obiektow Vertex i umieszczenie ich w slowniku
    vert = Vertex(str(row.getValue("ident")),row.getValue("X"),row.getValue("Y"))
    dictW[str(row.getValue("ident"))] = vert

# slownik krawedzi
dictE = {}

rows = arcpy.SearchCursor(infc)

for row in rows:
    # tworzenie obiektow Edge i umieszczenie ich w slowniku
    v_from = dictW[str(row.getValue("id_from"))]
    v_to = dictW[str(row.getValue("id_to"))]
    edg = Edge(v_from, v_to, str(row.getValue("id_jezdni")), str(row.getValue("LENGTH")), 10, 0)
    dictE[str(row.getValue("id_jezdni"))] = edg
    # uzupełnienie listy krawędzi
    v_from.edge_out.append(edg)
    v_to.edge_out.append(edg)

# uzupelnienie atrybutu edge_out o wychodzace krawedzie
rows = arcpy.SearchCursor("spatialJoin.shp")
for row in rows:
    x = str(row.getValue("identJ"))
    x = x[16:]

    tab = []
    while len(x) > 0:
        v = x[:16]
        tab.append(v)
        x = x[16:]
    dictW[str(row.getValue("ident"))].edge_out = tab
