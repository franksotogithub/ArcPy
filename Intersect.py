
import arcpy
from arcpy import env


env.workspace = r"D:/ArcGisShapesPruebas/"

desc="Shape07010100100.shp"
arcpy.Intersect_analysis (["D:/ArcGisShapesPruebas/VoronoiLine/Shape"+desc,"D:/ArcGisShapesPruebas/Edge/"+desc], "D:/ArcGisShapesPruebas/Intersections/"+desc, "", "", "point")

