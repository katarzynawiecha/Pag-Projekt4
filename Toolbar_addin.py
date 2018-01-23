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
        tool1.enabled = True

class Korek(object):
    """Implementation for Toolbar_addin.button3 (Button)"""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        korki = set()
        for row in arcpy.SearchCursor("lyr"):
            korki.add(row)
        tab_vert = a_star(stPt, endPt, korki)
        print("Sciezka:", [i.id for i in tab_vert])
        arcpy.Delete_management("lyr")
        wizualizacja(tab_vert, plik_z_krawedziami, plik_z_werteksami,"ominieteKorki")




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
        self.enabled = False
        self.shape = "NONE"
    def onClick(self):
        print("klik")
        arcpy.Delete_management(plik_z_werteksami[: plik_z_werteksami.rfind("\\")] + "start.shp")
        arcpy.Delete_management(plik_z_werteksami[: plik_z_werteksami.rfind("\\")] + "cel.shp")
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
        button3.enabled = True
        arcpy.env.workspace = plik_z_werteksami[: plik_z_werteksami.rfind("\\")]
        x = start_x  # z clicku poczatek
        y = start_y

        # szukanie najblizszego vertexu do wskazanego punktu - start
        arcpy.CreateFeatureclass_management("in_memory", "tmp", "POINT", plik_z_werteksami[plik_z_werteksami.rfind("\\") + 1:])
        cursor = arcpy.da.InsertCursor("tmp", ["SHAPE@"])
        cursor.insertRow((arcpy.PointGeometry(arcpy.Point(x, y))))

        arcpy.SpatialJoin_analysis("tmp", plik_z_werteksami[plik_z_werteksami.rfind("\\") + 1:], "start.shp", "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CLOSEST")
        cursor1 = arcpy.SearchCursor("start.shp")
        for row in cursor1:
            startPoint = row.getValue("ident_1")
        arcpy.AddMessage(startPoint)
        arcpy.Delete_management("tmp")
        arcpy.Delete_management("in_memory\\tmp")

        # szukanie najblizszego vertexu do wskazanego punktu - end
        x = end_x  # z clicku koniec
        y = end_y
        arcpy.CreateFeatureclass_management("in_memory", "tmp2", "POINT", plik_z_werteksami[plik_z_werteksami.rfind("\\") + 1:])
        cursor = arcpy.da.InsertCursor("tmp2", ["SHAPE@"])
        cursor.insertRow((arcpy.PointGeometry(arcpy.Point(x, y))))

        arcpy.SpatialJoin_analysis("tmp2", plik_z_werteksami[plik_z_werteksami.rfind("\\") + 1:], "cel.shp", "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CLOSEST")
        cursor1 = arcpy.SearchCursor("cel.shp")
        for row in cursor1:
            endPoint = row.getValue("ident_1")
        arcpy.AddMessage(endPoint)
        arcpy.Delete_management("tmp2")
        arcpy.Delete_management("in_memory\\tmp2")
        global stPt
        stPt = graf[0][startPoint]
        global endPt
        endPt = graf[0][endPoint]
        tab_vert = a_star(graf[0][startPoint], graf[0][endPoint], set())
        print("Sciezka:", [i.id for i in tab_vert])
        wizualizacja(tab_vert, plik_z_krawedziami, plik_z_werteksami,"bezKorkow")
