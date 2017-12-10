import arcpy
from arcpy import env

#edgeLayer to warstwa z krawêdziami z atrybutem 'id_jezdni'
edgeLayer=arcpy.GetParameterAsText(0)

#przyk³adowe dane
tablica=["0.070.67","5.723.77","1.488.17","5.790.92","0.0628.5"]

#stworzenie nowej warstwy do zapisywania samej œcie¿ki
out_path = arcpy.Describe(edgeLayer).path
out_name = "wizualizacja.shp"
geometry_type = "POLYLINE"
template = edgeLayer
has_m = "DISABLED"
has_z = "DISABLED"
spatial_reference = arcpy.Describe(edgeLayer).spatialReference

arcpy.CreateFeatureclass_management(out_path, out_name, geometry_type,template, has_m, has_z, spatial_reference)
visualLayer=out_path+'/'+out_name

#iteracja po tablicy i selekcja interesuj¹cych nas obiektów
for i in range(len(tablica)-1):
  tmp=tablica[i+1]+tablica[i]
  arcpy.SelectLayerByAttribute_management (edgeLayer, "ADD_TO_SELECTION",   "\"id_jezdni\" = " + "'" + tmp + "'")
  tmp1=tablica[i]+tablica[i+1]
  arcpy.SelectLayerByAttribute_management (edgeLayer, "ADD_TO_SELECTION",   "\"id_jezdni\" = " + "'" + tmp1 + "'")

#przeniesienie zaznaczonych obiektów do nowej klasy
arcpy.CopyFeatures_management(edgeLayer,visualLayer)

#dodanie warstwy z tras¹ do widoku
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]
layer = arcpy.mapping.Layer(visualLayer)
arcpy.mapping.AddLayer(df, layer, "AUTO_ARRANGE")