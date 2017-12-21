import arcpy

arcpy.env.workspace ="C:/Users/Pietruszka/Desktop/PAg/2/wyniki"

x=470518.47 #z clicku pocz¹tek
y=559870.96

#szukanie najbli¿szego vertexu do wskazanego punktu - start
arcpy.CreateFeatureclass_management("C:/Users/Pietruszka/Desktop/PAg/2/wyniki", "tmp.shp", "POINT", "vertex.shp")#tutaj vertex.shp jako wzór do stworzenia warstwy, aby nie podawaæ np. z "palca" uk³adu itp.
cursor = arcpy.da.InsertCursor("tmp.shp", ["SHAPE@"])
cursor.insertRow((arcpy.PointGeometry(arcpy.Point(x,y))))

arcpy.SpatialJoin_analysis("tmp.shp","vertex.shp", "spatJ.shp","JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CLOSEST")
cursor1 = arcpy.SearchCursor("spatJ.shp")
for row in cursor1:
 startPoint=row.getValue("ident_1")
arcpy.AddMessage(startPoint)

arcpy.DeleteFeatures_management("tmp.shp")
arcpy.DeleteFeatures_management("spatJ.shp")

#szukanie najbli¿szego vertexu do wskazanego punktu - end
x=471390.63 #z clicku koniec
y=559791.98

cursor = arcpy.da.InsertCursor("tmp.shp", ["SHAPE@"])
cursor.insertRow((arcpy.PointGeometry(arcpy.Point(x,y))))

arcpy.SpatialJoin_analysis("tmp.shp","vertex.shp", "spatJ.shp","JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CLOSEST")
cursor1 = arcpy.SearchCursor("spatJ.shp")
for row in cursor1:
 endPoint=row.getValue("ident_1")
arcpy.AddMessage(endPoint)

arcpy.Delete_management("tmp.shp")
arcpy.Delete_management("spatJ.shp")

#odczyt zaznaczonych krawêdzi z korkami
#mój pomys³ to najprostsze reprezentowanie korków przez selekcjê (zaznaczenie) danych obiektów liniowych
arcpy.CreateFeatureclass_management("C:/Users/Pietruszka/Desktop/PAg/2/wyniki", "korki.shp", "POLYLINE")
arcpy.CopyFeatures_management("dane.lyr", "korki.shp")#zamiana danych na Layer
cursor2 = arcpy.SearchCursor("korki.shp")
korki=[]
for row in cursor2:
 korki.append(row.getValue("id_jezdni"))

for x in korki:
    arcpy.AddMessage(x)

#usuniêcie zaznaczenia
arcpy.SelectLayerByAttribute_management("dane.lyr", "CLEAR_SELECTION")
