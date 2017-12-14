import arcpy
import csv

class Vertex:
    def __init__(self, ident, wsp_x, wsp_y, tab_kr):
        self.id = ident
        self.x = wsp_x
        self.y = wsp_y
        self.edge_out = tab_kr

class Edge:
    def __init__(self, v_from, v_to, ident, l, t, direction):
        self.vertex_from = v_from
        self.vertex_to = v_to
        self.id_jezdni = ident
        self.length = l
        self.time = t
        self.direction = direction  

#Ustawienie œrodowisk folderów zapisu/odczytu
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

#s³ownik wierzcho³ków
dictW={}

rows =  arcpy.SearchCursor("spatialJoin.shp")

for row in rows:
  x=str(row.getValue("identJ"))
  x=x[16:]
  tab=[]
  while len(x)>0:
    v = x[:16]
    tab.append(v)
    x = x[16:]
  dictW[str(row.getValue("ident"))]=tab

#wypisanie s³ownika - dla sprawdzenia
w = csv.writer(open("output.csv", "w"))
for key, val in dictW.items():
 w.writerow([key, val])

#s³ownik krawêdzi
dictE={}

rows =  arcpy.SearchCursor(infc)

for row in rows:
  dictE[str(row.getValue("id_jezdni"))]=[str(row.getValue("id_from")),str(row.getValue("id_to"))]

#wypisanie s³ownika - dla sprawdzenia
w = csv.writer(open("output1.csv", "w"))
for key, val in dictE.items():
 w.writerow([key, val])
