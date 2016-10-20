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

import SegmTabSeccion as Seccion
import SegmTabExportarCroquis as Croquis


#def ImportarTablasTrabajo(ubigeos):
#    arcpy.env.overwriteOutput = True
#    MZS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_MZS.shp"
#    VIVIENDAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp"
#    ZONAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
#    #VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
#    PUNTOS_INICIO_shp = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/PuntosInicio/PUNTOS_INICIO.shp"
#    MZS_AEU = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/MZS_AEU"
#
#    EJES_VIALES="D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_EJES_VIALES.shp"
#
#
#    if arcpy.Exists(VIVIENDAS):
#        arcpy.Delete_management(VIVIENDAS)
#    if arcpy.Exists(MZS):
#        arcpy.Delete_management(MZS)
#
#    if arcpy.Exists(ZONAS):
#        arcpy.Delete_management(ZONAS)
#
#    if arcpy.Exists(MZS_AEU):
#        arcpy.Delete_management(MZS_AEU)
#
#    if arcpy.Exists(EJES_VIALES):
#        arcpy.Delete_management(EJES_VIALES)
#
#    if arcpy.Exists(PUNTOS_INICIO_shp):
#        arcpy.Delete_management(PUNTOS_INICIO_shp)
#
#
#    arcpy.env.workspace = "Database Connections/PruebaSegmentacion.sde"
#
#    where_expression=UBIGEO.ExpresionUbigeosImportacion(ubigeos)
#
#    #arcpy.FeatureClassToFeatureClass_conversion("CPV_SEGMENTACION.dbo.TB_MZS",
#    #                                            "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/",
#    #                                            'TB_MZS.shp',where_expression)
#
#    arcpy.Select_analysis("CPV_SEGMENTACION.dbo.VW_MANZANA",
#                          #"D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_MZS.shp"
#                            MZS, where_expression)
#
#
#    arcpy.Select_analysis("CPV_SEGMENTACION.dbo.VW_ZONA_CENSAL",
#                                                ZONAS
#                                                ,where_expression)
#    arcpy.Select_analysis("CPV_SEGMENTACION.sde.VW_VIVIENDAS_U2",
#                                                VIVIENDAS
#                                                ,where_expression)
#
#    arcpy.Select_analysis("CPV_SEGMENTACION.dbo.TB_EJE_VIAL",
#                                                EJES_VIALES
#                                                , where_expression)
#
#    arcpy.Select_analysis("CPV_SEGMENTACION.sde.TB_PTOS_INICIO",
#                          PUNTOS_INICIO_shp
#                          )
#
#    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbanaTabular"
#
#    arcpy.DeleteField_management(MZS, ['AEU','IDMANZANA'])
#
#    arcpy.AddField_management(MZS, "IDMANZANA", "TEXT")
#    expression = "str(!UBIGEO!)+str(!ZONA!)+str(!MANZANA!)"
#    arcpy.CalculateField_management(MZS, "IDMANZANA", expression, "PYTHON_9.3")
#    arcpy.AddField_management(MZS, "AEU", "SHORT")
#    arcpy.AddField_management(MZS, "AEU_2", "SHORT")
#    arcpy.AddField_management(MZS, "FLG_MZ", "SHORT")


#def CrearMatrizAdyacencia(ubigeos):
#    arcpy.env.overwriteOutput = True
#    ADYACENCIA="D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/MatrizAdyacencia/adyacencia.dbf"
#    MZS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_MZS.shp"
#    ZONAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
#
#
#
#    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbanaTabular"
#    arcpy.env.workspace = "Database Connections"
#    if arcpy.Exists("PruebaSegmentacion.sde") == False:
#        arcpy.CreateDatabaseConnection_management("Database Connections",
#                                                  "PruebaSegmentacion.sde",
#                                                  "SQL_SERVER",
#                                                  "192.168.200.250",
#                                                  "DATABASE_AUTH",
#                                                  "sde",
#                                                  "$deDEs4Rr0lLo",
#                                                  "#",
#                                                  "CPV_SEGMENTACION",
#                                                  "#",
#                                                  "#",
#                                                  "#",
#                                                  "#")
#
#
#
#    prueba = "PruebaSegmentacion.sde"
#
#
#    arcpy.env.workspace = r"Database Connections/PruebaSegmentacion.sde"
#
#
#    if arcpy.Exists(r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.ADYACENCIA"):
#        arcpy.Delete_management("Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.adyacencia")
#
#    if arcpy.Exists(r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO"):
#        arcpy.Delete_management("Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO")
#
#
#
#
#    where_list = ubigeos
#
#    inFeatures = MZS
#    fieldName1 = "xCentroid"
#    fieldName2 = "yCentroid"
#    fieldPrecision = 18
#    fieldScale = 6
#    fieldScale2 = 2
#    #### Add fields
#
#    lst = arcpy.ListFields(MZS)
#    for f in lst:
#        if (f.name==fieldName1):
#            arcpy.DeleteField_management(inFeatures,["xCentroid"])
#        if (f.name==fieldName2):
#            arcpy.DeleteField_management(inFeatures,["yCentroid"])
#        if (f.name == "AREA"):
#            arcpy.DeleteField_management(inFeatures, ["AREA"])
#
#
#    arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE",
#                                      fieldPrecision, fieldScale)
#    arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE",
#                                  fieldPrecision, fieldScale)
#
#    arcpy.AddField_management(inFeatures, "AREA", "DOUBLE", fieldPrecision, fieldScale2)
#
#
#
#
#    # Calculate centroid
#
#    fields = ["SHAPE@X", "SHAPE@Y", "xCentroid", "yCentroid"]
#
#    with arcpy.da.UpdateCursor(inFeatures, fields) as cursorx:
#        for row0 in cursorx:
#            row0[2] = row0[0]
#            row0[3] = row0[1]
#            cursorx.updateRow(row0)
#
#    exp = "!SHAPE.AREA@METERS!"
#    arcpy.CalculateField_management(inFeatures, "AREA", exp, "PYTHON_9.3")
#
#
#
#    if arcpy.Exists(ADYACENCIA) == True:
#        arcpy.Delete_management(ADYACENCIA)
#
#    arcpy.CreateTable_management("D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/MatrizAdyacencia/", "adyacencia.dbf")
#
#    fieldName1 = "FirstX"
#    fieldName2 = "FirstY"
#
#    fieldName3 = "LastX"
#    fieldName4 = "LastY"
#
#    fieldPrecision = 18
#    fieldScale = 6
#
#    inFeatures = ADYACENCIA
#
#    # Add fields inicio
#
#
#
#    arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE",
#                              fieldPrecision, fieldScale)
#    arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE",
#                              fieldPrecision, fieldScale)
#    # Add fields inicio
#    arcpy.AddField_management(inFeatures, fieldName3, "DOUBLE",
#                              fieldPrecision, fieldScale)
#    arcpy.AddField_management(inFeatures, fieldName4, "DOUBLE",
#                              fieldPrecision, fieldScale)
#
#
#
#
#
#
#
#
#
#
#    where_expression=UBIGEO.ExpresionUbigeos(ubigeos)
#
#    for row in arcpy.da.SearchCursor(ZONAS, ["UBIGEO", "ZONA"],where_expression):
#        where_expression2=' "UBIGEO"=\'%s\' AND "ZONA"=\'%s\' ' % (row[0], row[1])
#        print where_expression2
#        desc=str(row[0])+str(row[1])
#        arcpy.MakeFeatureLayer_management(MZS, "manzanas",where_expression2)
#        arcpy.FeatureToPoint_management("manzanas",
#                                        "in_memory/Point" +desc ,
#                                        "CENTROID")
#
#        arcpy.AddField_management("in_memory/Point" +desc , 'Z', "SHORT")
#        arcpy.CalculateField_management("in_memory/Point" +desc , 'Z', 1)
#
#
#        arcpy.CreateThiessenPolygons_analysis("in_memory/Point" + desc,
#                                              "in_memory/VoronoiPolygon" + desc,
#                                              "ALL")
#
#
#
#
#        arcpy.FeatureTo3DByAttribute_3d("in_memory/Point" +desc, "in_memory/Points3D" + desc, 'Z')
#
#        Tin = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/MatrizAdyacencia/Tin/Shape" + str(row[0]) + "" + str(row[1])
#
#        arcpy.CreateTin_3d(Tin, "", "in_memory/Points3D"+desc, "DELAUNAY")
#
#        arcpy.TinEdge_3d(Tin, "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/MatrizAdyacencia/Edge/" + desc+".shp", edge_type='DATA')
#
#
#        inFeatures = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/MatrizAdyacencia/Edge/" + desc+".shp"
#        Edge="D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/MatrizAdyacencia/Edge/" + desc+".shp"
#
#        fieldName1 = "FirstX_1"
#        fieldName2 = "FirstY_1"
#
#        fieldName3 = "LastX_1"
#        fieldName4 = "LastY_1"
#
#        fieldPrecision = 18
#        fieldScale = 6
#
#        # Add fields inicio
#        arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE",
#                                  fieldPrecision, fieldScale)
#        arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE",
#                                  fieldPrecision, fieldScale)
#
#        # Add fields fin
#        arcpy.AddField_management(inFeatures, fieldName3, "DOUBLE",
#                                  fieldPrecision, fieldScale)
#        arcpy.AddField_management(inFeatures, fieldName4, "DOUBLE",
#                                  fieldPrecision, fieldScale)
#
#        # Calculate Points Firts
#        arcpy.CalculateField_management(inFeatures, fieldName1,
#                                        "!SHAPE.firstPoint.X!",
#                                        "PYTHON_9.3")
#        arcpy.CalculateField_management(inFeatures, fieldName2,
#                                        "!SHAPE.firstPoint.Y!",
#                                        "PYTHON_9.3")
#
#        # Calculate Points Last
#        arcpy.CalculateField_management(inFeatures, fieldName3,
#                                        "!SHAPE.lastPoint.X!",
#                                        "PYTHON_9.3")
#        arcpy.CalculateField_management(inFeatures, fieldName4,
#                                        "!SHAPE.lastPoint.Y!",
#                                        "PYTHON_9.3")
#
#
#
#    # pologonos de vonoi a polyline ignorando lados vecinos
#        arcpy.PolygonToLine_management("in_memory/VoronoiPolygon"+desc,
#                                   "in_memory/VoronoiLine" + desc,
#                                   "IGNORE_NEIGHBORS")
#
#    # polyline  a split lines
#
#        arcpy.SplitLine_management("in_memory/VoronoiLine" + desc,
#                               "in_memory/VoronoiSplitLine" + desc)
#
#        fieldName1 = "FirstX_2"
#        fieldName2 = "FirstY_2"
#        fieldName3 = "LastX_2"
#        fieldName4 = "LastY_2"
#
#        fieldPrecision = 18
#        fieldScale = 6
#
#
#
##        desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2]) + ".shp"
#        inFeatures = "in_memory/VoronoiSplitLine" + desc
#
#        # Add fields inicio
#        arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE",
#                                  fieldPrecision, fieldScale)
#        arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE",
#                                  fieldPrecision, fieldScale)
#
#        # Add fields fin
#        arcpy.AddField_management(inFeatures, fieldName3, "DOUBLE",
#                                  fieldPrecision, fieldScale)
#        arcpy.AddField_management(inFeatures, fieldName4, "DOUBLE",
#                                  fieldPrecision, fieldScale)
#
#        # Calculate Points Firts
#        arcpy.CalculateField_management(inFeatures, fieldName1,
#                                        "!SHAPE.firstPoint.X!",
#                                        "PYTHON_9.3")
#        arcpy.CalculateField_management(inFeatures, fieldName2,
#                                        "!SHAPE.firstPoint.Y!",
#                                        "PYTHON_9.3")
#
#        # Calculate Points Last
#        arcpy.CalculateField_management(inFeatures, fieldName3,
#                                        "!SHAPE.lastPoint.X!",
#                                        "PYTHON_9.3")
#        arcpy.CalculateField_management(inFeatures, fieldName4,
#                                        "!SHAPE.lastPoint.Y!",
#                                        "PYTHON_9.3")
#
#        # Eliminando los registros identicos
#        arcpy.DeleteIdentical_management("in_memory/VoronoiSplitLine" + desc, ["Shape"])
#
#        arcpy.Intersect_analysis(["in_memory/VoronoiSplitLine" + desc,
#                                  Edge],
#                                 "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/MatrizAdyacencia/Intersections/" + desc, "ALL", "", "point")
#
#
#        fc1 = Edge
#        fields1 = ['FID']
#        fc2 = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/MatrizAdyacencia/Intersections/" + desc+".shp"
#        fields2 = ['FID_'+str(row[0])]
#
#
#
#        with arcpy.arcpy.da.SearchCursor(fc1, fields1) as cursor1:
#            for row1 in cursor1:
#
#                with arcpy.arcpy.da.UpdateCursor(fc2, fields2) as cursor2:
#                    contador = 0
#                    for row2 in cursor2:
#                        if row1[0] == row2[0]:
#                            contador = contador + 1
#
#                        if contador > 3:
#                            cursor2.deleteRow()
#                            contador = contador - 1
#
#        del cursor1
#
#
#        fc = fc2
#        fields = ['FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1', 'FirstX_2', 'FirstY_2', 'LastX_2', 'LastY_2']
#    # a=np.array([2, 4, 6, 8])
#    # b = np.array([2, 4, 6, 8])
#
#        j = 0
#
#
#        with arcpy.da.UpdateCursor(fc, fields) as cursor:
#            for row in cursor:
#                a1 = row[0] - row[2]  # ax
#                a2 = row[1] - row[3]  # ay  a=(a1,a2)
#                b1 = row[4] - row[6]  # bx
#                b2 = row[5] - row[7]  # bx b =(b1,b2)
#
#                a = np.array([a1, a2])
#                b = np.array([b1, b2])
#
#                producto_escalar = np.dot(a, b)  # a.b=a1*b1 + a2*b2
#                coseno = abs(producto_escalar) / (np.linalg.norm(a) * np.linalg.norm(b))
#
#                # print  str(row[8])+":"+str(coseno)
#
#
#
#                if coseno >= 0.005:
#                    cursor.deleteRow()
#
#                j = j + 1
#
#            del cursor
#
#
#        input_table = fc2
#        out_lines ="D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/MatrizAdyacencia/ShapesFinal/" + desc+".shp"
#
#
#            # XY To Line
#        arcpy.XYToLine_management(input_table, out_lines,'FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1', "GEODESIC")
#
#        arcpy.DeleteIdentical_management(out_lines, ["Shape"])
#
#        adyacencias_x = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/MatrizAdyacencia/ShapesFinal/" + desc+".shp"
#        #adyacencias_x = "in_memory/ShapesFinal" + desc
#
#        manzanas = "manzanas"
#
#        EliminarAdyacencias.PorCantidadManzanasCruza(manzanas, adyacencias_x)
#
#        cursorInsertar = arcpy.da.InsertCursor(ADYACENCIA,
#                                   ['FirstX', 'FirstY', 'LastX', 'LastY'])
#        for row in arcpy.da.SearchCursor(adyacencias_x,
#                                     ['FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1']):
#        # print row
#            cursorInsertar.insertRow(row)
#        del cursorInsertar
#
#
#
#    arcpy.TableToTable_conversion(ADYACENCIA,
#                                  'Database Connections/PruebaSegmentacion.sde/', 'adyacencia')
#    MZS_TRABAJO = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_MZS_TRABAJO.shp"
#
#    arcpy.CopyFeatures_management(MZS,MZS_TRABAJO)
#
#    arcpy.FeatureClassToGeodatabase_conversion([MZS_TRABAJO],
#                                               'Database Connections/PruebaSegmentacion.sde/')



def CopiarTablas():
    env.overwriteOutput = True
    lista=[["D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp","D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_MZS.shp"],
           ["D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp","D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp"],
           ["D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp","D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"],
           ["D:/ShapesPruebasSegmentacionUrbana/AEU/PuntosInicio/PUNTOS_INICIO.shp","D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/PuntosInicio/PUNTOS_INICIO.shp"]
          ]


    for el in lista:
        arcpy.Copy_management(el[0],el[1])


def OrdenarManzanasFalsoCod():
    MZS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    MZS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_MZS_ORDENADAS.shp"
    if arcpy.Exists(MZS_ORDENADAS):
        arcpy.Delete_management(MZS_ORDENADAS)
    arcpy.Sort_management(MZS, MZS_ORDENADAS, ["UBIGEO", "ZONA", "FALSO_COD" ])


def CrearViviendasOrdenadas():
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbanaTabular"
    VIVIENDAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"

    if arcpy.Exists(VIVIENDAS_ORDENADAS):
        arcpy.Delete_management(VIVIENDAS_ORDENADAS)

    arcpy.Sort_management(VIVIENDAS, VIVIENDAS_ORDENADAS, ["UBIGEO", "ZONA", "FALSO_COD", "ID_REG_OR"])
    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "AEU", "SHORT")
    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "OR_VIV_AEU", "SHORT")
    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "FLG_CORTE", "SHORT")
    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "FLG_MZ", "SHORT")


def EnumerarAEUEnViviendasDeManzanas(ubigeos):
    arcpy.env.overwriteOutput = True
    MZS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_MZS_ORDENADAS.shp"
    VIVIENDAS="D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    ZONAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    VIVIENDAS_AEU_OR_MAX="in_memory//VIVIENDAS_AEU_OR_MAX"
    VIVIENDAS_MZS_OR_MAX = "in_memory//VIVIENDAS_MZS_OR_MAX"

#    if arcpy.Exists(VIVIENDAS_AEU_OR_MAX):
#        arcpy.Delete_management(VIVIENDAS_AEU_OR_MAX)
#
#    if arcpy.Exists(VIVIENDAS_MZS_OR_MAX):
#        arcpy.Delete_management(VIVIENDAS_MZS_OR_MAX)



    where_list=ubigeos
    m = 0
    where_expression = ""
    arcpy.AddField_management(MZS_ORDENADAS, "AEU", "SHORT")
    where_expression=UBIGEO.ExpresionUbigeos(ubigeos)
    for row in arcpy.da.SearchCursor(ZONAS,["UBIGEO", "ZONA"],where_expression):

        where_expression1 = "UBIGEO=\'" + str(row[0]) + "\' AND ZONA=\'" + str(row[1]) + "\' "
        #where_expression1 = "UBIGEO=\'" + str(row[0]) + "\' AND ZONA=\'" + str(row[1])+"\'  AND VIV_MZ>16 "

        numero_aeu = 1


        cant_vivi_agrupadas=0
        anterior_manzana=0
        cant_viv_anterior_manzana=0
        or_viv_aeu=1


        with arcpy.da.UpdateCursor(MZS_ORDENADAS,["UBIGEO", "ZONA", "MANZANA", "IDMANZANA", "VIV_MZ","AEU" ],where_expression1) as cursor1:
            for row1 in cursor1:
                cant_viv=int(row1[4])

                if (cant_viv>16):


                    division=float(cant_viv)/16.0
                    cant_aeus=math.ceil(division)
                    residuo=cant_viv%cant_aeus
                    viv_aeu=cant_viv/cant_aeus
                    i=0
                    or_viv_aeu=1
                    where_expression_viv = " UBIGEO=\'" + str(row1[0]) + "\'  AND  ZONA=\'" + str(row1[1]) + "\' AND MANZANA=\'" + str(row1[2])+"\'"
                    edificacion_anterior=0
                    numero_aeu_anterior=0
                    idmanzana_anterior=""

                    #Aqui se hace referencia a la manzana anterior
                    if anterior_manzana==1:  # la anterior manzana es una menor o igual a 16 viviendas
                        if cant_vivi_agrupadas!=0:

                            numero_aeu=numero_aeu+1
                        else:
                            print cant_vivi_agrupadas

                    cant_vivi_agrupadas = 0
                    anterior_manzana = 2  ##si la manzana es con mas de 16 viv entonces 2


                    with arcpy.da.UpdateCursor (VIVIENDAS_ORDENADAS, ["UBIGEO","ZONA","MANZANA","ID_REG_OR","AEU", "OR_VIV_AEU","EDIFICACIO","USOLOCAL","COND_USOLO","FLG_CORTE","FLG_MZ"],where_expression_viv ) as cursor2:
                        for row2 in cursor2:
                            row2[10] = 1
                            idmanzana=str(row2[0])+str(row2[1])+str(row2[2])
                            usolocal=int(row2[7])
                            usolocal_cond=int(row2[8])

                            edificacion=int(row2[6])

                            if (usolocal in [1,3]): #or (usolocal==6 and (usolocal_cond in [1,3])):
                                row2[4] = numero_aeu
                                row2[5]=or_viv_aeu
                                or_viv_aeu=or_viv_aeu+1

                            else:
                                if or_viv_aeu != 1:
                                    row2[4] = numero_aeu
                                else:
                                    if idmanzana == idmanzana_anterior:
                                        row2[4] = numero_aeu_anterior


                                    else:
                                        if edificacion==0:
                                            row2[4] = numero_aeu
                                        else:
                                            if edificacion==edificacion_anterior:
                                                    row2[4]=numero_aeu_anterior
                                            else:
                                                    row2[4] = numero_aeu


                            if residuo > 0:
                                if or_viv_aeu > (viv_aeu + 1):
                                    i = 1
                                    edificacion_anterior=edificacion
                                    numero_aeu_anterior=numero_aeu
                                    idmanzana_anterior=idmanzana
                                    numero_aeu = numero_aeu + 1
                                    residuo = residuo - 1
                                    or_viv_aeu=1

                            else:
                                if or_viv_aeu > (viv_aeu):
                                    edificacion_anterior=edificacion
                                    numero_aeu_anterior=numero_aeu
                                    numero_aeu = numero_aeu + 1
                                    idmanzana_anterior = idmanzana
                                    or_viv_aeu = 1

                            cursor2.updateRow(row2)
                        del cursor2


                else:

                    cant_vivi_agrupadas = cant_vivi_agrupadas + cant_viv


                    if (anterior_manzana==2 or anterior_manzana==0):  # si la manzana anterior es una manzana que tiene mas de 16 viviendas

                        cant_vivi_agrupadas = cant_viv    # cantidad  de viviendas del grupo regrewsa a 0 y se almacena la cantidad de viviendas
                        or_viv_aeu = 1
                        #if anterior_manzana==2:
                            #numero_aeu = numero_aeu + 1
                    else:
                        if cant_vivi_agrupadas<=16:
                            numero_aeu=numero_aeu

                            #or_viv_aeu

                        else:
                            cant_vivi_agrupadas=cant_viv
                            numero_aeu = numero_aeu+1
                            or_viv_aeu = 1

                    anterior_manzana = 1  ##si la manzana es menor igual a 16 viv entonces 1
                    where_expression_viv = " UBIGEO=\'" + str(row1[0]) + "\'  AND  ZONA=\'" + str(
                        row1[1]) + "\' AND MANZANA=\'" + str(row1[2]) + "\'"




                    with arcpy.da.UpdateCursor (VIVIENDAS_ORDENADAS, ["UBIGEO","ZONA","MANZANA","ID_REG_OR","AEU", "OR_VIV_AEU","EDIFICACIO","USOLOCAL","COND_USOLO","FLG_CORTE","FLG_MZ"],where_expression_viv ) as cursor2:
                        for row2 in cursor2:
                            row2[10] = 0
                            usolocal = int(row2[7])
                            usolocal_cond = int(row2[8])
                            row2[4] = numero_aeu
                            edificacion = int(row2[6])

                            if (usolocal in [1, 3]):  # or (usolocal==6 and (usolocal_cond in [1,3])):
                                row2[5] = or_viv_aeu
                                or_viv_aeu = or_viv_aeu + 1

                            cursor2.updateRow(row2)

                    del cursor2


                row1[5]=int(numero_aeu)

                cursor1.updateRow(row1)


    where_expression_l = "FLG_MZ=1"

    arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS, "viviendas_ordenadas", where_expression_l)

    arcpy.Statistics_analysis("viviendas_ordenadas", VIVIENDAS_AEU_OR_MAX, [["ID_REG_OR", "MAX"]],
                              ["UBIGEO", "ZONA", "MANZANA","AEU"])

    arcpy.Statistics_analysis("viviendas_ordenadas", VIVIENDAS_MZS_OR_MAX, [["ID_REG_OR", "MAX"]],
                              ["UBIGEO", "ZONA", "MANZANA"])

    #where_expressionx="FLG_MZ=1"

    # se obtiene los cortes de los puntos

    idmanzana_anteriorx=""
    i=0


    for row in arcpy.da.SearchCursor(VIVIENDAS_AEU_OR_MAX, ["UBIGEO", "ZONA","MANZANA","MAX_ID_REG_OR"]):
        where_expressionxx = " UBIGEO=\'" + str(row[0]) + "\'  AND  ZONA=\'" + str(row[1]) + "\' AND MANZANA=\'" + str(row[2])+"\' AND ID_REG_OR="+str(row[3])
        with arcpy.arcpy.da.UpdateCursor(VIVIENDAS_ORDENADAS, ["FLG_CORTE"],where_expressionxx ) as cursor2:
            for row2 in cursor2:
                row2[0]=1
                cursor2.updateRow(row2)
        del cursor2

    for row in arcpy.da.SearchCursor(VIVIENDAS_MZS_OR_MAX, ["UBIGEO", "ZONA","MANZANA","MAX_ID_REG_OR"]):
        where_expressionxx = " UBIGEO=\'" + str(row[0]) + "\'  AND  ZONA=\'" + str(row[1]) + "\' AND MANZANA=\'" + str(row[2])+"\' AND ID_REG_OR="+str(row[3])
        with arcpy.arcpy.da.UpdateCursor(VIVIENDAS_ORDENADAS, ["FLG_CORTE"],where_expressionxx ) as cursor2:
            for row2 in cursor2:
                row2[0]=0
                cursor2.updateRow(row2)
        del cursor2


def CrearMZS_AEU(ubigeos):
    arcpy.env.overwriteOutput = True
    MZS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_MZS_ORDENADAS.shp"
    MZS_AEU_1 = "in_memory//MZS_AEU_1"
    MZS_AEU_2 = "in_memory//MZS_AEU_2"
    MZS_AEU = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"
    MZS_MENORES_16="in_memory//MZS_MENORES_16"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    if arcpy.Exists(MZS_AEU):
        arcpy.Delete_management(MZS_AEU)

    where_expresion= UBIGEO.ExpresionUbigeos(ubigeos)
    where = " FLG_MZ=1 "
    arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS, "viviendas_ordenadas_3","("+where_expresion+") AND" + where)

    arcpy.Statistics_analysis("viviendas_ordenadas_3", MZS_AEU_1, [["OR_VIV_AEU", "MAX"]],
                              ["UBIGEO","CODCCPP" ,"ZONA","MANZANA","AEU","FALSO_COD"])



    arcpy.AddField_management(MZS_AEU_1, "CANT_VIV", "SHORT")
    expression="!MAX_OR_VIV_AEU!"

    arcpy.CalculateField_management(MZS_AEU_1, "CANT_VIV", expression, "PYTHON_9.3")




    arcpy.DeleteField_management(MZS_AEU_1, ['FREQUENCY','MAX_OR_VIV_AEU'])



    ####creacion de  la vista de manzanas menores a 16

    where2 = " VIV_MZ<=16 "
    arcpy.MakeFeatureLayer_management(MZS, "mzs_menores_16", "("+where_expresion +") AND " +where2)

    arcpy.Statistics_analysis("mzs_menores_16", MZS_MENORES_16, [["MANZANA", "COUNT"]],
                              ["UBIGEO", "CODCCPP","ZONA", "MANZANA", "AEU","FALSO_COD","VIV_MZ"])
    arcpy.AddField_management(MZS_MENORES_16, "CANT_VIV", "SHORT")
    expression = "!VIV_MZ!"
    arcpy.CalculateField_management(MZS_MENORES_16, "CANT_VIV", expression, "PYTHON_9.3")
    arcpy.DeleteField_management(MZS_MENORES_16, ['FID_','FREQUENCY','COUNT_MANZANA','VIV_MZ'])
    arcpy.Merge_management([MZS_AEU_1, MZS_MENORES_16],MZS_AEU_2 )
    arcpy.Sort_management(MZS_AEU_2, MZS_AEU, ["UBIGEO","CODCCPP","ZONA","FALSO_COD","AEU"])

def PrimeraViviendaPorAEU():
    TB_VIVIENDAS_ORDENADAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\EnumerarAEUViviendas\\TB_VIVIENDAS_ORDENADAS.shp"
    TB_VIVIENDAS_SELECT2_SORT_La = "TB_VIVIENDAS_SELECT1_SORT_La"
    TB_VIVIENDAS_ESCOGIDAS__4_ = "in_memory\\TB_VIVIENDAS_PRIMERAS_ESCOGIDAS"
    TB_VIVIENDAS_SELECT2_SORT = "in_memory\\TB_VIVIENDAS_SELECT1_SORT"
    TB_VIVIENDAS_SEGUNDA_VIVIENDA__3_ = "in_memory\\TB_VIVIENDAS_PRIMERAS_ESCOGIDAS"
    TB_VIVIENDAS_ESCOGIDAS__3_ = "in_memory\\TB_VIVIENDAS_PRIMERAS_ESCOGIDAS"
    TB_VIVIENDAS_SEGUNDA_VIVIENDA__4_ = "in_memory\\TB_VIVIENDAS_PRIMERAS_ESCOGIDAS"
    TB_VIVIENDAS_SEGUNDAS_ESCOGIDAS = "in_memory\\TB_VIVIENDAS_PRIMERAS_ESCOGIDAS"
    TB_VIVIENDAS_SELECT2__2_ = "in_memory\\TB_VIVIENDAS"
    TB_VIVIENDAS = "in_memory\\TB_VIVIENDAS"
    TB_VIVIENDAS_SELECT2_SORT_La__2_ = "TB_VIVIENDAS_SELECT1_SORT_La"
    TB_PRIMERA_VIVIENDA_AEU_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_PRIMERA_VIVIENDA_AEU.shp"


    if arcpy.Exists(TB_PRIMERA_VIVIENDA_AEU_shp):
        arcpy.Delete_management(TB_PRIMERA_VIVIENDA_AEU_shp)



    where="(\"USOLOCAL\"=1 OR \"USOLOCAL\"=3 ) AND FLG_MZ=1"
    # Process: Select (2)
    arcpy.Select_analysis(TB_VIVIENDAS_ORDENADAS_shp, TB_VIVIENDAS,
                          where)

    # Process: Delete Identical
    arcpy.DeleteIdentical_management(TB_VIVIENDAS, "Shape", "", "0")

    # Process: Sort
    arcpy.Sort_management(TB_VIVIENDAS_SELECT2__2_, TB_VIVIENDAS_SELECT2_SORT,
                          "UBIGEO ASCENDING;ZONA ASCENDING;AEU ASCENDING;ID_REG_OR ASCENDING", "UR")

    # Process: Make Feature Layer
    arcpy.MakeFeatureLayer_management(TB_VIVIENDAS_SELECT2_SORT, TB_VIVIENDAS_SELECT2_SORT_La, "", "",
                                      "FID FID VISIBLE NONE;Shape Shape VISIBLE NONE;ID ID VISIBLE NONE;UBIGEO UBIGEO VISIBLE NONE;CODCCPP CODCCPP VISIBLE NONE;ZONA ZONA VISIBLE NONE;MANZANA MANZANA VISIBLE NONE;NOMCCPP NOMCCPP VISIBLE NONE;DEPARTAMEN DEPARTAMEN VISIBLE NONE;PROVINCIA PROVINCIA VISIBLE NONE;DISTRITO DISTRITO VISIBLE NONE;AREA AREA VISIBLE NONE;FRENTE_ORD FRENTE_ORD VISIBLE NONE;ID_REG_OR ID_REG_OR VISIBLE NONE;EDIFICACIO EDIFICACIO VISIBLE NONE;USOLOCAL USOLOCAL VISIBLE NONE;COND_USOLO COND_USOLO VISIBLE NONE;AEU AEU VISIBLE NONE;OR_VIV_AEU OR_VIV_AEU VISIBLE NONE;FLG_CORTE FLG_CORTE VISIBLE NONE;FLG_MZ FLG_MZ VISIBLE NONE;FEAT_SEQ FEAT_SEQ VISIBLE NONE")

    # Process: Summary Statistics
    arcpy.Statistics_analysis(TB_VIVIENDAS_SELECT2_SORT, TB_VIVIENDAS_SEGUNDAS_ESCOGIDAS, "FID FIRST",
                              "UBIGEO;CODCCPP;ZONA;AEU")

    # Process: Add Field (3)
    arcpy.AddField_management(TB_VIVIENDAS_SEGUNDAS_ESCOGIDAS, "ID_SEG", "SHORT", "", "", "", "", "NULLABLE",
                              "NON_REQUIRED", "")

    # Process: Calculate Field (2)
    arcpy.CalculateField_management(TB_VIVIENDAS_SEGUNDA_VIVIENDA__4_, "ID_SEG", "[FIRST_FID]", "VB", "")

    # Process: Add Field (4)
    arcpy.AddField_management(TB_VIVIENDAS_ESCOGIDAS__3_, "flg_escogido", "SHORT", "", "", "", "", "NULLABLE",
                              "NON_REQUIRED", "")

    # Process: Calculate Field (5)
    arcpy.CalculateField_management(TB_VIVIENDAS_SEGUNDA_VIVIENDA__3_, "FLG_ESCOGIDO", "1", "VB", "")

    # Process: Add Join (2)
    arcpy.AddJoin_management(TB_VIVIENDAS_SELECT2_SORT_La, "FID", TB_VIVIENDAS_ESCOGIDAS__4_, "ID_SEG", "KEEP_ALL")

    # Process: Select (3)
    arcpy.Select_analysis(TB_VIVIENDAS_SELECT2_SORT_La__2_, TB_PRIMERA_VIVIENDA_AEU_shp, "\"flg_escogido\"=1")

    # Process: Add Field
    arcpy.AddField_management(TB_PRIMERA_VIVIENDA_AEU_shp, "UBIGEO", "TEXT")
    arcpy.AddField_management(TB_PRIMERA_VIVIENDA_AEU_shp, "CODCCPP", "TEXT")
    arcpy.AddField_management(TB_PRIMERA_VIVIENDA_AEU_shp, "ZONA", "TEXT")
    arcpy.AddField_management(TB_PRIMERA_VIVIENDA_AEU_shp, "MANZANA", "TEXT")
    arcpy.AddField_management(TB_PRIMERA_VIVIENDA_AEU_shp, "AEU", "SHORT")


    # Process: Calculate Field
    arcpy.CalculateField_management(TB_PRIMERA_VIVIENDA_AEU_shp, "UBIGEO",
                                    "[TB_VIVIE_1]", "VB", "")
    arcpy.CalculateField_management(TB_PRIMERA_VIVIENDA_AEU_shp, "CODCCPP",
                                    "[TB_VIVIE_2]", "VB", "")

    arcpy.CalculateField_management(TB_PRIMERA_VIVIENDA_AEU_shp, "ZONA",
                                    "[TB_VIVIE_3]", "VB", "")
    arcpy.CalculateField_management(TB_PRIMERA_VIVIENDA_AEU_shp, "MANZANA",
                                    "[TB_VIVIE_4]", "VB", "")
    arcpy.CalculateField_management(TB_PRIMERA_VIVIENDA_AEU_shp, "AEU",
                                    "[TB_VIVI_25]", "VB", "")


    field_delete=""


    for i in range(1,10):
        field_delete=";TB_VIVIE_"+str(i)+field_delete
    for j in range(10, 30):
        field_delete = ";TB_VIVI_" + str(j) + field_delete
    arcpy.DeleteField_management(TB_PRIMERA_VIVIENDA_AEU_shp,"TB_VIVIEND"+field_delete)

def SegundaViviendaPorAEU():
    TB_VIVIENDAS_ORDENADAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\EnumerarAEUViviendas\\TB_VIVIENDAS_ORDENADAS.shp"
    TB_VIVIENDAS_SELECT2_SORT_La = "TB_VIVIENDAS_SELECT2_SORT_La"
    TB_VIVIENDAS_ESCOGIDAS__4_ = "in_memory\\TB_VIVIENDAS_SEGUNDAS_ESCOGIDAS"
    TB_VIVIENDAS_SELECT2_SORT = "in_memory\\TB_VIVIENDAS_SELECT2_SORT"
    TB_VIVIENDAS_SEGUNDA_VIVIENDA__3_ = "in_memory\\TB_VIVIENDAS_SEGUNDAS_ESCOGIDAS"
    TB_VIVIENDAS_ESCOGIDAS__3_ = "in_memory\\TB_VIVIENDAS_SEGUNDAS_ESCOGIDAS"
    TB_VIVIENDAS_SEGUNDA_VIVIENDA__4_ = "in_memory\\TB_VIVIENDAS_SEGUNDAS_ESCOGIDAS"
    TB_VIVIENDAS_SEGUNDAS_ESCOGIDAS = "in_memory\\TB_VIVIENDAS_SEGUNDAS_ESCOGIDAS"
    TB_VIVIENDAS_SELECT2__2_ = "in_memory\\TB_VIVIENDASXXXXX"
    TB_VIVIENDASXXXXX = "in_memory\\TB_VIVIENDASXXXXX"
    TB_VIVIENDAS_SELECT2_SORT_La__2_ = "TB_VIVIENDAS_SELECT2_SORT_La"
    TB_SEGUNDA_VIVIENDA_AEU_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_SEGUNDA_VIVIENDA_AEU.shp"


    if arcpy.Exists(TB_SEGUNDA_VIVIENDA_AEU_shp):
        arcpy.Delete_management(TB_SEGUNDA_VIVIENDA_AEU_shp)

    # Process: Select (2)
    #where="(\"USOLOCAL\"=1 OR \"USOLOCAL\"=3 OR (\"USOLOCAL\"=6 AND (\"COND_USOLO\"=1 OR \"COND_USOLO\"=3 ))) AND FLG_MZ=1"
    where="(\"USOLOCAL\"=1 OR \"USOLOCAL\"=3 ) AND FLG_MZ=1"
    arcpy.Select_analysis(TB_VIVIENDAS_ORDENADAS_shp, TB_VIVIENDASXXXXX,
                          where)

    # Process: Delete Identical
    arcpy.DeleteIdentical_management(TB_VIVIENDASXXXXX, "Shape", "", "0")

    # Process: Sort
    arcpy.Sort_management(TB_VIVIENDAS_SELECT2__2_, TB_VIVIENDAS_SELECT2_SORT,
                          "UBIGEO ASCENDING;ZONA ASCENDING;AEU ASCENDING;ID_REG_OR ASCENDING", "UR")

    # Process: Make Feature Layer
    arcpy.MakeFeatureLayer_management(TB_VIVIENDAS_SELECT2_SORT, TB_VIVIENDAS_SELECT2_SORT_La, "", "",
                                      "FID FID VISIBLE NONE;Shape Shape VISIBLE NONE;ID ID VISIBLE NONE;UBIGEO UBIGEO VISIBLE NONE;CODCCPP CODCCPP VISIBLE NONE;ZONA ZONA VISIBLE NONE;MANZANA MANZANA VISIBLE NONE;NOMCCPP NOMCCPP VISIBLE NONE;DEPARTAMEN DEPARTAMEN VISIBLE NONE;PROVINCIA PROVINCIA VISIBLE NONE;DISTRITO DISTRITO VISIBLE NONE;AREA AREA VISIBLE NONE;FRENTE_ORD FRENTE_ORD VISIBLE NONE;ID_REG_OR ID_REG_OR VISIBLE NONE;EDIFICACIO EDIFICACIO VISIBLE NONE;USOLOCAL USOLOCAL VISIBLE NONE;COND_USOLO COND_USOLO VISIBLE NONE;AEU AEU VISIBLE NONE;OR_VIV_AEU OR_VIV_AEU VISIBLE NONE;FLG_CORTE FLG_CORTE VISIBLE NONE;FLG_MZ FLG_MZ VISIBLE NONE;FEAT_SEQ FEAT_SEQ VISIBLE NONE")

    # Process: Summary Statistics
    arcpy.Statistics_analysis(TB_VIVIENDAS_SELECT2_SORT, TB_VIVIENDAS_SEGUNDAS_ESCOGIDAS, "FID FIRST",
                              "UBIGEO;CODCCPP;ZONA;AEU")

    # Process: Add Field (3)
    arcpy.AddField_management(TB_VIVIENDAS_SEGUNDAS_ESCOGIDAS, "ID_SEG", "SHORT", "", "", "", "", "NULLABLE",
                              "NON_REQUIRED", "")

    # Process: Calculate Field (2)
    arcpy.CalculateField_management(TB_VIVIENDAS_SEGUNDA_VIVIENDA__4_, "ID_SEG", "[FIRST_FID] +1", "VB", "")

    # Process: Add Field (4)
    arcpy.AddField_management(TB_VIVIENDAS_ESCOGIDAS__3_, "flg_escogido", "SHORT", "", "", "", "", "NULLABLE",
                              "NON_REQUIRED", "")

    # Process: Calculate Field (5)
    arcpy.CalculateField_management(TB_VIVIENDAS_SEGUNDA_VIVIENDA__3_, "FLG_ESCOGIDO", "1", "VB", "")

    # Process: Add Join (2)
    arcpy.AddJoin_management(TB_VIVIENDAS_SELECT2_SORT_La, "FID", TB_VIVIENDAS_ESCOGIDAS__4_, "ID_SEG", "KEEP_ALL")

    # Process: Select (3)
    arcpy.Select_analysis(TB_VIVIENDAS_SELECT2_SORT_La__2_, TB_SEGUNDA_VIVIENDA_AEU_shp, "\"flg_escogido\"=1")

    # Process: Add Field
    arcpy.AddField_management(TB_SEGUNDA_VIVIENDA_AEU_shp, "UBIGEO", "TEXT")
    arcpy.AddField_management(TB_SEGUNDA_VIVIENDA_AEU_shp, "CODCCPP", "TEXT")
    arcpy.AddField_management(TB_SEGUNDA_VIVIENDA_AEU_shp, "ZONA", "TEXT")
    arcpy.AddField_management(TB_SEGUNDA_VIVIENDA_AEU_shp, "MANZANA", "TEXT")
    arcpy.AddField_management(TB_SEGUNDA_VIVIENDA_AEU_shp, "AEU", "SHORT")


    # Process: Calculate Field
    arcpy.CalculateField_management(TB_SEGUNDA_VIVIENDA_AEU_shp, "UBIGEO",
                                    "[TB_VIVIE_1]", "VB", "")

    arcpy.CalculateField_management(TB_SEGUNDA_VIVIENDA_AEU_shp, "CODCCPP",
                                    "[TB_VIVIE_2]", "VB", "")
    arcpy.CalculateField_management(TB_SEGUNDA_VIVIENDA_AEU_shp, "ZONA",
                                    "[TB_VIVIE_3]", "VB", "")
    arcpy.CalculateField_management(TB_SEGUNDA_VIVIENDA_AEU_shp, "MANZANA",
                                    "[TB_VIVIE_4]", "VB", "")
    arcpy.CalculateField_management(TB_SEGUNDA_VIVIENDA_AEU_shp, "AEU",
                                    "[TB_VIVI_24]", "VB", "")


    field_delete=""

    for i in range(1,10):
        field_delete=";TB_VIVIE_"+str(i)+field_delete
    for j in range(10, 30):
        field_delete = ";TB_VIVI_" + str(j) + field_delete


    #arcpy.DeleteField_management(TB_SEGUNDA_VIVIENDA_AEU_shp,"TB_VIVIEND"+field_delete)

def CrearRutasPreparacion(ubigeos):
    TB_VIVIENDAS_ORDENADAS_shp = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    TB_MZS_shp = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_MZS.shp"

    TB_VIVIENDAS_CORTES_shp = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/CrearRepresentacionAEU/TB_VIVIENDAS_CORTES.shp"
    TB_MZS_LINE_shp = "in_memory/TB_MZS_LINE"
    TB_MZS_TRABAJO_BUFFER_shp = "in_memory/TB_MZS_TRABAJO_BUFFER"
    PUNTOINICIO_BUFFER_shp = "in_memory/PUNTOINICIO_BUFFER"
    TB_MZS_ERASE_shp = "in_memory/TB_MZS_ERASE"
    PUNTOS_INICIO_shp = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/PuntosInicio/PUNTOS_INICIO.shp"
    TB_SPLIT_shp = "in_memory/TB_SPLIT"
    TB_DISSOLVE_shp = "in_memory/TB_DISSOLVE"
    TB_VIVIENDAS_CORTES_Buffer = "in_memory/TB_VIVIENDAS_CORTES_Buffer"
    TB_RUTAS_DISSOLVE_ERASE_shp = "in_memory/TB_RUTAS_DISSOLVE_ERASE"
    TB_RUTAS_PREPARACION_shp = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/CrearRepresentacionAEU/TB_RUTAS_PREPARACION.shp"



    if arcpy.Exists(TB_VIVIENDAS_CORTES_shp):
        arcpy.Delete_management(TB_VIVIENDAS_CORTES_shp)

    if arcpy.Exists(TB_RUTAS_PREPARACION_shp):
        arcpy.Delete_management(TB_RUTAS_PREPARACION_shp)
    # Process: Buffer

    where_expression= UBIGEO.ExpresionUbigeos(ubigeos)



    expression_2 = "flg_manzana(!VIV_MZ!)"
    codeblock = """def flg_manzana(VIV_MZ):\n  if (VIV_MZ>16):\n    return 1\n  else:\n    return 0"""

    arcpy.CalculateField_management(TB_MZS_shp, "FLG_MZ", expression_2, "PYTHON_9.3", codeblock)
    arcpy.CalculateField_management(TB_MZS_shp, "FLG_MZ", expression_2, "PYTHON_9.3", codeblock)

    arcpy.MakeFeatureLayer_management(TB_MZS_shp, 'MZS_layer', where_expression)
    arcpy.Buffer_analysis('MZS_layer', TB_MZS_TRABAJO_BUFFER_shp, "0.3 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")

    where_expression = " FLG_CORTE=1"


    arcpy.Select_analysis(TB_VIVIENDAS_ORDENADAS_shp,
                          TB_VIVIENDAS_CORTES_shp
                          , where_expression)

    arcpy.FeatureToLine_management(TB_MZS_TRABAJO_BUFFER_shp, TB_MZS_LINE_shp, "", "ATTRIBUTES")

    # Process: Merge
    # arcpy.Merge_management("'D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp';'D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp';'D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp'", PUNTOS_INICIO_shp, "IDMANZANA \"IDMANZANA\" true true false 15 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,IDMANZANA,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,IDMANZANA,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,IDMANZANA,-1,-1;OBJECTID \"OBJECTID\" true true false 10 Long 0 10 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,OBJECTID,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,OBJECTID,-1,-1;ORIG_FID \"ORIG_FID\" true true false 10 Long 0 10 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,ORIG_FID,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,ORIG_FID,-1,-1;NEAR_FID \"NEAR_FID\" true true false 10 Long 0 10 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,NEAR_FID,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,NEAR_FID,-1,-1;NEAR_DIST \"NEAR_DIST\" true true false 19 Double 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,NEAR_DIST,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,NEAR_DIST,-1,-1;NEAR_FC \"NEAR_FC\" true true false 254 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,NEAR_FC,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,NEAR_FC,-1,-1;idmax \"idmax\" true true false 254 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,idmax,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,idmax,-1,-1;MIN_NEAR_D \"MIN_NEAR_D\" true true false 19 Double 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,MIN_NEAR_D,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,MIN_NEAR_D,-1,-1;MODIF \"MODIF\" true true false 5 Short 0 5 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,MODIF,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,MODIF,-1,-1;UBIGEO \"UBIGEO\" true true false 6 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,UBIGEO,-1,-1;CODCCPP14 \"CODCCPP14\" true true false 4 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CODCCPP14,-1,-1;MZ_T \"MZ_T\" true true false 4 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,MZ_T,-1,-1;CCDD \"CCDD\" true true false 2 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CCDD,-1,-1;CCPP \"CCPP\" true true false 2 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CCPP,-1,-1;CCDI \"CCDI\" true true false 2 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CCDI,-1,-1;ZONA \"ZONA\" true true false 5 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,ZONA,-1,-1;MANZANA \"MANZANA\" true true false 4 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,MANZANA,-1,-1;CODCCPP \"CODCCPP\" true true false 4 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CODCCPP,-1,-1;NOMCCPP \"NOMCCPP\" true true false 60 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,NOMCCPP,-1,-1;DEPARTAMEN \"DEPARTAMEN\" true true false 50 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,DEPARTAMEN,-1,-1;PROVNCIA \"PROVNCIA\" true true false 50 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,PROVNCIA,-1,-1;DISTRITO \"DISTRITO\" true true false 50 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabular\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,DISTRITO,-1,-1")

    # Process: Buffer (2)
    arcpy.Buffer_analysis(PUNTOS_INICIO_shp, PUNTOINICIO_BUFFER_shp, "0.31 Meters", "FULL", "ROUND", "NONE", "",
                          "PLANAR")

    # Process: Erase
    arcpy.Erase_analysis(TB_MZS_LINE_shp, PUNTOINICIO_BUFFER_shp, TB_MZS_ERASE_shp, "")

    # Process: Split Line At Vertices
    arcpy.SplitLine_management(TB_MZS_ERASE_shp, TB_SPLIT_shp)

    # Process: Dissolve
    arcpy.Dissolve_management(TB_SPLIT_shp, TB_DISSOLVE_shp, "UBIGEO;CODCCPP;ZONA;MANZANA;FLG_MZ", "", "MULTI_PART", "DISSOLVE_LINES")

    # Process: Buffer (3)
    arcpy.Buffer_analysis(TB_VIVIENDAS_CORTES_shp, TB_VIVIENDAS_CORTES_Buffer, "0.6 Meters", "FULL", "ROUND", "NONE",
                          "", "PLANAR")

    # Process: Erase (2)
    arcpy.Erase_analysis(TB_DISSOLVE_shp, TB_VIVIENDAS_CORTES_Buffer, TB_RUTAS_DISSOLVE_ERASE_shp, "")

    # Process: Multipart To Singlepart
    arcpy.MultipartToSinglepart_management(TB_RUTAS_DISSOLVE_ERASE_shp, TB_RUTAS_PREPARACION_shp)

def CrearLineasAEUPrimeraPasada():
    TB_SEGUNDA_VIVIENDA_AEU_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_SEGUNDA_VIVIENDA_AEU.shp"
    TB_RUTAS_PREPARACION_shp__3_ = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_PREPARACION.shp"
    TB_RUTAS_Layer__2_ = "TB_RUTAS_Layer"
    TB_RUTAS_1_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_1.shp"
    TB_INTERSECT_RUTAS_VIVIENDA_SEGUNDO_PUNTO = "in_memory\\TB_INTERSECT_RUTAS_VIVIENDA_SEGUNDO_PUNTO"
    TB_INT_RUTAS_VIVIENDAS_AEU_MAX = "in_memory\\TB_INT_RUTAS_VIVIENDAS_AEU_MAX"
    TB_RUTAS_Layer = "TB_RUTAS_Layer"


    if arcpy.Exists(TB_RUTAS_1_shp):
        arcpy.Delete_management(TB_RUTAS_1_shp)


    # Process: Make Feature Layer
    arcpy.MakeFeatureLayer_management(TB_RUTAS_PREPARACION_shp__3_, TB_RUTAS_Layer, "\"FLG_MZ\"=1", "",
                                      "FID FID VISIBLE NONE;Shape Shape VISIBLE NONE;UBIGEO UBIGEO VISIBLE NONE;ZONA ZONA VISIBLE NONE;MANZANA MANZANA VISIBLE NONE;FLG_MZ FLG_MZ VISIBLE NONE;ORIG_FID ORIG_FID VISIBLE NONE")

    # Process: Intersect (3)
    arcpy.Intersect_analysis(
        "TB_RUTAS_Layer #;D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_SEGUNDA_VIVIENDA_AEU.shp #",
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


def ActualizarRutasViviendasMenoresIguales16():
    TB_RUTAS_1_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_1.shp"
    TB_RUTAS_PREPARACION_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_PREPARACION.shp"
    TB_RUTAS_2_shp_Layer="TB_RUTAS_2_shp_Layer"
    TB_RUTAS_2_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_2.shp"
    TB_RUTASS_shp = "in_memory\\TB_RUTASS"
    TB_RUTASS_Sort = "in_memory\\TB_RUTASS_Sort"
    TB_RUTASS_Sort_Layer = "TB_RUTASS_Sort_Layer"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"

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

    TB_RUTAS_1_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_1.shp"
    TB_RUTAS_2_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_2.shp"
    TB_RUTASS_shp = "in_memory\\TB_RUTASS"
    TB_RUTASS_Sort = "in_memory\\TB_RUTASS_Sort"
    TB_RUTASS_Sort_Layer = "TB_RUTASS_Sort_Layer"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"


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



#def CrearTablaSegundaPasada():
#    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
#    TB_RUTAS_DISSOLVE = "in_memory\\TB_RUTAS_DISSOLVE"
#    TB_RUTAS_DISSOLVE__2_ = "in_memory\\TB_RUTAS_DISSOLVE"
#    TB_RUTAS_DISSOLVE_Select2 = "in_memory\\TB_RUTAS_DISSOLVE_Select2"
#    TB_RUTAS_DISSOLVE_Select3 = "in_memory\\TB_RUTAS_DISSOLVE_Select3"
#    TB_RUTAS_DISSOLVE_Select3_Bu = "in_memory\\TB_RUTAS_DISSOLVE_Select3_Bu"
#    TB_RUTAS_INTERSECT = "in_memory\\TB_RUTAS_INTERSECT"
#    TB_RUTAS_SELECT_ZONA__2_ = "in_memory\\TB_RUTAS_SELECT_ZONA"
#    TB_RUTAS_SELECT_ZONA_shp__2_ = "in_memory\\TB_RUTAS_SELECT_ZONA"
#    TB_RUTAS_INTERSECT_SORT_Laye = "TB_RUTAS_INTERSECT_SORT_Laye"
#    TB_RUTAS_INTERSECT_SORT_Stat1 = "in_memory\\TB_RUTAS_INTERSECT_SORT_Stat1"
#    TB_RUTAS_SELECT_ZONA__4_ = "in_memory\\TB_RUTAS_SELECT_ZONA"
#    TB_RUTAS_INTERSECT_SORT = "in_memory\\TB_RUTAS_INTERSECT_SORT"
#    TB_RUTAS_INTERSECT_Sort_Stat__2_ = "in_memory\\TB_RUTAS_INTERSECT_SORT_Stat1"
#    TB_RUTAS_DISSOLVE_shp__3_ = "in_memory\\TB_RUTAS_DISSOLVE"
#    TB_RUTAS_INTERSECT_SORT_Laye__2_ = "TB_RUTAS_INTERSECT_SORT_Laye"
#    TB_SEGUNDA_PASADA_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\SegundaPasada\\TB_SEGUNDA_PASADA.shp"
#    TB_RUTAS_SELECT_ZONA = "in_memory\\TB_RUTAS_SELECT_ZONA"
#    TB_RUTAS_DISSOLVE_Select2_Fe = "in_memory\\TB_RUTAS_DISSOLVE_Select2_Fe"
#    TB_RUTAS_INTERSECT_Sort_Stat__4_ = "in_memory\\TB_RUTAS_INTERSECT_SORT_Stat1"
#
#
#    if arcpy.Exists(TB_SEGUNDA_PASADA_shp):
#        arcpy.Delete_management(TB_SEGUNDA_PASADA_shp)
#    # Process: Dissolve
#    arcpy.Dissolve_management(TB_RUTAS_LINEAS_shp, TB_RUTAS_DISSOLVE, "UBIGEO;ZONA;AEU;FLG_MZ",
#                              "MANZANA COUNT;CANT_VIV SUM", "MULTI_PART", "DISSOLVE_LINES")
#
#    # Process: Add Field (7)
#    arcpy.AddField_management(TB_RUTAS_DISSOLVE, "ID_RUTAAEU", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#
#    # Process: Calculate Field (7)
#    arcpy.CalculateField_management(TB_RUTAS_DISSOLVE_shp__3_, "ID_RUTAAEU", "[UBIGEO] & [ZONA] & [AEU]", "VB", "")
#
#    # Process: Select (2)
#    arcpy.Select_analysis(TB_RUTAS_DISSOLVE__2_, TB_RUTAS_DISSOLVE_Select3, "\"SUM_CANT_VIV\"<=0 AND \"FLG_MZ\"=0")
#
#    # Process: Buffer
#    arcpy.Buffer_analysis(TB_RUTAS_DISSOLVE_Select3, TB_RUTAS_DISSOLVE_Select3_Bu, "25 Meters", "FULL", "ROUND", "NONE",
#                          "", "PLANAR")
#
#    # Process: Select
#    arcpy.Select_analysis(TB_RUTAS_DISSOLVE__2_, TB_RUTAS_DISSOLVE_Select2, "\"FLG_MZ\"=1")
#
#    # Process: Feature Vertices To Points
#    arcpy.FeatureVerticesToPoints_management(TB_RUTAS_DISSOLVE_Select2, TB_RUTAS_DISSOLVE_Select2_Fe, "START")
#
#    # Process: Intersect
#    arcpy.Intersect_analysis("in_memory\\TB_RUTAS_DISSOLVE_Select3_Bu #;in_memory\\TB_RUTAS_DISSOLVE_Select2_Fe #",
#                             TB_RUTAS_INTERSECT, "ALL", "", "INPUT")
#
#    # Process: Select (4)
#    arcpy.Select_analysis(TB_RUTAS_INTERSECT, TB_RUTAS_SELECT_ZONA, "\"UBIGEO\"= \"UBIGEO_1\" AND \"ZONA\"=\"ZONA_1\"")
#
#    # Process: Delete Identical
#    arcpy.DeleteIdentical_management(TB_RUTAS_SELECT_ZONA, "UBIGEO;ZONA;AEU_1;FLG_MZ_1", "", "0")
#
#    # Process: Add Field (5)
#    arcpy.AddField_management(TB_RUTAS_SELECT_ZONA__2_, "TOTAL_VIV", "SHORT", "", "", "", "", "NULLABLE",
#                              "NON_REQUIRED", "")
#
#    # Process: Calculate Field (5)
#    arcpy.CalculateField_management(TB_RUTAS_SELECT_ZONA_shp__2_, "TOTAL_VIV", "[SUM_CANT_VIV]+ [SUM_CANT_VIV_1]", "VB",
#                                    "")
#
#    # Process: Sort
#    arcpy.Sort_management(TB_RUTAS_SELECT_ZONA__4_, TB_RUTAS_INTERSECT_SORT,
#                          "UBIGEO ASCENDING;ZONA ASCENDING;AEU ASCENDING;TOTAL_VIV ASCENDING", "UR")
#
#    # Process: Make Feature Layer
#    arcpy.MakeFeatureLayer_management(TB_RUTAS_INTERSECT_SORT, TB_RUTAS_INTERSECT_SORT_Laye, "", "",
#                                      "FID FID VISIBLE NONE;Shape Shape VISIBLE NONE;FID_TB_RUTAS_DISSOLVE_Select3_Bu FID_TB_RUTAS_DISSOLVE_Select3_Bu VISIBLE NONE;UBIGEO UBIGEO VISIBLE NONE;ZONA ZONA VISIBLE NONE;AEU AEU VISIBLE NONE;FLG_MZ FLG_MZ VISIBLE NONE;COUNT_MANZANA COUNT_MANZANA VISIBLE NONE;SUM_CANT_VIV SUM_CANT_VIV VISIBLE NONE;ID_RUTAAEU ID_RUTAAEU VISIBLE NONE;BUFF_DIST BUFF_DIST VISIBLE NONE;ORIG_FID ORIG_FID VISIBLE NONE;FID_TB_RUTAS_DISSOLVE_Select2_Fe FID_TB_RUTAS_DISSOLVE_Select2_Fe VISIBLE NONE;UBIGEO_1 UBIGEO_1 VISIBLE NONE;ZONA_1 ZONA_1 VISIBLE NONE;AEU_1 AEU_1 VISIBLE NONE;FLG_MZ_1 FLG_MZ_1 VISIBLE NONE;COUNT_MANZANA_1 COUNT_MANZANA_1 VISIBLE NONE;SUM_CANT_VIV_1 SUM_CANT_VIV_1 VISIBLE NONE;ID_RUTAAEU_1 ID_RUTAAEU_1 VISIBLE NONE;ORIG_FID_1 ORIG_FID_1 VISIBLE NONE;TOTAL_VIV TOTAL_VIV VISIBLE NONE")
#
#    # Process: Summary Statistics (3)
#    arcpy.Statistics_analysis(TB_RUTAS_INTERSECT_SORT_Laye, TB_RUTAS_INTERSECT_SORT_Stat1, "FID MIN", "UBIGEO;ZONA;AEU")
#
#    # Process: Add Field (6)
#    arcpy.AddField_management(TB_RUTAS_INTERSECT_SORT_Stat1, "flg_esc", "SHORT", "", "", "", "", "NULLABLE",
#                              "NON_REQUIRED", "")
#
#    # Process: Calculate Field (6)
#    arcpy.CalculateField_management(TB_RUTAS_INTERSECT_Sort_Stat__2_, "flg_esc", "1", "VB", "")
#
#    # Process: Add Join
#    arcpy.AddJoin_management(TB_RUTAS_INTERSECT_SORT_Laye, "FID", TB_RUTAS_INTERSECT_Sort_Stat__4_, "MIN_FID",
#                             "KEEP_COMMON")
#
#    # Process: Select (3)
#    arcpy.Select_analysis(TB_RUTAS_INTERSECT_SORT_Laye__2_, TB_SEGUNDA_PASADA_shp,
#                          "\"flg_esc\"=1 and \"TOTAL_VIV\"<=16")
#
#    # Process: Add Field
#    arcpy.AddField_management(TB_SEGUNDA_PASADA_shp, "UBIGEO", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#
#    # Process: Add Field (2)
#    arcpy.AddField_management(TB_SEGUNDA_PASADA_shp, "ZONA", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#
#    # Process: Add Field (3)
#    arcpy.AddField_management(TB_SEGUNDA_PASADA_shp, "AEU", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#
#    # Process: Add Field (4)
#    arcpy.AddField_management(TB_SEGUNDA_PASADA_shp, "AEU_1", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#
#    # Process: Calculate Field
#    arcpy.CalculateField_management(TB_SEGUNDA_PASADA_shp, "UBIGEO", "[TB_RUTAS_1]", "VB", "")
#
#    # Process: Calculate Field (2)
#    arcpy.CalculateField_management(TB_SEGUNDA_PASADA_shp, "ZONA", "[TB_RUTAS_2]", "VB", "")
#
#    # Process: Calculate Field (3)
#    arcpy.CalculateField_management(TB_SEGUNDA_PASADA_shp, "AEU", "[TB_RUTAS_3]", "VB", "")
#
#    # Process: Calculate Field (4)
#    arcpy.CalculateField_management(TB_SEGUNDA_PASADA_shp, "AEU_1", "[TB_RUTA_13]", "VB", "")
#
#    # Process: Delete Field
#    arcpy.DeleteField_management(TB_SEGUNDA_PASADA_shp,
#                                 "TB_RUTAS_I;TB_RUTAS_1;TB_RUTAS_2;TB_RUTAS_3;TB_RUTAS_4;TB_RUTAS_5;TB_RUTAS_6;TB_RUTAS_7;TB_RUTAS_8;TB_RUTAS_9;TB_RUTA_10;TB_RUTA_11;TB_RUTA_12;TB_RUTA_13;TB_RUTA_14;TB_RUTA_15;TB_RUTA_16;TB_RUTA_17;TB_RUTA_18;TB_RUTA_19;TB_RUTA_20;TB_RUTA_21;TB_RUTA_22;TB_RUTA_23;TB_RUTA_24;TB_RUTA_25;TB_RUTA_26")
#

#def ActualizarRutasAEUSegundaPasada():
#    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbanaTabular"
#   #MZS_AEU= "D:/ShapesPruebasSegmentacionUrbanaTabular/SegundaPasada/MZS_AEU.dbf"
#   #MZS_TRABAJO="D:/ShapesPruebasSegmentacionUrbanaTabular/SegundaPasada/TB_MZS_TRABAJO.shp"
#   #VIVIENDAS="D:/ShapesPruebasSegmentacionUrbanaTabular/SegundaPasada/TB_VIVIENDAS_U_TRABAJO.shp"
#   #RUTAS="D:/ShapesPruebasSegmentacionUrbanaTabular/SegundaPasada/TB_RUTAS.shp"
#
#
#    SEGUNDA_PASADA = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\SegundaPasada\\TB_SEGUNDA_PASADA.shp"
#
#    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
#    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
#    TB_VIVIENDAS_ORDENADAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\EnumerarAEUViviendas\\TB_VIVIENDAS_ORDENADAS.shp"
#    MZS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_MZS.shp"
#
#
#
#
#    with arcpy.da.SearchCursor(SEGUNDA_PASADA, ['UBIGEO', 'ZONA','AEU','AEU_1']) as cursor:
#        for row in cursor:
#            where=' UBIGEO=\''+str(row[0])+'\' AND ZONA=\''+str(row[1])+'\' AND AEU='+str(row[2])  # SE UBICA EL AEU DE LA MANZANA ESCOGIDA
#            where_2=' UBIGEO=\''+str(row[0])+'\' AND ZONA=\''+str(row[1])+'\' AND AEU='+str(row[3])  ##SE UBICA EL AEU DEL SEGMENTO ESCOGIDO
#            numero_aeu=int(row[3])
#            where_viviendas = ' UBIGEO=\'' + str(row[0]) + '\' AND ZONA=\'' + str(row[1]) + '\' AND AEU=' + str(row[2]) +' AND (USOLOCAl=1 OR USOLOCAl=3) ' # SE UBICA EL AEU DE LA MANZANA ESCOGIDA
#
#            with arcpy.da.UpdateCursor(MZS_AEU_dbf,['AEU'], where) as cursor8:
#                for row8 in cursor8:
#                    row8[0] = int(numero_aeu)
#                    cursor8.updateRow(row8)
#
#            del cursor8
#
#            #with arcpy.da.UpdateCursor(MZS,['AEU'], where) as cursor9:
#            #    for row9 in cursor9:
#            #        row9[0] = int(numero_aeu)
#            #        cursor9.updateRow(row9)
#            #del cursor9
#
#            or_max=0
#
#
##            with arcpy.da.SearchCursor(TB_VIVIENDAS_ORDENADAS_shp, ['AEU', 'OR_VIV_AEU'], where_2) as cursor7:
##                for row7 in cursor7:
##                    if or_max<int(row7[1]):
##                        or_max=int(row7[1])
##
##            del cursor7
##
##            or_max=or_max+1
##
##            with arcpy.da.UpdateCursor(TB_VIVIENDAS_ORDENADAS_shp,['AEU','OR_VIV_AEU'],where_viviendas ) as cursor10:
##                for row10 in cursor10:
##                    row10[0] = int(numero_aeu)
##                    row10[1]=or_max
##                    or_max=or_max+1
##                    cursor10.updateRow(row10)
##            del cursor10
#
#
#            with arcpy.da.UpdateCursor(TB_RUTAS_LINEAS_shp,['AEU'], where) as cursor11:
#                for row11 in cursor11:
#                    row11[0] = int(numero_aeu)
#                    cursor11.updateRow(row11)
#            del cursor11

         #  with arcpy.da.UpdateCursor(RUTAS, ['flg'], where_2) as cursor12:
         #      for row12 in cursor12:
         #          row12[0] = 1
         #          cursor12.updateRow(row12)
         #  del cursor12

#
#def Renumerar_AEU(ubigeos):
#    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbanaTabular"
#    arcpy.env.overwriteOutput = True
#
#    MIN_AEU = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\Renumerar\\MIN_AEU"
#    MIN_AEU_SORT = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\Renumerar\\MIN_AEU_SORT"
#    AEU_CANT_VIV = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\Renumerar\\AEU_CANT_VIV"
#    TB_VIVIENDAS_ORDENADAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\EnumerarAEUViviendas\\TB_VIVIENDAS_ORDENADAS.shp"
#    TB_MZS_shp = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_MZS.shp"
#    ZONAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
#    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
#    #TB_VIVIENDAS_ORDENADAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\EnumerarAEUViviendas\\TB_VIVIENDAS_ORDENADAS.shp"
#    #MZS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_MZS.shp"
#
#
#    #arcpy.AddField_management(MZS_AEU_dbf, "AEU_FINAL", "SHORT")
#
#
#
#
#
#   # if arcpy.Exists("D:/ShapesPruebasSegmentacionUrbanaTabular/Renumerar/TB_MZS_TRABAJO.shp"):
#   #     arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbanaTabular/Renumerar/TB_MZS_TRABAJO.shp")
#   # if arcpy.Exists("D:/ShapesPruebasSegmentacionUrbanaTabular/Renumerar/MZS_AEU.dbf"):
#   #     arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbanaTabular/Renumerar/MZS_AEU.dbf")
#   # if arcpy.Exists("D:/ShapesPruebasSegmentacionUrbanaTabular/Renumerar/TB_RUTAS.shp"):
#   #     arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbanaTabular/Renumerar/TB_RUTAS.shp")
#   # if arcpy.Exists("D:/ShapesPruebasSegmentacionUrbanaTabular/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp"):
#   #     arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbanaTabular/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp")
#   # if arcpy.Exists(MIN_AEU):
#   #     arcpy.Delete_management(MIN_AEU)
#   # if arcpy.Exists(MIN_AEU_SORT):
#   #     arcpy.Delete_management(MIN_AEU_SORT)
#   # if arcpy.Exists(AEU_CANT_VIV):
#   #     arcpy.Delete_management(AEU_CANT_VIV)
#
##    arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbanaTabular/SegundaPasada/TB_MZS_TRABAJO.shp",
##                                  "D:/ShapesPruebasSegmentacionUrbanaTabular/Renumerar/TB_MZS_TRABAJO.shp")
##    arcpy.AddField_management("D:/ShapesPruebasSegmentacionUrbanaTabular/Renumerar/TB_MZS_TRABAJO.shp", "AEU_FINAL",
##                              "SHORT")
##    arcpy.Copy_management("D:/ShapesPruebasSegmentacionUrbanaTabular/SegundaPasada/MZS_AEU.dbf",
##                          "D:/ShapesPruebasSegmentacionUrbanaTabular/Renumerar/MZS_AEU.dbf")
##    arcpy.AddField_management("D:/ShapesPruebasSegmentacionUrbanaTabular/Renumerar/MZS_AEU.dbf", "AEU_FINAL", "SHORT")
##
##    arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbanaTabular/SegundaPasada/TB_RUTAS.shp",
##                                  "D:/ShapesPruebasSegmentacionUrbanaTabular/Renumerar/TB_RUTAS.shp")
##    arcpy.AddField_management("D:/ShapesPruebasSegmentacionUrbanaTabular/Renumerar/TB_RUTAS.shp", "AEU_FINAL", "SHORT")
##    arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbanaTabular/SegundaPasada/TB_VIVIENDAS_U_TRABAJO.shp",
##                                  "D:/ShapesPruebasSegmentacionUrbanaTabular/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp")
#
#
#
#    arcpy.AddField_management(MZS_AEU_dbf,
#                              "AEU_FINAL", "SHORT")
#
#    arcpy.AddField_management(TB_VIVIENDAS_ORDENADAS_shp,
#                              "AEU_FINAL", "SHORT")
#
#
#
#    arcpy.AddField_management(MZS_AEU_dbf,
#                              "IDMANZANA", "TEXT")
#
#    arcpy.AddField_management(MZS_AEU_dbf,
#                              "IDFALSO", "TEXT")
#
#    arcpy.AddField_management(TB_MZS_shp,
#                              "AEU_FINAL", "SHORT")
#
#
#
#    arcpy.CalculateField_management(MZS_AEU_dbf, "IDMANZANA", "[UBIGEO]&[ZONA]&[MANZANA]", "VB", "")
#    arcpy.CalculateField_management(MZS_AEU_dbf, "IDFALSO", "[UBIGEO]&[ZONA]&[FALSO_COD]", "VB", "")
#
#    arcpy.MakeTableView_management(MZS_AEU_dbf, "mzs_aeu")
#    arcpy.MakeTableView_management(MZS_AEU_dbf, "mzs_aeu2")
#
#
#    #arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbanaTabular/Renumerar/TB_MZS_TRABAJO.shp",
#    #                                  "tb_mzs")
#
#    #arcpy.MakeFeatureLayer_management(ZONAS,
#    #                                  "zonas")
#
#    arcpy.Statistics_analysis(MZS_AEU_dbf, MIN_AEU, [["IDFALSO", "MIN"]], ["UBIGEO", "ZONA", "AEU"])
#    arcpy.Sort_management(MIN_AEU, MIN_AEU_SORT, ["MIN_IDFALSO", "AEU"])
#
#    arcpy.MakeTableView_management(MIN_AEU_SORT, "min_aeu_sort")
#
#    where_expression = UBIGEO.ExpresionUbigeos(ubigeos)
#
#    for row in arcpy.da.SearchCursor(ZONAS, ["UBIGEO", "ZONA"], where_expression):
#
#        ubigeo=row[0]
#        zona = row[1]
#
#        where_x = ' "UBIGEO"=\'' + str(ubigeo) + '\' AND "ZONA"=\'' + str(zona) + '\''
#        arcpy.SelectLayerByAttribute_management("min_aeu_sort", "NEW_SELECTION", where_x)
#        print where_x
#
#        numero_aeu_nuevo = 1
#
#        for row11 in arcpy.da.SearchCursor("min_aeu_sort", ['UBIGEO', 'ZONA', 'AEU', 'MIN_IDFALSO']):
#            aeu_anterior = str(row11[2])
#
#
#            where11 = ' "UBIGEO"=\'' + str(row11[0]) + '\' AND "ZONA"=\'' + str(row11[1]) + '\' AND AEU=' + str(aeu_anterior)
#
#            print  where11
#            #print ' UBIGEO ' + str(row11[0]) + ' ZONA' + str(row11[1]) + ' AEU ANTERIOR=' + str(aeu_anterior) + ' AEU NUEVO=' + str(numero_aeu_nuevo)
#
#            with arcpy.da.UpdateCursor(MZS_AEU_dbf,
#                                       ['AEU_FINAL'], where11) as cursor15:
#                for row15 in cursor15:
#                    row15[0] = numero_aeu_nuevo
#                    cursor15.updateRow(row15)
#
#
#            #del cursor8
#
#            with arcpy.da.UpdateCursor(TB_MZS_shp,
#                                       ['AEU_FINAL'], where11) as cursor16:
#                for row16 in cursor16:
#                    row16[0] = numero_aeu_nuevo
#                    cursor16.updateRow(row16)
#
#            with arcpy.da.UpdateCursor(TB_VIVIENDAS_ORDENADAS_shp,
#                                               ['AEU_FINAL'], where11) as cursor17:
#                for row17 in cursor17:
#                    row17[0] = numero_aeu_nuevo
#                    cursor17.updateRow(row17)
#
#            numero_aeu_nuevo = 1 + numero_aeu_nuevo

#def RenumerarRutas():
#    arcpy.env.overwriteOutput = True
#    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbanaTabular"
#    TB_RUTAS_PUNTOS_shp="D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"
#    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
#    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
#
#    arcpy.AddField_management(TB_RUTAS_LINEAS_shp,
#                              "AEU_FINAL", "SHORT")
#
#
#
#    for row in arcpy.da.SearchCursor(MZS_AEU_dbf, ["UBIGEO", "ZONA","AEU","AEU_FINAL"]):
#
#        where = ' "UBIGEO"=\'' + str(row[0]) + '\' AND "ZONA"=\'' + str(row[1]) + '\' AND AEU=' + str(row[2])
#        numero_aeu_nuevo=int(row[3])
#        with arcpy.da.UpdateCursor(TB_RUTAS_LINEAS_shp,
#                                   ['AEU_FINAL'], where) as cursorx:
#            for rowx in cursorx:
#                rowx[0] = numero_aeu_nuevo
#                cursorx.updateRow(rowx)
#
#        #with arcpy.da.UpdateCursor(TB_RUTAS_PUNTOS_shp,
#        #                                   ['AEU_FINAL'], where) as cursorxx:
#        #    for rowxx in cursorxx:
#        #        rowxx[0] = numero_aeu_nuevo
#        #        cursorxx.updateRow(rowxx)
#
#
#    field_delete = ""
#    for i in range(1, 10):
#        field_delete = ";TB_VIVIE_" + str(i) + field_delete
#    for j in range(10, 30):
#        field_delete = ";TB_VIVI_" + str(j) + field_delete
#    #arcpy.DeleteField_management(TB_RUTAS_PUNTOS_shp, "TB_VIVIEND" + field_delete)
#
#    #for row in arcpy.da.SearchCursor(MZS_AEU_dbf, ["UBIGEO", "ZONA","MANZANA","AEU"]):



def CrearTB_AEUS():
    AEUS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/Renumerar/TB_AEUS.dbf"
    AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    AEUS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/Renumerar/TB_AEUS_PUNTOS.shp"
    RUTAS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS.shp"
    #RUTAS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    TB_VIVIENDAS_ORDENADAS_shp = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    if arcpy.Exists (AEUS):
        arcpy.Delete_management(AEUS)
    if arcpy.Exists (AEUS_LINEAS):
        arcpy.Delete_management(AEUS_LINEAS)



    arcpy.AddField_management(RUTAS_LINEAS, "AEU_FINAL", "SHORT")
    arcpy.AddField_management(MZS_AEU_dbf, "AEU_FINAL", "SHORT")
    arcpy.AddField_management(MZS_AEU_dbf,"IDMANZANA" , "TEXT")
    arcpy.AddField_management(TB_VIVIENDAS_ORDENADAS_shp, "AEU_FINAL", "SHORT")
    arcpy.CalculateField_management(RUTAS_LINEAS, "AEU_FINAL", "!AEU!", "PYTHON_9.3")
    arcpy.CalculateField_management(MZS_AEU_dbf, "AEU_FINAL",
                                    "!AEU!", "PYTHON_9.3")

    arcpy.CalculateField_management(TB_VIVIENDAS_ORDENADAS_shp, "AEU_FINAL",
                                    "!AEU!", "PYTHON_9.3")

    arcpy.CalculateField_management(MZS_AEU_dbf, "IDMANZANA",
                                    "[UBIGEO]&[ZONA]&[MANZANA]", "VB")




    arcpy.Statistics_analysis(MZS_AEU_dbf, AEUS, [["CANT_VIV", "SUM"]], ["UBIGEO","CODCCPP" ,"ZONA", "AEU_FINAL"])
    arcpy.Dissolve_management(RUTAS_LINEAS, AEUS_LINEAS, ["UBIGEO", "CODCCPP","ZONA", "AEU_FINAL"], [["CANT_VIV", "SUM"]])
    arcpy.AddField_management(AEUS, "CANT_VIV", "SHORT")

    arcpy.CalculateField_management(AEUS, "CANT_VIV",
                                    "[SUM_CANT_V]", "VB", "")

    arcpy.AddField_management(AEUS_LINEAS, "CANT_VIV", "SHORT")

    arcpy.CalculateField_management(AEUS_LINEAS, "CANT_VIV",
                                    "[SUM_CANT_V]", "VB", "")

    arcpy.DeleteField_management(AEUS, ["SUM_CANT_V","FREQUENCY"])
    arcpy.DeleteField_management(AEUS_LINEAS, ["SUM_CANT_V","FREQUENCY"])

def CrearMarcosCroquis(ubigeos):
    env.overwriteOutput = True
    arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbanaTabular"
    ZONA_AEU="in_memory//zona_aeu"
    ZONA_CENSAL="in_memory//zona_censal.shp"
    MZS_AEU="D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"

    MZS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_MZS.shp"

    MARCOS_FINAL = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/Mapas/TB_MARCOS_AEUS.shp"

    if arcpy.Exists (MARCOS_FINAL):
        arcpy.Delete_management(MARCOS_FINAL)
    spatial_reference = arcpy.Describe(MZS).spatialReference


    arcpy.Statistics_analysis(MZS_AEU, ZONA_AEU, [["MANZANA", "COUNT"]], ["UBIGEO","CODCCPP" ,"ZONA", "AEU_FINAL"])

    arcpy.MakeTableView_management(ZONA_AEU, "zona_aeu")
    arcpy.MakeTableView_management(MZS_AEU, "mzs_aeu")
    arcpy.MakeFeatureLayer_management(MZS,"mzs_trabajo")


    where_list=ubigeos
    where_expression_xx = UBIGEO.ExpresionUbigeos(where_list)
    arrayll = arcpy.Array()

    j=0
    for row_cm_1 in arcpy.da.SearchCursor("zona_aeu", ["UBIGEO", "ZONA", "AEU_FINAL","CODCCPP"],where_expression_xx):
        arrayll=arcpy.Array()
        where1=' UBIGEO=\''+str(row_cm_1[0])+'\' AND ZONA=\''+str(row_cm_1[1])+'\' AND AEU_FINAL='+str(row_cm_1[2])
        i=0
        where_mzs=""
        for row_cm_2 in arcpy.da.SearchCursor("mzs_aeu", ["IDMANZANA"],where1):
            if i==0:
                where_mzs=where_mzs+' "IDMANZANA"=\''+str(row_cm_2[0])+'\''
            else:
                where_mzs = where_mzs + ' OR "IDMANZANA"=\'' + str(row_cm_2[0])+'\''
            i=i+1
        del row_cm_2


        in_features=arcpy.SelectLayerByAttribute_management("mzs_trabajo","NEW_SELECTION",where_mzs)

        out_feature = "D:\ShapesPruebasSegmentacionUrbana\AEU\Mapas\Marcos\Marco" + str(row_cm_1[0]) + str(
            row_cm_1[1]) + str(row_cm_1[2]) + ".shp"
        #out_feature = "in_memory//Marco"+str(row_cm_1[0])+str(row_cm_1[1])+str(row_cm_1[2])
        out_feature_2="in_memory//BufferDissolve"+str(row_cm_1[0])+str(row_cm_1[1])+str(row_cm_1[2])


        arcpy.FeatureEnvelopeToPolygon_management(in_features, out_feature)
        arcpy.Buffer_analysis(in_features, out_feature_2, "20 METERS", "", "","ALL")
        arcpy.FeatureEnvelopeToPolygon_management(out_feature_2, out_feature)


        arcpy.AddField_management(out_feature, "UBIGEO", "TEXT")
        arcpy.AddField_management(out_feature, "ZONA", "TEXT")
        arcpy.AddField_management(out_feature, "AEU_FINAL", "SHORT")
        arcpy.AddField_management(out_feature, "ID_MAPA", "TEXT")

        calculate_expression1 = "\'" + str(row_cm_1[0]) + "\'"
        calculate_expression2 = "\'" + str(row_cm_1[1]) + "\'"
        calculate_expression3 = int(row_cm_1[2])
        #calculate_expression4 = "[UBIGEO]&[ZONA]&[AEU_FINAL]"

        arcpy.CalculateField_management(out_feature, "UBIGEO", calculate_expression1,"PYTHON_9.3")
        arcpy.CalculateField_management(out_feature, "ZONA", calculate_expression2,"PYTHON_9.3")
        arcpy.CalculateField_management(out_feature, "AEU_FINAL", calculate_expression3,"PYTHON_9.3")
        #arcpy.CalculateField_management(out_feature, "ID_MAPA", calculate_expression4)


        if (j==0):
            arcpy.CopyFeatures_management(out_feature, MARCOS_FINAL)

        else:
            arcpy.Append_management(out_feature, MARCOS_FINAL)

        arcpy.Delete_management(out_feature)
        arcpy.Delete_management(out_feature_2)
        j=j+1

    del row_cm_1
    calculate_expression4 = "[UBIGEO]&[ZONA]&[AEU_FINAL]"
    arcpy.CalculateField_management(MARCOS_FINAL, "ID_MAPA", calculate_expression4, "VB")


def ModelarTablas(ubigeos):
    AEUS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/Renumerar/TB_AEUS.dbf"
    AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    RUTAS_LINEAS = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    SECCIONES="D:/ShapesPruebasSegmentacionUrbanaTabular/SECCIONES/EnumerarSecciones/TB_SECCIONES.shp"

    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"

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



def InsertarRegistros(ubigeos):
    arcpy.env.workspace = "Database Connections/PruebaSegmentacion.sde"
    TB_AEUS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/Renumerar/TB_AEUS.dbf"
    TB_AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    TB_RUTAS_LINEAS = "D:\\ShapesPruebasSegmentacionUrbanaTabular\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
    TB_RUTAS="D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"
    TB_SECCIONES = "D:/ShapesPruebasSegmentacionUrbanaTabular/SECCIONES/EnumerarSecciones/TB_SECCIONES.shp"
    TB_VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    TB_MARCOS_AEUS = "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/Mapas/TB_MARCOS_AEUS.shp"
    TB_MARCOS_SECCIONES = "D:/ShapesPruebasSegmentacionUrbanaTabular/SECCIONES/Mapas/TB_MARCOS_SECCIONES.shp"


    SEGM_ESP_SECCIONES = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_TAB_SECCION"
    SEGM_ESP_AEUS = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_TAB_AEU"
    SEGM_ESP_AEUS_LINEAS = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_TAB_AEU_LINEA"
    SEGM_ESP_RUTAS = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_TAB_RUTA"
    SEGM_ESP_RUTAS_LINEAS = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_TAB_RUTA_LINEA"
    SEGM_ESP_VIVIENDAS_U = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_TAB_VIVIENDA_U"
    SEGM_ESP_MARCO_AEU = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_TAB_MARCO_AEU"
    SEGM_ESP_MARCO_SECCION = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_TAB_MARCO_SECCION"

    where_list = UBIGEO.ExpresionUbigeos(ubigeos)
    arcpy.MakeFeatureLayer_management(TB_VIVIENDAS_ORDENADAS, "tb_viviendas_ordenadas", where_list)
    arcpy.MakeFeatureLayer_management(TB_SECCIONES, "tb_secciones", where_list)
    arcpy.MakeFeatureLayer_management(TB_AEUS_LINEAS, "tb_aeus_lineas", where_list)
    arcpy.MakeFeatureLayer_management(TB_RUTAS_LINEAS, "tb_rutas_lineas", where_list)
    arcpy.MakeTableView_management(TB_AEUS, "tb_aeus", where_list)
    arcpy.MakeTableView_management(TB_RUTAS, "tb_rutas", where_list)
    arcpy.MakeFeatureLayer_management(TB_MARCOS_AEUS, "tb_marcos_aeus", where_list)
    arcpy.MakeFeatureLayer_management(TB_MARCOS_SECCIONES, "tb_marcos_secciones", where_list)

    arcpy.Append_management("tb_viviendas_ordenadas", SEGM_ESP_VIVIENDAS_U, "NO_TEST")
    arcpy.Append_management("tb_secciones", SEGM_ESP_SECCIONES,"NO_TEST")
    arcpy.Append_management("tb_aeus_lineas", SEGM_ESP_AEUS_LINEAS, "NO_TEST")
    arcpy.Append_management("tb_rutas_lineas", SEGM_ESP_RUTAS_LINEAS, "NO_TEST")
    arcpy.Append_management("tb_aeus", SEGM_ESP_AEUS, "NO_TEST")
    arcpy.Append_management("tb_rutas", SEGM_ESP_RUTAS, "NO_TEST")
    arcpy.Append_management("tb_marcos_aeus", SEGM_ESP_MARCO_AEU, "NO_TEST")
    arcpy.Append_management("tb_marcos_secciones", SEGM_ESP_MARCO_SECCION, "NO_TEST")

    list_deletelayer=["tb_viviendas_ordenadas","tb_secciones","tb_aeus_lineas","tb_rutas_lineas","tb_aeus","tb_rutas","tb_marcos_aeus","tb_marcos_secciones"]

    for el in list_deletelayer:
        arcpy.Delete_management(el)







#
#ubigeos=["030602",
#"022001",
#"021509",
#"050601"]
