import random
import arcpy
import math
import numpy as np
import os
import shutil
from datetime import *
arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"
import UBIGEO


def EnumerarSecciones(ubigeos):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"

    #MZS_AEU_dbf = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"
    MZS_AEU_TEMP = "in_memory\\MZS_AEU_dbf"
    ZONA_CANT_AEU="in_memory\\ZONA_CANT_AEU"


    #ZONA_AEU = "D:/ShapesPruebasSegmentacionUrbana/SECCIONES/EnumerarSecciones/ZONA_AEU"


    ZONA_AEU = "in_memory\\ZONA_AEU"

    AEUS = "D:/ShapesPruebasSegmentacionUrbana/AEU/Renumerar/TB_AEUS.dbf"
    AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/Renumerar/TB_AEUS_LINEAS.shp"

    MZS_AEU="D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"
    #AEUS="D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/TB_AEUS.shp"

    RUTAS_LINEAS="D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"

    #RUTAS_LINEAS="in_memory\\TB_RUTAS_LINEAS"
    MARCOS_AEUS = "D:/ShapesPruebasSegmentacionUrbana/AEU/Mapas/TB_MARCOS_AEUS.shp"


    arcpy.Sort_management("D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/MZS_AEU.dbf", MZS_AEU_TEMP,
                          ["UBIGEO", "ZONA", "AEU_FINAL"])




    arcpy.Statistics_analysis(MZS_AEU_TEMP,ZONA_AEU , [["CANT_VIV", "SUM"]],
                              ["UBIGEO", "ZONA","AEU_FINAL"])  # SE OBTIENE LAS  AEU'S POR ZONA

    arcpy.Statistics_analysis(ZONA_AEU,ZONA_CANT_AEU, [["AEU_FINAL", "COUNT"]], ["UBIGEO", "ZONA"]) # SE OBTIENE LA  CANTIDAD DE AEU'S POR ZONA

    #arcpy.Statistics_analysis(RUTAS_DISSOLVE, ZONA_CANT_AEU, [["AEU", "COUNT"]],
    #                          ["UBIGEO", "ZONA"])  # SE OBTIENE LA  CANTIDAD DE AEU'S POR ZONA

    #arcpy.AddField_management(RUTAS, "SECCION", "SHORT")

    arcpy.AddField_management(RUTAS_LINEAS, "SECCION", "SHORT")
    arcpy.AddField_management(MZS_AEU, "SECCION", "SHORT")
    arcpy.AddField_management(ZONA_AEU, "SECCION", "SHORT")
    arcpy.AddField_management(AEUS, "SECCION", "SHORT")
    arcpy.AddField_management(AEUS_LINEAS, "SECCION", "SHORT")
    arcpy.AddField_management(MARCOS_AEUS, "SECCION", "SHORT")

    arcpy.AddField_management(ZONA_CANT_AEU, "CANT_SECC", "SHORT")
    arcpy.AddField_management(ZONA_CANT_AEU, "RESIDUO", "SHORT")
    arcpy.AddField_management(ZONA_CANT_AEU, "CANT_AEU_SEC", "SHORT")

    expression = "math.ceil(float( !COUNT_AEU_FINAL! )/6.0 )"
    arcpy.CalculateField_management(ZONA_CANT_AEU, "CANT_SECC",expression,"PYTHON_9.3" )

    expression2 = "math.floor(!COUNT_AEU_FINAL!/!CANT_SECC!)"
    arcpy.CalculateField_management(ZONA_CANT_AEU, "CANT_AEU_SEC", expression2, "PYTHON_9.3")

    expression3 = "!COUNT_AEU_FINAL!%!CANT_SECC!"
    arcpy.CalculateField_management(ZONA_CANT_AEU, "RESIDUO", expression3,"PYTHON_9.3")


    where_expression = ""

    where_expression=UBIGEO.ExpresionUbigeos(ubigeos)


    cant_secciones=0
    cant_aeu=0
    cant_aeu_secc=0
    residuo=0
    residuo_temp=0

    for row1 in arcpy.da.SearchCursor(ZONA_CANT_AEU,["UBIGEO", "ZONA", "COUNT_AEU_FINAL","CANT_SECC","CANT_AEU_SEC","RESIDUO"],where_expression):
        where_expression2 = " UBIGEO=\'" + str(row1[0]) + "\'  AND  ZONA=\'" + str(row1[1])+"\'"

        cant_aeu=int(row1[2])
        cant_secciones=int(row1[3])
        cant_aeu_secc=int(row1[4])
        residuo=int(row1[5])

        residuo_temp=residuo

        seccion=1

        i=1
        m=0

        with arcpy.arcpy.da.UpdateCursor(ZONA_AEU, ['AEU_FINAL', 'SECCION'],where_expression2) as cursor2:
            for row2 in cursor2:
                row2[1]=seccion
                where_expression3 = " UBIGEO=\'" + str(row1[0]) + "\'  AND  ZONA=\'" + str(row1[1]) + "\' AND AEU_FINAL="+str(row2[0])

                with arcpy.da.UpdateCursor(AEUS, ['AEU_FINAL', 'SECCION'], where_expression3) as cursor3:
                    for row3 in cursor3:
                        row3[1]=seccion
                        cursor3.updateRow(row3)
                del cursor3


                with arcpy.da.UpdateCursor(MARCOS_AEUS, ['AEU_FINAL', 'SECCION'], where_expression3) as cursor4:
                    for row4 in cursor4:
                        row4[1]=seccion
                        cursor4.updateRow(row4)
                del cursor4

                with arcpy.da.UpdateCursor(RUTAS_LINEAS, ['AEU_FINAL', 'SECCION'], where_expression3) as cursor5:
                    for row5 in cursor5:
                        row5[1]=seccion
                        cursor5.updateRow(row5)
                del cursor5

                with arcpy.da.UpdateCursor(AEUS_LINEAS, ['AEU_FINAL', 'SECCION'], where_expression3) as cursor6:
                    for row6 in cursor6:
                        row6[1]=seccion
                        cursor6.updateRow(row6)
                del cursor6

                with arcpy.da.UpdateCursor(MZS_AEU, ['AEU_FINAL', 'SECCION'], where_expression3) as cursor7:
                    for row7 in cursor7:
                        row7[1] = seccion
                        cursor7.updateRow(row7)
                del cursor7
                #residuo_temp=residuo_temp-1

                i = i + 1

                if residuo_temp>0:
                    if i>(cant_aeu_secc+1):
                        i=1
                        seccion=seccion+1
                        residuo_temp=residuo_temp-1

                else:
                    if i > (cant_aeu_secc):
                        i = 1
                        seccion = seccion + 1
                cursor2.updateRow(row2)


 # SE OBTIENE LAS RUTAS COMO UNA SOLA ENTIDAD
    del row1

def CrearMarcosSecciones():
    arcpy.env.overwriteOutput = True
    MARCOS_AEUS = "D:/ShapesPruebasSegmentacionUrbana/AEU/Mapas/TB_MARCOS_AEUS.shp"
    #MARCOS_AEUS = "D:/ShapesPruebasSegmentacionUrbana/SECCIONES/Mapas/TB_MARCOS_AEUS.shp"
    MARCOS_SECCIONES = "D:/ShapesPruebasSegmentacionUrbana/SECCIONES/Mapas/TB_MARCOS_SECCIONES.shp"

    if arcpy.Exists(MARCOS_SECCIONES):
        arcpy.Delete_management(MARCOS_SECCIONES)

    arcpy.Dissolve_management(MARCOS_AEUS, MARCOS_SECCIONES, ["UBIGEO","ZONA", "SECCION"],
                              [["AEU_FINAL", "SUM"]])
    arcpy.AddField_management(MARCOS_SECCIONES, "ID_MAPA", "TEXT")

    expression="str(!UBIGEO!)+str(!ZONA!)+str(!SECCION!)"

    arcpy.CalculateField_management(MARCOS_SECCIONES, "ID_MAPA", expression,"PYTHON_9.3")

def CrearSecciones(ubigeos):
    arcpy.env.overwriteOutput = True
    AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    SECCIONES="D:/ShapesPruebasSegmentacionUrbana/SECCIONES/EnumerarSecciones/TB_SECCIONES.shp"
    ZONA_AEU = "in_memory\\ZONA_AEU_2"
    ZONA_SECCION = "in_memory\\ZONA_SECCION_2"
    MZS_AEU = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"
    MZS_AEU_TEMP = "in_memory\\MZS_AEU_dbf_2"


    if arcpy.Exists(SECCIONES):
        arcpy.Delete_management(SECCIONES)

    arcpy.Sort_management(MZS_AEU, MZS_AEU_TEMP,
                          ["UBIGEO", "CODCCPP","ZONA", "SECCION", "AEU_FINAL"])

    arcpy.Statistics_analysis(MZS_AEU_TEMP, ZONA_AEU, [["CANT_VIV", "SUM"]],
                          ["UBIGEO", "CODCCPP","ZONA","SECCION" ,"AEU_FINAL"])  # SE OBTIENE LAS  AEU'S POR ZONA

    arcpy.Statistics_analysis(ZONA_AEU, ZONA_SECCION, [["SUM_CANT_VIV", "SUM"]],
                              ["UBIGEO", "CODCCPP","ZONA", "SECCION"])  # SE OBTIENE LAS  AEU'S POR ZONA


    arcpy.MakeFeatureLayer_management(AEUS_LINEAS,"aeus")
    where_expression = UBIGEO.ExpresionUbigeos(ubigeos)
    j=0

    for row1 in arcpy.da.SearchCursor(ZONA_SECCION, ["UBIGEO", "ZONA", "SECCION","SUM_SUM_CANT_VIV","CODCCPP"], where_expression):
        where_expression2 = " UBIGEO=\'" + str(row1[0]) + "\'  AND  ZONA=\'" + str(row1[1])  + "\'  AND  SECCION=" + str(row1[2])

        arcpy.SelectLayerByAttribute_management("aeus", "NEW_SELECTION", where_expression2)


        out_feature_1 = "in_memory/Buffer" + str(row1[0]) + str(row1[1]) + str(row1[2])
        out_feature_2 = "in_memory/FeatureToLine" + str(row1[0]) + str(row1[1]) + str(row1[2])
        out_feature_3 = "in_memory/FeatureToPolygon" + str(row1[0]) + str(row1[1]) + str(row1[2])
        out_feature = "D:/ShapesPruebasSegmentacionUrbana/SECCIONES/Mapas/Dissolve/" + str(row1[0]) + str(
            row1[1]) + str(row1[2]) + ".shp"


        arcpy.Buffer_analysis("aeus",out_feature_1, '5 METERS','FULL', 'ROUND','LIST',['UBIGEO','ZONA','SECCION'])
        arcpy.FeatureToLine_management(out_feature_1,out_feature_2 )
        arcpy.FeatureToPolygon_management(out_feature_2,out_feature_3)
        arcpy.Dissolve_management( out_feature_3,out_feature )

        arcpy.AddField_management(out_feature, "UBIGEO", "TEXT")
        arcpy.AddField_management(out_feature, "CODCCPP", "TEXT")
        arcpy.AddField_management(out_feature, "ZONA", "TEXT")
        arcpy.AddField_management(out_feature, "SECCION", "SHORT")
        arcpy.AddField_management(out_feature, "CANT_VIV", "SHORT")



        calculate_expression1="\'"+str(row1[0])+"\'"
        calculate_expression2 = "\'" + str(row1[1])+"\'"

        calculate_expression3 = str(row1[2])
        calculate_expression4 = str(row1[3])

        calculate_expression5 = "\'" + str(row1[4]) + "\'"

        arcpy.CalculateField_management(out_feature, "UBIGEO",calculate_expression1 , "PYTHON_9.3")
        arcpy.CalculateField_management(out_feature, "CODCCPP", calculate_expression5, "PYTHON_9.3")
        arcpy.CalculateField_management(out_feature, "ZONA", calculate_expression2, "PYTHON_9.3")
        arcpy.CalculateField_management(out_feature, "SECCION", calculate_expression3, "PYTHON_9.3")
        arcpy.CalculateField_management(out_feature, "CANT_VIV", calculate_expression4, "PYTHON_9.3")

        if (j == 0):
            arcpy.CopyFeatures_management(out_feature, SECCIONES)
        else:
            arcpy.Append_management(out_feature, SECCIONES)
        j = j + 1
        arcpy.Delete_management(out_feature_1)
        arcpy.Delete_management(out_feature_2)
        arcpy.Delete_management(out_feature_3)

    del row1



