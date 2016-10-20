import arcpy
import random
#import  CalculateCircle as c
import math
import CalculoFuncionObjetivo as funcionObjetivo


arcpy.env.workspace = r"D:/ArcGisShapesPruebas"
fc="D:/ArcGisShapesPruebas/Zones/Shape15013300100.shp"

def ActualizarViviendas(zona):

# ASIGNAR LOS GRUPOS AL SHAPE

    fc=zona
    numero_grupo = 0
    fields = ["TOT_VIV"]
     # print numero_grupo
     # print where_expression
    with arcpy.da.UpdateCursor(fc, fields) as cursor:
        for row in cursor:
            row[0] = random.randint(0, 15)
            cursor.updateRow(row)




where_list=["150133"]
where_expression=' "IDDIST"=%s ' % (where_list[0])
i=0
max_zonas=8




for row  in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/Zones/zona_censal.shp", ["IDDIST","CODZONA","SUFZONA"]):

    desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])+".shp"
    fc="D:/ArcGisShapesPruebas/Zones/"+desc
    #print fc
    ActualizarViviendas(fc)
    i=i+1
    if i>max_zonas:
        break