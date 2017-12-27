import arcpy
from arcpy import env

#edgeLayer to warstwa z krawêdziami z atrybutem 'id_jezdni'
#nale¿y j¹ mieæ w podg¹dzie ArcMapy aby dzia³a³ SelectLayerByAttribute
edgeLayer=arcpy.GetParameterAsText(0)

#przyk³adowe dane w tablicy wierzcho³ków
tablica=["0.070.67","5.723.77","1.488.17","5.790.92","0.0628.5","3.675.82","1.723.21","1.0751.8","3.864.36"]
tablicaEdge=["5.723.770.070.67","1.488.175.723.77","1.488.175.790.92","0.0628.55.790.92","0.0628.53.675.82","1.723.213.675.82","1.0751.81.723.21","3.864.361.0751.8"]

#tablica z 'korkami'- póŸniej do usuniêcia ten fragment
korki=[]#muszê j¹ sobie stworzyæ poniewa¿ tablica korki jest aktualnie w innym pliku - po po³¹czeniu plików ten fragment nie bêdzie potrzebny
cursor1 = arcpy.SearchCursor("C:/Users/Pietruszka/Desktop/PAg/2/wyniki/korki.shp")
for row in cursor1:
 korki.append(row.getValue("id_jezdni"))

#stworzenie warstwy drogowej bez korków        
arcpy.env.workspace = 'C:/Users/Pietruszka/Desktop/PAg/2/wyniki'
arcpy.Erase_analysis("dane.shp","korki.shp","daneBezKorkow.shp")

#przejrzenie tablicy jezdni i sprawdzenie czy któraœ ma "korek" - jeœli tak to nadpisuje j¹ zerem
for idx, item in enumerate(tablicaEdge):
   if item in korki:
       tablicaEdge[idx] = "0"

tmp=[]#tablica odcinków (indeksów tablicy) w których s¹ korki-tablice wierzcholkow
tmp2=[]#tablica odcinków (indeksów tablicy) w których s¹ korki-wszystkie wierzcholki
noweTrasy=[]#zbiór do przechowywania nowych wierzcholkow juz bez korkow - wyniki funkcji a*
flagaCzyKoniec=0
vertex2del=[]#wierzcho³ki w korku
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
     vertex2del.append(idx)#index koñca korka
     tmp2.append(idx)#index koñca korka
     #liczenie trasê miêdzy start i last w vertex2del - wywo³anie funkcji i do³¹czenie wyników do []tmp
     tmp.append(vertex2del)
     noweTrasy.append([8,9])#powiedzmy zwrócony wynik dzia³ania funkcji, wa¿ne aby pamiêtaæ ¿e ma zwracaæ równie¿ w tej tablicy równie¿ start i koniec
     vertex2del=[]
     flagaCzyKoniec=0

#tablica wierzcho³ków start gdzie wstawiæ nowe trasy
tmp3=[]
for idx, item in enumerate(tmp):
    tmp3.append(item[0])

#tablica wierzcho³ków poza korkami - ostateczna
tablicaBezKorkow=[]
i=0 #licznik któr¹ z nowo obliczonych tras wybraæ
for idx, item in enumerate(tablica):
  if idx in tmp2:
    if idx in tmp3:
      for id, itm in enumerate(noweTrasy[i]):
        tablicaBezKorkow.insert(idx+id,itm)
      i=i+1
  else:
    tablicaBezKorkow.append(tablica[idx])

#WIZUALIZACJA
#"tablica" to tablica z wierzcho³kami trasy
#stworzenie nowej warstwy do zapisywania samej œcie¿ki
out_path = arcpy.Describe(edgeLayer).path
out_name = "wizualBezKorkow.shp"
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
