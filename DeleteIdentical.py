import arcpy
from arcpy import env

env.workspace = r"D:/ArcGisShapesPruebas/WriteGeometry"
desc="Shape15013300200.shp"

arcpy.DeleteIdentical_management(r"D:/ArcGisShapesPruebas/WriteGeometry/"+desc, ["Shape"])


