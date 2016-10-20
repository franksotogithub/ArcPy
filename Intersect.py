
import arcpy
from arcpy import env


env.workspace = r"D:/ArcGisShapesPruebas/"

#desc="Shape07010100100.shp"
desc="Shape15013300200.shp"
arcpy.Intersect_analysis (["D:/ArcGisShapesPruebas/WriteGeometry/"+desc,"D:/ArcGisShapesPruebas/Edge/"+desc], "D:/ArcGisShapesPruebas/IntersectionsInitial/Tolerancia"+desc, "ALL", "", "point")

