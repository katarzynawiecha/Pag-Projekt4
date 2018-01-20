import arcpy
from arcpy import env

#edgeShp to warstwa z krawedziami z atrybutem 'id_jezdni'
#nalezy ja miec w podgadzie ArcMapy aby dzialal SelectLayerByAttribute
# edgeShp=arcpy.GetParameterAsText(0)

# #przykladowe dane w tablicy wierzcholkow
# tablica=["0.070.67","5.723.77","1.488.17","5.790.92","0.0628.5","3.675.82","1.723.21","1.0751.8","3.864.36"]
# tablicaEdge=["5.723.770.070.67","1.488.175.723.77","1.488.175.790.92","0.0628.55.790.92","0.0628.53.675.82","1.723.213.675.82","1.0751.81.723.21","3.864.361.0751.8"]

# #tablica z 'korkami'- pozniej do usuniecia ten fragment
# korki=[]#musze ja sobie stworzyc poniewaz tablica korki jest aktualnie w innym pliku - po polaczeniu plikow ten fragment nie bedzie potrzebny
# cursor1 = arcpy.SearchCursor("C:/Users/Pietruszka/Desktop/PAg/2/wyniki/korki.shp")
# for row in cursor1:
#  korki.append(row.getValue("id_jezdni"))

# #stworzenie warstwy drogowej bez korkow        
# arcpy.env.workspace = 'C:/Users/Pietruszka/Desktop/PAg/2/wyniki'
# arcpy.Erase_analysis("dane.shp","korki.shp","daneBezKorkow.shp")

# #przejrzenie tablicy jezdni i sprawdzenie czy ktoras ma "korek" - jesli tak to nadpisuje ja zerem
# for idx, item in enumerate(tablicaEdge):
#    if item in korki:
#        tablicaEdge[idx] = "0"

# tmp=[]#tablica odcinkow (indeksow tablicy) w ktorych sa korki-tablice wierzcholkow
# tmp2=[]#tablica odcinkow (indeksow tablicy) w ktorych sa korki-wszystkie wierzcholki
# noweTrasy=[]#zbior do przechowywania nowych wierzcholkow juz bez korkow - wyniki funkcji a*
# flagaCzyKoniec=0
# vertex2del=[]#wierzcholki w korku
# flaga=0
# for idx, item in enumerate(tablicaEdge):
#   if item=="0":
#     if flaga==0:
#       flaga=1
#     flagaCzyKoniec=flagaCzyKoniec+1
#     vertex2del.append(idx)
#     tmp2.append(idx)
#   else:
#     flaga=0
#     if flagaCzyKoniec!=0:
#      vertex2del.append(idx)#index konca korka
#      tmp2.append(idx)#index konca korka
#      #liczenie trase miedzy start i last w vertex2del - wywolanie funkcji i dolaczenie wynikow do []tmp
#      tmp.append(vertex2del)
#      noweTrasy.append([8,9])#powiedzmy zwrocony wynik dzialania funkcji, wazne aby pamietac ze ma zwracac rowniez w tej tablicy rowniez start i koniec
#      vertex2del=[]
#      flagaCzyKoniec=0

# #tablica wierzcholkow start gdzie wstawic nowe trasy
# tmp3=[]
# for idx, item in enumerate(tmp):
#     tmp3.append(item[0])

# #tablica wierzcholkow poza korkami - ostateczna
# tablicaBezKorkow=[]
# i=0 #licznik ktora z nowo obliczonych tras wybrac
# for idx, item in enumerate(tablica):
#   if idx in tmp2:
#     if idx in tmp3:
#       for id, itm in enumerate(noweTrasy[i]):
#         tablicaBezKorkow.insert(idx+id,itm)
#       i=i+1
#   else:
#     tablicaBezKorkow.append(tablica[idx])

#WIZUALIZACJA
#"tablica" to tablica z wierzcholkami trasy
#stworzenie nowej warstwy do zapisywania samej sciezki
def wizualizacja(vertexy, edgeShp, katalog):  
  out_path = arcpy.Describe(katalog).path
  out_name = "bezKorkow.shp"
  geometry_type = "POLYLINE"
  template = edgeShp
  has_m = "DISABLED"
  has_z = "DISABLED"
  spatial_reference = arcpy.Describe(edgeShp).spatialReference

  arcpy.CreateFeatureclass_management(out_path, out_name, geometry_type,template, has_m, has_z, spatial_reference)
  visualLayer=out_path+'/'+out_name

  print("Wizualizacja")
  print(edgeShp)
  print(visualLayer)

  #iteracja po tablicy i selekcja interesujacych nas obiektow
  # edgeLayer = out_path+'/edgeLayer.lyr'
  edgeLayer = 'test_lyr'
  arcpy.MakeFeatureLayer_management(edgeShp, edgeLayer)
  mxd = arcpy.mapping.MapDocument("CURRENT")
  lyr = arcpy.mapping.Layer(edgeLayer)
  for v, w in zip(vertexy[:-1], vertexy[1:]):
    tmp = v.id + w.id
    arcpy.SelectLayerByAttribute_management (lyr, "ADD_TO_SELECTION",   "id_jezdni={}".format(tmp))
    tmp = w.id + v.id
    arcpy.SelectLayerByAttribute_management (lyr, "ADD_TO_SELECTION",   "id_jezdni={}".format(tmp))

  #przeniesienie zaznaczonych obiektow do nowej klasy
  arcpy.CopyFeatures_management(lyr,visualLayer)

  #dodanie warstwy z trasa do widoku
  df = arcpy.mapping.ListDataFrames(mxd)[0]
  layer = arcpy.mapping.Layer(visualLayer)
  arcpy.mapping.AddLayer(df, layer, "AUTO_ARRANGE")
