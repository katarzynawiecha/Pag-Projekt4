import arcpy
import pythonaddins

class ButtonClass5(object):
    """Implementation for Tool_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        print wsp_x
        arcpy.env.workspace = "C:/Users/Pietruszka/Desktop/PAg/2/wyniki"

        x = start_x  # z clicku pocz¹tek
        y = start_y

        # szukanie najbli¿szego vertexu do wskazanego punktu - start
        arcpy.CreateFeatureclass_management("C:/Users/Pietruszka/Desktop/PAg/2/wyniki", "tmp.shp", "POINT",
                                            "vertex.shp")  # tutaj vertex.shp jako wzór do stworzenia warstwy, aby nie podawaæ np. z "palca" uk³adu itp.
        cursor = arcpy.da.InsertCursor("tmp.shp", ["SHAPE@"])
        cursor.insertRow((arcpy.PointGeometry(arcpy.Point(x, y))))

        arcpy.SpatialJoin_analysis("tmp.shp", "vertex.shp", "spatJ.shp", "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CLOSEST")
        cursor1 = arcpy.SearchCursor("spatJ.shp")
        for row in cursor1:
            startPoint = row.getValue("ident_1")
        arcpy.AddMessage(startPoint)

        arcpy.DeleteFeatures_management("tmp.shp")
        arcpy.DeleteFeatures_management("spatJ.shp")

        # szukanie najbli¿szego vertexu do wskazanego punktu - end
        x = end_x  # z clicku koniec
        y = end_y

        cursor = arcpy.da.InsertCursor("tmp.shp", ["SHAPE@"])
        cursor.insertRow((arcpy.PointGeometry(arcpy.Point(x, y))))

        arcpy.SpatialJoin_analysis("tmp.shp", "vertex.shp", "spatJ.shp", "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CLOSEST")
        cursor1 = arcpy.SearchCursor("spatJ.shp")
        for row in cursor1:
            endPoint = row.getValue("ident_1")
        arcpy.AddMessage(endPoint)

        arcpy.Delete_management("tmp.shp")
        arcpy.Delete_management("spatJ.shp")

        # odczyt zaznaczonych krawêdzi z korkami
        # mój pomys³ to najprostsze reprezentowanie korków przez selekcjê (zaznaczenie) danych obiektów liniowych na pliku .lyr!
        arcpy.CreateFeatureclass_management("C:/Users/Pietruszka/Desktop/PAg/2/wyniki", "korki.shp", "POLYLINE")
        arcpy.CopyFeatures_management("dane.lyr", "korki.shp")  # zamiana danych na Layer
        cursor2 = arcpy.SearchCursor("korki.shp")
        korki = []
        for row in cursor2:
            korki.append(row.getValue("id_jezdni"))
        for x in korki:
            arcpy.AddMessage(x)

        # usuniêcie zaznaczenia
        arcpy.SelectLayerByAttribute_management("dane.lyr", "CLEAR_SELECTION")

class ToolClass2(object):
    """Implementation for Tool_addin.tool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
    def onMouseDown(self, x, y, button, shift):
        pass
    def onMouseDownMap(self, x, y, button, shift):
        global start_x
        start_x = x
        global start_y
        start_y = y

class ToolClass4(object):
    """Implementation for Tool_addin.tool_1 (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
    def onMouseDown(self, x, y, button, shift):
        pass
    def onMouseDownMap(self, x, y, button, shift):
        global end_x
        end_x = x
        global end_y
        end_y = y
