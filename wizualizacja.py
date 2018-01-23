import arcpy
from arcpy import env


#WIZUALIZACJA

#stworzenie nowej warstwy do zapisywania samej sciezki
def wizualizacja(vertexy, edgeShp, katalog, nazwa):
  mxd = arcpy.mapping.MapDocument('current')
  out_path = arcpy.Describe(katalog).path
  geometry_type = "POLYLINE"
  template = edgeShp
  has_m = "DISABLED"
  has_z = "DISABLED"
  spatial_reference = arcpy.Describe(edgeShp).spatialReference

  visualLayer = out_path + "\\" + nazwa



  #iteracja po tablicy i selekcja interesujacych nas obiektow

  edgeLayer = 'lyr'
  arcpy.MakeFeatureLayer_management(edgeShp, edgeLayer)

  for v, w in zip(vertexy[:-1], vertexy[1:]):
    tmp = v.id + w.id
    arcpy.SelectLayerByAttribute_management (edgeLayer, "ADD_TO_SELECTION",   "id_jezdni='{}'".format(tmp))
    tmp = w.id + v.id
    arcpy.SelectLayerByAttribute_management (edgeLayer, "ADD_TO_SELECTION",   "id_jezdni='{}'".format(tmp))


  #przeniesienie zaznaczonych obiektow do nowej klasy
  arcpy.CopyFeatures_management(edgeLayer,visualLayer)
  arcpy.SelectLayerByAttribute_management(edgeLayer, "REMOVE_FROM_SELECTION")
  #dodanie warstwy z trasa do widoku
  df = arcpy.mapping.ListDataFrames(mxd)[0]
