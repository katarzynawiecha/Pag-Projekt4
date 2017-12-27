import arcpy
from arcpy import env

#edgeLayer to warstwa z kraw�dziami z atrybutem 'id_jezdni'
#nale�y j� mie� w podg�dzie ArcMapy aby dzia�a� SelectLayerByAttribute
edgeLayer=arcpy.GetParameterAsText(0)

#przyk�adowe dane w tablicy wierzcho�k�w
tablica=["0.070.67","5.723.77","1.488.17","5.790.92","0.0628.5","3.675.82","1.723.21","1.0751.8","3.864.36"]
tablicaEdge=["5.723.770.070.67","1.488.175.723.77","1.488.175.790.92","0.0628.55.790.92","0.0628.53.675.82","1.723.213.675.82","1.0751.81.723.21","3.864.361.0751.8"]

#tablica z 'korkami'- p�niej do usuni�cia ten fragment
korki=[]#musz� j� sobie stworzy� poniewa� tablica korki jest aktualnie w innym pliku - po po��czeniu plik�w ten fragment nie b�dzie potrzebny
cursor1 = arcpy.SearchCursor("C:/Users/Pietruszka/Desktop/PAg/2/wyniki/korki.shp")
for row in cursor1:
 korki.append(row.getValue("id_jezdni"))

#stworzenie warstwy drogowej bez kork�w        
arcpy.env.workspace = 'C:/Users/Pietruszka/Desktop/PAg/2/wyniki'
arcpy.Erase_analysis("dane.shp","korki.shp","daneBezKorkow.shp")

#przejrzenie tablicy jezdni i sprawdzenie czy kt�ra� ma "korek" - je�li tak to nadpisuje j� zerem
for idx, item in enumerate(tablicaEdge):
   if item in korki:
       tablicaEdge[idx] = "0"

tmp=[]#tablica odcink�w (indeks�w tablicy) w kt�rych s� korki-tablice wierzcholkow
tmp2=[]#tablica odcink�w (indeks�w tablicy) w kt�rych s� korki-wszystkie wierzcholki
noweTrasy=[]#zbi�r do przechowywania nowych wierzcholkow juz bez korkow - wyniki funkcji a*
flagaCzyKoniec=0
vertex2del=[]#wierzcho�ki w korku
flaga=0
for idx, item in enumerate(tablicaEdge):
  if item=="0":
    if flaga==0:
      flaga=1
    flagaCzyKoniec=flagaCzyKoniec+1
    vertex2del.append(idx)
    tmp2.append(idx)
  else:
    flaga=0
    if flagaCzyKoniec!=0:
     vertex2del.append(idx)#index ko�ca korka
     tmp2.append(idx)#index ko�ca korka
     #liczenie tras� mi�dzy start i last w vertex2del - wywo�anie funkcji i do��czenie wynik�w do []tmp
     tmp.append(vertex2del)
     noweTrasy.append([8,9])#powiedzmy zwr�cony wynik dzia�ania funkcji, wa�ne aby pami�ta� �e ma zwraca� r�wnie� w tej tablicy r�wnie� start i koniec
     vertex2del=[]
     flagaCzyKoniec=0

#tablica wierzcho�k�w start gdzie wstawi� nowe trasy
tmp3=[]
for idx, item in enumerate(tmp):
    tmp3.append(item[0])

#tablica wierzcho�k�w poza korkami - ostateczna
tablicaBezKorkow=[]
i=0 #licznik kt�r� z nowo obliczonych tras wybra�
for idx, item in enumerate(tablica):
  if idx in tmp2:
    if idx in tmp3:
      for id, itm in enumerate(noweTrasy[i]):
        tablicaBezKorkow.insert(idx+id,itm)
      i=i+1
  else:
    tablicaBezKorkow.append(tablica[idx])

#WIZUALIZACJA
#"tablica" to tablica z wierzcho�kami trasy
#stworzenie nowej warstwy do zapisywania samej �cie�ki
out_path = arcpy.Describe(edgeLayer).path
out_name = "wizualBezKorkow.shp"
geometry_type = "POLYLINE"
template = edgeLayer
has_m = "DISABLED"
has_z = "DISABLED"
spatial_reference = arcpy.Describe(edgeLayer).spatialReference

arcpy.CreateFeatureclass_management(out_path, out_name, geometry_type,template, has_m, has_z, spatial_reference)
visualLayer=out_path+'/'+out_name

#iteracja po tablicy i selekcja interesuj�cych nas obiekt�w
for i in range(len(tablica)-1):
  tmp=tablica[i+1]+tablica[i]
  arcpy.SelectLayerByAttribute_management (edgeLayer, "ADD_TO_SELECTION",   "\"id_jezdni\" = " + "'" + tmp + "'")
  tmp1=tablica[i]+tablica[i+1]
  arcpy.SelectLayerByAttribute_management (edgeLayer, "ADD_TO_SELECTION",   "\"id_jezdni\" = " + "'" + tmp1 + "'")

#przeniesienie zaznaczonych obiekt�w do nowej klasy
arcpy.CopyFeatures_management(edgeLayer,visualLayer)

#dodanie warstwy z tras� do widoku
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]
layer = arcpy.mapping.Layer(visualLayer)
arcpy.mapping.AddLayer(df, layer, "AUTO_ARRANGE")
