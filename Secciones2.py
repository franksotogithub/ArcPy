import random
import arcpy
import math
import numpy as np
import os
import shutil

arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"


def EnumerarSecciones(ubigeos):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"

    MZS_AEU_dbf = "D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/MZS_AEU.dbf"
    ZONA_CANT_AEU="in_memory/ZONA_CANT_AEU"
    ZONA_AEU = "in_memory/ZONA_AEU"

    AEUS="D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/TB_AEUS.shp"
    RUTAS="D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/TB_RUTAS.shp"

    MARCOS_AEUS="D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/TB_MARCOS_AEUS.shp"
    #MARCOS_SECCIONES = "D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/TB_MARCOS_SECCIONES.shp"

    #if arcpy.Exists(ZONA_CANT_AEU):
    #    arcpy.Delete_management(ZONA_CANT_AEU)
    if arcpy.Exists(AEUS):
        arcpy.Delete_management(AEUS)
    #if arcpy.Exists(ZONA_AEU):
    #    arcpy.Delete_management(ZONA_AEU)
    if arcpy.Exists(MZS_AEU_dbf):
        arcpy.Delete_management(MZS_AEU_dbf)
    if arcpy.Exists(RUTAS):
        arcpy.Delete_management(RUTAS)

    if arcpy.Exists(MARCOS_AEUS):
        arcpy.Delete_management(MARCOS_AEUS)

    #arcpy.Copy_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf", MZS_AEU_dbf)
    #arcpy.AddField_management(MZS_AEU_dbf, "SECCION", "SHORT")

    arcpy.Sort_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_RUTAS.shp", RUTAS, ["UBIGEO","ZONA","AEU_FINAL"] )

    #arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_RUTAS.shp", RUTAS)


    arcpy.Sort_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf", MZS_AEU_dbf,
                          ["UBIGEO", "ZONA", "AEU_FINAL"])


    #arcpy.Copy_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf", MZS_AEU_dbf)



    arcpy.Copy_management("D:/ShapesPruebasSegmentacionUrbana/Mapas/TB_MARCOS_AEUS.shp",
                          MARCOS_AEUS)




    #arcpy.Statistics_analysis(MZS_AEU_dbf, , [["IDMANZANA", "MIN"]], ["UBIGEO", "ZONA", "AEU"])

    arcpy.Dissolve_management(RUTAS, AEUS,["UBIGEO", "ZONA","AEU_FINAL"], [["VIV_AEU","SUM"]]) # SE OBTIENE LAS RUTAS COMO UNA SOLA ENTIDAD




    arcpy.Statistics_analysis(MZS_AEU_dbf,ZONA_AEU , [["VIV_AEU", "SUM"]],
                              ["UBIGEO", "ZONA","AEU_FINAL"])  # SE OBTIENE LAS  AEU'S POR ZONA

    arcpy.Statistics_analysis(ZONA_AEU,ZONA_CANT_AEU, [["AEU_FINAL", "COUNT"]], ["UBIGEO", "ZONA"]) # SE OBTIENE LA  CANTIDAD DE AEU'S POR ZONA

    #arcpy.Statistics_analysis(RUTAS_DISSOLVE, ZONA_CANT_AEU, [["AEU", "COUNT"]],
    #                          ["UBIGEO", "ZONA"])  # SE OBTIENE LA  CANTIDAD DE AEU'S POR ZONA

    #arcpy.AddField_management(RUTAS, "SECCION", "SHORT")

    arcpy.AddField_management(RUTAS, "SECCION", "SHORT")
    arcpy.AddField_management(MZS_AEU_dbf, "SECCION", "SHORT")
    arcpy.AddField_management(ZONA_AEU, "SECCION", "SHORT")
    arcpy.AddField_management(AEUS, "SECCION", "SHORT")
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

    #arcpy.AddField_management(ZONA_CANT_AEU, "CANT_SECC", "SHORT")

    where_list=ubigeos
    m = 0
    where_expression = ""

    for x in where_list:
        if (m + 1) == len(where_list):
            where_expression = where_expression + ' "UBIGEO"=\'%s\' ' % where_list[m]
        else:
            where_expression = where_expression + ' "UBIGEO"=\'%s\' OR' % (where_list[m])

        m = m + 1

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
                where_expression4 = " UBIGEO=\'" + str(int(row1[0])) + "\'  AND  ZONA=\'" + str(int(row1[1])) + "\' AND AEU_FINAL=" + str(row2[0])

                with arcpy.arcpy.da.UpdateCursor(AEUS, ['AEU_FINAL', 'SECCION'], where_expression3) as cursor3:
                    for row3 in cursor3:
                        row3[1]=seccion
                        cursor3.updateRow(row3)
                del cursor3



                with arcpy.arcpy.da.UpdateCursor(MARCOS_AEUS, ['AEU_FINAL', 'SECCION'], where_expression4) as cursor4:
                    for row4 in cursor4:
                        row4[1]=seccion
                        cursor4.updateRow(row4)
                del cursor4

                with arcpy.arcpy.da.UpdateCursor(RUTAS, ['AEU_FINAL', 'SECCION'], where_expression3) as cursor5:
                    for row5 in cursor5:
                        row4[1]=seccion
                        cursor5.updateRow(row4)
                del cursor5

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

def CrearMarcosSecciones():
    MARCOS_AEUS="D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/TB_MARCOS_AEUS.shp"
    MARCOS_SECCIONES = "D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/TB_MARCOS_SECCIONES.shp"

    if arcpy.Exists(MARCOS_SECCIONES):
        arcpy.Delete_management(MARCOS_SECCIONES)

    arcpy.Dissolve_management(MARCOS_AEUS, MARCOS_SECCIONES, ["UBIGEO", "ZONA", "SECCION"],
                              [["AEU_FINAL", "SUM"]])


    arcpy.AddField_management(MARCOS_SECCIONES, "ID_MAPA", "TEXT")

    expression="str(!UBIGEO!)+str(!ZONA!)+str(!SECCION!)"

    arcpy.CalculateField_management(MARCOS_SECCIONES, "ID_MAPA", expression,"PYTHON_9.3")


def CrearSecciones(ubigeos):

    AEUS = "D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/TB_AEUS.shp"
    SECCIONES="D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/TB_SECCIONES.shp"

    #MARCOS_SECCIONES = "D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/TB_MARCOS_SECCIONES.shp"

    ZONA_AEU = "D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/ZONA_AEU"
    ZONA_SECCION = "D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/ZONA_SECCION"
    arcpy.MakeFeatureLayer_management(AEUS,
                                      "aeus")

    BUFFER="D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/Buffer/"
    FEATURETOLINE = "D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/FeatureToLine/"
    FEATURETOPOLYGON = "D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/FeatureToPolygon/"
    DISSOLVE = "D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/Dissolve/"

    if arcpy.Exists(ZONA_SECCION):
        arcpy.Delete_management(ZONA_SECCION)

    if arcpy.Exists(SECCIONES):
        arcpy.Delete_management(SECCIONES)

    #Eliminado Carpetas de los marcos
    if os.path.exists(BUFFER):
        shutil.rmtree(BUFFER)
    if os.path.exists(FEATURETOLINE):
        shutil.rmtree(FEATURETOLINE)
    if os.path.exists(FEATURETOPOLYGON):
        shutil.rmtree(FEATURETOPOLYGON)

    if os.path.exists(DISSOLVE):
        shutil.rmtree(DISSOLVE)
    ####creando las carpetas de los marcos

    os.mkdir(BUFFER)
    os.mkdir(FEATURETOLINE)
    os.mkdir(FEATURETOPOLYGON)
    os.mkdir(DISSOLVE)


    arcpy.Statistics_analysis(ZONA_AEU, ZONA_SECCION, [["SUM_VIV_AEU", "SUM"]],
                              ["UBIGEO", "ZONA", "SECCION"])  # SE OBTIENE LAS  AEU'S POR ZONA

    #SECCIONES = "D:/ShapesPruebasSegmentacionUrbana/Marcos/TB_SECCIONES.shp"

    where_list=ubigeos
    m = 0
    where_expression = ""

    for x in where_list:
        if (m + 1) == len(where_list):
            where_expression = where_expression + ' "UBIGEO"=\'%s\' ' % where_list[m]
        else:
            where_expression = where_expression + ' "UBIGEO"=\'%s\' OR' % (where_list[m])

        m = m + 1



    #for row1 in arcpy.da.SearchCursor(AEUS,["UBIGEO", "ZONA", "AEU_FINAL", "SECCION"],where_expression):

    j=0

    for row1 in arcpy.da.SearchCursor(ZONA_SECCION, ["UBIGEO", "ZONA", "SECCION","SUM_SUM_VIV_AEU"], where_expression):
        where_expression2 = " UBIGEO=\'" + str(row1[0]) + "\'  AND  ZONA=\'" + str(row1[1])  + "\'  AND  SECCION=" + str(row1[2])
        arcpy.SelectLayerByAttribute_management("aeus", "NEW_SELECTION", where_expression2)

        #for row1 in arcpy.da.SearchCursor(ZONA_SECCION, ["UBIGEO", "ZONA", "AEU_FINAL", "SECCION"], where_expression):


        arcpy.Buffer_analysis("aeus",
                              "D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/Buffer/" + str(row1[0]) + str(row1[1]) + str(
                                  row1[2]) + ".shp", '5 METERS',
                              'FULL', 'ROUND','LIST',['UBIGEO','ZONA','SECCION'])
        arcpy.FeatureToLine_management("D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/Buffer/" + str(row1[0]) + str(row1[1]) + str(
                                  row1[2]) + ".shp","D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/FeatureToLine/" + str(row1[0]) + str(row1[1]) + str(
                                  row1[2]) + ".shp" )

        arcpy.FeatureToPolygon_management("D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/FeatureToLine/" + str(row1[0]) + str(row1[1]) + str(
                                  row1[2]) + ".shp","D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/FeatureToPolygon/" + str(row1[0]) + str(row1[1]) + str(
                                  row1[2]) + ".shp")

        arcpy.Dissolve_management(
            "D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/FeatureToPolygon/" + str(row1[0]) + str(row1[1]) + str(
                row1[2]) + ".shp",
            "D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/Dissolve/" + str(row1[0]) + str(row1[1]) + str(
                row1[2]) + ".shp")




        out_feature = "D:/ShapesPruebasSegmentacionUrbana/MapasSecciones/Dissolve/"+str(row1[0])+str(row1[1])+str(row1[2])+".shp"
        arcpy.AddField_management(out_feature, "UBIGEO", "TEXT")
        arcpy.AddField_management(out_feature, "ZONA", "TEXT")
        arcpy.AddField_management(out_feature, "SECCION", "SHORT")
        arcpy.AddField_management(out_feature, "CANT_VIV", "SHORT")


        calculate_expression1="\'"+str(row1[0])+"\'"
        calculate_expression2 = "\'" + str(row1[1])+"\'"
        calculate_expression3 = str(row1[2])
        calculate_expression4 =   str(row1[3])

        arcpy.CalculateField_management(out_feature, "UBIGEO",calculate_expression1 , "PYTHON_9.3")
        arcpy.CalculateField_management(out_feature, "ZONA", calculate_expression2, "PYTHON_9.3")
        arcpy.CalculateField_management(out_feature, "SECCION", calculate_expression3, "PYTHON_9.3")
        arcpy.CalculateField_management(out_feature, "CANT_VIV", calculate_expression4, "PYTHON_9.3")

        if (j == 0):
            arcpy.CopyFeatures_management(out_feature, SECCIONES)
        else:
            arcpy.Append_management(out_feature, SECCIONES)
        j = j + 1



        #arcpy.FeatureToPolygon(
        #    "D:/ShapesPruebasSegmentacionUrbana/Mapas/Buffer/" + str(row1[0]) + str(row1[1]) + str(
        #        row1[2]) + ".shp",
        #    "D:/ShapesPruebasSegmentacionUrbana/Mapas/FeatureToLine/" + str(row1[0]) + str(row1[1]) + str(
        #        row1[2]) + ".shp")





ubigeos=["020601","021806","110204"]
#EnumerarSecciones(ubigeos)
#CrearMarcosSecciones()
CrearSecciones(ubigeos)



