import arcpy
import pythonaddins
import sys
import os

sys.path.append(os.path.dirname(__file__))
import lab1
import lab2

from klasy import Vertex, Edge
from agwiazdka import a_star
from wizualizacja import wizualizacja

class ButtonClass1(object):
    """Implementation for Toolbar_addin.button1 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        global plik_z_krawedziami
        plik_z_krawedziami = pythonaddins.OpenDialog("Open",False,"")
        global plik_z_werteksami
        plik_z_werteksami = pythonaddins.SaveDialog("Save", "dane.shp", "", lambda x: x and x.lower().endswith('.shp'),"Shapefile")
        lab1.wczytaj_dane(plik_z_krawedziami, plik_z_werteksami)
        global graf
        graf = lab2.stworz_graf(plik_z_werteksami, plik_z_krawedziami)

class Korek(object):
    """Implementation for Toolbar_addin.button3 (Button)"""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        pass

class cel(object):
    """Implementation for Toolbar_addin.tool2 (Tool)"""
    def __init__(self):
        self.enabled = False
        self.shape = "NONE"
    def onMouseDownMap(self, x, y, button, shift):
        global end_x
        end_x = x
        global end_y
        end_y = y
        button2.enabled=True

class start(object):
    """Implementation for Toolbar_addin.tool1 (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "NONE"
    def onMouseDownMap(self, x, y, button, shift):
        global start_x
        start_x = x
        global start_y
        start_y = y
        tool2.enabled=True


class wyznacztrase(object):
    """Implementation for Toolbar_addin.button2 (Button)"""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        inpt = pythonaddins.OpenDialog("Otworz plik z werteksami", False, "")
        arcpy.env.workspace = inpt[: inpt.rfind("\\")]

        x = start_x  # z clicku poczatek
        y = start_y

        # szukanie najblizszego vertexu do wskazanego punktu - start
        arcpy.CreateFeatureclass_management(inpt[: inpt.rfind("\\")], "tmp.shp", "POINT", inpt[inpt.rfind("\\") + 1:])
        cursor = arcpy.da.InsertCursor("tmp.shp", ["SHAPE@"])
        cursor.insertRow((arcpy.PointGeometry(arcpy.Point(x, y))))

        arcpy.SpatialJoin_analysis("tmp.shp", inpt[inpt.rfind("\\") + 1:], "start.shp", "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CLOSEST")
        cursor1 = arcpy.SearchCursor("start.shp")
        for row in cursor1:
            startPoint = row.getValue("ident_1")
        arcpy.AddMessage(startPoint)

        arcpy.Delete_management("tmp.shp")

        # szukanie najblizszego vertexu do wskazanego punktu - end
        x = end_x  # z clicku koniec
        y = end_y
        arcpy.CreateFeatureclass_management(inpt[: inpt.rfind("\\")], "tmp2.shp", "POINT", inpt[inpt.rfind("\\") + 1:])
        cursor = arcpy.da.InsertCursor("tmp2.shp", ["SHAPE@"])
        cursor.insertRow((arcpy.PointGeometry(arcpy.Point(x, y))))

        arcpy.SpatialJoin_analysis("tmp2.shp", inpt[inpt.rfind("\\") + 1:], "cel.shp", "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CLOSEST")
        cursor1 = arcpy.SearchCursor("cel.shp")
        for row in cursor1:
            endPoint = row.getValue("ident_1")
        arcpy.AddMessage(endPoint)

        arcpy.Delete_management("tmp2.shp")

        tab_vert = a_star(graf[0][startPoint], graf[0][endPoint], set())
        print("Sciezka:", [i.id for i in tab_vert])
        wizualizacja(tab_vert, plik_z_krawedziami, plik_z_werteksami)
        button3.enabled = True