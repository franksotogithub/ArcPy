import math
import numpy as np
import os
import shutil
import arcpy
import  SolucionInicialUrbano as s

import ActualizarAEU as a

import ImportarExportarSQL as ie
import  UBIGEO


arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"


MZS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp"
expression_2 = "flg_manzana(!VIV_MZ!)"
codeblock = """
def flg_manzana(VIV_MZ):
  if (VIV_MZ>16):
      return 1
  else:
      return 0"""

arcpy.CalculateField_management(MZS, "FLG_MZ", expression_2, "PYTHON_9.3", codeblock)