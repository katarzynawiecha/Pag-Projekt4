import arcpy

#Ustawienie œrodowisk folderów zapisu/odczytu
infc = "C:/Users/Pietruszka/Desktop/PAg/2/dane.shp"
outfc = "C:/Users/Pietruszka/Desktop/PAg/2/wyniki"

desc = arcpy.Describe(infc)
shapefieldname = desc.ShapeFieldName

rows =  arcpy.SearchCursor(infc)

arcpy.AddField_management(infc, "id_from", "TEXT")
arcpy.AddField_management(infc, "id_to", "TEXT")
arcpy.AddField_management(infc, "id_jezdni", "TEXT")

#Stworzenie nowej klasy punktowej na wêz³y
arcpy.CreateFeatureclass_management(outfc, "vertex.shp", "POINT", "", "DISABLED", "DISABLED",arcpy.Describe(infc).spatialReference)
arcpy.AddField_management(outfc+"/vertex.shp", "ident", "TEXT")
arcpy.AddField_management(outfc+"/vertex.shp", "X", "DOUBLE")
arcpy.AddField_management(outfc+"/vertex.shp", "Y", "DOUBLE")
arcpy.AddField_management(outfc+"/vertex.shp", "identJ", "TEXT")

cursor = arcpy.da.InsertCursor(outfc+"/vertex.shp", ("FID", "SHAPE@XY","ident","X","Y","identJ"))

licznik=0
for row in rows:
    feat = row.getValue(shapefieldname)

    #Pobranie pierwszego punktu danego obiektu
    startpt = feat.firstPoint

    startx = startpt.X
    starty = startpt.Y

    identStart=("".join([str(startx)[-4:],str(starty)[-4:]]))

    #Pobranie ostatniego punktu danego obiektu
    endpt = feat.lastPoint

    endx = endpt.X
    endy = endpt.Y

    identEnd=("".join([str(endx)[-4:],str(endy)[-4:]]))

    identJezdni="".join([identStart,identEnd])

    cursor.insertRow(("1",(startx, starty),identStart,startx,starty,identJezdni))
    cursor.insertRow(("1",(endx, endy),identEnd,endx,endy,identJezdni))
    
    #Zaktualizowanie pól id_from, id_to utworzonymi identyfikatorami punktów
    expression = arcpy.AddFieldDelimiters(infc, "FID") + ' = ' + str(licznik)
    with arcpy.da.UpdateCursor(infc,["id_from","id_to","id_jezdni"],expression) as updCur:
      for u in updCur:
        u[0]=identStart
        u[1]=identEnd
	u[2]=identJezdni
        updCur.updateRow(u)

    licznik+=1

arcpy.DeleteIdentical_management(outfc+"/vertex.shp", "ident")

arcpy.AddGeometryAttributes_management(infc, "LENGTH", "KILOMETERS", "", "")
