import arcpy
import numpy as np
import CreateLineGeometry as c
arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"


inFeatures = "D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"
arcpy.AddField_management(inFeatures, "IDMANZANA", "TEXT")
exp = "!UBIGEO!+!ZONA!+!MANZANA!"
arcpy.CalculateField_management(inFeatures, "IDMANZANA", exp, "PYTHON_9.3")