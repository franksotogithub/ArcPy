import random
import math
import numpy as np
import os
import shutil
import arcpy
import  SolucionInicialUrbano as s
from arcpy import env
import ActualizarAEU as a

import ImportarExportarSQL as ie
import  UBIGEO
import EliminarAdyacencias
import ConectionSQL as conx
import CreateLineGeometry as c

from time import time
from datetime import *
arcpy.env.overwriteOutput = True

#
#def ImportarManzanas(ubigeos):
#    MZS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/TB_MZS_2.shp"
#    arcpy.env.workspace = "Database Connections/PruebaSegmentacion.sde"
#
#    where_expression=UBIGEO.ExpresionUbigeosImportacion(ubigeos)
#
#
#    arcpy.Select_analysis("CPV_SEGMENTACION.dbo.VW_MANZANA",MZS, where_expression)
#    arcpy.AddField_management(MZS, "IDMANZANA", "TEXT")
#    expression = "str(!UBIGEO!)+str(!ZONA!)+str(!MANZANA!)"
#    arcpy.CalculateField_management(MZS, "IDMANZANA", expression, "PYTHON_9.3")
#


def ImportarTablasTrabajo(ubigeos):
    arcpy.env.overwriteOutput = True
    MZS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    VIVIENDAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp"
    ZONAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    PUNTOS_INICIO_shp = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/PuntosInicio/PUNTOS_INICIO.shp"
    EJES_VIALES="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_EJES_VIALES.shp"
    MZS_CONDOMINIOS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS_CONDOMINIOS.dbf"


    if arcpy.Exists("PruebaSegmentacion.sde") == False:
        arcpy.CreateDatabaseConnection_management("Database Connections",
                                                  "PruebaSegmentacion.sde",
                                                  "SQL_SERVER",
                                                  "192.168.200.250",
                                                  "DATABASE_AUTH",
                                                  "sde",
                                                  "$deDEs4Rr0lLo",
                                                  "#",
                                                  "CPV_SEGMENTACION",
                                                  "#",
                                                  "#",
                                                  "#",
                                                  "#")


#    if arcpy.Exists(VIVIENDAS):
#        arcpy.Delete_management(VIVIENDAS)
#    if arcpy.Exists(MZS):
#        arcpy.Delete_management(MZS)
#
#    if arcpy.Exists(ZONAS):
#        arcpy.Delete_management(ZONAS)
#
#    if arcpy.Exists(EJES_VIALES):
#        arcpy.Delete_management(EJES_VIALES)
#
#    if arcpy.Exists(PUNTOS_INICIO_shp):
#        arcpy.Delete_management(PUNTOS_INICIO_shp)
#
#    if arcpy.Exists(BLOQUES):
#        arcpy.Delete_management(BLOQUES)

    arcpy.env.workspace = "Database Connections/PruebaSegmentacion.sde"

    where_expression=UBIGEO.ExpresionUbigeosImportacion(ubigeos)
    #arcpy.FeatureClassToFeatureClass_conversion("CPV_SEGMENTACION.dbo.TB_MZS",
    #                                            "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/",
    #                                            'TB_MZS.shp',where_expression)


    arcpy.Select_analysis("CPV_SEGMENTACION.dbo.TB_PUNTO_INICIO",
                          PUNTOS_INICIO_shp
                          )


    arcpy.Select_analysis("CPV_SEGMENTACION.dbo.VW_MANZANA",MZS, where_expression)

    arcpy.Select_analysis("CPV_SEGMENTACION.dbo.VW_ZONA_CENSAL",
                                                ZONAS
                                                ,where_expression)
    arcpy.Select_analysis("CPV_SEGMENTACION.sde.VW_VIVIENDAS_U3",
                                                VIVIENDAS
                                                ,where_expression)

    arcpy.Select_analysis("CPV_SEGMENTACION.dbo.TB_EJE_VIAL",
                                                EJES_VIALES
                                                , where_expression)

    arcpy.TableToTable_conversion('CPV_SEGMENTACION.sde.VW_MZS_CONDOMINIOS', 'D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/', 'TB_MZS_CONDOMINIOS.dbf')


    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbanaCondominios"
    arcpy.DeleteField_management(MZS, ['AEU','IDMANZANA'])

    arcpy.AddField_management(MZS, "IDMANZANA", "TEXT")
    expression = "str(!UBIGEO!)+str(!ZONA!)+str(!MANZANA!)"
    arcpy.CalculateField_management(MZS, "IDMANZANA", expression, "PYTHON_9.3")
    arcpy.AddField_management(MZS, "AEU", "SHORT")
    arcpy.AddField_management(MZS, "AEU_2", "SHORT")
    arcpy.AddField_management(MZS, "FLG_MZ", "SHORT")


def CrearMatrizAdyacencia(ubigeos):
    arcpy.env.overwriteOutput = True
    ADYACENCIA="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/MatrizAdyacencia/adyacencia.dbf"
    MZS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    ZONAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"



    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbanaCondominios"
    arcpy.env.workspace = "Database Connections"
    if arcpy.Exists("PruebaSegmentacion.sde") == False:
        arcpy.CreateDatabaseConnection_management("Database Connections",
                                                  "PruebaSegmentacion.sde",
                                                  "SQL_SERVER",
                                                  "192.168.200.250",
                                                  "DATABASE_AUTH",
                                                  "sde",
                                                  "$deDEs4Rr0lLo",
                                                  "#",
                                                  "CPV_SEGMENTACION",
                                                  "#",
                                                  "#",
                                                  "#",
                                                  "#")








    where_list = ubigeos

    inFeatures = MZS
    fieldName1 = "xCentroid"
    fieldName2 = "yCentroid"
    fieldPrecision = 18
    fieldScale = 6
    fieldScale2 = 2
    #### Add fields

    lst = arcpy.ListFields(MZS)
    for f in lst:
        if (f.name==fieldName1):
            arcpy.DeleteField_management(inFeatures,["xCentroid"])
        if (f.name==fieldName2):
            arcpy.DeleteField_management(inFeatures,["yCentroid"])
        if (f.name == "AREA"):
            arcpy.DeleteField_management(inFeatures, ["AREA"])


    arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE",
                                      fieldPrecision, fieldScale)
    arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE",
                                  fieldPrecision, fieldScale)

    arcpy.AddField_management(inFeatures, "AREA", "DOUBLE", fieldPrecision, fieldScale2)




    # Calculate centroid

    fields = ["SHAPE@X", "SHAPE@Y", "xCentroid", "yCentroid"]

    with arcpy.da.UpdateCursor(inFeatures, fields) as cursorx:
        for row0 in cursorx:
            row0[2] = row0[0]
            row0[3] = row0[1]
            cursorx.updateRow(row0)

    exp = "!SHAPE.AREA@METERS!"
    arcpy.CalculateField_management(inFeatures, "AREA", exp, "PYTHON_9.3")



    if arcpy.Exists(ADYACENCIA) == True:
        arcpy.Delete_management(ADYACENCIA)

    arcpy.CreateTable_management("D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/MatrizAdyacencia/", "adyacencia.dbf")

    fieldName1 = "FirstX"
    fieldName2 = "FirstY"

    fieldName3 = "LastX"
    fieldName4 = "LastY"

    fieldPrecision = 18
    fieldScale = 6

    inFeatures = ADYACENCIA

    # Add fields inicio



    arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE",
                              fieldPrecision, fieldScale)
    arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE",
                              fieldPrecision, fieldScale)
    # Add fields inicio
    arcpy.AddField_management(inFeatures, fieldName3, "DOUBLE",
                              fieldPrecision, fieldScale)
    arcpy.AddField_management(inFeatures, fieldName4, "DOUBLE",
                              fieldPrecision, fieldScale)


    where_expression=UBIGEO.ExpresionUbigeos(ubigeos)

    for row in arcpy.da.SearchCursor(ZONAS, ["UBIGEO", "ZONA"],where_expression):
        where_expression2=' "UBIGEO"=\'%s\' AND "ZONA"=\'%s\' ' % (row[0], row[1])
        print where_expression2
        desc=str(row[0])+str(row[1])
        arcpy.MakeFeatureLayer_management(MZS, "manzanas",where_expression2)
        arcpy.MakeFeatureLayer_management(ZONAS, "zona_temp", where_expression2)
        arcpy.FeatureToPoint_management("manzanas",
                                        "in_memory/Point" +desc ,
                                        "CENTROID")

        arcpy.AddField_management("in_memory/Point" +desc , 'Z', "SHORT")
        arcpy.CalculateField_management("in_memory/Point" +desc , 'Z', 1)


        arcpy.CreateThiessenPolygons_analysis("in_memory/Point" + desc,
                                              "in_memory/VoronoiPolygon" + desc,
                                              "ALL")

        arcpy.FeatureTo3DByAttribute_3d("in_memory/Point" +desc, "in_memory/Points3D" + desc, 'Z')

        Tin = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/MatrizAdyacencia/Tin/Shape" + str(row[0]) + "" + str(row[1])

        arcpy.CreateTin_3d(Tin, "", "in_memory/Points3D"+desc, "DELAUNAY")

        arcpy.TinEdge_3d(Tin, "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/MatrizAdyacencia/Edge/" + desc+".shp", edge_type='DATA')


        inFeatures = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/MatrizAdyacencia/Edge/" + desc+".shp"
        Edge="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/MatrizAdyacencia/Edge/" + desc+".shp"

        fieldName1 = "FirstX_1"
        fieldName2 = "FirstY_1"

        fieldName3 = "LastX_1"
        fieldName4 = "LastY_1"

        fieldPrecision = 18
        fieldScale = 6

        # Add fields inicio
        arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE",
                                  fieldPrecision, fieldScale)
        arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE",
                                  fieldPrecision, fieldScale)

        # Add fields fin
        arcpy.AddField_management(inFeatures, fieldName3, "DOUBLE",
                                  fieldPrecision, fieldScale)
        arcpy.AddField_management(inFeatures, fieldName4, "DOUBLE",
                                  fieldPrecision, fieldScale)

        # Calculate Points Firts
        arcpy.CalculateField_management(inFeatures, fieldName1,
                                        "!SHAPE.firstPoint.X!",
                                        "PYTHON_9.3")
        arcpy.CalculateField_management(inFeatures, fieldName2,
                                        "!SHAPE.firstPoint.Y!",
                                        "PYTHON_9.3")

        # Calculate Points Last
        arcpy.CalculateField_management(inFeatures, fieldName3,
                                        "!SHAPE.lastPoint.X!",
                                        "PYTHON_9.3")
        arcpy.CalculateField_management(inFeatures, fieldName4,
                                        "!SHAPE.lastPoint.Y!",
                                        "PYTHON_9.3")



    # pologonos de vonoi a polyline ignorando lados vecinos
        arcpy.PolygonToLine_management("in_memory/VoronoiPolygon"+desc,
                                   "in_memory/VoronoiLine" + desc,
                                   "IGNORE_NEIGHBORS")

    # polyline  a split lines

        arcpy.SplitLine_management("in_memory/VoronoiLine" + desc,
                               "in_memory/VoronoiSplitLine" + desc)

        fieldName1 = "FirstX_2"
        fieldName2 = "FirstY_2"
        fieldName3 = "LastX_2"
        fieldName4 = "LastY_2"

        fieldPrecision = 18
        fieldScale = 6



#        desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2]) + ".shp"
        inFeatures = "in_memory/VoronoiSplitLine" + desc

        # Add fields inicio
        arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE",
                                  fieldPrecision, fieldScale)
        arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE",
                                  fieldPrecision, fieldScale)

        # Add fields fin
        arcpy.AddField_management(inFeatures, fieldName3, "DOUBLE",
                                  fieldPrecision, fieldScale)
        arcpy.AddField_management(inFeatures, fieldName4, "DOUBLE",
                                  fieldPrecision, fieldScale)

        # Calculate Points Firts
        arcpy.CalculateField_management(inFeatures, fieldName1,
                                        "!SHAPE.firstPoint.X!",
                                        "PYTHON_9.3")
        arcpy.CalculateField_management(inFeatures, fieldName2,
                                        "!SHAPE.firstPoint.Y!",
                                        "PYTHON_9.3")

        # Calculate Points Last
        arcpy.CalculateField_management(inFeatures, fieldName3,
                                        "!SHAPE.lastPoint.X!",
                                        "PYTHON_9.3")
        arcpy.CalculateField_management(inFeatures, fieldName4,
                                        "!SHAPE.lastPoint.Y!",
                                        "PYTHON_9.3")

        # Eliminando los registros identicos
        arcpy.DeleteIdentical_management("in_memory/VoronoiSplitLine" + desc, ["Shape"])

        arcpy.Intersect_analysis(["in_memory/VoronoiSplitLine" + desc,
                                  Edge],
                                 "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/MatrizAdyacencia/Intersections/" + desc, "ALL", "", "point")


        fc1 = Edge
        fields1 = ['FID']
        fc2 = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/MatrizAdyacencia/Intersections/" + desc+".shp"
        fields2 = ['FID_'+str(row[0])]



        with arcpy.arcpy.da.SearchCursor(fc1, fields1) as cursor1:
            for row1 in cursor1:

                with arcpy.arcpy.da.UpdateCursor(fc2, fields2) as cursor2:
                    contador = 0
                    for row2 in cursor2:
                        if row1[0] == row2[0]:
                            contador = contador + 1

                        #if contador > 3:
                        #    cursor2.deleteRow()
                        #    contador = contador - 1

        del cursor1


        fc = fc2
        fields = ['FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1', 'FirstX_2', 'FirstY_2', 'LastX_2', 'LastY_2']


        j = 0


        with arcpy.da.UpdateCursor(fc, fields) as cursor:
            for row in cursor:
                a1 = row[0] - row[2]  # ax
                a2 = row[1] - row[3]  # ay  a=(a1,a2)
                b1 = row[4] - row[6]  # bx
                b2 = row[5] - row[7]  # bx b =(b1,b2)

                a = np.array([a1, a2])
                b = np.array([b1, b2])

                producto_escalar = np.dot(a, b)  # a.b=a1*b1 + a2*b2
                coseno = abs(producto_escalar) / (np.linalg.norm(a) * np.linalg.norm(b))





                #if coseno >= 0.005:

                #    cursor.deleteRow()

                j = j + 1

            del cursor


        input_table = fc2
        out_lines ="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/MatrizAdyacencia/ShapesFinal/" + desc+".shp"


            # XY To Line
        arcpy.XYToLine_management(input_table, out_lines,'FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1', "GEODESIC")

        arcpy.DeleteIdentical_management(out_lines, ["Shape"])

        adyacencias_x = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/MatrizAdyacencia/ShapesFinal/" + desc+".shp"


        manzanas = "manzanas"

        EliminarAdyacencias.PorCantidadManzanasCruza(manzanas, adyacencias_x)
        EliminarAdyacencias.PorZonaCruza("zona_temp",adyacencias_x)
        cursorInsertar = arcpy.da.InsertCursor(ADYACENCIA,
                                   ['FirstX', 'FirstY', 'LastX', 'LastY'])
        for row in arcpy.da.SearchCursor(adyacencias_x,
                                     ['FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1']):
        # print row
            cursorInsertar.insertRow(row)
        del cursorInsertar

        arcpy.Delete_management("in_memory/Point" +desc)
        arcpy.Delete_management("in_memory/VoronoiPolygon" + desc)
        arcpy.Delete_management("in_memory/Points3D"+desc)
        arcpy.Delete_management("in_memory/VoronoiSplitLine" + desc)
        arcpy.Delete_management("in_memory/VoronoiLine" + desc)


def ExportarTablasAdyacencia():
    arcpy.env.overwriteOutput = True
    ADYACENCIA = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/MatrizAdyacencia/adyacencia.dbf"
    MZS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    arcpy.env.workspace = r"Database Connections/PruebaSegmentacion.sde"

    if arcpy.Exists(r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.ADYACENCIA"):
        arcpy.Delete_management("Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.adyacencia")

    if arcpy.Exists(r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO"):
        arcpy.Delete_management("Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO")

    arcpy.TableToTable_conversion(ADYACENCIA,
                                  'Database Connections/PruebaSegmentacion.sde/', 'adyacencia')
    MZS_TRABAJO = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS_TRABAJO.shp"

    arcpy.CopyFeatures_management(MZS,MZS_TRABAJO)

    arcpy.FeatureClassToGeodatabase_conversion([MZS_TRABAJO],
                                               'Database Connections/PruebaSegmentacion.sde/')


def CrearViviendasOrdenadas():
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbanaCondominios"
    VIVIENDAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp"

    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"

    if arcpy.Exists(VIVIENDAS_ORDENADAS):
        arcpy.Delete_management(VIVIENDAS_ORDENADAS)

    arcpy.Sort_management(VIVIENDAS, VIVIENDAS_ORDENADAS, ["UBIGEO", "ZONA", "MANZANA", "ID_REG_OR"])

    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "AEU", "SHORT")
    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "OR_VIV_AEU", "SHORT")
    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "FLG_CORTE", "SHORT")
    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "FLG_MZ", "SHORT")

def EnumerarAEUEnViviendasDeManzanasCantVivMayores16(ubigeos):
    arcpy.env.overwriteOutput = True
    MZS="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    VIVIENDAS="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    ZONAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    #VIVIENDAS_OR_MAX = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/VIVIENDAS_OR_MAX"
    VIVIENDAS_AEU_OR_MAX="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/VIVIENDAS_AEU_OR_MAX"
    VIVIENDAS_MZS_OR_MAX = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/VIVIENDAS_MZS_OR_MAX"
    #arcpy.AddField_management(MZS_AEU_dbf, "SECCION", "SHORT")
    MZS_CONDOMINIOS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS_CONDOMINIOS.dbf"
    #TB_BLOQUES="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_BLOQUES.dbf"
    #arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbanaCondominios/Renumerar/TB_RUTAS.shp", RUTAS)

    arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS, "viviendas_ordenadas")

    if arcpy.Exists(VIVIENDAS_AEU_OR_MAX):
        arcpy.Delete_management(VIVIENDAS_AEU_OR_MAX)

    if arcpy.Exists(VIVIENDAS_MZS_OR_MAX):
        arcpy.Delete_management(VIVIENDAS_MZS_OR_MAX)

    #arcpy.AddField_management(MZS, "IDMANZANA", "TEXT")


    #arcpy.MakeFeatureLayer_management(MZS, "mzs", "VIV_MZS>16")

    where_list=ubigeos
    m = 0
    where_expression = ""

    where_expression=UBIGEO.ExpresionUbigeos(ubigeos)


    for row in arcpy.da.SearchCursor(ZONAS,["UBIGEO", "ZONA"],where_expression):
        where_expression1 = "UBIGEO=\'" + str(row[0]) + "\' AND ZONA=\'" + str(row[1])+"\'  AND VIV_MZ>16 "
        numero_aeu = 1
        for row1 in arcpy.da.SearchCursor(MZS,["UBIGEO", "ZONA", "MANZANA", "IDMANZANA", "VIV_MZ","MZS_COND"],where_expression1):

            where_expression_viv = " UBIGEO=\'" + str(row1[0]) + "\'  AND  ZONA=\'" + str(
                row1[1]) + "\' AND MANZANA=\'" + str(row1[2]) + "\'"

            mzs_cond=int(row1[5])

            if (mzs_cond==0):
                cant_viv=int(row1[4])
                division=float(cant_viv)/16.0
                cant_aeus=math.ceil(division)
                residuo=cant_viv%cant_aeus
                viv_aeu=cant_viv/cant_aeus
                i=0
                or_viv_aeu=1

                edificacion_anterior=0
                numero_aeu_anterior=0
                idmanzana_anterior=""
                #P19A EDIFICACION
                #P29 USO DE LOCAL = 1 2 3 4 5 6 ( 1 .- VIVIENDA 3 .- VIVENDA ESTABLECIMIENTO 6 .- PUERTA DE CONDOMINIO)
                cant_aeus_aux=0

                with arcpy.da.UpdateCursor (VIVIENDAS_ORDENADAS, ["UBIGEO","ZONA","MANZANA","ID_REG_OR","AEU", "OR_VIV_AEU","P19A","P29","FLG_MZ"],where_expression_viv ) as cursor2:
                    for row2 in cursor2:
                        #flg manzana en 1
                        row2[8] = 1
                        idmanzana=str(row2[0])+str(row2[1])+str(row2[2])
                        usolocal=int(row2[7])


                        edificacion=int(row2[6])


                        if (usolocal in [1,3]) :
                            row2[4] = numero_aeu
                            row2[5]=or_viv_aeu
                            or_viv_aeu=or_viv_aeu+1

                        elif (usolocal == 6):
                            row2[4] = 0

                        else:
                            if or_viv_aeu != 1:
                                row2[4] = numero_aeu
                            else:
                                if idmanzana == idmanzana_anterior:
                                    if edificacion == edificacion_anterior:
                                        row2[4] = numero_aeu_anterior
                                    elif (edificacion != edificacion_anterior and cant_aeus_aux==cant_aeus):
                                        row2[4] = numero_aeu_anterior
                                    elif (edificacion==1 and edificacion_anterior!=1):
                                        row2[4] = numero_aeu_anterior
                                    else:
                                        row2[4] = numero_aeu


                                else:
                                    row2[4] = numero_aeu
                                    #row2[4] = numero_aeu_anterior





                        if residuo > 0:
                            if or_viv_aeu > (viv_aeu + 1):
                                i = 1
                                edificacion_anterior=edificacion
                                numero_aeu_anterior=numero_aeu
                                idmanzana_anterior=idmanzana
                                numero_aeu = numero_aeu + 1
                                residuo = residuo - 1
                                or_viv_aeu=1
                                cant_aeus_aux=cant_aeus_aux+1

                        else:
                            if or_viv_aeu > (viv_aeu):
                                edificacion_anterior=edificacion
                                numero_aeu_anterior=numero_aeu
                                numero_aeu = numero_aeu + 1
                                idmanzana_anterior = idmanzana
                                or_viv_aeu = 1
                                cant_aeus_aux = cant_aeus_aux + 1

                        cursor2.updateRow(row2)
                del cursor2
            else:


                ################OBTENEMOS LA CANTIDAD DE BLOQUES DEL CONDOMINIO EN LA MANZANA############################

                # P19A EDIFICACION
                # P29 USO DE LOCAL = 1 2 3 4 5 6 ( 1 .- VIVIENDA 3 .- VIVENDA ESTABLECIMIENTO 6 .- PUERTA DE CONDOMINIO)
                # P29M representa lo mismo que el P29 solo que es rellenado cuando solo representa un condominio
                # P23 Numero de bloque al cual pertenece el registro, si el registro tiene (P29=6 y P29_1 =2 es decir condominio)   representa la cantidad de bloques que tiene el condominio



                condominio_anterior = 0
                numero_aeu_anterior = 0

                #arcpy.Statistics_analysis("condominios", VIVIENDAS_AEU_OR_MAX, [["ID_REG_OR", "MAX"]],["UBIGEO", "ZONA", "MANZANA","AEU"])
                
                #for bloques in [ [str(x[0]),str(x[1]),str(x[2]),int(x[3]),int(x[4]),int(x[5])] for x in arcpy.da.SearchCursor(MZS_CONDOMINIOS, ["UBIGEO","ZONA","MANZANA","CONDOMINIO","N_BLOCK","VIV_BLOCK"], where_expression_viv)]:
                for condominios in [[str(x[0]), str(x[1]), str(x[2]), int(x[3]), int(x[4])] for x in
                                arcpy.da.SearchCursor(MZS_CONDOMINIOS,
                                                      ["UBIGEO", "ZONA", "MANZANA", "CONDOMINIO","VIV_COND"], where_expression_viv)]:
                    cant_viv_cond=condominios[4]

                    if (cant_viv_cond==0):
                        cant_aeu_condominio=1
                        viv_aeu_condominio = 0
                        res_viv_condominio=0
                    else:
                        ##########cant aeu_condominio es la cantidad de aeus por block ########################
                        cant_aeu_condominio=int(math.ceil(float(condominios[4])/16.0))
                    ##########viv_aeu_block es la cantidad de viviendas por block#####################
                        viv_aeu_condominio=int(condominios[4])/int(cant_aeu_condominio)
                    ##########res_viv_block es el residuo de viviendas por block######################

                        res_viv_condominio=int(condominios[4])%int(cant_aeu_condominio)

                        #print "cant_aeu_block"+str(cant_aeu_block)
                        #print "viv_aeu_block"+str(viv_aeu_block)
                        #print "res_viv_block"+str(res_viv_block)

                    or_viv_aeu = 1


                    #where_expression_viv_cond = " UBIGEO=\'" + condominios[0] + "\'  AND  ZONA=\'" + condominios[1] + "\' AND MANZANA=\'" + condominios[2] + "\' AND " \
                    #                            " P19A="+str(condominios[3])+" AND P23=\'"+str(condominios[4])+"\'"

                    where_expression_viv_cond = " UBIGEO=\'" + condominios[0] + "\'  AND  ZONA=\'" + condominios[1] + "\' AND MANZANA=\'" + condominios[2] + "\' AND  P19A=" + str(condominios[3])


                    print  where_expression_viv_cond


                    with arcpy.da.UpdateCursor(VIVIENDAS_ORDENADAS,
                                               ["UBIGEO", "ZONA", "MANZANA", "ID_REG_OR", "AEU", "OR_VIV_AEU", "P19A",
                                                "P29", "FLG_MZ","P23"], where_expression_viv_cond) as cursor2:
                        for row2 in cursor2:
                            # flg manzana en 1
                            row2[8] = 1
                            idmanzana = str(row2[0]) + str(row2[1]) + str(row2[2])
                            usolocal = int(row2[7])

                            condominio = int(row2[6])

                            #condominio=int(row2[9])
                            #print  bloque
                            if (usolocal in [1, 3]):
                                row2[4] = numero_aeu
                                row2[5] = or_viv_aeu
                                or_viv_aeu = or_viv_aeu + 1
                            elif (usolocal==6):
                                row2[4] = 0

                            else:
                                if or_viv_aeu != 1:
                                    row2[4] = numero_aeu

#                                else:
#                                    if idmanzana == idmanzana_anterior:
#                                        row2[4] = numero_aeu_anterior
#                                    else:
#                                        if bloque_anterior == 0:
#                                            row2[4] = numero_aeu
#                                        else:

                                else:


                                    if condominio == condominio_anterior:
                                        row2[4] = numero_aeu_anterior
                                    else:
                                        row2[4] = numero_aeu

                            # cursor.updateRow(row2)
                            if res_viv_condominio> 0:
                                #print "residuo de viv del bloque:"+str(res_viv_block)
                                if or_viv_aeu > (viv_aeu_condominio + 1):
                                    i = 1
                                    condominio_anterior = condominio
                                    numero_aeu_anterior = numero_aeu
                                    idmanzana_anterior = idmanzana
                                    numero_aeu = numero_aeu + 1
                                    residuo = residuo - 1
                                    or_viv_aeu = 1

                            else:

                                #print "residuo de viv del bloque:" + str(res_viv_block)
                                if or_viv_aeu > (viv_aeu_condominio):
                                    condominio_anterior = condominio
                                    numero_aeu_anterior = numero_aeu
                                    numero_aeu = numero_aeu + 1
                                    idmanzana_anterior = idmanzana
                                    or_viv_aeu = 1

                            cursor2.updateRow(row2)
                    del cursor2

#    where_expression_l = "FLG_MZ=1 AND P29<>6"
#    arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS, "viviendas_ordenadas", where_expression_l)
#
#
#
#    arcpy.Statistics_analysis("viviendas_ordenadas", VIVIENDAS_AEU_OR_MAX, [["ID_REG_OR", "MAX"]],
#                              ["UBIGEO", "ZONA", "MANZANA","AEU"])
#
#
#
#
#    arcpy.Statistics_analysis("viviendas_ordenadas", VIVIENDAS_MZS_OR_MAX, [["ID_REG_OR", "MAX"]],
#                              ["UBIGEO", "ZONA", "MANZANA"])
#
#
#    arcpy.AddField_management("viviendas_ordenadas", "ID_VIV", "TEXT")
#    arcpy.CalculateField_management("viviendas_ordenadas", "ID_VIV", "!UBIGEO!+!ZONA!+!MANZANA!+str(!ID_REG_OR!)",
#                                    "PYTHON_9.3")
#
#
#
#    arcpy.AddField_management( VIVIENDAS_AEU_OR_MAX,"ID_VIV","TEXT")
#    arcpy.CalculateField_management(VIVIENDAS_AEU_OR_MAX, "ID_VIV", "!UBIGEO!+!ZONA!+!MANZANA!+str(!MAX_ID_REG_OR!)",
#                                    "PYTHON_9.3")








    #for row in arcpy.da.SearchCursor(VIVIENDAS_AEU_OR_MAX, ["UBIGEO", "ZONA","MANZANA","MAX_ID_REG_OR"]):
    #    where_expressionxx = " UBIGEO=\'" + str(row[0]) + "\'  AND  ZONA=\'" + str(row[1]) + "\' AND MANZANA=\'" + str(row[2])+"\' AND ID_REG_OR="+str(row[3])
    #    with arcpy.arcpy.da.UpdateCursor(VIVIENDAS_ORDENADAS, ["FLG_CORTE"],where_expressionxx ) as cursor2:
    #        for row2 in cursor2:
    #            row2[0]=1
    #            cursor2.updateRow(row2)
    #    del cursor2
#
#
    #for row in arcpy.da.SearchCursor(VIVIENDAS_MZS_OR_MAX, ["UBIGEO", "ZONA","MANZANA","MAX_ID_REG_OR"]):
    #    where_expressionxx = " UBIGEO=\'" + str(row[0]) + "\'  AND  ZONA=\'" + str(row[1]) + "\' AND MANZANA=\'" + str(row[2])+"\' AND ID_REG_OR="+str(row[3])
    #    with arcpy.arcpy.da.UpdateCursor(VIVIENDAS_ORDENADAS, ["FLG_CORTE"],where_expressionxx ) as cursor2:
    #        for row2 in cursor2:
    #            row2[0]=0
    #            cursor2.updateRow(row2)
    #    del cursor2




def CrearViviendasCortes():
    arcpy.env.overwriteOutput = True
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    VIVIENDAS_AEU_OR_MAX_Stadistics = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/VIVIENDAS_AEU_OR_MAX_Stadistics"
    VIVIENDAS_MZS_OR_MAX_Stadistics = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/VIVIENDAS_MZS_OR_MAX_Stadistics"
    VIVIENDAS_AEU_OR_MAX = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/VIVIENDAS_AEU_OR_MAX.shp"
    VIVIENDAS_MZS_OR_MAX = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/VIVIENDAS_MZS_OR_MAX.shp"

    TB_VIVIENDAS_CORTES_shp = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_VIVIENDAS_CORTES.shp"

    where_expression_l = "FLG_MZ=1 AND P29<>6"
    arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS, "viviendas_ordenadas", where_expression_l)


    ########################calculando el ID de viviendas###########################################
    arcpy.AddField_management("viviendas_ordenadas", "ID_VIV", "TEXT")
    arcpy.CalculateField_management("viviendas_ordenadas", "ID_VIV", "!UBIGEO!+!ZONA!+!MANZANA!+str(!ID_REG_OR!)",
                                    "PYTHON_9.3")

    ##############Calculando los puntos maximos de cada AEU##########################################
    arcpy.Statistics_analysis("viviendas_ordenadas", VIVIENDAS_AEU_OR_MAX_Stadistics, [["ID_REG_OR", "MAX"]],
                              ["UBIGEO", "ZONA", "MANZANA", "AEU"])

    arcpy.AddField_management(VIVIENDAS_AEU_OR_MAX_Stadistics, "ID_VIV", "TEXT")
    arcpy.CalculateField_management(VIVIENDAS_AEU_OR_MAX_Stadistics, "ID_VIV", "!UBIGEO!+!ZONA!+!MANZANA!+str(int(!MAX_ID_REG_OR!))",
                                    "PYTHON_9.3")

    arcpy.AddJoin_management("viviendas_ordenadas","ID_VIV",VIVIENDAS_AEU_OR_MAX_Stadistics,"ID_VIV","KEEP_COMMON")

    arcpy.CopyFeatures_management("viviendas_ordenadas",VIVIENDAS_AEU_OR_MAX)

    add_fields=[["UBIGEO","TEXT"],["CODCCPP","TEXT"],["ZONA","TEXT"],["MANZANA","TEXT"],["AEU","SHORT"],["ID_REG_OR","SHORT"]]

    calculate_fields = [["UBIGEO", "!TB_VIVIE_1!"], ["CODCCPP", "!TB_VIVIE_2!"], ["ZONA", "!TB_VIVIE_3!"],
                        ["MANZANA", "!TB_VIVIE_4!"], ["AEU", "!TB_VIVI_19!"],["ID_REG_OR","!TB_VIVI_12!"]]


    for el in add_fields:
        arcpy.AddField_management(VIVIENDAS_AEU_OR_MAX,el[0],el[1])

    for el in calculate_fields:
        arcpy.CalculateField_management(VIVIENDAS_AEU_OR_MAX,el[0],el[1],"PYTHON_9.3")

    delete_fields = ["TB_VIVIEND", "viviendas_", "viviendas1"]

    for el in range(1, 10):
        delete_fields.append("TB_VIVIE_" + str(el))

    for el in range(10, 24):
        delete_fields.append("TB_VIVI_" + str(el))

    for el in range(1, 8):
        delete_fields.append("vivienda_" + str(el))

    arcpy.DeleteField_management(VIVIENDAS_AEU_OR_MAX, delete_fields)

    ##############Calculando los puntos maximos de cada Manzana##########################################
    where_expression_l = "FLG_MZ=1 AND P29<>6"
    arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS, "viviendas_ordenadas2", where_expression_l)


    arcpy.Statistics_analysis("viviendas_ordenadas2", VIVIENDAS_MZS_OR_MAX_Stadistics, [["ID_REG_OR", "MAX"]],
                              ["UBIGEO", "ZONA", "MANZANA"])

    arcpy.AddField_management(VIVIENDAS_MZS_OR_MAX_Stadistics, "ID_VIV", "TEXT")
    arcpy.CalculateField_management(VIVIENDAS_MZS_OR_MAX_Stadistics, "ID_VIV", "!UBIGEO!+!ZONA!+!MANZANA!+str(int(!MAX_ID_REG_OR!))",
                                    "PYTHON_9.3")


    arcpy.AddJoin_management("viviendas_ordenadas2","ID_VIV",VIVIENDAS_MZS_OR_MAX_Stadistics,"ID_VIV","KEEP_COMMON")


    arcpy.CopyFeatures_management("viviendas_ordenadas2",VIVIENDAS_MZS_OR_MAX)

    add_fields = [["UBIGEO", "TEXT"], ["CODCCPP", "TEXT"], ["ZONA", "TEXT"], ["MANZANA", "TEXT"], ["AEU", "SHORT"],["ID_REG_OR","SHORT"]]
    calculate_fields = [["UBIGEO", "!TB_VIVIE_1!"], ["CODCCPP", "!TB_VIVIE_2!"], ["ZONA", "!TB_VIVIE_3!"],
                        ["MANZANA", "!TB_VIVIE_4!"], ["AEU", "!TB_VIVI_19!"],["ID_REG_OR", "!TB_VIVI_12!"]]


    for el in add_fields:
        arcpy.AddField_management(VIVIENDAS_MZS_OR_MAX,el[0],el[1])

    for el in calculate_fields:
        arcpy.CalculateField_management(VIVIENDAS_MZS_OR_MAX,el[0],el[1],"PYTHON_9.3")

    delete_fields = ["TB_VIVIEND", "viviendas_", "viviendas1"]

    for el in range(1, 10):
        delete_fields.append("TB_VIVIE_" + str(el))

    for el in range(10, 24):
        delete_fields.append("TB_VIVI_" + str(el))

    for el in range(1, 8):
        delete_fields.append("vivienda_" + str(el))

    #arcpy.DeleteField_management(VIVIENDAS_MZS_OR_MAX, delete_fields)


    arcpy.Delete_management("viviendas_ordenas")
    arcpy.Delete_management("viviendas_ordenas2")
    ######################################Diferencia Simetrica######################

    arcpy.SymDiff_analysis(VIVIENDAS_AEU_OR_MAX, VIVIENDAS_MZS_OR_MAX,TB_VIVIENDAS_CORTES_shp)







    #arcpy.SymDiff_analysis(VIVIENDAS_AEU_OR_MAX)

#
#def EnumerarAEUEnViviendasCondominios(row1):
#    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
#    TB_BLOQUES = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_BLOQUES"
#    arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS, "viviendas_ordenadas")
#    where_expression_viv_cond = " UBIGEO=\'" + str(row1[0]) + "\'  AND  ZONA=\'" + str(row1[1]) + "\' AND MANZANA=\'" + str(row1[2]) + "\' AND (P29=1 or P29=3) AND (P23<>\'\')  "
#    ################OBTENEMOS LA CANTIDAD DE BLOQUES DEL CONDOMINIO EN LA MANZANA############################
#    # P19A EDIFICACION
#    # P29 USO DE LOCAL = 1 2 3 4 5 6 ( 1 .- VIVIENDA 3 .- VIVENDA ESTABLECIMIENTO 6 .- PUERTA DE CONDOMINIO)
#    # P29M representa lo mismo que el P29 solo que es rellenado cuando solo representa un condominio
#    # P23 Numero de bloque al cual pertenece el registro, si el registro tiene (P29=6 y P29_1 =2 es decir condominio)   representa la cantidad de bloques que tiene el condominio
#    cant_bloques = 0
#    arcpy.SelectLayerByAttribute_management("viviendas_ordenadas", "NEW_SELECTION", where_expression_viv_cond)
#    stats = [["ID_REG_OR", "COUNT"]]
#    casefield = ["UBIGEO", "CODCCPP", "ZONA", "MANZANA", "P19A","P23"]
#
#
#    arcpy.Statistics_analysis("viviendas_ordenadas", TB_BLOQUES, stats, casefield)
#




def EnumerarAEUEnViviendasDeManzanasCantVivMenoresIguales16(ubigeos):
    arcpy.env.overwriteOutput = True
    ZONAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    MZS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    ZONA_AEU_MAX = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/ZONA_AEU_MAX"
    where_expression = UBIGEO.ExpresionUbigeos(ubigeos)

    if arcpy.Exists(ZONA_AEU_MAX):
        arcpy.Delete_management(ZONA_AEU_MAX)


    where_expression_l=" FLG_MZ=1 "

    #############se obtiene una estadistica del maximo aeu por zona que ya ha sido asignada a las manzanas con mas de 16 viv##########################
    arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS, "viviendas_ordenadas_2", where_expression_l)

    arcpy.Statistics_analysis("viviendas_ordenadas_2",ZONA_AEU_MAX, [["AEU", "MAX"]],
                              ["UBIGEO", "ZONA"])



    ##############################se hace un bucle a cada zona######################################
    for row  in arcpy.da.SearchCursor(ZONAS, ["UBIGEO","ZONA"],where_expression):

        where_expressionx = "UBIGEO=\'" + str(row[0]) + "\' AND ZONA=\'" + str(row[1]) + "\' "

        aeu_max=0


        #####################################Bucle para obtener el numero de aue maximo de la zona###########################
        for row_aeu in arcpy.da.SearchCursor(ZONA_AEU_MAX, ["UBIGEO", "ZONA", "MAX_AEU"], where_expressionx):
            aeu_max=int(row_aeu[2])

        where_expression1 = "UBIGEO=\'" + str(row[0]) + "\' AND ZONA=\'" + str(row[1]) + "\'  AND VIV_MZ<=16 "



        ####################################Se revisa la tabla MZS  para obtener el ID de manzana#############################

        nuevo_aeu=0
        aeu_anterior=0
        usolocal = 0
        or_viv_aeu=0
        with arcpy.da.UpdateCursor(MZS, ["UBIGEO", "ZONA", "MANZANA", "IDMANZANA", "VIV_MZ","AEU","AEU_2"], where_expression1) as  cursor1:
            for row1 in cursor1:

                nuevo_aeu = int(row1[5]) + aeu_max
                row1[6]=nuevo_aeu  ###########se actualiza el nuevo aeu

                ###############se prepara la expresion para obtener las viviendas de esa  manzana#####################################
                where_expression2 = "UBIGEO=\'" + str(row1[0]) + "\' AND ZONA=\'" + str(row1[1]) + "\'  AND MANZANA=\'"+str(row1[2])+"\' "


                if aeu_anterior!=nuevo_aeu: #######si el aeu anterior es diferente del nuevo aeu, el orden de vivenda empieza en 1###############
                    or_viv_aeu=1
                    aeu_anterior=nuevo_aeu

                with arcpy.da.UpdateCursor(VIVIENDAS_ORDENADAS, ["UBIGEO", "ZONA", "MANZANA", "ID_REG_OR", "AEU", "OR_VIV_AEU", "P19A",
                                                "P29", "FLG_MZ","P23"],where_expression2) as cursor2:
                    for row2 in cursor2:
                        row2[4]=nuevo_aeu
                        usolocal=int(row2[7])


                        if (usolocal in [1, 3]):
                            row2[5] = or_viv_aeu
                            or_viv_aeu=or_viv_aeu+1


                        cursor2.updateRow(row2)

                cursor1.updateRow(row1)


    del row



def AgruparManzanasCantVivMenoresIguales16(ubigeos):
    arcpy.env.overwriteOutput = True
    ZONAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    MZS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"

    Lista_adyacencia = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/MatrizAdyacencia/lista_adyacencia.dbf"
    #Lista_adyacencia = "lista_adyacencia.dbf"
    where_expression = UBIGEO.ExpresionUbigeos(ubigeos)

    for row  in arcpy.da.SearchCursor(ZONAS, ["UBIGEO","ZONA","CODCCPP"],where_expression):
        where_expression1 = "UBIGEO=\'" + str(row[0]) + "\' AND ZONA=\'" + str(row[1]) + "\'  AND VIV_MZ<=16 "

        numero_aeu = 1
        desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])+".shp"
        print "zona: "+desc
        # Algoritmo Normal

        #fc = "D:/ShapesPruebasSegmentacionUrbanaCondominios/Zones/" + desc
        fc = "D:/ShapesPruebasSegmentacionUrbanaCondominios/Zones/" + desc

        manzanas=[]


        arcpy.MakeFeatureLayer_management(MZS, "manzanas", where_expression1)
        for row1 in arcpy.da.SearchCursor("manzanas", ["IDMANZANA", "VIV_MZ", "AREA", "xCentroid", "yCentroid"]):
            manzana = [str(row1[0]), int(row1[1]), float(row1[2]), float(row1[3]), float(row1[4])]
            manzanas.append(manzana)
        del row1

        #manzanas = s.Manzanas_menores_iguales_16(fc)[:]
        manzanas1 = manzanas[:]
        componentes = s.Componentes_conexas2(Lista_adyacencia,manzanas1)[:]

        SM_FINAL=[]

        for componente in componentes:
            if s.Total_Viviendas(componente) <= 16:
                SM_FINAL.append(componente)
                #SM_INICIAL.append(componente)
            else:
                SM=[]
                #SM=prueba.AgrupacionPrueba(componente)[:]
                #SM=s.Componentes_conexas_cantidad_viv(componente)
                SM=s.Agrupacion2(Lista_adyacencia,componente)
                for el2 in SM:
                    SM_FINAL.append(el2)

        a.ActualizarAEU3(MZS, SM_FINAL, manzanas)

    del row

def CrearMZS_AEU(ubigeos):
    arcpy.env.overwriteOutput = True
    MZS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    MZS_AEU_1 = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/MZS_AEU_1"
    MZS_AEU_2 = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/MZS_AEU_2.dbf"
    MZS_AEU = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"
    MZS_MENORES_16="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/MZS_MENORES_16"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"

    if arcpy.Exists(MZS_AEU):
        arcpy.Delete_management(MZS_AEU)
    if arcpy.Exists(MZS_AEU_1):
        arcpy.Delete_management(MZS_AEU_1)

    if arcpy.Exists(MZS_AEU_2):
        arcpy.Delete_management(MZS_AEU_2)

    if arcpy.Exists(MZS_MENORES_16):
        arcpy.Delete_management(MZS_MENORES_16)

    where = " FLG_MZ=1 AND P29<>6"
    arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS, "viviendas_ordenadas_3",where)

    arcpy.Statistics_analysis("viviendas_ordenadas_3", MZS_AEU_1, [["OR_VIV_AEU", "MAX"]],
                              ["UBIGEO","CODCCPP" ,"ZONA","MANZANA","AEU","FALSO_COD"])



    arcpy.AddField_management(MZS_AEU_1, "CANT_VIV", "SHORT")
    expression="!MAX_OR_VIV_AEU!"

    arcpy.CalculateField_management(MZS_AEU_1, "CANT_VIV", expression, "PYTHON_9.3")




    arcpy.DeleteField_management(MZS_AEU_1, ['FREQUENCY','MAX_OR_VIV_AEU'])



    ####creacion de  la vista de manzanas menores a 16

    where2 = " VIV_MZ<=16 "
    arcpy.MakeFeatureLayer_management(MZS, "mzs_menores_16", where2)

    arcpy.Statistics_analysis("mzs_menores_16", MZS_MENORES_16, [["MANZANA", "COUNT"]],
                              ["UBIGEO", "CODCCPP","ZONA", "MANZANA", "AEU_2","FALSO_COD","VIV_MZ"])



    arcpy.AddField_management(MZS_MENORES_16, "AEU", "SHORT")
    arcpy.AddField_management(MZS_MENORES_16, "CANT_VIV", "SHORT")


    expression = "!VIV_MZ!"
    expression2 = "!AEU_2!"
    arcpy.CalculateField_management(MZS_MENORES_16, "CANT_VIV", expression, "PYTHON_9.3")
    arcpy.CalculateField_management(MZS_MENORES_16, "AEU", expression2, "PYTHON_9.3")
    arcpy.DeleteField_management(MZS_MENORES_16, ['FID_','FREQUENCY','COUNT_MANZANA','VIV_MZ','AEU_2'])
    arcpy.Merge_management([MZS_AEU_1, MZS_MENORES_16],MZS_AEU_2 )
    arcpy.Sort_management(MZS_AEU_2, MZS_AEU, ["UBIGEO","CODCCPP","ZONA","FALSO_COD","AEU"])


def CrearRutasPuntos():
    arcpy.env.overwriteOutput = True

    TB_RUTAS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    PUERTAS_VIVIENDAS_MULTIFAMILIAR = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_PUERTAS_VIVIENDAS_MULTIFAMILIAR.shp"
    VIVIENDAS_ORDENADAS_MULTIFAMILIAR = "VIVIENDAS_ORDENADAS_MULTIFAMILIAR"
    VIVIENDAS_ORDENADAS_MULTIFAMILIAR_2="VIVIENDAS_ORDENADAS_MULTIFAMILIAR_2"
    TB_RUTAS_PUNTOS_MIN = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_MIN.shp"
    TB_RUTAS_PUNTOS_CANT_AEU_IGUAL_1 = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_CANT_AEU_IGUAL_1"
    TB_RUTAS_PUNTOS_AEU_IDENTICOS="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_AEU_IDENTICOS"
    TB_RUTAS_PUNTOS_MIN_SELECT="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_MIN_SELECT.shp"

    spatial_reference = arcpy.Describe(VIVIENDAS_ORDENADAS).spatialReference

    where = "P29=6"
    where2 = "P29M=1 OR P29M=3"
    arcpy.Select_analysis(VIVIENDAS_ORDENADAS, PUERTAS_VIVIENDAS_MULTIFAMILIAR, where)

    arcpy.DeleteIdentical_management(PUERTAS_VIVIENDAS_MULTIFAMILIAR,["UBIGEO","CODCCPP","ZONA","MANZANA","P19A"])
    arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS, VIVIENDAS_ORDENADAS_MULTIFAMILIAR, where2)
    arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS,VIVIENDAS_ORDENADAS_MULTIFAMILIAR_2,where2)

    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"

    AEU_MULTIFAMILIAR = "in_memory/aeu_multifamiliar"
    AEU_MULTIFAMILIAR_ID_REG_OR="in_memory/aeu_multifamiliar_id_reg_or"
    AEU_MULTIFAMILIAR_Layer="AEU_MULTIFAMILIAR_Layer"

    # arcpy.CreateFeatureclass_management(out_path, out_name, geometry_type, template, has_m, has_z, spatial_reference)


    if arcpy.Exists(TB_RUTAS_PUNTOS):
        arcpy.Delete_management(TB_RUTAS_PUNTOS)
    if arcpy.Exists(TB_RUTAS_PUNTOS_MIN):
        arcpy.Delete_management(TB_RUTAS_PUNTOS_MIN)

    if arcpy.Exists(TB_RUTAS_PUNTOS) == False:
        arcpy.CreateFeatureclass_management("D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU",
                                            "TB_RUTAS_PUNTOS.shp",
                                            "POINT",
                                            "",
                                            "",
                                            "",
                                            spatial_reference)

    list_field = ["SHAPE@", "UBIGEO", "CODCCPP", "ZONA", "MANZANA", "AEU","ID_REG_OR" ,"CANT_VIV"]
    list_addfield = [["UBIGEO", "TEXT"], ["CODCCPP", "TEXT"], ["ZONA", "TEXT"], ["MANZANA", "TEXT"], ["AEU", "SHORT"],["ID_REG_OR","SHORT"],
                     ["CANT_VIV", "SHORT"]]



    for el in list_addfield:
        arcpy.AddField_management(TB_RUTAS_PUNTOS, el[0], el[1])

    # cursor = arcpy.da.InsertCursor(TB_RUTAS_PUNTOS, list_field)

    with arcpy.da.InsertCursor(TB_RUTAS_PUNTOS, list_field) as cursor_insert:


        for row in arcpy.da.SearchCursor(PUERTAS_VIVIENDAS_MULTIFAMILIAR,
                                         ["UBIGEO", "CODCCPP", "ZONA", "MANZANA", "P19A", "SHAPE@XY"]):
            where_multifamiliar = " UBIGEO=\'" + str(row[0]) + "\' AND CODCCPP=\'" + str(
                row[1]) + "\' AND ZONA=\'" + str(row[2]) + "\' AND MANZANA=\'" + str(row[3]) + "\' AND P19A=" + str(
                row[4])
            #print  where_multifamiliar


            arcpy.SelectLayerByAttribute_management(VIVIENDAS_ORDENADAS_MULTIFAMILIAR, "NEW_SELECTION",
                                                    where_multifamiliar)




            arcpy.Statistics_analysis(VIVIENDAS_ORDENADAS_MULTIFAMILIAR, AEU_MULTIFAMILIAR, [["OR_VIV_AEU", "COUNT"],["ID_REG_OR", "MAX"]],
                                      ["UBIGEO", "CODCCPP", "ZONA", "MANZANA", "P19A", "AEU"])


            where_multifamiliar_2 = " UBIGEO=\'" + str(row[0]) + "\' AND CODCCPP=\'" + str(
                row[1]) + "\' AND ZONA=\'" + str(row[2]) + "\' AND MANZANA=\'" + str(row[3])+"\' "




            #arcpy.SelectLayerByAttribute_management(VIVIENDAS_ORDENADAS_MULTIFAMILIAR_2, "NEW_SELECTION",
            #                                        where_multifamiliar_2)
#
#
            #arcpy.Statistics_analysis(VIVIENDAS_ORDENADAS_MULTIFAMILIAR_2, AEU_MULTIFAMILIAR_ID_REG_OR,
            #                          [ ["ID_REG_OR", "MAX"]],["UBIGEO", "CODCCPP", "ZONA", "MANZANA", "AEU"])


            #layerx=arcpy.MakeFeatureLayer_management(AEU_MULTIFAMILIAR, AEU_MULTIFAMILIAR_Layer)



            #cant_aeus=int(arcpy.GetCount_management(AEU_MULTIFAMILIAR).getOutput(0))


            #cant_aeus
            #cant_puntos_repetidos = 0

            # cursor = arcpy.da.InsertCursor(TB_RUTAS_PUNTOS, list_field)


            for row2 in arcpy.da.SearchCursor(AEU_MULTIFAMILIAR, ["UBIGEO", "CODCCPP", "ZONA", "MANZANA", "P19A", "AEU",
                                                                  "MAX_ID_REG_OR","COUNT_OR_VIV_AEU"]):
                #where_xx = " UBIGEO=\'" + str(row2[0]) + "\' AND CODCCPP=\'" + str(
                #    row2[1]) + "\' AND ZONA=\'" + str(row2[2]) + "\' AND MANZANA=\'" + str(row2[3]) + "\' AND AEU=" + str(row2[5])

                #id_max=0
                #if(cant_aeus==1):
                #    for row3 in arcpy.da.SearchCursor(AEU_MULTIFAMILIAR_ID_REG_OR,
                #                                  ["MAX_ID_REG_OR"],where_xx):
                #        print where_xx
                #        id_max=int(row3[0])

                #if cant_aeus <= 1:
                #    corte = 0  ###no hay corte
                #else:
                #    corte=1  ### si es corte
                #print id_max
                #print int(row2[6])

                #if ((id_max)!=int(row2[6]) and cant_aeus==1 ):
                #    corte = 0
                #else:
                #    corte = 1

                point = arcpy.Point(row[5][0], row[5][1])
                rowArray = [point, str(row2[0]), str(row2[1]), str(row2[2]), str(row2[3]), str(row2[5]), str(row2[6]),str(row2[7])]
                cursor_insert.insertRow(rowArray)


    sort_fields = [["UBIGEO", "ASCENDING"], ["CODCCPP", "ASCENDING"], ["ZONA", "ASCENDING"],
                               ["MANZANA", "ASCENDING"],
                               ["AEU", "ASCENDING"], ["ID_REG_OR", "ASCENDING"]]

    #arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS, VIVIENDAS_ORDENADAS_MULTIFAMILIAR)

    arcpy.Sort_management(TB_RUTAS_PUNTOS, TB_RUTAS_PUNTOS_MIN, sort_fields)

    arcpy.DeleteIdentical_management(TB_RUTAS_PUNTOS_MIN, ["Shape"])


    #WHERE=' "CORTE"=1 '
    #arcpy.Select_analysis(TB_RUTAS_PUNTOS_MIN, TB_RUTAS_PUNTOS_MIN_SELECT, WHERE)

    #arcpy.DeleteField_management(TB_RUTAS_PUNTOS_MIN_SELECT,)
            #if (cant_puntos_repetidos>1):
            #
            #
            #    for row2 in arcpy.da.SearchCursor(AEU_MULTIFAMILIAR,
            #                                      ["UBIGEO", "CODCCPP", "ZONA", "MANZANA", "P19A", "AEU",
            #                                       "MAX_ID_REG_OR", "COUNT_OR_VIV_AEU"]):
            #
            #        point = arcpy.Point(row[5][0], row[5][1])
            #        rowArray = [point, str(row2[0]), str(row2[1]), str(row2[2]), str(row2[3]), str(row2[5]), str(row2[6]),
            #            str(row2[7])]
            #        cursor_insert.insertRow(rowArray)



def CrearRutasPuntosCortes():
    arcpy.env.overwriteOutput = True

    TB_RUTAS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"
    TB_RUTAS_PUNTOS_Layer="TB_RUTAS_PUNTOS_Layer"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    PUERTAS_VIVIENDAS_MULTIFAMILIAR = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_PUERTAS_VIVIENDAS_MULTIFAMILIAR.shp"
    VIVIENDAS_ORDENADAS_MULTIFAMILIAR = "VIVIENDAS_ORDENADAS_MULTIFAMILIAR"
    TB_RUTAS_PUNTOS_MIN = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_MIN.shp"
    TB_RUTAS_PUNTOS_CANT_AEU_IGUAL_1 = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_CANT_AEU_IGUAL_1"
    TB_RUTAS_PUNTOS_CANT_AEU_IGUAL_1_Layer = "TB_RUTAS_PUNTOS_CANT_AEU_IGUAL_1_Layer"
    TB_RUTAS_PUNTOS_AEU_IDENTICOS="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_AEU_IDENTICOS"

    sort_fields = [["UBIGEO", "ASCENDING"], ["CODCCPP", "ASCENDING"], ["ZONA", "ASCENDING"], ["MANZANA", "ASCENDING"],
                   ["AEU", "ASCENDING"], ["ID_REG_OR", "ASCENDING"]]

    arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS, VIVIENDAS_ORDENADAS_MULTIFAMILIAR)
    arcpy.Sort_management(TB_RUTAS_PUNTOS, TB_RUTAS_PUNTOS_MIN, sort_fields)

    arcpy.DeleteIdentical_management(TB_RUTAS_PUNTOS_MIN, ["Shape"])
    arcpy.FindIdentical_management(TB_RUTAS_PUNTOS, TB_RUTAS_PUNTOS_AEU_IDENTICOS, ["Shape"])
    arcpy.Statistics_analysis(TB_RUTAS_PUNTOS_AEU_IDENTICOS, TB_RUTAS_PUNTOS_CANT_AEU_IGUAL_1, [["Rowid", "MIN"]],
                              ["FEAT_SEQ"])

    arcpy.MakeTableView_management(TB_RUTAS_PUNTOS_CANT_AEU_IGUAL_1,TB_RUTAS_PUNTOS_CANT_AEU_IGUAL_1_Layer, "FREQUENCY>1")

    arcpy.MakeFeatureLayer_management(TB_RUTAS_PUNTOS, TB_RUTAS_PUNTOS_Layer)

    arcpy.AddJoin_management(TB_RUTAS_PUNTOS_Layer, "FID", TB_RUTAS_PUNTOS_CANT_AEU_IGUAL_1, "MIN_ROWID")

    list_addfield = [["UBIGEO", "TEXT"], ["CODCCPP", "TEXT"], ["ZONA", "TEXT"], ["MANZANA", "TEXT"], ["AEU", "SHORT"],["ID_REG_OR","SHORT"],
                     ["CANT_VIV", "SHORT"]]

    for el in list_addfield:
        arcpy.AddField_management(TB_RUTAS_PUNTOS, el[0], el[1])






def CrearRutasPreparacion():

    TB_VIVIENDAS_ORDENADAS_shp = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    TB_MZS_shp = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    TB_RUTAS_PUNTOS_MIN = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_MIN.shp"
    TB_RUTAS_PUNTOS_MIN_SELECT = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_MIN_SELECT.shp"
    # TB_MZS_TRABAJO_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\Manzanas\\TB_MZS_TRABAJO.shp"
    # PUNTO_INICIO_CARHUAZ_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp"

    TB_VIVIENDAS_CORTES_shp = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_VIVIENDAS_CORTES.shp"
    # TB_VIVIENDAS_CORTES_shp__2_ = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\Viviendas\\TB_VIVIENDAS_CORTES.shp"
    # P_021806_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp"
    # P_110204_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp"
    TB_MZS_LINE_shp = "in_memory/TB_MZS_LINE"
    TB_MZS_TRABAJO_BUFFER_shp = "in_memory/TB_MZS_TRABAJO_BUFFER"
    PUNTOINICIO_BUFFER_shp = "in_memory/PUNTOINICIO_BUFFER"
    TB_MZS_ERASE_shp = "in_memory/TB_MZS_ERASE"
    PUNTOS_INICIO_shp = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/PuntosInicio/PUNTOS_INICIO.shp"
    TB_SPLIT_shp = "in_memory/TB_SPLIT"
    TB_DISSOLVE_shp = "in_memory/TB_DISSOLVE"
    TB_CORTES_Buffer = "in_memory/TB_VIVIENDAS_CORTES_Buffer"

    TB_VIVIENDAS_CORTES_Buffer = "in_memory/TB_VIVIENDAS_CORTES_Buffer"
    TB_RUTAS_DISSOLVE_ERASE_shp = "in_memory/TB_RUTAS_DISSOLVE_ERASE"
    TB_RUTAS_DISSOLVE_ERASE_shp_2="in_memory/TB_RUTAS_DISSOLVE_ERASE_2"
    TB_RUTAS_PUNTOS_MIN_BUFFER_shp="in_memory/TB_RUTAS_PUNTOS_MIN_BUFFER"

    TB_RUTAS_PREPARACION_shp = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PREPARACION.shp"
    TB_VERTICES_FINAL = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_VERTICES_FINAL.shp"
    TB_PUNTOS_CORTE_Merge="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_PUNTOS_CORTE_Merge.shp"
    #TB_RUTAS_PUNTOS="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"



    TB_PUNTOS_CORTE_Merge_Ord="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_PUNTOS_CORTE_Merge_Ord.shp"
    #if arcpy.Exists(TB_VIVIENDAS_CORTES_shp):
    #    arcpy.Delete_management(TB_VIVIENDAS_CORTES_shp)
    if arcpy.Exists(TB_VERTICES_FINAL):
        arcpy.Delete_management(TB_VERTICES_FINAL)


    if arcpy.Exists(TB_RUTAS_PREPARACION_shp):
        arcpy.Delete_management(TB_RUTAS_PREPARACION_shp)




    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbanaCondominios"

    MZS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    expression_2 = "flg_manzana(!VIV_MZ!)"
    codeblock = """def flg_manzana(VIV_MZ):\n  if (VIV_MZ>16):\n    return 1\n  else:\n    return 0"""

    arcpy.CalculateField_management(MZS, "FLG_MZ", expression_2, "PYTHON_9.3", codeblock)
    arcpy.Buffer_analysis(TB_MZS_shp, TB_MZS_TRABAJO_BUFFER_shp, "0.31 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")






    # Process: Feature To Line

    #where_expression = " FLG_CORTE=1"
    #arcpy.Select_analysis(TB_VIVIENDAS_ORDENADAS_shp,
    #                      TB_VIVIENDAS_CORTES_shp
    #                      , where_expression)

    arcpy.FeatureToLine_management(TB_MZS_TRABAJO_BUFFER_shp, TB_MZS_LINE_shp, "", "ATTRIBUTES")

    # Obteniendo los ultimos vertices:
    #arcpy.FeatureVerticesToPoints_management(TB_MZS_LINE_shp, TB_VETICES_FINAL, "END")


    # Process: Merge
    # arcpy.Merge_management("'D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp';'D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp';'D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp'", PUNTOS_INICIO_shp, "IDMANZANA \"IDMANZANA\" true true false 15 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,IDMANZANA,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,IDMANZANA,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,IDMANZANA,-1,-1;OBJECTID \"OBJECTID\" true true false 10 Long 0 10 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,OBJECTID,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,OBJECTID,-1,-1;ORIG_FID \"ORIG_FID\" true true false 10 Long 0 10 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,ORIG_FID,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,ORIG_FID,-1,-1;NEAR_FID \"NEAR_FID\" true true false 10 Long 0 10 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,NEAR_FID,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,NEAR_FID,-1,-1;NEAR_DIST \"NEAR_DIST\" true true false 19 Double 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,NEAR_DIST,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,NEAR_DIST,-1,-1;NEAR_FC \"NEAR_FC\" true true false 254 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,NEAR_FC,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,NEAR_FC,-1,-1;idmax \"idmax\" true true false 254 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,idmax,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,idmax,-1,-1;MIN_NEAR_D \"MIN_NEAR_D\" true true false 19 Double 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,MIN_NEAR_D,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,MIN_NEAR_D,-1,-1;MODIF \"MODIF\" true true false 5 Short 0 5 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,MODIF,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,MODIF,-1,-1;UBIGEO \"UBIGEO\" true true false 6 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,UBIGEO,-1,-1;CODCCPP14 \"CODCCPP14\" true true false 4 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CODCCPP14,-1,-1;MZ_T \"MZ_T\" true true false 4 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,MZ_T,-1,-1;CCDD \"CCDD\" true true false 2 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CCDD,-1,-1;CCPP \"CCPP\" true true false 2 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CCPP,-1,-1;CCDI \"CCDI\" true true false 2 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CCDI,-1,-1;ZONA \"ZONA\" true true false 5 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,ZONA,-1,-1;MANZANA \"MANZANA\" true true false 4 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,MANZANA,-1,-1;CODCCPP \"CODCCPP\" true true false 4 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CODCCPP,-1,-1;NOMCCPP \"NOMCCPP\" true true false 60 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,NOMCCPP,-1,-1;DEPARTAMEN \"DEPARTAMEN\" true true false 50 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,DEPARTAMEN,-1,-1;PROVNCIA \"PROVNCIA\" true true false 50 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,PROVNCIA,-1,-1;DISTRITO \"DISTRITO\" true true false 50 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,DISTRITO,-1,-1")

    # Process: Buffer (2)
    arcpy.Buffer_analysis(PUNTOS_INICIO_shp, PUNTOINICIO_BUFFER_shp, "0.6 Meters", "FULL", "ROUND", "NONE", "",
                          "PLANAR")


    # Process: Erase
    arcpy.Erase_analysis(TB_MZS_LINE_shp, PUNTOINICIO_BUFFER_shp, TB_MZS_ERASE_shp, "")



    #arcpy.Po(TB_MZS_LINE_shp, PUNTOINICIO_BUFFER_shp, TB_MZS_ERASE_shp, "")

    # Process: Split Line At Vertices


    arcpy.SplitLine_management(TB_MZS_ERASE_shp, TB_SPLIT_shp)

    # Process: Dissolve
    arcpy.Dissolve_management(TB_SPLIT_shp, TB_DISSOLVE_shp, "UBIGEO;CODCCPP;ZONA;MANZANA;FLG_MZ", "", "MULTI_PART", "DISSOLVE_LINES")


    # Obteniendo los ultimos vertices:
    arcpy.FeatureVerticesToPoints_management(TB_DISSOLVE_shp, TB_VERTICES_FINAL, "END")

    # Process: Buffer (3)
    #arcpy.Buffer_analysis(TB_VIVIENDAS_CORTES_shp, TB_VIVIENDAS_CORTES_Buffer, "0.6 Meters", "FULL", "ROUND", "NONE",
    #                      "", "PLANAR")



    #Process:Buffer Puntos AEU
    #arcpy.Buffer_analysis(TB_RUTAS_PUNTOS_MIN_SELECT, TB_RUTAS_PUNTOS_MIN_BUFFER_shp, "0.6 Meters", "FULL", "ROUND", "NONE", "",
    #                      "PLANAR")



    # Process: Add Field
    arcpy.AddField_management(TB_RUTAS_PUNTOS_MIN, "FLG", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Calculate Field
    arcpy.CalculateField_management(TB_RUTAS_PUNTOS_MIN, "FLG", "1", "VB", "")

    # Process: Merge (2)
    arcpy.Merge_management([TB_RUTAS_PUNTOS_MIN,TB_VIVIENDAS_CORTES_shp], TB_PUNTOS_CORTE_Merge,
                           "UBIGEO \"UBIGEO\" true true false 254 Text 0 0 ,First,#,TB_VIVIENDAS_CORTES,UBIGEO,-1,-1,TB_RUTAS_PUNTOS_MIN,UBIGEO,-1,-1;CODCCPP \"CODCCPP\" true true false 254 Text 0 0 ,First,#,TB_VIVIENDAS_CORTES,CODCCPP,-1,-1,TB_RUTAS_PUNTOS_MIN,CODCCPP,-1,-1;ZONA \"ZONA\" true true false 254 Text 0 0 ,First,#,TB_VIVIENDAS_CORTES,ZONA,-1,-1,TB_RUTAS_PUNTOS_MIN,ZONA,-1,-1;MANZANA \"MANZANA\" true true false 254 Text 0 0 ,First,#,TB_VIVIENDAS_CORTES,MANZANA,-1,-1,TB_RUTAS_PUNTOS_MIN,MANZANA,-1,-1;AEU \"AEU\" true true false 5 Short 0 5 ,First,#,TB_VIVIENDAS_CORTES,AEU,-1,-1,TB_RUTAS_PUNTOS_MIN,AEU,-1,-1;ID_REG_OR \"ID_REG_OR\" true true false 5 Short 0 5 ,First,#,TB_VIVIENDAS_CORTES,ID_REG_OR,-1,-1,TB_RUTAS_PUNTOS_MIN,ID_REG_OR,-1,-1;FLG \"FLG\" true true false 0 Short 0 0 ,First,#,TB_RUTAS_PUNTOS_MIN,FLG,-1,-1")

    # Process: Sort
    arcpy.Sort_management(TB_PUNTOS_CORTE_Merge, TB_PUNTOS_CORTE_Merge_Ord,
                          "UBIGEO ASCENDING;CODCCPP ASCENDING;ZONA ASCENDING;MANZANA ASCENDING;AEU ASCENDING;ID_REG_OR DESCENDING;FLG DESCENDING",
                          "UR")

    # Process: Delete Identical
    arcpy.DeleteIdentical_management(TB_PUNTOS_CORTE_Merge_Ord, "UBIGEO;CODCCPP;ZONA;MANZANA;AEU", "", "0")

    arcpy.Buffer_analysis(TB_PUNTOS_CORTE_Merge_Ord, TB_CORTES_Buffer, "0.6 Meters", "FULL", "ROUND",
                          "NONE", "","PLANAR")
    # Process: Erase (2)
    #arcpy.Erase_analysis(TB_DISSOLVE_shp, TB_VIVIENDAS_CORTES_Buffer, TB_RUTAS_DISSOLVE_ERASE_shp, "")
#
#
#
#
    ## Process: Erase Puntos AEU(2)
   # arcpy.Erase_analysis(TB_RUTAS_DISSOLVE_ERASE_shp, TB_CORTES_Buffer, TB_RUTAS_DISSOLVE_ERASE_shp_2, "")
    arcpy.Erase_analysis(TB_DISSOLVE_shp, TB_CORTES_Buffer, TB_RUTAS_DISSOLVE_ERASE_shp_2, "")

    # Process: Multipart To Singlepart
    arcpy.MultipartToSinglepart_management(TB_RUTAS_DISSOLVE_ERASE_shp_2, TB_RUTAS_PREPARACION_shp)



def RelacionarVerticeFinalInicioConAEUMax():
    arcpy.env.overwriteOutput = True
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    VIVIENDAS_MZS_MAX_AEU = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_MZS_MAX_AEU"
    TB_VERTICES_FINAL = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_VERTICES_FINAL.shp"
    TB_VERTICES_FINAL_Layer="TB_VERTICES_FINAL_Layer"
    #PUNTOS_INICIO_shp = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/PuntosInicio/PUNTOS_INICIO.shp"
    #PUNTOS_INICIO_Layer = "PUNTOS_INICIO_Layer"
    #PUNTOS_INICIO_AEU = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/PUNTOS_INICIO_AEU.shp"
    TB_VERTICES_FINAL_AEU = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_VERTICES_FINAL_AEU.shp"

    arcpy.MakeFeatureLayer_management(TB_VERTICES_FINAL, TB_VERTICES_FINAL_Layer)

    arcpy.Statistics_analysis(VIVIENDAS_ORDENADAS, VIVIENDAS_MZS_MAX_AEU, [["AEU", "MAX"],["ID_REG_OR","MAX"]],
                              ["UBIGEO", "ZONA", "MANZANA"])

    arcpy.AddField_management(TB_VERTICES_FINAL_Layer,"IDMANZANA", "TEXT")
    arcpy.CalculateField_management(TB_VERTICES_FINAL_Layer, "IDMANZANA", "!UBIGEO!+!ZONA!+!MANZANA!","PYTHON_9.3")


    arcpy.AddField_management(VIVIENDAS_MZS_MAX_AEU, "IDMANZANA", "TEXT")
    arcpy.CalculateField_management(VIVIENDAS_MZS_MAX_AEU, "IDMANZANA", "!UBIGEO!+!ZONA!+!MANZANA!", "PYTHON_9.3")



    arcpy.AddJoin_management(TB_VERTICES_FINAL_Layer,"IDMANZANA",VIVIENDAS_MZS_MAX_AEU,"IDMANZANA")

    arcpy.CopyFeatures_management(TB_VERTICES_FINAL_Layer, TB_VERTICES_FINAL_AEU)



    add_field = [["UBIGEO","TEXT"], ["CODCCPP","TEXT"], ["ZONA","TEXT"], ["MANZANA","TEXT"], ["AEU","SHORT"],["ID_REG_OR","SHORT"]]

    for el in add_field:
        arcpy.AddField_management(TB_VERTICES_FINAL_AEU,el[0],el[1])

    calculate_field= [["UBIGEO","!TB_VERTICE!"],["ZONA","!TB_VERTI_1!"],["ZONA","!TB_VERTI_2!"],["MANZANA","!TB_VERTI_3!"],["AEU","!tb_vivie_6!"],["ID_REG_OR","!tb_vivie_7!"]]


    for el in calculate_field:
        arcpy.CalculateField_management(TB_VERTICES_FINAL_AEU,el[0],el[1],"PYTHON_9.3")



    list_deletefield = ["TB_VERTICE", "tb_viviend"]
    for el in range(1,7):
        list_deletefield.append("TB_VERTI_" + str(el))
    for el in range(1,9):
        list_deletefield.append("tb_vivie_"+str(el))

    arcpy.DeleteField_management(TB_VERTICES_FINAL_AEU, list_deletefield)

##############Relacionando Rutas de Lineas con AEU usando la segunda vivienda de cada AEU############################
def RelacionarRutasLineasConAEUSegundaVivienda():
    TB_SEGUNDA_VIVIENDA_AEU_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_SEGUNDA_VIVIENDA_AEU.shp"
    TB_RUTAS_PREPARACION_shp__3_ = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_PREPARACION.shp"
    TB_RUTAS_Layer__2_ = "TB_RUTAS_Layer"
    TB_RUTAS_1_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_1.shp"
    TB_INTERSECT_RUTAS_VIVIENDA_SEGUNDO_PUNTO = "in_memory\\TB_INTERSECT_RUTAS_VIVIENDA_SEGUNDO_PUNTO"
    TB_INT_RUTAS_VIVIENDAS_AEU_MAX = "in_memory\\TB_INT_RUTAS_VIVIENDAS_AEU_MAX"
    TB_RUTAS_Layer = "TB_RUTAS_Layer"

    TB_VETICES_FINAL = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_VERTICES_FINAL.shp"
    ###PEGANDO EL AEU MAX DE CADA MANZANA A SUS VERTICES FINALES :



    #    arcpy.Statistics_analysis("viviendas_ordenadas", VIVIENDAS_AEU_OR_MAX, [["ID_REG_OR", "MAX"]],
    #                              ["UBIGEO", "ZONA", "MANZANA","AEU"])




    if arcpy.Exists(TB_RUTAS_1_shp):
        arcpy.Delete_management(TB_RUTAS_1_shp)


    # Process: Make Feature Layer
    arcpy.MakeFeatureLayer_management(TB_RUTAS_PREPARACION_shp__3_, TB_RUTAS_Layer, "\"FLG_MZ\"=1", "",
                                      "FID FID VISIBLE NONE;Shape Shape VISIBLE NONE;UBIGEO UBIGEO VISIBLE NONE;ZONA ZONA VISIBLE NONE;MANZANA MANZANA VISIBLE NONE;FLG_MZ FLG_MZ VISIBLE NONE;ORIG_FID ORIG_FID VISIBLE NONE")

    # Process: Intersect (3)
    arcpy.Intersect_analysis(
        "TB_RUTAS_Layer #;D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_SEGUNDA_VIVIENDA_AEU.shp #",
        TB_INTERSECT_RUTAS_VIVIENDA_SEGUNDO_PUNTO, "ALL", "0.35 Meters", "INPUT")

    # Process: Summary Statistics (3)
    arcpy.Statistics_analysis(TB_INTERSECT_RUTAS_VIVIENDA_SEGUNDO_PUNTO, TB_INT_RUTAS_VIVIENDAS_AEU_MAX, "AEU MAX",
                              "FID_TB_RUTAS_PREPARACION")

    # Process: Add Join
    arcpy.AddJoin_management(TB_RUTAS_Layer, "FID", TB_INT_RUTAS_VIVIENDAS_AEU_MAX, "FID_TB_RUTAS_PREPARACION",
                             "KEEP_ALL")

    # Process: Copy Features (2)
    arcpy.CopyFeatures_management(TB_RUTAS_Layer__2_, TB_RUTAS_1_shp, "", "0", "0", "0")
    arcpy.AddField_management(TB_RUTAS_1_shp, "UBIGEO", "TEXT")
    arcpy.AddField_management(TB_RUTAS_1_shp, "CODCCPP", "TEXT")
    arcpy.AddField_management(TB_RUTAS_1_shp, "ZONA", "TEXT")
    arcpy.AddField_management(TB_RUTAS_1_shp, "MANZANA", "TEXT")
    arcpy.AddField_management(TB_RUTAS_1_shp, "AEU", "SHORT")
    arcpy.AddField_management(TB_RUTAS_1_shp, "FLG_MZ", "SHORT")


    # Process: Calculate Field

    arcpy.CalculateField_management(TB_RUTAS_1_shp, "UBIGEO",
                                    "[TB_RUTAS_P]", "VB", "")

    arcpy.CalculateField_management(TB_RUTAS_1_shp, "CODCCPP",
                                    "[TB_RUTAS_1]", "VB", "")

    arcpy.CalculateField_management(TB_RUTAS_1_shp, "ZONA",
                                    "[TB_RUTAS_2]", "VB", "")
    arcpy.CalculateField_management(TB_RUTAS_1_shp, "MANZANA",
                                    "[TB_RUTAS_3]", "VB", "")
    arcpy.CalculateField_management(TB_RUTAS_1_shp, "AEU",
                                    "[TB_INT_R_3]", "VB", "")

    arcpy.CalculateField_management(TB_RUTAS_1_shp, "FLG_MZ",
                                    "1", "VB", "")

    field_delete=""
    field_delete2 = ""

    for i in range(1,7):
        field_delete=";TB_RUTAS_"+str(i)+field_delete
    for j in range(1,4):
        field_delete2 = ";TB_INT_R_" + str(j) + field_delete2


    arcpy.DeleteField_management(TB_RUTAS_1_shp,"TB_RUTAS_P"+field_delete+";TB_INT_RUT"+field_delete2)




def RelacionarRutasLineasConAEU():
    arcpy.env.overwriteOutput = True
    TB_VIVIENDAS_CORTES_shp = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_VIVIENDAS_CORTES.shp"
    TB_RUTAS_PUNTOS_MIN = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_MIN.shp"
    TB_RUTAS_PUNTOS_MIN_SELECT = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_MIN_SELECT.shp"
    TB_INTERSECT_RUTAS_1="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_INTERSECT_RUTAS_1.shp"
    TB_INTERSECT_RUTAS_2 = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_INTERSECT_RUTAS_2.shp"
    TB_INTERSECT_RUTAS_3= "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_INTERSECT_RUTAS_3.shp"
    MZS_AEU = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"
    TB_INTERSECT_RUTAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_INTERSECT_RUTAS.shp"
    TB_STADISTICS_INTERSECT_RUTAS="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_STADISTICS_INTERSECT_RUTAS"
    TB_RUTAS_LINEAS="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS.shp"

    TB_RUTAS_PREPARACION = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_PREPARACION.shp"
    TB_RUTAS_PREPARACION_Layer="TB_RUTAS_PREPARACION_Layer"
    VIVIENDAS_MZS_OR_MAX = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/VIVIENDAS_MZS_OR_MAX.shp"

    TB_VERTICES_FINAL_AEU = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_VERTICES_FINAL_AEU.shp"
    TB_RUTAS_LINEAS_TEMP="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS_TEMP.shp"
    TB_RUTAS_LINEAS_DISSOLVE="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS_DISSOLVE.shp"
    TB_RUTAS_LINEAS_DISSOLVE_Layer = "TB_RUTAS_LINEAS_DISSOLVE_Layer"
    TB_RUTAS_LINEAS_TEMP_2="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS_TEMP_2.shp"

    arcpy.MakeFeatureLayer_management(TB_RUTAS_PREPARACION,TB_RUTAS_PREPARACION_Layer)

    #arcpy.Intersect_analysis(
    #    [TB_RUTAS_PREPARACION,TB_VIVIENDAS_CORTES_shp],
    #    TB_INTERSECT_RUTAS_1, "ALL", "0.70 Meters", "INPUT")
    arcpy.Intersect_analysis(
        [TB_RUTAS_PREPARACION, TB_VIVIENDAS_CORTES_shp],
        TB_INTERSECT_RUTAS_1, "ALL", "0.70 Meters", "INPUT")

    list_deletefield=["FID_VIVIEN","FLG_CORTE","FLG_MZ_1","ORIG_FID","FID_TB_VIV","ID","UBIGEO_1","CODCCPP_1","ZONA_1","MANZANA_1","FALSO_COD","NOMCCPP","DEPARTAMEN","PROVINCIA","DISTRITO","AREA","FRENTE_ORD","ID_REG_OR","P19A","P29","P29M","p29_1","ID_P23","P23","OR_VIV_AEU"]

    list_deletefield = ["FID_VIVIEN", "FLG_CORTE", "FLG_MZ_1", "ORIG_FID", "FID_TB_VIV", "ID", "UBIGEO_1", "CODCCPP_1",
                        "ZONA_1", "MANZANA_1", "FALSO_COD", "NOMCCPP", "DEPARTAMEN", "PROVINCIA", "DISTRITO", "AREA",
                        "FRENTE_ORD", "P19A", "P29", "P29M", "p29_1", "ID_P23", "P23", "OR_VIV_AEU"]

    arcpy.DeleteField_management(TB_INTERSECT_RUTAS_1,list_deletefield)
    arcpy.Intersect_analysis(
        [TB_RUTAS_PREPARACION, TB_RUTAS_PUNTOS_MIN],
        TB_INTERSECT_RUTAS_2, "ALL", "0.70 Meters", "INPUT")
    list_deletefield = [ "ORIG_FID", "FID_TB_AEU", "ID", "UBIGEO_1", "CODCCPP_1", "ZONA_1", "MANZANA_1","CANT_VIV"]

    arcpy.DeleteField_management(TB_INTERSECT_RUTAS_2, list_deletefield)



    arcpy.Intersect_analysis(
        [TB_RUTAS_PREPARACION, TB_VERTICES_FINAL_AEU],
        TB_INTERSECT_RUTAS_3, "ALL", "0.20 Meters", "INPUT")

    list_deletefield = ["FID_TB_VER", "ORIG_FID", "FID_TB_AEU", "ID", "UBIGEO_1", "CODCCPP_1", "ZONA_1", "MANZANA_1",
                        "CANT_VIV"]

    arcpy.DeleteField_management(TB_INTERSECT_RUTAS_3, list_deletefield)

    arcpy.Merge_management([TB_INTERSECT_RUTAS_1,TB_INTERSECT_RUTAS_2,TB_INTERSECT_RUTAS_3],TB_INTERSECT_RUTAS)
    #arcpy.([TB_INTERSECT_RUTAS_1, TB_INTERSECT_RUTAS_2], TB_INTERSECT_RUTAS)

    arcpy.Statistics_analysis(TB_INTERSECT_RUTAS,TB_STADISTICS_INTERSECT_RUTAS,[["AEU","MAX"],["ID_REG_OR","MAX"]],["FID_TB_RUT"])

    arcpy.AddJoin_management(TB_RUTAS_PREPARACION_Layer,"FID",TB_STADISTICS_INTERSECT_RUTAS,"FID_TB_RUT")

    arcpy.CopyFeatures_management(TB_RUTAS_PREPARACION_Layer,TB_RUTAS_LINEAS_TEMP)


    #alter_field=[["TB_RUTAS_P","UBIGEO"],["TB_RUTAS_1","CODCCPP"],["TB_RUTAS_2","ZONA"],["TB_RUTAS_3","MANZANA"],["tb_stadi_4","AEU"]]


    #add_field=["UBIGEO","CODCCPP","ZONA","MANZANA","AEU"]
    add_field = [["UBIGEO","TEXT"], ["CODCCPP","TEXT"], ["ZONA","TEXT"], ["MANZANA","TEXT"],["FLG_MZ","SHORT"] ,["AEU","SHORT"],["ID_REG_OR","SHORT"]]

    for el in add_field:
        arcpy.AddField_management(TB_RUTAS_LINEAS_TEMP,el[0],el[1])

    calculate_field= [["UBIGEO","!TB_RUTAS_P!"],["CODCCPP","!TB_RUTAS_1!"],["ZONA","!TB_RUTAS_2!"],["MANZANA","!TB_RUTAS_3!"],["FLG_MZ","!TB_RUTAS_4!"],["AEU","!tb_stadi_4!"],["ID_REG_OR","!tb_stadi_5!"]]

    for el in calculate_field:
        arcpy.CalculateField_management(TB_RUTAS_LINEAS_TEMP,el[0],el[1],"PYTHON_9.3")
    #for el in alter_field:
    #    arcpy.AlterField_management(TB_RUTAS_CONDOMINIOS, el[0], el[1])

    list_deletefield = ["TB_RUTAS_P","TB_RUTAS_1","TB_RUTAS_2","TB_RUTAS_3","TB_RUTAS_4", "TB_RUTAS_5", "tb_stadist", "tb_stadi_1", "tb_stadi_2", "tb_stadi_3","tb_stadi_4","tb_stadi_5"]


    arcpy.DeleteField_management(TB_RUTAS_LINEAS_TEMP, list_deletefield)



    sort_fields = [["UBIGEO", "ASCENDING"], ["CODCCPP", "ASCENDING"], ["ZONA", "ASCENDING"], ["MANZANA", "ASCENDING"],
                   ["AEU", "ASCENDING"], ["ID_REG_OR", "ASCENDING"]]


    arcpy.Sort_management(TB_RUTAS_LINEAS_TEMP, TB_RUTAS_LINEAS_TEMP_2, sort_fields)



    arcpy.Dissolve_management(TB_RUTAS_LINEAS_TEMP_2, TB_RUTAS_LINEAS_DISSOLVE, ["UBIGEO","CODCCPP","ZONA","MANZANA","FLG_MZ","AEU"],"", "MULTI_PART", "DISSOLVE_LINES")


    arcpy.MakeFeatureLayer_management(TB_RUTAS_LINEAS_DISSOLVE, TB_RUTAS_LINEAS_DISSOLVE_Layer)
    #TB_RUTAS_LINEAS_DISSOLVE_Layer
    arcpy.AddField_management(TB_RUTAS_LINEAS_DISSOLVE_Layer, "ID_RUTA","TEXT")
    arcpy.CalculateField_management(TB_RUTAS_LINEAS_DISSOLVE_Layer, "ID_RUTA", "!UBIGEO!+!CODCCPP!+!ZONA!+!MANZANA!+str(!AEU!)", "PYTHON_9.3")

    arcpy.AddField_management(MZS_AEU, "ID_RUTA","TEXT")
    arcpy.CalculateField_management(MZS_AEU, "ID_RUTA", "!UBIGEO!+!CODCCPP!+!ZONA!+!MANZANA!+str(!AEU!)",
                                    "PYTHON_9.3")

    arcpy.AddJoin_management(TB_RUTAS_LINEAS_DISSOLVE_Layer,"ID_RUTA",MZS_AEU,"ID_RUTA")

    arcpy.CopyFeatures_management(TB_RUTAS_LINEAS_DISSOLVE_Layer, TB_RUTAS_LINEAS)

    add_field = [["UBIGEO", "TEXT"], ["CODCCPP", "TEXT"], ["ZONA", "TEXT"], ["MANZANA", "TEXT"], ["FLG_MZ", "SHORT"],
                 ["AEU", "SHORT"],["CANT_VIV", "SHORT"]]

    for el in add_field:
        arcpy.AddField_management(TB_RUTAS_LINEAS,el[0],el[1])

    calculate_field= [["UBIGEO","!TB_RUTAS_L!"],["CODCCPP","!TB_RUTAS_1!"],["ZONA","!TB_RUTAS_2!"],["MANZANA","!TB_RUTAS_3!"],["FLG_MZ","!TB_RUTAS_4!"],["AEU","!TB_RUTAS_5!"],["CANT_VIV","!MZS_AEU_CA!"]]

    for el in calculate_field:
        arcpy.CalculateField_management(TB_RUTAS_LINEAS,el[0],el[1],"PYTHON_9.3")

    list_deletefield = ["TB_RUTAS_P", "TB_RUTAS_1", "TB_RUTAS_2", "TB_RUTAS_3", "TB_RUTAS_4", "TB_RUTAS_5", "TB_RUTAS_6","MZS_AEU_OI","MZS_AEU_FI","MZS_AEU_UB","MZS_AEU_CO","MZS_AEU_ZO","MZS_AEU_MA","MZS_AEU_CA","MZS_AEU_ID"]
    arcpy.DeleteField_management(TB_RUTAS_LINEAS, list_deletefield)

    #"FID_TB_RUT"


##############Relacionando Rutas de Lineas con AEU usando la primera vivienda de cada AEU############################
def RelacionarRutasLineasConAEUPrimeraPuerta():
    arcpy.env.overwriteOutput = True


    TB_RUTAS_1_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_1.shp"
    TB_INTERSECT_RUTAS_PRIMERA_PUERTA = "in_memory\\TB_INTERSECT_RUTAS_PRIMERA_PUERTA"
    TB_INT_RUTAS_PRIMERA_PUERTA_AEU_MAX = "in_memory\\TB_INT_RUTAS_PRIMERA_PUERTA_AEU_MAX"
    TB_RUTAS_1_Layer = "TB_RUTAS_1"
    TB_RUTAS_1_PRIMERA_PUERTA_shp="D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_1_PRIMERA_PUERTA.shp"
    TB_RUTAS_1_shp_DISSOLVE="in_memory\\TB_RUTAS_1_shp_DISSOLVE"

    arcpy.MakeFeatureLayer_management(TB_RUTAS_1_shp,TB_RUTAS_1_Layer, "\"AEU\"=0")



    arcpy.Intersect_analysis(
        "TB_RUTAS_1 #;D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_PRIMERA_PUERTA_AEU.shp #",
        TB_INTERSECT_RUTAS_PRIMERA_PUERTA, "ALL", "0.35 Meters", "INPUT")
    # Process: Summary Statistics (3)
    arcpy.Statistics_analysis(TB_INTERSECT_RUTAS_PRIMERA_PUERTA, TB_INT_RUTAS_PRIMERA_PUERTA_AEU_MAX, "AEU_1 MAX",
                              "FID_TB_RUTAS_1")

    # Process: Add Join
    arcpy.AddJoin_management(TB_RUTAS_1_Layer, "FID", TB_INT_RUTAS_PRIMERA_PUERTA_AEU_MAX, "FID_TB_RUTAS_1",
                             "KEEP_ALL")



    # Process: Copy Features (2)
    arcpy.CopyFeatures_management(TB_RUTAS_1_Layer, TB_RUTAS_1_PRIMERA_PUERTA_shp, "", "0", "0", "0")

    #######ACTUALIZANDO EN TB_RUTAS_1 El aeu correcto#################################
    for row in  arcpy.da.SearchCursor(TB_RUTAS_1_PRIMERA_PUERTA_shp, ['TB_INT_R_1', 'TB_INT_R_3']):  #'TB_INT_R_1' es el FID (identificador) del segmento rutas y 'TB_INT_R_3' es el aeu que se va a pegar al segemnto ruta

        where='FID='+str(row[0])
        numero_aeu=int(row[1])
        with arcpy.da.UpdateCursor(TB_RUTAS_1_shp, ['AEU'], where) as cursor2:
            for row2 in cursor2:
                row2[0] = int(numero_aeu)
                cursor2.updateRow(row2)
        del cursor2

    arcpy.Dissolve_management(TB_RUTAS_1_shp,TB_RUTAS_1_shp_DISSOLVE,['UBIGEO','CODCCPP','ZONA','MANZANA','AEU','FLG_MZ'])
    arcpy.CopyFeatures_management(TB_RUTAS_1_shp_DISSOLVE,TB_RUTAS_1_shp)

def ActualizarRutasViviendasMenoresIguales16():
    TB_RUTAS_1_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_1.shp"
    TB_RUTAS_PREPARACION_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_PREPARACION.shp"
    TB_RUTAS_2_shp_Layer="TB_RUTAS_2_shp_Layer"
    TB_RUTAS_2_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_2.shp"
    TB_RUTASS_shp = "in_memory\\TB_RUTASS"
    TB_RUTASS_Sort = "in_memory\\TB_RUTASS_Sort"
    TB_RUTASS_Sort_Layer = "TB_RUTASS_Sort_Layer"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"

    if arcpy.Exists(TB_RUTAS_2_shp):
        arcpy.Delete_management(TB_RUTAS_2_shp)


    #arcpy.Select_analysis(TB_RUTAS_PREPARACION_shp, TB_RUTAS_2_shp, "\"FLG_MZ\"=0")
    #arcpy.MakeFeatureLayer_management(TB_RUTAS_PREPARACION_shp, TB_RUTAS_2_shp, "\"FLG_MZ\"=0")
    # Process: Delete Field (2)
    #arcpy.DeleteField_management(TB_RUTAS_2_shp, "ORIG_FID")

    # Process: Merge (2)
    # arcpy.Merge_management([TB_RUTAS_1_1_shp, TB_RUTAS_1_2_shp, TB_RUTAS_2_shp], TB_RUTASS_shp)
    #

    arcpy.MakeFeatureLayer_management(TB_RUTAS_PREPARACION_shp, TB_RUTAS_2_shp_Layer, "\"FLG_MZ\"=0", "",
                                      "FID FID VISIBLE NONE;Shape Shape VISIBLE NONE;UBIGEO UBIGEO VISIBLE NONE;CODCCPP CODCCPP VISIBLE NONE;ZONA ZONA VISIBLE NONE;MANZANA MANZANA VISIBLE NONE;AEU AEU VISIBLE NONE;FLG_MZ FLG_MZ VISIBLE NONE")

    # Process: Add Field
    arcpy.AddField_management(TB_RUTAS_2_shp_Layer, "IDRUTA", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Calculate Field
    arcpy.CalculateField_management(TB_RUTAS_2_shp_Layer, "IDRUTA", "[UBIGEO] & [ZONA] & [MANZANA] ", "VB", "")

    # Process: Add Field (2)
    arcpy.AddField_management(MZS_AEU_dbf, "IDRUTA", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Calculate Field (2)
    arcpy.CalculateField_management(MZS_AEU_dbf, "IDRUTA", "[UBIGEO] & [ZONA] & [MANZANA] ", "VB", "")

    # Process: Add Join
    arcpy.AddJoin_management(TB_RUTAS_2_shp_Layer, "IDRUTA", MZS_AEU_dbf, "IDRUTA", "KEEP_ALL")

    # Process: Copy Features
    arcpy.CopyFeatures_management(TB_RUTAS_2_shp_Layer,TB_RUTAS_2_shp, "", "0", "0", "0")
    # Process: Add Field (3)

    arcpy.AddField_management(TB_RUTAS_2_shp, "UBIGEO", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    arcpy.AddField_management(TB_RUTAS_2_shp, "CODCCPP", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Add Field (4)
    arcpy.AddField_management(TB_RUTAS_2_shp, "ZONA", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Add Field (5)
    arcpy.AddField_management(TB_RUTAS_2_shp, "MANZANA", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    # Process: Add Field (6)
    arcpy.AddField_management(TB_RUTAS_2_shp, "AEU", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Add Field (7)
    arcpy.AddField_management(TB_RUTAS_2_shp, "FLG_MZ", "SHORT")


    arcpy.CalculateField_management(TB_RUTAS_2_shp, "UBIGEO", "[TB_RUTAS_P]", "VB", "")

    # Process: Calculate Field (4)
    arcpy.CalculateField_management(TB_RUTAS_2_shp, "CODCCPP", "[TB_RUTAS_1]", "VB", "")

    # Process: Calculate Field (4)
    arcpy.CalculateField_management(TB_RUTAS_2_shp, "ZONA", "[TB_RUTAS_2]", "VB", "")

    # Process: Calculate Field (5)
    arcpy.CalculateField_management(TB_RUTAS_2_shp, "MANZANA", "[TB_RUTAS_3]", "VB", "")

    # Process: Calculate Field (6)
    arcpy.CalculateField_management(TB_RUTAS_2_shp, "AEU", "[MZS_AEU_AE]", "VB", "")

    # Process: Calculate Field (7)
    arcpy.CalculateField_management(TB_RUTAS_2_shp, "FLG_MZ", "0", "VB", "")

    arcpy.DeleteField_management(TB_RUTAS_2_shp,"TB_RUTAS_P;TB_RUTAS_1;TB_RUTAS_2;TB_RUTAS_3;TB_RUTAS_4;TB_RUTAS_5;;TB_RUTAS_6;MZS_AEU_OI;MZS_AEU_FI;MZS_AEU_UB;MZS_AEU_ZO;MZS_AEU_MA;MZS_AEU_AE;MZS_AEU_CA;MZS_AEU_ID;MZS_AEU_FI;MZS_AEU__1;MZS_AEU_ID;MZS_AEU__2;MZS_AEU_CO;MZS_AEU_FA")




def CrearLineasAEUFinal():
    TB_PRIMERA_VIVIENDA_AEU_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_PRIMERA_VIVIENDA_AEU.shp"
    TB_RUTAS_1_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_1.shp"
    TB_RUTAS_2_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_2.shp"
    TB_RUTASS_shp = "in_memory\\TB_RUTASS"
    TB_RUTASS_Sort = "in_memory\\TB_RUTASS_Sort"
    TB_RUTASS_Sort_Layer = "TB_RUTASS_Sort_Layer"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"


    if arcpy.Exists(TB_RUTAS_LINEAS_shp):
        arcpy.Delete_management(TB_RUTAS_LINEAS_shp)


    arcpy.Merge_management([TB_RUTAS_1_shp, TB_RUTAS_2_shp], TB_RUTASS_shp)
    # Process: Sort

    arcpy.Sort_management(TB_RUTASS_shp, TB_RUTASS_Sort,
                          "UBIGEO ASCENDING;ZONA ASCENDING;MANZANA ASCENDING;AEU ASCENDING", "UR")

    arcpy.MakeFeatureLayer_management(TB_RUTASS_Sort, TB_RUTASS_Sort_Layer, "", "",
                                      "FID FID VISIBLE NONE;Shape Shape VISIBLE NONE;UBIGEO UBIGEO VISIBLE NONE;CODCCPP CODCCPP VISIBLE NONE;ZONA ZONA VISIBLE NONE;MANZANA MANZANA VISIBLE NONE;AEU AEU VISIBLE NONE;FLG_MZ FLG_MZ VISIBLE NONE")

    # Process: Add Field
    arcpy.AddField_management(TB_RUTASS_Sort_Layer, "IDRUTA", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Calculate Field
    arcpy.CalculateField_management(TB_RUTASS_Sort_Layer, "IDRUTA", "[UBIGEO] & [ZONA] & [MANZANA] & [AEU]", "VB", "")

    # Process: Add Field (2)
    arcpy.AddField_management(MZS_AEU_dbf, "IDRUTA", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Calculate Field (2)
    arcpy.CalculateField_management(MZS_AEU_dbf, "IDRUTA", "[UBIGEO] & [ZONA] & [MANZANA] & [AEU]", "VB", "")

    # Process: Add Join
    arcpy.AddJoin_management(TB_RUTASS_Sort_Layer, "IDRUTA", MZS_AEU_dbf, "IDRUTA", "KEEP_ALL")

    # Process: Copy Features
    arcpy.CopyFeatures_management(TB_RUTASS_Sort_Layer, TB_RUTAS_LINEAS_shp, "", "0", "0", "0")

    # Process: Add Field (3)
    arcpy.AddField_management(TB_RUTAS_LINEAS_shp, "UBIGEO", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    arcpy.AddField_management(TB_RUTAS_LINEAS_shp, "CODCCPP", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Add Field (4)
    arcpy.AddField_management(TB_RUTAS_LINEAS_shp, "ZONA", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Add Field (5)
    arcpy.AddField_management(TB_RUTAS_LINEAS_shp, "MANZANA", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    # Process: Add Field (6)
    arcpy.AddField_management(TB_RUTAS_LINEAS_shp, "AEU", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Add Field (7)
    arcpy.AddField_management(TB_RUTAS_LINEAS_shp, "FLG_MZ", "SHORT")
    arcpy.AddField_management(TB_RUTAS_LINEAS_shp, "CANT_VIV", "SHORT")

    # Process: Calculate Field (3)
    arcpy.CalculateField_management(TB_RUTAS_LINEAS_shp, "UBIGEO", "[TB_RUTASS_]", "VB", "")

    # Process: Calculate Field (4)
    arcpy.CalculateField_management(TB_RUTAS_LINEAS_shp, "CODCCPP", "[TB_RUTASS1]", "VB", "")

    # Process: Calculate Field (4)
    arcpy.CalculateField_management(TB_RUTAS_LINEAS_shp, "ZONA", "[TB_RUTAS_1]", "VB", "")

    # Process: Calculate Field (5)
    arcpy.CalculateField_management(TB_RUTAS_LINEAS_shp, "MANZANA", "[TB_RUTAS_2]", "VB", "")

    # Process: Calculate Field (6)
    arcpy.CalculateField_management(TB_RUTAS_LINEAS_shp, "AEU", "[TB_RUTAS_3]", "VB", "")

    # Process: Calculate Field (7)
    arcpy.CalculateField_management(TB_RUTAS_LINEAS_shp, "FLG_MZ", "[TB_RUTAS_4]", "VB", "")
    arcpy.CalculateField_management(TB_RUTAS_LINEAS_shp, "CANT_VIV", "[MZS_AEU_CA]", "VB", "")


    # Process: Delete Field
    arcpy.DeleteField_management(TB_RUTAS_LINEAS_shp,
                                 "TB_RUTASS_;TB_RUTASS1;TB_RUTAS_1;TB_RUTAS_2;TB_RUTAS_3;TB_RUTAS_4;TB_RUTAS_5;MZS_AEU_OI;MZS_AEU_UB;MZS_AEU_ZO;MZS_AEU_MA;MZS_AEU_AE;MZS_AEU_CA;MZS_AEU_ID;MZS_AEU_FI;MZS_AEU__1;MZS_AEU_CO;MZS_AEU__2;MZS_AEU_FA")







def UnirManzanasConViviendasCeros():
    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
    TB_RUTAS_DISSOLVE = "in_memory\\TB_RUTAS_DISSOLVE"
    TB_RUTAS_DISSOLVE__2_ = "in_memory\\TB_RUTAS_DISSOLVE"
    TB_RUTAS_DISSOLVE_Select2 = "in_memory\\TB_RUTAS_DISSOLVE_Select2"
    TB_RUTAS_DISSOLVE_Select3 = "in_memory\\TB_RUTAS_DISSOLVE_Select3"
    TB_RUTAS_DISSOLVE_Select3_Bu = "in_memory\\TB_RUTAS_DISSOLVE_Select3_Bu"
    TB_RUTAS_INTERSECT = "in_memory\\TB_RUTAS_INTERSECT"
    TB_RUTAS_SELECT_ZONA__2_ = "in_memory\\TB_RUTAS_SELECT_ZONA"
    TB_RUTAS_SELECT_ZONA_shp__2_ = "in_memory\\TB_RUTAS_SELECT_ZONA"
    TB_RUTAS_INTERSECT_SORT_Laye = "TB_RUTAS_INTERSECT_SORT_Laye"
    TB_RUTAS_INTERSECT_SORT_Stat1 = "in_memory\\TB_RUTAS_INTERSECT_SORT_Stat1"
    TB_RUTAS_SELECT_ZONA__4_ = "in_memory\\TB_RUTAS_SELECT_ZONA"
    TB_RUTAS_INTERSECT_SORT = "in_memory\\TB_RUTAS_INTERSECT_SORT"
    TB_RUTAS_INTERSECT_Sort_Stat__2_ = "in_memory\\TB_RUTAS_INTERSECT_SORT_Stat1"
    TB_RUTAS_DISSOLVE_shp__3_ = "in_memory\\TB_RUTAS_DISSOLVE"
    TB_RUTAS_INTERSECT_SORT_Laye__2_ = "TB_RUTAS_INTERSECT_SORT_Laye"
    TB_SEGUNDA_PASADA_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\SegundaPasada\\TB_SEGUNDA_PASADA.shp"
    TB_RUTAS_SELECT_ZONA = "in_memory\\TB_RUTAS_SELECT_ZONA"
    TB_RUTAS_DISSOLVE_Select2_Fe = "in_memory\\TB_RUTAS_DISSOLVE_Select2_Fe"
    TB_RUTAS_INTERSECT_Sort_Stat__4_ = "in_memory\\TB_RUTAS_INTERSECT_SORT_Stat1"


    if arcpy.Exists(TB_SEGUNDA_PASADA_shp):
        arcpy.Delete_management(TB_SEGUNDA_PASADA_shp)
    # Process: Dissolve
    arcpy.Dissolve_management(TB_RUTAS_LINEAS_shp, TB_RUTAS_DISSOLVE, "UBIGEO;ZONA;AEU;FLG_MZ",
                              "MANZANA COUNT;CANT_VIV SUM", "MULTI_PART", "DISSOLVE_LINES")

    # Process: Add Field (7)
    arcpy.AddField_management(TB_RUTAS_DISSOLVE, "ID_RUTAAEU", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Calculate Field (7)
    arcpy.CalculateField_management(TB_RUTAS_DISSOLVE_shp__3_, "ID_RUTAAEU", "[UBIGEO] & [ZONA] & [AEU]", "VB", "")

    # Process: Select (2)
    arcpy.Select_analysis(TB_RUTAS_DISSOLVE__2_, TB_RUTAS_DISSOLVE_Select3, "\"SUM_CANT_VIV\"<=0 AND \"FLG_MZ\"=0")

    # Process: Buffer
    arcpy.Buffer_analysis(TB_RUTAS_DISSOLVE_Select3, TB_RUTAS_DISSOLVE_Select3_Bu, "25 Meters", "FULL", "ROUND", "NONE",
                          "", "PLANAR")

    # Process: Select
    arcpy.Select_analysis(TB_RUTAS_DISSOLVE__2_, TB_RUTAS_DISSOLVE_Select2, "\"FLG_MZ\"=1")

    # Process: Feature Vertices To Points
    arcpy.FeatureVerticesToPoints_management(TB_RUTAS_DISSOLVE_Select2, TB_RUTAS_DISSOLVE_Select2_Fe, "START")

    # Process: Intersect
    arcpy.Intersect_analysis("in_memory\\TB_RUTAS_DISSOLVE_Select3_Bu #;in_memory\\TB_RUTAS_DISSOLVE_Select2_Fe #",
                             TB_RUTAS_INTERSECT, "ALL", "", "INPUT")

    # Process: Select (4)
    arcpy.Select_analysis(TB_RUTAS_INTERSECT, TB_RUTAS_SELECT_ZONA, "\"UBIGEO\"= \"UBIGEO_1\" AND \"ZONA\"=\"ZONA_1\"")

    # Process: Delete Identical
    arcpy.DeleteIdentical_management(TB_RUTAS_SELECT_ZONA, "UBIGEO;ZONA;AEU_1;FLG_MZ_1", "", "0")

    # Process: Add Field (5)
    arcpy.AddField_management(TB_RUTAS_SELECT_ZONA__2_, "TOTAL_VIV", "SHORT", "", "", "", "", "NULLABLE",
                              "NON_REQUIRED", "")

    # Process: Calculate Field (5)
    arcpy.CalculateField_management(TB_RUTAS_SELECT_ZONA_shp__2_, "TOTAL_VIV", "[SUM_CANT_VIV]+ [SUM_CANT_VIV_1]", "VB",
                                    "")

    # Process: Sort
    arcpy.Sort_management(TB_RUTAS_SELECT_ZONA__4_, TB_RUTAS_INTERSECT_SORT,
                          "UBIGEO ASCENDING;ZONA ASCENDING;AEU ASCENDING;TOTAL_VIV ASCENDING", "UR")

    # Process: Make Feature Layer
    arcpy.MakeFeatureLayer_management(TB_RUTAS_INTERSECT_SORT, TB_RUTAS_INTERSECT_SORT_Laye, "", "",
                                      "FID FID VISIBLE NONE;Shape Shape VISIBLE NONE;FID_TB_RUTAS_DISSOLVE_Select3_Bu FID_TB_RUTAS_DISSOLVE_Select3_Bu VISIBLE NONE;UBIGEO UBIGEO VISIBLE NONE;ZONA ZONA VISIBLE NONE;AEU AEU VISIBLE NONE;FLG_MZ FLG_MZ VISIBLE NONE;COUNT_MANZANA COUNT_MANZANA VISIBLE NONE;SUM_CANT_VIV SUM_CANT_VIV VISIBLE NONE;ID_RUTAAEU ID_RUTAAEU VISIBLE NONE;BUFF_DIST BUFF_DIST VISIBLE NONE;ORIG_FID ORIG_FID VISIBLE NONE;FID_TB_RUTAS_DISSOLVE_Select2_Fe FID_TB_RUTAS_DISSOLVE_Select2_Fe VISIBLE NONE;UBIGEO_1 UBIGEO_1 VISIBLE NONE;ZONA_1 ZONA_1 VISIBLE NONE;AEU_1 AEU_1 VISIBLE NONE;FLG_MZ_1 FLG_MZ_1 VISIBLE NONE;COUNT_MANZANA_1 COUNT_MANZANA_1 VISIBLE NONE;SUM_CANT_VIV_1 SUM_CANT_VIV_1 VISIBLE NONE;ID_RUTAAEU_1 ID_RUTAAEU_1 VISIBLE NONE;ORIG_FID_1 ORIG_FID_1 VISIBLE NONE;TOTAL_VIV TOTAL_VIV VISIBLE NONE")

    # Process: Summary Statistics (3)
    arcpy.Statistics_analysis(TB_RUTAS_INTERSECT_SORT_Laye, TB_RUTAS_INTERSECT_SORT_Stat1, "FID MIN", "UBIGEO;ZONA;AEU")

    # Process: Add Field (6)
    arcpy.AddField_management(TB_RUTAS_INTERSECT_SORT_Stat1, "flg_esc", "SHORT", "", "", "", "", "NULLABLE",
                              "NON_REQUIRED", "")

    # Process: Calculate Field (6)
    arcpy.CalculateField_management(TB_RUTAS_INTERSECT_Sort_Stat__2_, "flg_esc", "1", "VB", "")

    # Process: Add Join
    arcpy.AddJoin_management(TB_RUTAS_INTERSECT_SORT_Laye, "FID", TB_RUTAS_INTERSECT_Sort_Stat__4_, "MIN_FID",
                             "KEEP_COMMON")

    # Process: Select (3)
    arcpy.Select_analysis(TB_RUTAS_INTERSECT_SORT_Laye__2_, TB_SEGUNDA_PASADA_shp,
                          "\"flg_esc\"=1 and \"TOTAL_VIV\"<=16")

    # Process: Add Field
    arcpy.AddField_management(TB_SEGUNDA_PASADA_shp, "UBIGEO", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Add Field (2)
    arcpy.AddField_management(TB_SEGUNDA_PASADA_shp, "ZONA", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Add Field (3)
    arcpy.AddField_management(TB_SEGUNDA_PASADA_shp, "AEU", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Add Field (4)
    arcpy.AddField_management(TB_SEGUNDA_PASADA_shp, "AEU_1", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Calculate Field
    arcpy.CalculateField_management(TB_SEGUNDA_PASADA_shp, "UBIGEO", "[TB_RUTAS_1]", "VB", "")

    # Process: Calculate Field (2)
    arcpy.CalculateField_management(TB_SEGUNDA_PASADA_shp, "ZONA", "[TB_RUTAS_2]", "VB", "")

    # Process: Calculate Field (3)
    arcpy.CalculateField_management(TB_SEGUNDA_PASADA_shp, "AEU", "[TB_RUTAS_3]", "VB", "")

    # Process: Calculate Field (4)
    arcpy.CalculateField_management(TB_SEGUNDA_PASADA_shp, "AEU_1", "[TB_RUTA_13]", "VB", "")

    # Process: Delete Field
    arcpy.DeleteField_management(TB_SEGUNDA_PASADA_shp,
                                 "TB_RUTAS_I;TB_RUTAS_1;TB_RUTAS_2;TB_RUTAS_3;TB_RUTAS_4;TB_RUTAS_5;TB_RUTAS_6;TB_RUTAS_7;TB_RUTAS_8;TB_RUTAS_9;TB_RUTA_10;TB_RUTA_11;TB_RUTA_12;TB_RUTA_13;TB_RUTA_14;TB_RUTA_15;TB_RUTA_16;TB_RUTA_17;TB_RUTA_18;TB_RUTA_19;TB_RUTA_20;TB_RUTA_21;TB_RUTA_22;TB_RUTA_23;TB_RUTA_24;TB_RUTA_25;TB_RUTA_26")





def CrearTablaSegundaPasada():
    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
    TB_RUTAS_DISSOLVE = "in_memory\\TB_RUTAS_DISSOLVE"
    TB_RUTAS_DISSOLVE__2_ = "in_memory\\TB_RUTAS_DISSOLVE"
    TB_RUTAS_DISSOLVE_Select2 = "in_memory\\TB_RUTAS_DISSOLVE_Select2"
    TB_RUTAS_DISSOLVE_Select3 = "in_memory\\TB_RUTAS_DISSOLVE_Select3"
    TB_RUTAS_DISSOLVE_Select3_Bu = "in_memory\\TB_RUTAS_DISSOLVE_Select3_Bu"
    TB_RUTAS_INTERSECT = "in_memory\\TB_RUTAS_INTERSECT"
    TB_RUTAS_SELECT_ZONA__2_ = "in_memory\\TB_RUTAS_SELECT_ZONA"
    TB_RUTAS_SELECT_ZONA_shp__2_ = "in_memory\\TB_RUTAS_SELECT_ZONA"
    TB_RUTAS_INTERSECT_SORT_Laye = "TB_RUTAS_INTERSECT_SORT_Laye"
    TB_RUTAS_INTERSECT_SORT_Stat1 = "in_memory\\TB_RUTAS_INTERSECT_SORT_Stat1"
    TB_RUTAS_SELECT_ZONA__4_ = "in_memory\\TB_RUTAS_SELECT_ZONA"
    TB_RUTAS_INTERSECT_SORT = "in_memory\\TB_RUTAS_INTERSECT_SORT"
    TB_RUTAS_INTERSECT_Sort_Stat__2_ = "in_memory\\TB_RUTAS_INTERSECT_SORT_Stat1"
    TB_RUTAS_DISSOLVE_shp__3_ = "in_memory\\TB_RUTAS_DISSOLVE"
    TB_RUTAS_INTERSECT_SORT_Laye__2_ = "TB_RUTAS_INTERSECT_SORT_Laye"
    TB_SEGUNDA_PASADA_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\SegundaPasada\\TB_SEGUNDA_PASADA.shp"
    TB_RUTAS_SELECT_ZONA = "in_memory\\TB_RUTAS_SELECT_ZONA"
    TB_RUTAS_DISSOLVE_Select2_Fe = "in_memory\\TB_RUTAS_DISSOLVE_Select2_Fe"
    TB_RUTAS_INTERSECT_Sort_Stat__4_ = "in_memory\\TB_RUTAS_INTERSECT_SORT_Stat1"


    if arcpy.Exists(TB_SEGUNDA_PASADA_shp):
        arcpy.Delete_management(TB_SEGUNDA_PASADA_shp)
    # Process: Dissolve
    arcpy.Dissolve_management(TB_RUTAS_LINEAS_shp, TB_RUTAS_DISSOLVE, "UBIGEO;ZONA;AEU;FLG_MZ",
                              "MANZANA COUNT;CANT_VIV SUM", "MULTI_PART", "DISSOLVE_LINES")

    # Process: Add Field (7)
    arcpy.AddField_management(TB_RUTAS_DISSOLVE, "ID_RUTAAEU", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Calculate Field (7)
    arcpy.CalculateField_management(TB_RUTAS_DISSOLVE_shp__3_, "ID_RUTAAEU", "[UBIGEO] & [ZONA] & [AEU]", "VB", "")

    # Process: Select (2)
    arcpy.Select_analysis(TB_RUTAS_DISSOLVE__2_, TB_RUTAS_DISSOLVE_Select3, "\"SUM_CANT_VIV\"<=0 AND \"FLG_MZ\"=0")

    # Process: Buffer
    arcpy.Buffer_analysis(TB_RUTAS_DISSOLVE_Select3, TB_RUTAS_DISSOLVE_Select3_Bu, "50 Meters", "FULL", "ROUND", "NONE",
                          "", "PLANAR")

    # Process: Select
    arcpy.Select_analysis(TB_RUTAS_DISSOLVE__2_, TB_RUTAS_DISSOLVE_Select2, "\"FLG_MZ\"=1")

    # Process: Feature Vertices To Points



    #arcpy.FeatureVerticesToPoints_management(TB_RUTAS_DISSOLVE_Select2, TB_RUTAS_DISSOLVE_Select2_Fe, "START")

    # Process: Intersect

    #arcpy.Intersect_analysis("in_memory\\TB_RUTAS_DISSOLVE_Select3_Bu #;in_memory\\TB_RUTAS_DISSOLVE_Select2_Fe #",
    #                         TB_RUTAS_INTERSECT, "ALL", "", "INPUT")


    arcpy.Intersect_analysis("in_memory\\TB_RUTAS_DISSOLVE_Select3_Bu #;in_memory\\TB_RUTAS_DISSOLVE_Select2 #",
                             TB_RUTAS_INTERSECT, "ALL", "", "INPUT")


    #arcpy.Intersect_analysis("in_memory\\TB_RUTAS_DISSOLVE_Select3_Bu #;in_memory\\TB_RUTAS_DISSOLVE_Select2_Fe #",
    #                         TB_RUTAS_INTERSECT, "ALL", "", "INPUT")

    # Process: Select (4)
    arcpy.Select_analysis(TB_RUTAS_INTERSECT, TB_RUTAS_SELECT_ZONA, "\"UBIGEO\"= \"UBIGEO_1\" AND \"ZONA\"=\"ZONA_1\"")

    # Process: Delete Identical
    arcpy.DeleteIdentical_management(TB_RUTAS_SELECT_ZONA, "UBIGEO;ZONA;AEU_1;FLG_MZ_1", "", "0")

    # Process: Add Field (5)
    arcpy.AddField_management(TB_RUTAS_SELECT_ZONA__2_, "TOTAL_VIV", "SHORT", "", "", "", "", "NULLABLE",
                              "NON_REQUIRED", "")

    # Process: Calculate Field (5)
    arcpy.CalculateField_management(TB_RUTAS_SELECT_ZONA_shp__2_, "TOTAL_VIV", "[SUM_CANT_VIV]+ [SUM_CANT_VIV_1]", "VB",
                                    "")

    # Process: Sort
    arcpy.Sort_management(TB_RUTAS_SELECT_ZONA__4_, TB_RUTAS_INTERSECT_SORT,
                          "UBIGEO ASCENDING;ZONA ASCENDING;AEU ASCENDING;TOTAL_VIV ASCENDING", "UR")

    # Process: Make Feature Layer
    arcpy.MakeFeatureLayer_management(TB_RUTAS_INTERSECT_SORT, TB_RUTAS_INTERSECT_SORT_Laye, "", "",
                                      "FID FID VISIBLE NONE;Shape Shape VISIBLE NONE;FID_TB_RUTAS_DISSOLVE_Select3_Bu FID_TB_RUTAS_DISSOLVE_Select3_Bu VISIBLE NONE;UBIGEO UBIGEO VISIBLE NONE;ZONA ZONA VISIBLE NONE;AEU AEU VISIBLE NONE;FLG_MZ FLG_MZ VISIBLE NONE;COUNT_MANZANA COUNT_MANZANA VISIBLE NONE;SUM_CANT_VIV SUM_CANT_VIV VISIBLE NONE;ID_RUTAAEU ID_RUTAAEU VISIBLE NONE;BUFF_DIST BUFF_DIST VISIBLE NONE;ORIG_FID ORIG_FID VISIBLE NONE;FID_TB_RUTAS_DISSOLVE_Select2_Fe FID_TB_RUTAS_DISSOLVE_Select2_Fe VISIBLE NONE;UBIGEO_1 UBIGEO_1 VISIBLE NONE;ZONA_1 ZONA_1 VISIBLE NONE;AEU_1 AEU_1 VISIBLE NONE;FLG_MZ_1 FLG_MZ_1 VISIBLE NONE;COUNT_MANZANA_1 COUNT_MANZANA_1 VISIBLE NONE;SUM_CANT_VIV_1 SUM_CANT_VIV_1 VISIBLE NONE;ID_RUTAAEU_1 ID_RUTAAEU_1 VISIBLE NONE;ORIG_FID_1 ORIG_FID_1 VISIBLE NONE;TOTAL_VIV TOTAL_VIV VISIBLE NONE")

    # Process: Summary Statistics (3)
    arcpy.Statistics_analysis(TB_RUTAS_INTERSECT_SORT_Laye, TB_RUTAS_INTERSECT_SORT_Stat1, "FID MIN", "UBIGEO;ZONA;AEU")

    # Process: Add Field (6)
    arcpy.AddField_management(TB_RUTAS_INTERSECT_SORT_Stat1, "flg_esc", "SHORT", "", "", "", "", "NULLABLE",
                              "NON_REQUIRED", "")

    # Process: Calculate Field (6)
    arcpy.CalculateField_management(TB_RUTAS_INTERSECT_Sort_Stat__2_, "flg_esc", "1", "VB", "")

    # Process: Add Join
    arcpy.AddJoin_management(TB_RUTAS_INTERSECT_SORT_Laye, "FID", TB_RUTAS_INTERSECT_Sort_Stat__4_, "MIN_FID",
                             "KEEP_COMMON")

    # Process: Select (3)
    arcpy.Select_analysis(TB_RUTAS_INTERSECT_SORT_Laye__2_, TB_SEGUNDA_PASADA_shp,
                          "\"flg_esc\"=1 and \"TOTAL_VIV\"<=16")

    # Process: Add Field
    arcpy.AddField_management(TB_SEGUNDA_PASADA_shp, "UBIGEO", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Add Field (2)
    arcpy.AddField_management(TB_SEGUNDA_PASADA_shp, "ZONA", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Add Field (3)
    arcpy.AddField_management(TB_SEGUNDA_PASADA_shp, "AEU", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Add Field (4)
    arcpy.AddField_management(TB_SEGUNDA_PASADA_shp, "AEU_1", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Calculate Field
    arcpy.CalculateField_management(TB_SEGUNDA_PASADA_shp, "UBIGEO", "[TB_RUTAS_1]", "VB", "")

    # Process: Calculate Field (2)
    arcpy.CalculateField_management(TB_SEGUNDA_PASADA_shp, "ZONA", "[TB_RUTAS_2]", "VB", "")

    # Process: Calculate Field (3)
    arcpy.CalculateField_management(TB_SEGUNDA_PASADA_shp, "AEU", "[TB_RUTAS_4]", "VB", "")

    # Process: Calculate Field (4)
    arcpy.CalculateField_management(TB_SEGUNDA_PASADA_shp, "AEU_1", "[TB_RUTA_14]", "VB", "")

    # Process: Delete Field
    arcpy.DeleteField_management(TB_SEGUNDA_PASADA_shp,
                                 "TB_RUTAS_I;TB_RUTAS_1;TB_RUTAS_2;TB_RUTAS_3;TB_RUTAS_4;TB_RUTAS_5;TB_RUTAS_6;TB_RUTAS_7;TB_RUTAS_8;TB_RUTAS_9;TB_RUTA_10;TB_RUTA_11;TB_RUTA_12;TB_RUTA_13;TB_RUTA_14;TB_RUTA_15;TB_RUTA_16;TB_RUTA_17;TB_RUTA_18;TB_RUTA_19;TB_RUTA_20;TB_RUTA_21;TB_RUTA_22;TB_RUTA_23;TB_RUTA_24;TB_RUTA_25;TB_RUTA_26")

def ActualizarRutasAEUSegundaPasada():
    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbanaCondominios"
   #MZS_AEU= "D:/ShapesPruebasSegmentacionUrbanaCondominios/SegundaPasada/MZS_AEU.dbf"
   #MZS_TRABAJO="D:/ShapesPruebasSegmentacionUrbanaCondominios/SegundaPasada/TB_MZS_TRABAJO.shp"
   #VIVIENDAS="D:/ShapesPruebasSegmentacionUrbanaCondominios/SegundaPasada/TB_VIVIENDAS_U_TRABAJO.shp"
   #RUTAS="D:/ShapesPruebasSegmentacionUrbanaCondominios/SegundaPasada/TB_RUTAS.shp"


    SEGUNDA_PASADA = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\SegundaPasada\\TB_SEGUNDA_PASADA.shp"

    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    TB_VIVIENDAS_ORDENADAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\EnumerarAEUViviendas\\TB_VIVIENDAS_ORDENADAS.shp"
    MZS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"




    with arcpy.da.SearchCursor(SEGUNDA_PASADA, ['UBIGEO', 'ZONA','AEU','AEU_1']) as cursor:
        for row in cursor:
            where=' UBIGEO=\''+str(row[0])+'\' AND ZONA=\''+str(row[1])+'\' AND AEU='+str(row[2])  # SE UBICA EL AEU DE LA MANZANA ESCOGIDA
            where_2=' UBIGEO=\''+str(row[0])+'\' AND ZONA=\''+str(row[1])+'\' AND AEU='+str(row[3])  ##SE UBICA EL AEU DEL SEGMENTO ESCOGIDO
            numero_aeu=int(row[3])
            where_viviendas = ' UBIGEO=\'' + str(row[0]) + '\' AND ZONA=\'' + str(row[1]) + '\' AND AEU=' + str(row[2])  # SE UBICA EL AEU DE LA MANZANA ESCOGIDA

            with arcpy.da.UpdateCursor(MZS_AEU_dbf,['AEU'], where) as cursor8:
                for row8 in cursor8:
                    row8[0] = int(numero_aeu)
                    cursor8.updateRow(row8)

            del cursor8

            with arcpy.da.UpdateCursor(MZS,['AEU'], where) as cursor9:
                for row9 in cursor9:
                    row9[0] = int(numero_aeu)
                    cursor9.updateRow(row9)
            del cursor9

            or_max=0


#            with arcpy.da.SearchCursor(TB_VIVIENDAS_ORDENADAS_shp, ['AEU', 'OR_VIV_AEU'], where_2) as cursor7:
#                for row7 in cursor7:
#                    if or_max<int(row7[1]):
#                        or_max=int(row7[1])
#
#            del cursor7
#
#            or_max=or_max+1
#
            with arcpy.da.UpdateCursor(TB_VIVIENDAS_ORDENADAS_shp,['AEU','OR_VIV_AEU'],where_viviendas ) as cursor10:
                for row10 in cursor10:
                    row10[0] = int(numero_aeu)
                    row10[1]=or_max
                    or_max=or_max+1
                    cursor10.updateRow(row10)
            del cursor10


            with arcpy.da.UpdateCursor(TB_RUTAS_LINEAS_shp,['AEU'], where) as cursor11:
                for row11 in cursor11:
                    row11[0] = int(numero_aeu)
                    cursor11.updateRow(row11)
            del cursor11



         #  with arcpy.da.UpdateCursor(RUTAS, ['flg'], where_2) as cursor12:
         #      for row12 in cursor12:
         #          row12[0] = 1
         #          cursor12.updateRow(row12)
         #  del cursor12

def CodigoFalso():
    MZS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    MIN_AEU = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\Renumerar\\MIN_AEU"
    MIN_AEU_SORT = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\Renumerar\\MIN_AEU_SORT"
    #arcpy.AddField_management(MZS,
    #                          "FALSCOD2", "TEXT")
 #   expresion= """" def FindLabel ( [MANZANA] ): mzs_temp=[MANZANA][0:3]
 #    mzs_int=int(mzs_temp)
 #   mzs=str(mzs_int)+[MANZANA][3:]
#
 # return mzs
 #   """"
    expression_2 = "idcodfalso(!FALSO_COD!)"

    codeblock = """def idcodfalso(FALSO_COD):\n  return "0" * (3 - len(str(FALSO_COD)))+str(FALSO_COD)"""

    arcpy.AddField_management(MZS,
                              "O", "TEXT")
    arcpy.CalculateField_management(MZS, "O", expression_2, "PYTHON_9.3", codeblock)



    #arcpy.CalculateField_management(MZS, "O", expresion, {expression_type}, {code_block})
    #arcpy.CalculateField_management(MZS, "O", expresion, {expression_type}, {code_block})
    #CalculateField_management(in_table, field, expression, {expression_type}, {code_block})
    #arcpy.CalculateField_management(MZS, "FALSCOD2", )



    #arcpy.Statistics_analysis(MZS, MIN_AEU, [["IDFALSO", "MIN"]], ["UBIGEO", "ZONA", "AEU"])
    #arcpy.Sort_management(MIN, MIN_AEU_SORT, ["MIN_IDFALSO", "AEU"])

def Renumerar_AEU(ubigeos):
    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbanaCondominios"
    arcpy.env.overwriteOutput = True
    MIN_AEU = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\Renumerar\\MIN_AEU"
    MIN_AEU_SORT = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\Renumerar\\MIN_AEU_SORT"
    AEU_CANT_VIV = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\Renumerar\\AEU_CANT_VIV"
    TB_VIVIENDAS_ORDENADAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\EnumerarAEUViviendas\\TB_VIVIENDAS_ORDENADAS.shp"
    TB_MZS_shp = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    ZONAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    #TB_VIVIENDAS_ORDENADAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\EnumerarAEUViviendas\\TB_VIVIENDAS_ORDENADAS.shp"
    #MZS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"


    #arcpy.AddField_management(MZS_AEU_dbf, "AEU_FINAL", "SHORT")





   # if arcpy.Exists("D:/ShapesPruebasSegmentacionUrbanaCondominios/Renumerar/TB_MZS_TRABAJO.shp"):
   #     arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbanaCondominios/Renumerar/TB_MZS_TRABAJO.shp")
   # if arcpy.Exists("D:/ShapesPruebasSegmentacionUrbanaCondominios/Renumerar/MZS_AEU.dbf"):
   #     arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbanaCondominios/Renumerar/MZS_AEU.dbf")
   # if arcpy.Exists("D:/ShapesPruebasSegmentacionUrbanaCondominios/Renumerar/TB_RUTAS.shp"):
   #     arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbanaCondominios/Renumerar/TB_RUTAS.shp")
   # if arcpy.Exists("D:/ShapesPruebasSegmentacionUrbanaCondominios/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp"):
   #     arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbanaCondominios/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp")
   # if arcpy.Exists(MIN_AEU):
   #     arcpy.Delete_management(MIN_AEU)
   # if arcpy.Exists(MIN_AEU_SORT):
   #     arcpy.Delete_management(MIN_AEU_SORT)
   # if arcpy.Exists(AEU_CANT_VIV):
   #     arcpy.Delete_management(AEU_CANT_VIV)

#    arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbanaCondominios/SegundaPasada/TB_MZS_TRABAJO.shp",
#                                  "D:/ShapesPruebasSegmentacionUrbanaCondominios/Renumerar/TB_MZS_TRABAJO.shp")
#    arcpy.AddField_management("D:/ShapesPruebasSegmentacionUrbanaCondominios/Renumerar/TB_MZS_TRABAJO.shp", "AEU_FINAL",
#                              "SHORT")
#    arcpy.Copy_management("D:/ShapesPruebasSegmentacionUrbanaCondominios/SegundaPasada/MZS_AEU.dbf",
#                          "D:/ShapesPruebasSegmentacionUrbanaCondominios/Renumerar/MZS_AEU.dbf")
#    arcpy.AddField_management("D:/ShapesPruebasSegmentacionUrbanaCondominios/Renumerar/MZS_AEU.dbf", "AEU_FINAL", "SHORT")
#
#    arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbanaCondominios/SegundaPasada/TB_RUTAS.shp",
#                                  "D:/ShapesPruebasSegmentacionUrbanaCondominios/Renumerar/TB_RUTAS.shp")
#    arcpy.AddField_management("D:/ShapesPruebasSegmentacionUrbanaCondominios/Renumerar/TB_RUTAS.shp", "AEU_FINAL", "SHORT")
#    arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbanaCondominios/SegundaPasada/TB_VIVIENDAS_U_TRABAJO.shp",
#                                  "D:/ShapesPruebasSegmentacionUrbanaCondominios/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp")
    arcpy.AddField_management(MZS_AEU_dbf,
                              "AEU_FINAL", "SHORT")

    arcpy.AddField_management(TB_VIVIENDAS_ORDENADAS_shp,
                              "AEU_FINAL", "SHORT")

    arcpy.AddField_management(MZS_AEU_dbf,
                              "IDMANZANA", "TEXT")

    arcpy.AddField_management(MZS_AEU_dbf,
                              "IDFALSO", "TEXT")
    arcpy.AddField_management(MZS_AEU_dbf,
                              "FALSCOD2", "TEXT")

    arcpy.AddField_management(TB_MZS_shp,
                              "AEU_FINAL", "SHORT")

    expression_2 = "idcodfalso(!FALSO_COD!)"

    codeblock = """def idcodfalso(FALSO_COD):\n  return "0" * (3 - len(str(FALSO_COD)))+str(FALSO_COD)"""

    arcpy.AddField_management(MZS_AEU_dbf,"FALSCOD2", "TEXT")

    arcpy.CalculateField_management(MZS_AEU_dbf, "FALSCOD2", expression_2, "PYTHON_9.3", codeblock)
    arcpy.CalculateField_management(MZS_AEU_dbf, "IDMANZANA", "[UBIGEO]&[ZONA]&[MANZANA]", "VB", "")
    arcpy.CalculateField_management(MZS_AEU_dbf, "IDFALSO", "[UBIGEO]&[ZONA]&[FALSCOD2]", "VB", "")

    arcpy.MakeTableView_management(MZS_AEU_dbf, "mzs_aeu")
    arcpy.MakeTableView_management(MZS_AEU_dbf, "mzs_aeu2")


    arcpy.Statistics_analysis(MZS_AEU_dbf, MIN_AEU, [["IDFALSO", "MIN"]], ["UBIGEO", "ZONA", "AEU"])
    arcpy.Sort_management(MIN_AEU, MIN_AEU_SORT, ["MIN_IDFALSO", "AEU"])
    arcpy.MakeTableView_management(MIN_AEU_SORT, "min_aeu_sort")

    where_expression = UBIGEO.ExpresionUbigeos(ubigeos)

    for row in arcpy.da.SearchCursor(ZONAS, ["UBIGEO", "ZONA"], where_expression):

        ubigeo=row[0]
        zona = row[1]

        where_x = ' "UBIGEO"=\'' + str(ubigeo) + '\' AND "ZONA"=\'' + str(zona) + '\''
        arcpy.SelectLayerByAttribute_management("min_aeu_sort", "NEW_SELECTION", where_x)
        print where_x

        numero_aeu_nuevo = 1

        for row11 in arcpy.da.SearchCursor("min_aeu_sort", ['UBIGEO', 'ZONA', 'AEU', 'MIN_IDFALSO']):
            aeu_anterior = str(row11[2])


            where11 = ' "UBIGEO"=\'' + str(row11[0]) + '\' AND "ZONA"=\'' + str(row11[1]) + '\' AND AEU=' + str(aeu_anterior)
            with arcpy.da.UpdateCursor(MZS_AEU_dbf,
                                       ['AEU_FINAL'], where11) as cursor15:
                for row15 in cursor15:
                    row15[0] = numero_aeu_nuevo
                    cursor15.updateRow(row15)

            del cursor15


            with arcpy.da.UpdateCursor(TB_MZS_shp,
                                       ['AEU_FINAL'], where11) as cursor16:
                for row16 in cursor16:
                    row16[0] = numero_aeu_nuevo
                    cursor16.updateRow(row16)
            del cursor16

            with arcpy.da.UpdateCursor(TB_VIVIENDAS_ORDENADAS_shp,
                                               ['AEU_FINAL'], where11) as cursor17:
                for row17 in cursor17:
                    row17[0] = numero_aeu_nuevo
                    cursor17.updateRow(row17)

            del cursor17
            numero_aeu_nuevo = 1 + numero_aeu_nuevo

def RenumerarRutas():
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbanaCondominios"
    TB_RUTAS_PUNTOS_shp="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"
    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"

    arcpy.AddField_management(TB_RUTAS_LINEAS_shp,
                              "AEU_FINAL", "SHORT")

    arcpy.AddField_management(TB_RUTAS_PUNTOS_shp,
                              "AEU_FINAL", "SHORT")


    for row in arcpy.da.SearchCursor(MZS_AEU_dbf, ["UBIGEO", "ZONA","AEU","AEU_FINAL"]):

        where = ' "UBIGEO"=\'' + str(row[0]) + '\' AND "ZONA"=\'' + str(row[1]) + '\' AND AEU=' + str(row[2])
        numero_aeu_nuevo=int(row[3])
        with arcpy.da.UpdateCursor(TB_RUTAS_LINEAS_shp,
                                   ['AEU_FINAL'], where) as cursorx:
            for rowx in cursorx:
                rowx[0] = numero_aeu_nuevo
                cursorx.updateRow(rowx)

        with arcpy.da.UpdateCursor(TB_RUTAS_PUNTOS_shp,
                                           ['AEU_FINAL'], where) as cursorxx:
            for rowxx in cursorxx:
                rowxx[0] = numero_aeu_nuevo
                cursorxx.updateRow(rowxx)
    del cursorx



    field_delete = ""
    for i in range(1, 10):
        field_delete = ";TB_VIVIE_" + str(i) + field_delete
    for j in range(10, 30):
        field_delete = ";TB_VIVI_" + str(j) + field_delete
    #arcpy.DeleteField_management(TB_RUTAS_PUNTOS_shp, "TB_VIVIEND" + field_delete)

    #for row in arcpy.da.SearchCursor(MZS_AEU_dbf, ["UBIGEO", "ZONA","MANZANA","AEU"]):

def CrearTB_AEUS():
    AEUS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Renumerar/TB_AEUS.dbf"
    AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    AEUS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Renumerar/TB_AEUS_PUNTOS.shp"
    RUTAS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS.shp"
    RUTAS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"


    if arcpy.Exists (AEUS):
        arcpy.Delete_management(AEUS)

    if arcpy.Exists (AEUS_LINEAS):
        arcpy.Delete_management(AEUS_LINEAS)

    if arcpy.Exists (AEUS_PUNTOS):
        arcpy.Delete_management(AEUS_PUNTOS)

    arcpy.Statistics_analysis(MZS_AEU_dbf, AEUS, [["CANT_VIV", "SUM"]], ["UBIGEO","CODCCPP" ,"ZONA", "AEU_FINAL"])
    arcpy.Dissolve_management(RUTAS_LINEAS, AEUS_LINEAS, ["UBIGEO", "CODCCPP","ZONA", "AEU_FINAL"], [["CANT_VIV", "SUM"]])
    arcpy.Dissolve_management(RUTAS_PUNTOS, AEUS_PUNTOS, ["UBIGEO","CODCCPP","ZONA", "AEU_FINAL"], [["CANT_VIV", "SUM"]])
    arcpy.AddField_management(AEUS, "CANT_VIV", "SHORT")

    arcpy.CalculateField_management(AEUS, "CANT_VIV",
                                    "[SUM_CANT_V]", "VB", "")

    arcpy.AddField_management(AEUS_LINEAS, "CANT_VIV", "SHORT")

    arcpy.CalculateField_management(AEUS_LINEAS, "CANT_VIV",
                                    "[SUM_CANT_V]", "VB", "")
    arcpy.AddField_management(AEUS_PUNTOS, "CANT_VIV", "SHORT")

    arcpy.CalculateField_management(AEUS_PUNTOS, "CANT_VIV",
                                    "[SUM_CANT_V]", "VB", "")

    arcpy.DeleteField_management(AEUS, ["SUM_CANT_V"])
    arcpy.DeleteField_management(AEUS, ["FREQUENCY"])
    arcpy.DeleteField_management(AEUS_LINEAS, ["SUM_CANT_V"])
    arcpy.DeleteField_management(AEUS_PUNTOS, ["SUM_CANT_V"])


def CrearRutasMultipart():

    RUTAS_LINEAS="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS.shp"
    RUTAS_LINEAS_MULTIPART="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS_MULTIPART.shp"
    arcpy.MultipartToSinglepart_management(RUTAS_LINEAS,RUTAS_LINEAS_MULTIPART)



def ModelarTablas(ubigeos):
    AEUS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Renumerar/TB_AEUS.dbf"
    AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    RUTAS_LINEAS = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    SECCIONES="D:/ShapesPruebasSegmentacionUrbanaCondominios/SECCIONES/EnumerarSecciones/TB_SECCIONES.shp"

    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"

    arcpy.DeleteField_management(MZS_AEU_dbf, ["IDRUTA","IDMANZANA"])

    arcpy.AddField_management(RUTAS_LINEAS, "LLAVE_MZS", "TEXT")
    arcpy.AddField_management(RUTAS_LINEAS, "LLAVE_AEU", "TEXT")
    arcpy.AddField_management(RUTAS_LINEAS, "LLAVE_RUTA", "TEXT")

    arcpy.AddField_management(MZS_AEU_dbf, "LLAVE_MZS", "TEXT")
    arcpy.AddField_management(MZS_AEU_dbf, "LLAVE_AEU", "TEXT")
    arcpy.AddField_management(MZS_AEU_dbf, "LLAVE_RUTA", "TEXT")

    arcpy.AddField_management(AEUS_LINEAS, "LLAVE_SECC", "TEXT")
    arcpy.AddField_management(AEUS_LINEAS, "LLAVE_AEU", "TEXT")
    arcpy.AddField_management(AEUS_LINEAS, "LLAVE_CCPP", "TEXT")


    arcpy.AddField_management(AEUS, "LLAVE_SECC", "TEXT")
    arcpy.AddField_management(AEUS, "LLAVE_AEU", "TEXT")
    arcpy.AddField_management(AEUS, "LLAVE_CCPP", "TEXT")
    arcpy.AddField_management(AEUS, "EST_CROQ", "SHORT")
    arcpy.AddField_management(AEUS, "EST_SEG", "SHORT")



    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "LLAVE_VIV", "TEXT")
    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "LLAVE_AEU", "TEXT")
    arcpy.AddField_management(SECCIONES, "LLAVE_SECC", "TEXT")



    expression = "str(!UBIGEO!)+str(!CODCCPP!)+str(!ZONA!)+str(!MANZANA!)"
    arcpy.CalculateField_management(MZS_AEU_dbf, "LLAVE_MZS", expression, "PYTHON_9.3")

    expression = "str(!UBIGEO!)+str(!CODCCPP!)+str(!ZONA!)+str(!AEU_FINAL!)"
    arcpy.CalculateField_management(MZS_AEU_dbf, "LLAVE_AEU", expression, "PYTHON_9.3")

    expression = "str(!UBIGEO!)+str(!CODCCPP!)+str(!ZONA!)+str(!MANZANA!)+str(!AEU_FINAL!)"
    arcpy.CalculateField_management(MZS_AEU_dbf, "LLAVE_RUTA", expression, "PYTHON_9.3")



    expression = "str(!UBIGEO!)+str(!CODCCPP!)+str(!ZONA!)+str(!MANZANA!)"
    arcpy.CalculateField_management(RUTAS_LINEAS, "LLAVE_MZS", expression, "PYTHON_9.3")

    expression = "str(!UBIGEO!)+str(!CODCCPP!)+str(!ZONA!)+str(!AEU_FINAL!)"
    arcpy.CalculateField_management(RUTAS_LINEAS, "LLAVE_AEU", expression, "PYTHON_9.3")

    expression = "str(!UBIGEO!)+str(!CODCCPP!)+str(!ZONA!)+str(!MANZANA!)+str(!AEU_FINAL!)"
    arcpy.CalculateField_management(RUTAS_LINEAS, "LLAVE_RUTA", expression, "PYTHON_9.3")




    expression = "str(!UBIGEO!)+str(!CODCCPP!)+str(!ZONA!)+str(!SECCION!)"
    arcpy.CalculateField_management(AEUS_LINEAS, "LLAVE_SECC", expression, "PYTHON_9.3")

    expression = "str(!UBIGEO!)+str(!CODCCPP!)+str(!ZONA!)+str(!AEU_FINAL!)"
    arcpy.CalculateField_management(AEUS_LINEAS, "LLAVE_AEU", expression, "PYTHON_9.3")

    expression = "str(!UBIGEO!)+str(!CODCCPP!)"
    arcpy.CalculateField_management(AEUS_LINEAS, "LLAVE_CCPP", expression, "PYTHON_9.3")




    expression = "str(!UBIGEO!)+str(!CODCCPP!)+str(!ZONA!)+str(!SECCION!)"
    arcpy.CalculateField_management(AEUS, "LLAVE_SECC", expression, "PYTHON_9.3")

    expression = "str(!UBIGEO!)+str(!CODCCPP!)+str(!ZONA!)+str(!AEU_FINAL!)"
    arcpy.CalculateField_management(AEUS, "LLAVE_AEU", expression, "PYTHON_9.3")

    expression = "str(!UBIGEO!)+str(!CODCCPP!)"
    arcpy.CalculateField_management(AEUS, "LLAVE_CCPP", expression, "PYTHON_9.3")





    expression = "str(!UBIGEO!)+str(!ZONA!)+str(!MANZANA!)+str(!ID_REG_OR!)"
    arcpy.CalculateField_management(VIVIENDAS_ORDENADAS, "LLAVE_VIV", expression, "PYTHON_9.3")


    expression = "str(!UBIGEO!)+str(!ZONA!)+str(!MANZANA!)+str(!AEU_FINAL!)"
    arcpy.CalculateField_management(VIVIENDAS_ORDENADAS, "LLAVE_AEU", expression, "PYTHON_9.3")

    expression = "str(!UBIGEO!)+str(!ZONA!)+str(!MANZANA!)+str(!AEU_FINAL!)"
    arcpy.CalculateField_management(VIVIENDAS_ORDENADAS, "LLAVE_AEU", expression, "PYTHON_9.3")

    expression = "str(!UBIGEO!)+str(!CODCCPP!)+str(!ZONA!)+str(!SECCION!)"

    arcpy.CalculateField_management(SECCIONES, "LLAVE_SECC", expression, "PYTHON_9.3")


#def EliminarRegistros(ubigeos):
#    arcpy.env.workspace = "Database Connections/PruebaSegmentacion.sde"
#    SEGM_ESP_SECCIONES = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_ESP_SECCION"
#    SEGM_ESP_AEUS = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_ESP_AEU"
#    SEGM_ESP_AEUS_LINEAS = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_ESP_AEU_LINEA"
#    SEGM_ESP_RUTAS = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_ESP_RUTA"
#    SEGM_ESP_RUTAS_LINEAS = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_ESP_RUTA_LINEA"
#    SEGM_ESP_VIVIENDAS_U = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_ESP_VIVIENDA_U"
#    where_list=UBIGEO.ExpresionUbigeosImportacion(ubigeos)
#
#    arcpy.MakeFeatureLayer_management(SEGM_ESP_SECCIONES, "tmp_secciones", where_list)
#    arcpy.MakeFeatureLayer_management(SEGM_ESP_AEUS_LINEAS, "tmp_aeus_lineas", where_list)
#    arcpy.MakeFeatureLayer_management(SEGM_ESP_RUTAS_LINEAS, "tmp_rutas_lineas", where_list)
#    arcpy.MakeFeatureLayer_management(SEGM_ESP_VIVIENDAS_U, "tmp_viviendas_u", where_list)
#    arcpy.MakeTableView_management(SEGM_ESP_AEUS, "tmp_aeus", where_list)
#    arcpy.MakeTableView_management(SEGM_ESP_RUTAS, "tmp_rutas", where_list)
#
#
#    try:
#
#
#        if int(arcpy.GetCount_management("tmp_secciones").getOutput(0)) > 0:
#            arcpy.TruncateTable_management("tmp_secciones")
#
#        if int(arcpy.GetCount_management("tmp_aeus_lineas").getOutput(0)) > 0:
#            arcpy.TruncateTable_management("tmp_aeus_lineas")
#
#        if int(arcpy.GetCount_management("tmp_rutas_lineas").getOutput(0)) > 0:
#            arcpy.TruncateTable_management("tmp_rutas_lineas")
#
#        if int(arcpy.GetCount_management("tmp_viviendas_u").getOutput(0)) > 0:
#            arcpy.TruncateTable_management("tmp_viviendas_u")
#
#        if int(arcpy.GetCount_management("tmp_aeus").getOutput(0)) > 0:
#            arcpy.TruncateTable_management("tmp_aeus")
#
#        if int(arcpy.GetCount_management("tmp_rutas").getOutput(0)) > 0:
#            arcpy.TruncateTable_management("tmp_rutas")
#
#            #arcpy.DeleteRows_management(AEUS_TEMP)
#
#    except Exception as err:
#        print(err.args[0])

def InsertarRegistros(ubigeos):
    arcpy.env.workspace = "Database Connections/PruebaSegmentacion.sde"
    TB_AEUS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Renumerar/TB_AEUS.dbf"
    TB_AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    TB_RUTAS_LINEAS = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
    TB_RUTAS="D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"
    TB_SECCIONES = "D:/ShapesPruebasSegmentacionUrbanaCondominios/SECCIONES/EnumerarSecciones/TB_SECCIONES.shp"
    TB_VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    #TB_MARCOS_AEUS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Mapas/TB_MARCOS_AEUS.shp"
    #TB_MARCOS_SECCIONES = "D:/ShapesPruebasSegmentacionUrbanaCondominios/SECCIONES/Mapas/TB_MARCOS_SECCIONES.shp"

    SEGM_ESP_SECCIONES = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_ESP_SECCION"
    SEGM_ESP_AEUS = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_ESP_AEU"
    SEGM_ESP_AEUS_LINEAS = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_ESP_AEU_LINEA"
    SEGM_ESP_RUTAS = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_ESP_RUTA"
    SEGM_ESP_RUTAS_LINEAS = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_ESP_RUTA_LINEA"
    SEGM_ESP_VIVIENDAS_U = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_ESP_VIVIENDA_U"
    SEGM_ESP_MARCO_AEU = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_ESP_MARCO_AEU"
    SEGM_ESP_MARCO_SECCION = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_ESP_MARCO_SECCION"

    where_list = UBIGEO.ExpresionUbigeos(ubigeos)
   # where_list2 = UBIGEO.ExpresionUbigeos(int(ubigeos))
    arcpy.MakeFeatureLayer_management(TB_VIVIENDAS_ORDENADAS, "tb_viviendas_ordenadas", where_list)
    arcpy.MakeFeatureLayer_management(TB_SECCIONES, "tb_secciones", where_list)
    arcpy.MakeFeatureLayer_management(TB_AEUS_LINEAS, "tb_aeus_lineas", where_list)
    arcpy.MakeFeatureLayer_management(TB_RUTAS_LINEAS, "tb_rutas_lineas", where_list)
    #arcpy.MakeFeatureLayer_management(TB_MARCOS_AEUS, "tb_marcos_aeus", where_list)
    #arcpy.MakeFeatureLayer_management(TB_MARCOS_SECCIONES, "tb_marcos_secciones", where_list)
    arcpy.MakeTableView_management(TB_AEUS, "tb_aeus", where_list)
    arcpy.MakeTableView_management(TB_RUTAS, "tb_rutas", where_list)
    arcpy.Append_management("tb_viviendas_ordenadas", SEGM_ESP_VIVIENDAS_U, "NO_TEST")
    arcpy.Append_management("tb_secciones", SEGM_ESP_SECCIONES,"NO_TEST")
    arcpy.Append_management("tb_aeus_lineas", SEGM_ESP_AEUS_LINEAS, "NO_TEST")
    arcpy.Append_management("tb_rutas_lineas", SEGM_ESP_RUTAS_LINEAS, "NO_TEST")
    arcpy.Append_management("tb_aeus", SEGM_ESP_AEUS, "NO_TEST")
    arcpy.Append_management("tb_rutas", SEGM_ESP_RUTAS, "NO_TEST")
    #arcpy.Append_management("tb_marcos_aeus", SEGM_ESP_MARCO_AEU, "NO_TEST")
    #arcpy.Append_management("tb_marcos_secciones", SEGM_ESP_MARCO_SECCION, "NO_TEST")

    list_deletelayer=["tb_viviendas_ordenadas","tb_secciones","tb_aeus_lineas","tb_rutas_lineas",
                      "tb_aeus","tb_rutas","tb_marcos_aeus","tb_marcos_secciones"]

    for el in list_deletelayer:
        arcpy.Delete_management(el)



   #fields4 = [ 'UBIGEO', 'CODCCPP', 'ZONA', 'AEU_FINAL', 'SUM_VIV_AE',
   #            'SECCION', 'LLAVE_SECCION', 'LLAVE_AEU', 'LLAVE_CCPP']


   #row_insert4 = arcpy.da.InsertCursor(
   #        "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_AEUS",
   #        fields4)


   #for row4 in arcpy.da.SearchCursor(TB_AEUS_LINEAS,
   #                                  ['UBIGEO', 'CODCCPP', 'ZONA', 'AEU_FINAL', 'CANT_VIV',
   #            'SECCION', 'LLAVE_SECC', 'LLAVE_AEU', 'LLAVE_CCPP'],where_list):
   #    row_insert4.insertRow(row4)



            #print row

#ubigeos=["090208",
#"150407",
#"021509",
#"030602",
#"050601",
#"080407",
#"090301",
#"150705",
#"050619",
#"150604",
#"022001",
#"050617",
#"080302"]
#ImportarManzanas(ubigeos)

#ubigeos=["020601","021806","110204","240106"]
#conx.ActualizarCantViviendasMzs()
#print "ActualizarCantViviendasMzs"
#print datetime.today()
#ImportarTablasTrabajo(ubigeos)
#print "ImportarTablasTrabajo"
#print datetime.today()
#CrearMatrizAdyacencia(ubigeos)
#print "CrearMatrizAdyacencia"
#print datetime.today()
#conx.InsertarAdyacencia()
#print "InsertarAdyacencia"
#print datetime.today()
#Ruta="D:\ShapesPruebasSegmentacionUrbanaCondominios\AEU\MatrizAdyacencia"
#Lista_adyacencia="lista_adyacencia.dbf"
#ie.Importar_Lista_ADYACENCIA(Ruta,Lista_adyacencia)
##
##
#print "ImportarAdyacencia"
#print datetime.today()
#CrearViviendasOrdenadas()
#print "CrearViviendasOrdenadas"
#print datetime.today()
#EnumerarAEUEnViviendasDeManzanasCantVivMayores16(ubigeos)
#print "EnumerarAEUEnViviendasDeManzanasCantVivMayores16"
#print datetime.today()
#AgruparManzanasCantVivMenoresIguales16(ubigeos)
#print "AgruparManzanasCantVivMenoresIguales16"
#print datetime.today()
#EnumerarAEUEnViviendasDeManzanasCantVivMenoresIguales16(ubigeos)
#print "EnumerarAEUEnViviendasDeManzanasCantVivMenoresIguales16"
#print datetime.today()
#CrearMZS_AEU(ubigeos)
#print "CrearMZS_AEU"
#print datetime.today()
###CrearRutasPuntos(ubigeos)
###print "CrearRutasPuntos"
#
#
#

#CrearRutasPreparacion()
#print "CrearRutasPreparacion"
#print datetime.today()
#PrimeraViviendaPorAEU()
#print "PrimeraViviendaPorAEU"
#print datetime.today()
#SegundaViviendaPorAEU()
#print "SegundaViviendaPorAEU"
#print datetime.today()
#
#RelacionarRutasLineasConAEUSegundaVivienda()
#print "RelacionarRutasLineasConAEUSegundaVivienda"
#print datetime.today()
####
#ActualizarRutasViviendasMenoresIguales16()
#print "ActualizarRutasViviendasMenoresIguales16"
#print datetime.today()
####
#CrearLineasAEUFinal()
#print "CrearLineasAEUFinal"
#print datetime.today()
##
#CrearTablaSegundaPasada()
#print "CrearTablaSegundaPasada"
#print datetime.today()
##
##
#ActualizarRutasAEUSegundaPasada()
#print "ActualizarRutasAEUSegundaPasada"
#print datetime.today()
#
#
#
#
###
####CrearLineasAEUSegundaPasada()
####print "CrearLineasAEUSegundaPasada"
###
###
####ActualizarRutasViviendasMenoresIguales16()
####print "ActualizarRutasViviendasMenoresIguales16"
####print datetime.today()
###
###CrearTablaSegundaPasada()
###print "CrearTablaSegundaPasada"
###print datetime.today()
####ActualizarRutasAEUSegundaPasada()
####print "ActualizarRutasAEUSegundaPasada"
####print datetime.today()
###
#
#


#Renumerar_AEU(ubigeos)
#print "Renumerar_AEU"
#print datetime.today()
#RenumerarRutas()
#print "RenumerarRutas"
#print datetime.today()

#CrearMarcosCroquis(ubigeos)
#print "CrearMarcosCroquis"
#print datetime.today()
#
#CrearTB_AEUS()
#
#print "CrearTB_AEUS"
#print datetime.today()

#ModelarTablas(ubigeos)
#print "ModelarTablas"
#print datetime.today()


#ModelarTablas(ubigeos)

#EliminarRegistros(ubigeos)
#print "EliminarRegistros"
#print datetime.today()
#InsertarRegistros(ubigeos)
#print "InsertarRegistros"
#print datetime.today()
#CodigoFalso()
#ubigeos=["030602",
#"022001",
#"021509",
#"050601"]
#conx.LimpiarRegistrosSegmentacionEspUbigeo(ubigeos)
#InsertarRegistros(ubigeos)




#def PruebaViviendas():
#    arcpy.env.workspace = "Database Connections/PruebaSegmentacion.sde"
#    VIV="Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.dbo.TB_VIVIENDA_U"
#    arcpy.CalculateField_management(VIV, "OR_VIV_AEU", "0")

    #arcpy.AddField_management(MZS, "AEU", "SHORT")

#def PruebaViviendas2():


