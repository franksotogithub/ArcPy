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

import SegmEspSeccion

arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"

#############################################AGRUPACION Y ENUMARCION INICIAL DE AEUS Y  DE VIVIENDAS##################################################






def ImportarTablasTrabajo(ubigeos):
    arcpy.env.overwriteOutput = True
    MZS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    VIVIENDAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp"
    ZONAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"

    MZS_AEU = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/MZS_AEU"

    EJES_VIALES="D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_EJES_VIALES.shp"


    if arcpy.Exists(VIVIENDAS):
        arcpy.Delete_management(VIVIENDAS)
    if arcpy.Exists(MZS):
        arcpy.Delete_management(MZS)

    if arcpy.Exists(ZONAS):
        arcpy.Delete_management(ZONAS)

    if arcpy.Exists(MZS_AEU):
        arcpy.Delete_management(MZS_AEU)

    if arcpy.Exists(EJES_VIALES):
        arcpy.Delete_management(EJES_VIALES)


    arcpy.env.workspace = "Database Connections/PruebaSegmentacion.sde"

    where_expression=UBIGEO.ExpresionUbigeosImportacion(ubigeos)

    #arcpy.FeatureClassToFeatureClass_conversion("CPV_SEGMENTACION.dbo.TB_MZS",
    #                                            "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/",
    #                                            'TB_MZS.shp',where_expression)

    arcpy.Select_analysis("CPV_SEGMENTACION.dbo.VW_MANZANA",
                          "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp"
                          , where_expression)


    arcpy.Select_analysis("CPV_SEGMENTACION.dbo.VW_ZONA_CENSAL",
                                                "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
                                                ,where_expression)
    arcpy.Select_analysis("CPV_SEGMENTACION.sde.VW_VIVIENDAS_U2",
                                                "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp"
                                                ,where_expression)

    arcpy.Select_analysis("CPV_SEGMENTACION.dbo.TB_EJE_VIAL",
                                                "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_EJES_VIALES.shp"
                                                , where_expression)


    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"

    arcpy.DeleteField_management(MZS, ['AEU','IDMANZANA'])

    arcpy.AddField_management(MZS, "IDMANZANA", "TEXT")
    expression = "str(!UBIGEO!)+str(!ZONA!)+str(!MANZANA!)"
    arcpy.CalculateField_management(MZS, "IDMANZANA", expression, "PYTHON_9.3")
    arcpy.AddField_management(MZS, "AEU", "SHORT")
    arcpy.AddField_management(MZS, "AEU_2", "SHORT")
    arcpy.AddField_management(MZS, "FLG_MZ", "SHORT")


def CrearMatrizAdyacencia(ubigeos):
    arcpy.env.overwriteOutput = True
    ADYACENCIA="D:/ShapesPruebasSegmentacionUrbana/AEU/MatrizAdyacencia/adyacencia.dbf"
    MZS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    ZONAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"



    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"
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



    prueba = "PruebaSegmentacion.sde"


    arcpy.env.workspace = r"Database Connections/PruebaSegmentacion.sde"


    if arcpy.Exists(r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.ADYACENCIA"):
        arcpy.Delete_management("Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.adyacencia")

    if arcpy.Exists(r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO"):
        arcpy.Delete_management("Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO")




    where_list = ubigeos

#    m = 0
#
#    where_expression = ""
#    for x in where_list:
#        if (m + 1) == len(where_list):
#            where_expression = where_expression + ' "UBIGEO"=%s' % where_list[m]
#        else:
#            where_expression = where_expression + ' "UBIGEO"=%s OR' % (where_list[m])
#        m = m + 1
#

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


    #arcpy.AddField_management(inFeatures, "IDMANZANA", "TEXT")
    #exp = "!UBIGEO!+!ZONA!+!MANZANA!"
    #arcpy.CalculateField_management(inFeatures, "IDMANZANA", exp, "PYTHON_9.3")

    # arcpy.AddField_management(inFeatures, "AEU", "SHORT")

    #############CREAMOS LA MATRIZ DE ADYACENCIA
    if arcpy.Exists(ADYACENCIA) == True:
        arcpy.Delete_management(ADYACENCIA)

    arcpy.CreateTable_management("D:/ShapesPruebasSegmentacionUrbana/AEU/MatrizAdyacencia/", "adyacencia.dbf")

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

 #   if arcpy.Exists(ADYACENCIA) == False:
 #       arcpy.CreateTable_management(ADYACENCIA)
#








    where_expression=UBIGEO.ExpresionUbigeos(ubigeos)

    for row in arcpy.da.SearchCursor(ZONAS, ["UBIGEO", "ZONA"],where_expression):
        where_expression2=' "UBIGEO"=\'%s\' AND "ZONA"=\'%s\' ' % (row[0], row[1])
        print where_expression2
        desc=str(row[0])+str(row[1])
        arcpy.MakeFeatureLayer_management(MZS, "manzanas",where_expression2)
        arcpy.FeatureToPoint_management("manzanas",
                                        "in_memory/Point" +desc ,
                                        "CENTROID")

        arcpy.AddField_management("in_memory/Point" +desc , 'Z', "SHORT")
        arcpy.CalculateField_management("in_memory/Point" +desc , 'Z', 1)


        arcpy.CreateThiessenPolygons_analysis("in_memory/Point" + desc,
                                              "in_memory/VoronoiPolygon" + desc,
                                              "ALL")




        arcpy.FeatureTo3DByAttribute_3d("in_memory/Point" +desc, "in_memory/Points3D" + desc, 'Z')

        Tin = "D:/ShapesPruebasSegmentacionUrbana/AEU/MatrizAdyacencia/Tin/Shape" + str(row[0]) + "" + str(row[1])

        arcpy.CreateTin_3d(Tin, "", "in_memory/Points3D"+desc, "DELAUNAY")

        arcpy.TinEdge_3d(Tin, "D:/ShapesPruebasSegmentacionUrbana/AEU/MatrizAdyacencia/Edge/" + desc+".shp", edge_type='DATA')


        inFeatures = "D:/ShapesPruebasSegmentacionUrbana/AEU/MatrizAdyacencia/Edge/" + desc+".shp"
        Edge="D:/ShapesPruebasSegmentacionUrbana/AEU/MatrizAdyacencia/Edge/" + desc+".shp"

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

        #c.CreateLineGeometry(desc)

        # obteniendo los puntos de interseccion

            #"D:/ShapesPruebasSegmentacionUrbana/AEU/MatrizAdyacencia/Edge/" + desc
        arcpy.Intersect_analysis(["in_memory/VoronoiSplitLine" + desc,
                                  Edge],
                                 "D:/ShapesPruebasSegmentacionUrbana/AEU/MatrizAdyacencia/Intersections/" + desc, "ALL", "", "point")

      # arcpy.Intersect_analysis(["in_memory/WriteGeometry" + desc,
      #                           "in_memory/Edge" + desc],
      #                          "in_memory/Intersections" + desc, "ALL", "", "point")





        # depurando los puntos duplicados
        fc1 = Edge
        fields1 = ['FID']
        fc2 = "D:/ShapesPruebasSegmentacionUrbana/AEU/MatrizAdyacencia/Intersections/" + desc+".shp"
        fields2 = ['FID_'+str(row[0])]

      # fc3 = "in_memory/IntersectionsInitial" + desc
      # fields3 = ['FID_Shap_1']



#        with arcpy.da.SearchCursor(fc1, fields1) as cursor1:
#
#            # contador=0
#            for row1 in cursor1:
#                # print "ID:" + str(row1[0])
#                contador = 0
#                with arcpy.arcpy.da.UpdateCursor(fc3, fields3) as cursor2:
#
#                    for row2 in cursor2:
#                        if row1[0] == row2[0]:
#                            contador = contador + 1
#                            # print "contador:" + str(contador)
#                        if contador > 2:
#                            cursor2.deleteRow()
#                            contador = contador - 1
#                del cursor2
#
#
#
#        del cursor1

        with arcpy.arcpy.da.SearchCursor(fc1, fields1) as cursor1:
            for row1 in cursor1:

                with arcpy.arcpy.da.UpdateCursor(fc2, fields2) as cursor2:
                    contador = 0
                    for row2 in cursor2:
                        if row1[0] == row2[0]:
                            contador = contador + 1

                        if contador > 3:
                            cursor2.deleteRow()
                            contador = contador - 1

        del cursor1


        fc = fc2
        fields = ['FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1', 'FirstX_2', 'FirstY_2', 'LastX_2', 'LastY_2']
    # a=np.array([2, 4, 6, 8])
    # b = np.array([2, 4, 6, 8])

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

                # print  str(row[8])+":"+str(coseno)



                if coseno >= 0.005:
                    cursor.deleteRow()

                j = j + 1

            del cursor


        input_table = fc2
        out_lines ="D:/ShapesPruebasSegmentacionUrbana/AEU/MatrizAdyacencia/ShapesFinal/" + desc+".shp"


            # XY To Line
        arcpy.XYToLine_management(input_table, out_lines,'FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1', "GEODESIC")

        arcpy.DeleteIdentical_management(out_lines, ["Shape"])

        adyacencias_x = "D:/ShapesPruebasSegmentacionUrbana/AEU/MatrizAdyacencia/ShapesFinal/" + desc+".shp"
        #adyacencias_x = "in_memory/ShapesFinal" + desc

        manzanas = "manzanas"

        EliminarAdyacencias.PorCantidadManzanasCruza(manzanas, adyacencias_x)

        cursorInsertar = arcpy.da.InsertCursor(ADYACENCIA,
                                   ['FirstX', 'FirstY', 'LastX', 'LastY'])
        for row in arcpy.da.SearchCursor(adyacencias_x,
                                     ['FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1']):
        # print row
            cursorInsertar.insertRow(row)
        del cursorInsertar



    arcpy.TableToTable_conversion(ADYACENCIA,
                                  'Database Connections/PruebaSegmentacion.sde/', 'adyacencia')
    MZS_TRABAJO = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS_TRABAJO.shp"

    arcpy.CopyFeatures_management(MZS,MZS_TRABAJO)

    arcpy.FeatureClassToGeodatabase_conversion([MZS_TRABAJO],
                                               'Database Connections/PruebaSegmentacion.sde/')





# sql.Exportar_TB_MZS_TRABAJO()



# arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/adyacencia.dbf")
# arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp")


# arcpy.FeatureClassToFeatureClass_conversion("CPV_SEGMENTACION.dbo.distritos", "D:/ArcGisShapesZones/", "distritos_prueba2" ,' "IDDIST" = \'150132\' ')






# if arcpy.Exists ("CPV_SEGMENTACION.dbo.departamentos_centroide")==False:
#    arcpy.CreateFeatureclass_management(r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.dbo.base_limites_nacionales",
#                               "CPV_SEGMENTACION.dbo.departamentos_centroide",
#                               "POINT",
#                              "",
#                              "",
#                              "",
#                              "")




# cursor= arcpy.da.InsertCursor("CPV_SEGMENTACION.dbo.departamentos_centroide",["SHAPE@"])

# for row in arcpy.da.SearchCursor("CPV_SEGMENTACION.dbo.departamentos", ["SHAPE@"]):
#   rowArray = []
#   rowArray.append(row[0].centroid)
#   cursor.insertRow(rowArray)
#   print row[0].centroid






















# arcpy.AddField_management("CPV_SEGMENTACION.dbo.departamentos","limites_buffer","TEXT","10")
# arcpy.Buffer_analysis("CPV_SEGMENTACION.dbo.departamentos","CPV_SEGMENTACION.dbo.departamentos_buffer",'10 miles')


# if arcpy.Exists ("CPV_SEGMENTACION.dbo.departamentos_centroide")==False:
#    arcpy.CreateFeatureclass_management(r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.dbo.base_limites_nacionales",
#                                    "CPV_SEGMENTACION.dbo.departamentos_centroide",
#                                    "POINT",
#                                    "",
#                                    "",
#                                    "",
#                                    "")
# arcpy.AddField_management(outCentroids, 'ORIG_ID', 'LONG')




# cursor= arcpy.da.InsertCursor("CPV_SEGMENTACION.dbo.departamentos_centroide",["SHAPE@"])

# for row in arcpy.da.SearchCursor("CPV_SEGMENTACION.dbo.departamentos", ["SHAPE@"]):
# s    rowArray = []
#    rowArray.append(row[0].centroid)
#    cursor.insertRow(rowArray)
#    print row[0].centroid





def CrearViviendasOrdenadas():
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"
    VIVIENDAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp"

    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"

    if arcpy.Exists(VIVIENDAS_ORDENADAS):
        arcpy.Delete_management(VIVIENDAS_ORDENADAS)

    arcpy.Sort_management(VIVIENDAS, VIVIENDAS_ORDENADAS, ["UBIGEO", "ZONA", "MANZANA", "ID_REG_OR"])

    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "AEU", "SHORT")
    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "OR_VIV_AEU", "SHORT")
    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "FLG_CORTE", "SHORT")
    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "FLG_MZ", "SHORT")
    # 0 SI LA VIVIENDA PERTENECE A MANZANAS MAYORES A 16, 1 SI LA VIVIENDA PERTENECE A MANZANAS






def EnumerarAEUEnViviendasDeManzanasCantVivMayores16(ubigeos):
    arcpy.env.overwriteOutput = True
    MZS="D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    VIVIENDAS="D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    ZONAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    #VIVIENDAS_OR_MAX = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/VIVIENDAS_OR_MAX"
    VIVIENDAS_AEU_OR_MAX="D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/VIVIENDAS_AEU_OR_MAX"
    VIVIENDAS_MZS_OR_MAX = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/VIVIENDAS_MZS_OR_MAX"
    #arcpy.AddField_management(MZS_AEU_dbf, "SECCION", "SHORT")

    #arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_RUTAS.shp", RUTAS)



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

        for row1 in arcpy.da.SearchCursor(MZS,["UBIGEO", "ZONA", "MANZANA", "IDMANZANA", "VIV_MZ" ],where_expression1):

            cant_viv=int(row1[4])
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

            with arcpy.arcpy.da.UpdateCursor (VIVIENDAS_ORDENADAS, ["UBIGEO","ZONA","MANZANA","ID_REG_OR","AEU", "OR_VIV_AEU","EDIFICACIO","USOLOCAL","COND_USOLO","FLG_CORTE","FLG_MZ"],where_expression_viv ) as cursor2:
                for row2 in cursor2:
                    #row2[9]=1
                    row2[10] = 1
                    idmanzana=str(row2[0])+str(row2[1])+str(row2[2])
                    usolocal=int(row2[7])
                    usolocal_cond=int(row2[8])

                    edificacion=int(row2[6])
                    #row2[1]=numero_aeu

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






                    #cursor.updateRow(row2)
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



    #       with arcpy.da.UpdateCursor(VIVIENDAS_ORDENADAS,["FLG_CORTE"], where_expressionxx) as cursor2:
#           for row2 in cursor2:
#               row2[0]=1
#               cursor2.updateRow(row2)

#       i=i+1


    # SE OBTIENE LAS  AEU'S POR ZONA

                    #with arcpy.arcpy.da.UpdateCursor(VIVIENDAS_ORDENADAS,["ID_REG_OR", "AEU", "OR_VIV_AEU", "EDIFICACIO", "USOLOCAL"],where_expression_viv2) as cursor3:



def EnumerarAEUEnViviendasDeManzanasCantVivMenoresIguales16(ubigeos):
    arcpy.env.overwriteOutput = True
    ZONAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    MZS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    ZONA_AEU_MAX = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/ZONA_AEU_MAX"
    where_expression = UBIGEO.ExpresionUbigeos(ubigeos)



    if arcpy.Exists(ZONA_AEU_MAX):
        arcpy.Delete_management(ZONA_AEU_MAX)


    where_expression_l=" FLG_MZ=1 "

    #where_expression_l = "FLG_MZ=1"

    arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS, "viviendas_ordenadas_2", where_expression_l)

    arcpy.Statistics_analysis("viviendas_ordenadas_2",ZONA_AEU_MAX, [["AEU", "MAX"]],
                              ["UBIGEO", "ZONA"])




    for row  in arcpy.da.SearchCursor(ZONAS, ["UBIGEO","ZONA"],where_expression):

        where_expressionx = "UBIGEO=\'" + str(row[0]) + "\' AND ZONA=\'" + str(row[1]) + "\' "

        aeu_max=0
        for row_aeu in arcpy.da.SearchCursor(ZONA_AEU_MAX, ["UBIGEO", "ZONA", "MAX_AEU"], where_expressionx):
            aeu_max=int(row_aeu[2])

        where_expression1 = "UBIGEO=\'" + str(row[0]) + "\' AND ZONA=\'" + str(row[1]) + "\'  AND VIV_MZ<=16 "

        #numero_aeu_max = int(row[2])
        nuevo_aeu=0

        with arcpy.da.UpdateCursor(MZS, ["UBIGEO", "ZONA", "MANZANA", "IDMANZANA", "VIV_MZ","AEU","AEU_2"], where_expression1) as  cursor1:
            for row1 in cursor1:

                nuevo_aeu = int(row1[5]) + aeu_max

                row1[6]=nuevo_aeu

                where_expression2 = "UBIGEO=\'" + str(row1[0]) + "\' AND ZONA=\'" + str(row1[1]) + "\'  AND MANZANA=\'"+str(row1[2])+"\' "

                or_viv_aeu=1
                usolocal=0
                with arcpy.da.UpdateCursor(VIVIENDAS_ORDENADAS, ["AEU","OR_VIV_AEU","USOLOCAL","COND_USOLO"],where_expression2) as cursor2:
                    for row2 in cursor2:
                        row2[0]=nuevo_aeu
                        usolocal=int(row2[2])
                        usolocal_cond=int(int(row2[3]))

                        if (usolocal in [1, 3]) or (usolocal == 6 and (usolocal_cond in [1, 3])):
                            row2[1] = or_viv_aeu
                            or_viv_aeu=or_viv_aeu+1


                        cursor2.updateRow(row2)

                cursor1.updateRow(row1)


    del row




def AgruparManzanasCantVivMenoresIguales16(ubigeos):
    arcpy.env.overwriteOutput = True
    ZONAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    MZS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp"

    Lista_adyacencia = "D:/ShapesPruebasSegmentacionUrbana/AEU/MatrizAdyacencia/lista_adyacencia.dbf"
    #Lista_adyacencia = "lista_adyacencia.dbf"
    where_expression = UBIGEO.ExpresionUbigeos(ubigeos)

    for row  in arcpy.da.SearchCursor(ZONAS, ["UBIGEO","ZONA","CODCCPP"],where_expression):
        where_expression1 = "UBIGEO=\'" + str(row[0]) + "\' AND ZONA=\'" + str(row[1]) + "\'  AND VIV_MZ<=16 "

        numero_aeu = 1
        desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])+".shp"
        print "zona: "+desc
        # Algoritmo Normal

        #fc = "D:/ShapesPruebasSegmentacionUrbana/Zones/" + desc
        fc = "D:/ShapesPruebasSegmentacionUrbana/Zones/" + desc

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
    MZS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    MZS_AEU_1 = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/MZS_AEU_1"
    MZS_AEU_2 = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/MZS_AEU_2.dbf"
    MZS_AEU = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"
    MZS_MENORES_16="D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/MZS_MENORES_16"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"

    if arcpy.Exists(MZS_AEU):
        arcpy.Delete_management(MZS_AEU)
    if arcpy.Exists(MZS_AEU_1):
        arcpy.Delete_management(MZS_AEU_1)

    if arcpy.Exists(MZS_AEU_2):
        arcpy.Delete_management(MZS_AEU_2)

    if arcpy.Exists(MZS_MENORES_16):
        arcpy.Delete_management(MZS_MENORES_16)

    ###creacion de la vista de manzanas mayores a 16

    where = " FLG_MZ=1 "
    arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS, "viviendas_ordenadas_3",where)

    arcpy.Statistics_analysis("viviendas_ordenadas_3", MZS_AEU_1, [["OR_VIV_AEU", "MAX"]],
                              ["UBIGEO","CODCCPP" ,"ZONA","MANZANA","AEU"])



    arcpy.AddField_management(MZS_AEU_1, "CANT_VIV", "SHORT")
    expression="!MAX_OR_VIV_AEU!"

    arcpy.CalculateField_management(MZS_AEU_1, "CANT_VIV", expression, "PYTHON_9.3")


    arcpy.DeleteField_management(MZS_AEU_1, ['FREQUENCY','MAX_OR_VIV_AEU'])


    ####creacion de  la vista de manzanas menores a 16

    where2 = " VIV_MZ<=16 "
    arcpy.MakeFeatureLayer_management(MZS, "mzs_menores_16", where2)

    arcpy.Statistics_analysis("mzs_menores_16", MZS_MENORES_16, [["MANZANA", "COUNT"]],
                              ["UBIGEO", "CODCCPP","ZONA", "MANZANA", "AEU_2", "VIV_MZ"])



    arcpy.AddField_management(MZS_MENORES_16, "AEU", "SHORT")
    arcpy.AddField_management(MZS_MENORES_16, "CANT_VIV", "SHORT")


    expression = "!VIV_MZ!"
    expression2 = "!AEU_2!"
    arcpy.CalculateField_management(MZS_MENORES_16, "CANT_VIV", expression, "PYTHON_9.3")
    arcpy.CalculateField_management(MZS_MENORES_16, "AEU", expression2, "PYTHON_9.3")

    arcpy.DeleteField_management(MZS_MENORES_16, ['FID_','FREQUENCY', 'COUNT_MANZANA','VIV_MZ','AEU_2'])

    arcpy.Merge_management([MZS_AEU_1, MZS_MENORES_16],MZS_AEU_2 )
    arcpy.Sort_management(MZS_AEU_2, MZS_AEU, ["UBIGEO","CODCCPP","ZONA","MANZANA","AEU"])

    #(in_dataset, out_dataset, sort_field, {spatial_sort_method})

#############################################CREANDO REPRESENTACIONES DE AEUS##################################################

#############################CREANDO REPRESENTACION DE LOS AEU'S CONDOMINIOS, O QUINTAS, VIVIENDAS CON MAS DE UN PISO ,ETC....#############################

def CrearRutasPuntos(ubigeos):
    arcpy.env.overwriteOutput = True
    TB_VIVIENDAS_ORDENADAS_shp = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    TB_VIVIENDAS_ORDENADAS_Layer = "TB_VIVIENDAS_ORDENADAS_Layer"
    TB_VIVIENDAS_ORDENADAS_FindI1 = "in_memory/TB_VIVIENDAS_ORDENADAS_FindI1"
    TB_VIVIENDAS_ORDENADAS_Layer__3_ = "TB_VIVIENDAS_ORDENADAS_Layer"
    TB_VIVIENDAS_ORDENADAS_Stati = "in_memory/TB_VIVIENDAS_ORDENADAS_Stati"
    TB_VIVIENDAS_ORDENADAS_Layer__4_ = "TB_VIVIENDAS_ORDENADAS_Layer"
    TB_RUTAS_PUNTOS_shp = "D:/ShapesPruebasSegmentacionUrbana/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"  # representacion de los aeu y puntos condominios
    if arcpy.Exists(TB_RUTAS_PUNTOS_shp):
        arcpy.Delete_management(TB_RUTAS_PUNTOS_shp)

    # Process: Make Feature Layer
    arcpy.MakeFeatureLayer_management(TB_VIVIENDAS_ORDENADAS_shp, TB_VIVIENDAS_ORDENADAS_Layer, "", "",
                                      "FID FID VISIBLE NONE;Shape Shape VISIBLE NONE;ID ID VISIBLE NONE;UBIGEO UBIGEO VISIBLE NONE;CODCCPP CODCCPP VISIBLE NONE;ZONA ZONA VISIBLE NONE;MANZANA MANZANA VISIBLE NONE;NOMCCPP NOMCCPP VISIBLE NONE;DEPARTAMEN DEPARTAMEN VISIBLE NONE;PROVINCIA PROVINCIA VISIBLE NONE;DISTRITO DISTRITO VISIBLE NONE;AREA AREA VISIBLE NONE;FRENTE_ORD FRENTE_ORD VISIBLE NONE;ID_REG_OR ID_REG_OR VISIBLE NONE;EDIFICACIO EDIFICACIO VISIBLE NONE;USOLOCAL USOLOCAL VISIBLE NONE;COND_USOLO COND_USOLO VISIBLE NONE;AEU AEU VISIBLE NONE;OR_VIV_AEU OR_VIV_AEU VISIBLE NONE;FLG_CORTE FLG_CORTE VISIBLE NONE;FLG_MZ FLG_MZ VISIBLE NONE")

    # Process: Find Identical
    arcpy.FindIdentical_management(TB_VIVIENDAS_ORDENADAS_Layer, TB_VIVIENDAS_ORDENADAS_FindI1,
                                   "Shape;UBIGEO;CODCCPP;ZONA;MANZANA;AEU", "", "0", "ALL")

    # Process: Add Join
    arcpy.AddJoin_management(TB_VIVIENDAS_ORDENADAS_Layer, "FID", TB_VIVIENDAS_ORDENADAS_FindI1, "IN_FID", "KEEP_ALL")

    # Process: Summary Statistics
    arcpy.Statistics_analysis(TB_VIVIENDAS_ORDENADAS_Layer__3_, TB_VIVIENDAS_ORDENADAS_Stati,
                              "TB_VIVIENDAS_ORDENADAS.FID COUNT;TB_VIVIENDAS_ORDENADAS.FID FIRST",
                              "TB_VIVIENDAS_ORDENADAS.UBIGEO;TB_VIVIENDAS_ORDENADAS.CODCCPP;MTB_VIVIENDAS_ORDENADAS.ZONA;TB_VIVIENDAS_ORDENADAS.AEU;TB_VIVIENDAS_ORDENADAS_FindI1.FEAT_SEQ")

    # Process: Add Join (2)
    arcpy.AddJoin_management(TB_VIVIENDAS_ORDENADAS_Layer, "TB_VIVIENDAS_ORDENADAS.FID", TB_VIVIENDAS_ORDENADAS_Stati,
                             "FIRST_TB_VIVIENDAS_ORDENADAS_FID", "KEEP_ALL")

    # Process: Select
    arcpy.Select_analysis(TB_VIVIENDAS_ORDENADAS_Layer__4_, TB_RUTAS_PUNTOS_shp,
                          "TB_VIVIENDAS_ORDENADAS_Stati.COUNT_TB_VIVIENDAS_ORDENADAS_FID>1")

    # Process: Add Field
    arcpy.AddField_management(TB_RUTAS_PUNTOS_shp, "UBIGEO", "TEXT")
    arcpy.AddField_management(TB_RUTAS_PUNTOS_shp, "CODCCPP", "TEXT")
    arcpy.AddField_management(TB_RUTAS_PUNTOS_shp, "ZONA", "TEXT")
    arcpy.AddField_management(TB_RUTAS_PUNTOS_shp, "MANZANA", "TEXT")
    arcpy.AddField_management(TB_RUTAS_PUNTOS_shp, "AEU", "SHORT")
    arcpy.AddField_management(TB_RUTAS_PUNTOS_shp, "CANT_VIV", "SHORT")

    # Process: Calculate Field
    arcpy.CalculateField_management(TB_RUTAS_PUNTOS_shp, "UBIGEO",
                                    "[TB_VIVIE_1]", "VB", "")
    arcpy.CalculateField_management(TB_RUTAS_PUNTOS_shp, "CODCCPP",
                                    "[TB_VIVIE_2]", "VB", "")

    arcpy.CalculateField_management(TB_RUTAS_PUNTOS_shp, "ZONA",
                                    "[TB_VIVIE_3]", "VB", "")
    arcpy.CalculateField_management(TB_RUTAS_PUNTOS_shp, "MANZANA",
                                    "[TB_VIVIE_4]", "VB", "")
    arcpy.CalculateField_management(TB_RUTAS_PUNTOS_shp, "AEU",
                                    "[TB_VIVI_26]", "VB", "")
    arcpy.CalculateField_management(TB_RUTAS_PUNTOS_shp, "CANT_VIV",
                                    "[TB_VIVI_28]", "VB", "")
    # Process: Delete Field
 #   field_delete=""
 #   for i in range(1,10):
 #           field_delete=";TB_VIVIE_"+str(i)+field_delete
 #   for j in range(10, 30):
 #       field_delete = ";TB_VIVI_" + str(j) + field_delete
 #   arcpy.DeleteField_management(TB_RUTAS_PUNTOS_shp,"TB_VIVIEND"+field_delete)


#############################CREANDO REPRESENTACION DE LOS AEU'S DEL RESTO DE VIVIENDAS....#############################

def CrearRutasPreparacion():

    TB_VIVIENDAS_ORDENADAS_shp = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    TB_MZS_shp = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp"

    # TB_MZS_TRABAJO_shp = "D:\\ShapesPruebasSegmentacionUrbana\\Manzanas\\TB_MZS_TRABAJO.shp"
    # PUNTO_INICIO_CARHUAZ_shp = "D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp"

    TB_VIVIENDAS_CORTES_shp = "D:/ShapesPruebasSegmentacionUrbana/AEU/CrearRepresentacionAEU/TB_VIVIENDAS_CORTES.shp"
    # TB_VIVIENDAS_CORTES_shp__2_ = "D:\\ShapesPruebasSegmentacionUrbana\\Viviendas\\TB_VIVIENDAS_CORTES.shp"
    # P_021806_shp = "D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp"
    # P_110204_shp = "D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp"
    TB_MZS_LINE_shp = "in_memory/TB_MZS_LINE"
    TB_MZS_TRABAJO_BUFFER_shp = "in_memory/TB_MZS_TRABAJO_BUFFER"
    PUNTOINICIO_BUFFER_shp = "in_memory/PUNTOINICIO_BUFFER"
    TB_MZS_ERASE_shp = "in_memory/TB_MZS_ERASE"
    PUNTOS_INICIO_shp = "D:/ShapesPruebasSegmentacionUrbana/AEU/CrearRepresentacionAEU/PUNTOS_INICIO.shp"
    TB_SPLIT_shp = "in_memory/TB_SPLIT"
    TB_DISSOLVE_shp = "in_memory/TB_DISSOLVE"
    TB_VIVIENDAS_CORTES_Buffer = "in_memory/TB_VIVIENDAS_CORTES_Buffer"
    TB_RUTAS_DISSOLVE_ERASE_shp = "in_memory/TB_RUTAS_DISSOLVE_ERASE"
    TB_RUTAS_PREPARACION_shp = "D:/ShapesPruebasSegmentacionUrbana/AEU/CrearRepresentacionAEU/TB_RUTAS_PREPARACION.shp"



    if arcpy.Exists(TB_VIVIENDAS_CORTES_shp):
        arcpy.Delete_management(TB_VIVIENDAS_CORTES_shp)

    if arcpy.Exists(TB_RUTAS_PREPARACION_shp):
        arcpy.Delete_management(TB_RUTAS_PREPARACION_shp)
    # Process: Buffer


    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"

    MZS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    expression_2 = "flg_manzana(!VIV_MZ!)"
    codeblock = """def flg_manzana(VIV_MZ):\n  if (VIV_MZ>16):\n    return 1\n  else:\n    return 0"""

    arcpy.CalculateField_management(MZS, "FLG_MZ", expression_2, "PYTHON_9.3", codeblock)


    arcpy.Buffer_analysis(TB_MZS_shp, TB_MZS_TRABAJO_BUFFER_shp, "0.3 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")

    # Process: Feature To Line

    where_expression = " FLG_CORTE=1"
    arcpy.Select_analysis(TB_VIVIENDAS_ORDENADAS_shp,
                          TB_VIVIENDAS_CORTES_shp
                          , where_expression)

    arcpy.FeatureToLine_management(TB_MZS_TRABAJO_BUFFER_shp, TB_MZS_LINE_shp, "", "ATTRIBUTES")

    # Process: Merge
    # arcpy.Merge_management("'D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp';'D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp';'D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp'", PUNTOS_INICIO_shp, "IDMANZANA \"IDMANZANA\" true true false 15 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,IDMANZANA,-1,-1,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,IDMANZANA,-1,-1,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,IDMANZANA,-1,-1;OBJECTID \"OBJECTID\" true true false 10 Long 0 10 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,OBJECTID,-1,-1,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,OBJECTID,-1,-1;ORIG_FID \"ORIG_FID\" true true false 10 Long 0 10 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,ORIG_FID,-1,-1,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,ORIG_FID,-1,-1;NEAR_FID \"NEAR_FID\" true true false 10 Long 0 10 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,NEAR_FID,-1,-1,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,NEAR_FID,-1,-1;NEAR_DIST \"NEAR_DIST\" true true false 19 Double 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,NEAR_DIST,-1,-1,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,NEAR_DIST,-1,-1;NEAR_FC \"NEAR_FC\" true true false 254 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,NEAR_FC,-1,-1,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,NEAR_FC,-1,-1;idmax \"idmax\" true true false 254 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,idmax,-1,-1,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,idmax,-1,-1;MIN_NEAR_D \"MIN_NEAR_D\" true true false 19 Double 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,MIN_NEAR_D,-1,-1,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,MIN_NEAR_D,-1,-1;MODIF \"MODIF\" true true false 5 Short 0 5 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,MODIF,-1,-1,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,MODIF,-1,-1;UBIGEO \"UBIGEO\" true true false 6 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,UBIGEO,-1,-1;CODCCPP14 \"CODCCPP14\" true true false 4 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CODCCPP14,-1,-1;MZ_T \"MZ_T\" true true false 4 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,MZ_T,-1,-1;CCDD \"CCDD\" true true false 2 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CCDD,-1,-1;CCPP \"CCPP\" true true false 2 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CCPP,-1,-1;CCDI \"CCDI\" true true false 2 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CCDI,-1,-1;ZONA \"ZONA\" true true false 5 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,ZONA,-1,-1;MANZANA \"MANZANA\" true true false 4 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,MANZANA,-1,-1;CODCCPP \"CODCCPP\" true true false 4 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CODCCPP,-1,-1;NOMCCPP \"NOMCCPP\" true true false 60 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,NOMCCPP,-1,-1;DEPARTAMEN \"DEPARTAMEN\" true true false 50 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,DEPARTAMEN,-1,-1;PROVNCIA \"PROVNCIA\" true true false 50 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,PROVNCIA,-1,-1;DISTRITO \"DISTRITO\" true true false 50 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbana\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,DISTRITO,-1,-1")

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




def PrimeraViviendaPorAEU():
    TB_VIVIENDAS_ORDENADAS_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\EnumerarAEUViviendas\\TB_VIVIENDAS_ORDENADAS.shp"
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
    TB_PRIMERA_VIVIENDA_AEU_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_PRIMERA_VIVIENDA_AEU.shp"


    if arcpy.Exists(TB_PRIMERA_VIVIENDA_AEU_shp):
        arcpy.Delete_management(TB_PRIMERA_VIVIENDA_AEU_shp)


    #where="(\"USOLOCAL\"=1 OR \"USOLOCAL\"=3 OR (\"USOLOCAL\"=6 AND (\"COND_USOLO\"=1 OR \"COND_USOLO\"=3 ))) AND FLG_MZ=1"
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
                                    "[TB_VIVI_15]", "VB", "")


    field_delete=""


    for i in range(1,10):
        field_delete=";TB_VIVIE_"+str(i)+field_delete
    for j in range(10, 28):
        field_delete = ";TB_VIVI_" + str(j) + field_delete
    arcpy.DeleteField_management(TB_PRIMERA_VIVIENDA_AEU_shp,"TB_VIVIEND"+field_delete)



def SegundaViviendaPorAEU():
    TB_VIVIENDAS_ORDENADAS_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\EnumerarAEUViviendas\\TB_VIVIENDAS_ORDENADAS.shp"
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
    TB_SEGUNDA_VIVIENDA_AEU_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_SEGUNDA_VIVIENDA_AEU.shp"


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
                                    "[TB_VIVI_15]", "VB", "")


    field_delete=""

    for i in range(1,10):
        field_delete=";TB_VIVIE_"+str(i)+field_delete
    for j in range(10, 28):
        field_delete = ";TB_VIVI_" + str(j) + field_delete


    arcpy.DeleteField_management(TB_SEGUNDA_VIVIENDA_AEU_shp,"TB_VIVIEND"+field_delete)



####pegando los aues primera pasada
def CrearLineasAEUPrimeraPasada():
    TB_SEGUNDA_VIVIENDA_AEU_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_SEGUNDA_VIVIENDA_AEU.shp"
    TB_RUTAS_PREPARACION_shp__3_ = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_PREPARACION.shp"
    TB_RUTAS_Layer__2_ = "TB_RUTAS_Layer"
    TB_RUTAS_1_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_1.shp"
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
        "TB_RUTAS_Layer #;D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_SEGUNDA_VIVIENDA_AEU.shp #",
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
    TB_RUTAS_1_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_1.shp"
    TB_RUTAS_PREPARACION_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_PREPARACION.shp"
    TB_RUTAS_2_shp_Layer="TB_RUTAS_2_shp_Layer"
    TB_RUTAS_2_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_2.shp"
    TB_RUTASS_shp = "in_memory\\TB_RUTASS"
    TB_RUTASS_Sort = "in_memory\\TB_RUTASS_Sort"
    TB_RUTASS_Sort_Layer = "TB_RUTASS_Sort_Layer"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"

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

    arcpy.DeleteField_management(TB_RUTAS_2_shp,"TB_RUTAS_P;TB_RUTAS_1;TB_RUTAS_2;TB_RUTAS_3;TB_RUTAS_4;TB_RUTAS_5;;TB_RUTAS_6;MZS_AEU_OI;MZS_AEU_FI;MZS_AEU_UB;MZS_AEU_ZO;MZS_AEU_MA;MZS_AEU_AE;MZS_AEU_CA;MZS_AEU_ID;MZS_AEU_FI;MZS_AEU__1;MZS_AEU_ID;MZS_AEU__2;MZS_AEU_CO")



def CrearLineasAEUFinal():
    TB_PRIMERA_VIVIENDA_AEU_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_PRIMERA_VIVIENDA_AEU.shp"
    TB_RUTAS_1_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_1.shp"
    TB_RUTAS_2_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_2.shp"
    TB_RUTASS_shp = "in_memory\\TB_RUTASS"
    TB_RUTASS_Sort = "in_memory\\TB_RUTASS_Sort"
    TB_RUTASS_Sort_Layer = "TB_RUTASS_Sort_Layer"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"


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
                                 "TB_RUTASS_;TB_RUTASS1;TB_RUTAS_1;TB_RUTAS_2;TB_RUTAS_3;TB_RUTAS_4;TB_RUTAS_5;MZS_AEU_OI;MZS_AEU_UB;MZS_AEU_ZO;MZS_AEU_MA;MZS_AEU_AE;MZS_AEU_CA;MZS_AEU_ID;MZS_AEU_FI;MZS_AEU__1;MZS_AEU_CO;MZS_AEU__2")



def CrearLineasAEUSegundaPasada():
    TB_PRIMERA_VIVIENDA_AEU_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_PRIMERA_VIVIENDA_AEU.shp"
    TB_RUTAS_1_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_1.shp"
    TB_RUTAS_PREPARACION_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_PREPARACION.shp"
    TB_INTERSECT_RUTAS_PRIMERA_VIVIENDA = "in_memory\\TB_INTERSECT_RUTAS_PRIMERA_VIVIENDA"
    TB_RUTAS_1_Layer = "TB_RUTAS_1_Layer"
    TB_RUTAS_1_Layer__4_ = "TB_RUTAS_1_Layer"
    TB_RUTAS_1_1_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_1_1.shp"
    TB_RUTAS_1_Layer__5_ = "TB_RUTAS_1_Layer"
    TB_RUTAS_1_2_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_1_2.shp"
    TB_RUTAS_2_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_2.shp"
    TB_RUTASS_shp = "in_memory\\TB_RUTASS"
    TB_RUTASS_Sort = "in_memory\\TB_RUTASS_Sort"
    TB_RUTASS_Sort_Layer = "TB_RUTASS_Sort_Layer"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"


#    if arcpy.Exists(TB_RUTAS_1_1_shp):
#        arcpy.Delete_management(TB_RUTAS_1_1_shp)
#
#    if arcpy.Exists(TB_RUTAS_1_2_shp):
#        arcpy.Delete_management(TB_RUTAS_1_2_shp)

    if arcpy.Exists(TB_RUTAS_2_shp):
        arcpy.Delete_management(TB_RUTAS_2_shp)

    if arcpy.Exists(TB_RUTAS_LINEAS_shp):
        arcpy.Delete_management(TB_RUTAS_LINEAS_shp)







    # Process: Select (2)
#    arcpy.Select_analysis(TB_RUTAS_1_shp, TB_RUTAS_1_1_shp, "\"AEU\"<>0")
#
#    # Process: Make Feature Layer
#    arcpy.MakeFeatureLayer_management(TB_RUTAS_1_shp, TB_RUTAS_1_Layer, "", "",
#                                      "FID FID VISIBLE NONE;Shape Shape VISIBLE NONE;UBIGEO UBIGEO VISIBLE NONE;CODCCPP CODCCPP VISIBLE NONE;ZONA ZONA VISIBLE NONE;MANZANA MANZANA VISIBLE NONE;AEU AEU VISIBLE NONE;FLG_MZ FLG_MZ VISIBLE NONE")
#
#    # Process: Select Layer By Attribute (2)
#    arcpy.SelectLayerByAttribute_management(TB_RUTAS_1_Layer, "NEW_SELECTION", "\"AEU\"=0")
#
#    # Process: Intersect (5)
#    arcpy.Intersect_analysis(
#        "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_PRIMERA_VIVIENDA_AEU.shp #;TB_RUTAS_1_Layer #",
#        TB_INTERSECT_RUTAS_PRIMERA_VIVIENDA, "ALL", "0.32 Meters", "INPUT")
#
#    # Process: Add Join
#    arcpy.AddJoin_management(TB_RUTAS_1_Layer__4_, "FID", TB_INTERSECT_RUTAS_PRIMERA_VIVIENDA, "FID_TB_RUTAS_1",
#                             "KEEP_ALL")
#
#    # Process: Select
#    arcpy.Select_analysis(TB_RUTAS_1_Layer__5_, TB_RUTAS_1_2_shp, "")
#
#    # Process: Add Field
#    arcpy.AddField_management(TB_RUTAS_1_2_shp, "UBIGEO", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#
#    # Process: Calculate Field
#    arcpy.CalculateField_management(TB_RUTAS_1_2_shp, "UBIGEO", "[TB_RUTAS_1]", "VB", "")
#
#    # Process: Add Field (2)
#    arcpy.AddField_management(TB_RUTAS_1_2_shp, "CODCCPP", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#
#    # Process: Calculate Field (2)
#    arcpy.CalculateField_management(TB_RUTAS_1_2_shp, "CODCCPP", "[TB_RUTAS_2]", "VB", "")
#
#
#
#    arcpy.AddField_management(TB_RUTAS_1_2_shp, "ZONA", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#
#    # Process: Calculate Field (2)
#    arcpy.CalculateField_management(TB_RUTAS_1_2_shp, "ZONA", "[TB_RUTAS_3]", "VB", "")
#
#    # Process: Add Field (3)
#    arcpy.AddField_management(TB_RUTAS_1_2_shp, "MANZANA", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#
#    # Process: Calculate Field (3)
#    arcpy.CalculateField_management(TB_RUTAS_1_2_shp, "MANZANA", "[TB_RUTAS_4]", "VB", "")
#
#    # Process: Add Field (4)
#    arcpy.AddField_management(TB_RUTAS_1_2_shp, "AEU", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#
#    # Process: Calculate Field (4)
#    arcpy.CalculateField_management(TB_RUTAS_1_2_shp, "AEU", "[TB_INTER_6]", "VB", "")
#
#    # Process: Add Field (5)
#    arcpy.AddField_management(TB_RUTAS_1_2_shp, "FLG_MZ", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#
#    # Process: Calculate Field (5)
#    arcpy.CalculateField_management(TB_RUTAS_1_2_shp, "FLG_MZ", "[TB_INTE_12]", "VB", "")
#
#    # Process: Delete Field
#    arcpy.DeleteField_management(TB_RUTAS_1_2_shp,
#                                 "TB_RUTAS_1;TB_RUTAS_2;TB_RUTAS_3;TB_RUTAS_4;TB_RUTAS_5;TB_RUTAS_6;TB_INTERSE;TB_INTER_1;TB_INTER_2;TB_INTER_3;TB_INTER_4;TB_INTER_5;TB_INTER_6;TB_INTER_7;TB_INTER_8;TB_INTER_9;TB_INTE_10;TB_INTE_11")

    # Process: Select (3)
    arcpy.Select_analysis(TB_RUTAS_PREPARACION_shp, TB_RUTAS_2_shp, "\"FLG_MZ\"=0")

    # Process: Delete Field (2)
    arcpy.DeleteField_management(TB_RUTAS_2_shp, "ORIG_FID")

    # Process: Merge (2)
    #arcpy.Merge_management([TB_RUTAS_1_1_shp, TB_RUTAS_1_2_shp, TB_RUTAS_2_shp], TB_RUTASS_shp)
    #
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
                                 "TB_RUTASS_;TB_RUTASS1;TB_RUTAS_1;TB_RUTAS_2;TB_RUTAS_3;TB_RUTAS_4;TB_RUTAS_5;MZS_AEU_OI;MZS_AEU_UB;MZS_AEU_ZO;MZS_AEU_MA;MZS_AEU_AE;MZS_AEU_CA;MZS_AEU_ID;MZS_AEU_FI;MZS_AEU__1;MZS_AEU_CO;MZS_AEU__2")


#
#
#def ActualizarRutasViviendasMenoresIguales16():
#    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/"
#    arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp", "manzanas")
#    arcpy.MakeFeatureLayer_management("D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp",
#                                      "rutas_lineas")
#    #arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/MZS_AEU.dbf", "aeu_manzana")
#    where_inicial= " VIV_MZ<=16 "
#    aeu=0
#    viv_aeu=0
#
#    with arcpy.da.SearchCursor("manzanas", ['UBIGEO','ZONA','MANZANA','VIV_MZ','AEU_2'],where_inicial) as cursor3:
#        for row3 in cursor3:
#
#            where_expression = " UBIGEO=\'" + str(row3[0]) + "\'  AND  ZONA=\'" + str(
#                row3[1]) + "\' AND MANZANA=\'" + str(row3[2]) + "\' "
#
#            cant_viv=int(row3[3])
#            aeu=int(row3[4])
#            #where_expression2 = " IDMANZANA=\'" + str(row3[0])+(row3[1]) + str(row3[2]) + "\' "
#
#            #arcpy.SelectLayerByAttribute_management("aeu_manzana", "NEW_SELECTION")
#
#            with arcpy.da.UpdateCursor("rutas_lineas", ['AEU','CANT_VIV'],where_expression) as cursor5:
#                for row5 in cursor5:
#                    row5[0]=aeu
#                    row5[1] = cant_viv
#                    cursor5.updateRow(row5)
#
#            del cursor5
#        del cursor3




def CrearTablaSegundaPasada():
    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
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
    TB_SEGUNDA_PASADA_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\SegundaPasada\\TB_SEGUNDA_PASADA.shp"
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
    arcpy.Select_analysis(TB_RUTAS_DISSOLVE__2_, TB_RUTAS_DISSOLVE_Select3, "\"SUM_CANT_VIV\"<=8 AND \"FLG_MZ\"=0")

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



def ActualizarRutasAEUSegundaPasada():
    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"
   #MZS_AEU= "D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/MZS_AEU.dbf"
   #MZS_TRABAJO="D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/TB_MZS_TRABAJO.shp"
   #VIVIENDAS="D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/TB_VIVIENDAS_U_TRABAJO.shp"
   #RUTAS="D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/TB_RUTAS.shp"

    TB_SEGUNDA_PASADA_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\SegundaPasada\\TB_SEGUNDA_PASADA.shp"
    SEGUNDA_PASADA = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\SegundaPasada\\TB_SEGUNDA_PASADA.shp"

    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    TB_VIVIENDAS_ORDENADAS_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\EnumerarAEUViviendas\\TB_VIVIENDAS_ORDENADAS.shp"
    MZS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp"




    with arcpy.da.SearchCursor(SEGUNDA_PASADA, ['UBIGEO', 'ZONA','AEU','AEU_1']) as cursor:
        for row in cursor:
            where=' UBIGEO=\''+str(row[0])+'\' AND ZONA=\''+str(row[1])+'\' AND AEU='+str(row[2])  # SE UBICA EL AEU DE LA MANZANA ESCOGIDA
            where_2=' UBIGEO=\''+str(row[0])+'\' AND ZONA=\''+str(row[1])+'\' AND AEU='+str(row[3])  ##SE UBICA EL AEU DEL SEGMENTO ESCOGIDO
            numero_aeu=int(row[3])
            where_viviendas = ' UBIGEO=\'' + str(row[0]) + '\' AND ZONA=\'' + str(row[1]) + '\' AND AEU=' + str(row[2]) +' AND (USOLOCAl=1 OR USOLOCAl=3) ' # SE UBICA EL AEU DE LA MANZANA ESCOGIDA

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


            with arcpy.da.SearchCursor(TB_VIVIENDAS_ORDENADAS_shp, ['AEU', 'OR_VIV_AEU'], where_2) as cursor7:
                for row7 in cursor7:
                    if or_max<int(row7[1]):
                        or_max=int(row7[1])

            del cursor7

            or_max=or_max+1

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



def Renumerar_AEU():
    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"


    MIN_AEU = "in_memory/MIN_AEU"
    MIN_AEU_SORT = "in_memory/MIN_AEU_SORT"
    AEU_CANT_VIV = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\Renumerar\\AEU_CANT_VIV"
    TB_VIVIENDAS_ORDENADAS_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\EnumerarAEUViviendas\\TB_VIVIENDAS_ORDENADAS.shp"
    TB_MZS_shp = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp"

    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    #TB_VIVIENDAS_ORDENADAS_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\EnumerarAEUViviendas\\TB_VIVIENDAS_ORDENADAS.shp"
    #MZS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp"


    #arcpy.AddField_management(MZS_AEU_dbf, "AEU_FINAL", "SHORT")





   # if arcpy.Exists("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp"):
   #     arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp")
   # if arcpy.Exists("D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf"):
   #     arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf")
   # if arcpy.Exists("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_RUTAS.shp"):
   #     arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_RUTAS.shp")
   # if arcpy.Exists("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp"):
   #     arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp")
   # if arcpy.Exists(MIN_AEU):
   #     arcpy.Delete_management(MIN_AEU)
   # if arcpy.Exists(MIN_AEU_SORT):
   #     arcpy.Delete_management(MIN_AEU_SORT)
   # if arcpy.Exists(AEU_CANT_VIV):
   #     arcpy.Delete_management(AEU_CANT_VIV)

#    arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/TB_MZS_TRABAJO.shp",
#                                  "D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp")
#    arcpy.AddField_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp", "AEU_FINAL",
#                              "SHORT")
#    arcpy.Copy_management("D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/MZS_AEU.dbf",
#                          "D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf")
#    arcpy.AddField_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf", "AEU_FINAL", "SHORT")
#
#    arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/TB_RUTAS.shp",
#                                  "D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_RUTAS.shp")
#    arcpy.AddField_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_RUTAS.shp", "AEU_FINAL", "SHORT")
#    arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/TB_VIVIENDAS_U_TRABAJO.shp",
#                                  "D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp")



    arcpy.AddField_management(MZS_AEU_dbf,
                              "AEU_FINAL", "SHORT")

    arcpy.AddField_management(TB_VIVIENDAS_ORDENADAS_shp,
                              "AEU_FINAL", "SHORT")

    arcpy.AddField_management(MZS_AEU_dbf,
                              "IDMANZANA", "TEXT")


    arcpy.AddField_management(TB_MZS_shp,
                              "AEU_FINAL", "SHORT")




    arcpy.CalculateField_management(MZS_AEU_dbf, "IDMANZANA", "[UBIGEO]&[ZONA]&[MANZANA]", "VB", "")

    arcpy.MakeTableView_management(MZS_AEU_dbf, "mzs_aeu")
    arcpy.MakeTableView_management(MZS_AEU_dbf, "mzs_aeu2")
    #arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp",
    #                                  "tb_mzs")

    arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp",
                                      "zonas")

    arcpy.Statistics_analysis(MZS_AEU_dbf, MIN_AEU, [["IDMANZANA", "MIN"]], ["UBIGEO", "ZONA", "AEU"])
    arcpy.Sort_management(MIN_AEU, MIN_AEU_SORT, ["MIN_IDMANZANA", "AEU"])
    arcpy.MakeTableView_management(MIN_AEU_SORT, "min_aeu_sort")


    where_expression = UBIGEO.ExpresionUbigeos(ubigeos)
    for row in arcpy.da.SearchCursor("zonas", ["UBIGEO", "ZONA"], where_expression):

        ubigeo=row[0]
        zona = row[1]

        where_x = ' "UBIGEO"=\'' + str(ubigeo) + '\' AND "ZONA"=\'' + str(zona) + '\''
        arcpy.SelectLayerByAttribute_management("min_aeu_sort", "NEW_SELECTION", where_x)


        numero_aeu_nuevo = 1

        for row11 in arcpy.da.SearchCursor("min_aeu_sort", ['UBIGEO', 'ZONA', 'AEU', 'MIN_IDMANZANA']):
            aeu_anterior = str(row11[2])

            where11 = ' "UBIGEO"=\'' + str(row11[0]) + '\' AND "ZONA"=\'' + str(row11[1]) + '\' AND AEU=' + str(aeu_anterior)

            #print ' UBIGEO ' + str(row11[0]) + ' ZONA' + str(row11[1]) + ' AEU ANTERIOR=' + str(aeu_anterior) + ' AEU NUEVO=' + str(numero_aeu_nuevo)

            with arcpy.da.UpdateCursor(MZS_AEU_dbf,
                                       ['AEU_FINAL'], where11) as cursor15:
                for row15 in cursor15:
                    row15[0] = numero_aeu_nuevo
                    cursor15.updateRow(row15)


            #del cursor8

            with arcpy.da.UpdateCursor(TB_MZS_shp,
                                       ['AEU_FINAL'], where11) as cursor16:
                for row16 in cursor16:
                    row16[0] = numero_aeu_nuevo
                    cursor16.updateRow(row16)

            with arcpy.da.UpdateCursor(TB_VIVIENDAS_ORDENADAS_shp,
                                               ['AEU_FINAL'], where11) as cursor17:
                for row17 in cursor17:
                    row17[0] = numero_aeu_nuevo
                    cursor17.updateRow(row17)

            numero_aeu_nuevo = 1 + numero_aeu_nuevo


#    arcpy.Statistics_analysis(MZS_AEU_dbf, AEU_CANT_VIV,
#                              [["VIV_AEU", "SUM"]], ["UBIGEO", "ZONA", "AEU_FINAL"])

def RenumerarRutas():
    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"
    TB_RUTAS_PUNTOS_shp="D:/ShapesPruebasSegmentacionUrbana/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"
    TB_RUTAS_LINEAS_shp = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"

    arcpy.AddField_management(TB_RUTAS_LINEAS_shp,
                              "AEU_FINAL", "SHORT")

    #arcpy.AddField_management(TB_RUTAS_PUNTOS_shp,
    #                          "AEU_FINAL", "SHORT")

    # Process: Delete Field




    for row in arcpy.da.SearchCursor(MZS_AEU_dbf, ["UBIGEO", "ZONA","AEU","AEU_FINAL"]):

        where = ' "UBIGEO"=\'' + str(row[0]) + '\' AND "ZONA"=\'' + str(row[1]) + '\' AND AEU=' + str(row[2])
        numero_aeu_nuevo=int(row[3])
        with arcpy.da.UpdateCursor(TB_RUTAS_LINEAS_shp,
                                   ['AEU_FINAL'], where) as cursorx:
            for rowx in cursorx:
                rowx[0] = numero_aeu_nuevo
                cursorx.updateRow(rowx)

        #with arcpy.da.UpdateCursor(TB_RUTAS_PUNTOS_shp,
        #                                   ['AEU_FINAL'], where) as cursorxx:
        #    for rowxx in cursorxx:
        #        rowxx[0] = numero_aeu_nuevo
        #        cursorxx.updateRow(rowxx)


    field_delete = ""
    for i in range(1, 10):
        field_delete = ";TB_VIVIE_" + str(i) + field_delete
    for j in range(10, 30):
        field_delete = ";TB_VIVI_" + str(j) + field_delete
    #arcpy.DeleteField_management(TB_RUTAS_PUNTOS_shp, "TB_VIVIEND" + field_delete)

    #for row in arcpy.da.SearchCursor(MZS_AEU_dbf, ["UBIGEO", "ZONA","MANZANA","AEU"]):

#
#def CrearAEULineas():
#
#    arcpy.MakeFeatureLayer_management(
#        "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp",
#        "rutas_lineas")
#


def CrearTB_AEUS():
    AEUS = "D:/ShapesPruebasSegmentacionUrbana/AEU/Renumerar/TB_AEUS.dbf"
    AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    AEUS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbana/AEU/Renumerar/TB_AEUS_PUNTOS.shp"
    RUTAS_LINEAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS.shp"
    #RUTAS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbana/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"


    if arcpy.Exists (AEUS):
        arcpy.Delete_management(AEUS)

    if arcpy.Exists (AEUS_LINEAS):
        arcpy.Delete_management(AEUS_LINEAS)

    #if arcpy.Exists (AEUS_PUNTOS):
    #    arcpy.Delete_management(AEUS_PUNTOS)

    arcpy.Statistics_analysis(MZS_AEU_dbf, AEUS, [["CANT_VIV", "SUM"]], ["UBIGEO","CODCCPP" ,"ZONA", "AEU_FINAL"])
    arcpy.Dissolve_management(RUTAS_LINEAS, AEUS_LINEAS, ["UBIGEO", "CODCCPP","ZONA", "AEU_FINAL"], [["CANT_VIV", "SUM"]])
    #arcpy.Dissolve_management(RUTAS_PUNTOS, AEUS_PUNTOS, ["UBIGEO", "ZONA", "AEU_FINAL"], [["CANT_VIV", "SUM"]])
    arcpy.AddField_management(AEUS, "CANT_VIV", "SHORT")

    arcpy.CalculateField_management(AEUS, "CANT_VIV",
                                    "[SUM_CANT_V]", "VB", "")

    arcpy.AddField_management(AEUS_LINEAS, "CANT_VIV", "SHORT")

    arcpy.CalculateField_management(AEUS_LINEAS, "CANT_VIV",
                                    "[SUM_CANT_V]", "VB", "")
    #arcpy.AddField_management(AEUS_PUNTOS, "CANT_VIV", "SHORT")

    #arcpy.CalculateField_management(AEUS_PUNTOS, "CANT_VIV",
    #                                "[SUM_CANT_V]", "VB", "")

    arcpy.DeleteField_management(AEUS, ["SUM_CANT_V"])
    arcpy.DeleteField_management(AEUS_LINEAS, ["SUM_CANT_V"])
    #arcpy.DeleteField_management(AEUS_LINEAS, ["SUM_CANT_V"])

def CrearMarcosCroquis(ubigeos):
    env.overwriteOutput = True
    arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbana"
    ZONA_AEU="in_memory//zona_aeu"
    ZONA_CENSAL="in_memory//zona_censal.shp"
    MZS_AEU="D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"

    MZS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp"

    MARCOS_FINAL = "D:/ShapesPruebasSegmentacionUrbana/AEU/Mapas/TB_MARCOS_AEUS.shp"

    if arcpy.Exists (MARCOS_FINAL):
        arcpy.Delete_management(MARCOS_FINAL)
    spatial_reference = arcpy.Describe(MZS).spatialReference


    arcpy.Statistics_analysis(MZS_AEU, ZONA_AEU, [["IDMANZANA", "COUNT"]], ["UBIGEO","CODCCPP" ,"ZONA", "AEU_FINAL"])

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


        out_feature = "in_memory//Marco"+str(row_cm_1[0])+str(row_cm_1[1])+str(row_cm_1[2])
        out_feature_2="in_memory//BufferDissolve"+str(row_cm_1[0])+str(row_cm_1[1])+str(row_cm_1[2])
        arcpy.FeatureEnvelopeToPolygon_management(in_features, out_feature)
        arcpy.Buffer_analysis(in_features, out_feature_2, "20 METERS", "", "","ALL")
        arcpy.FeatureEnvelopeToPolygon_management(out_feature_2, out_feature)

        arcpy.AddField_management(out_feature, "UBIGEO", "TEXT")
        arcpy.AddField_management(out_feature, "CODCCPP", "TEXT")
        arcpy.AddField_management(out_feature, "ZONA", "TEXT")
        arcpy.AddField_management(out_feature, "AEU_FINAL", "SHORT")
        arcpy.AddField_management(out_feature, "ID_MAPA", "TEXT")



        arcpy.CalculateField_management(out_feature,"UBIGEO",row_cm_1[0])
        arcpy.CalculateField_management(out_feature, "CODCCPP", row_cm_1[3])
        arcpy.CalculateField_management(out_feature, "ZONA", row_cm_1[1])
        arcpy.CalculateField_management(out_feature, "AEU_FINAL", int(row_cm_1[2]))
        arcpy.CalculateField_management(out_feature, "ID_MAPA", "[UBIGEO]&[CODCCPP]&[ZONA]&[AEU_FINAL]")
        if (j==0):
            arcpy.CopyFeatures_management(out_feature, MARCOS_FINAL)
        else:
            arcpy.Append_management(out_feature, MARCOS_FINAL)
        j=j+1



def Crear_Carpetas_Croquis_AEU(ubigeos):


    arcpy.MakeFeatureLayer_management(r"D:\ShapesPruebasSegmentacionUrbana\AEU\EnumerarAEUViviendas\TB_ZONA_CENSAL.shp",
                                      "zonas")

    where_list=ubigeos
    #where_list = ["020601", "021806", "110204"]


    if os.path.exists("D:/ShapesPruebasSegmentacionUrbana/AEU/CroquisUrbanoAEU")==False:
        os.mkdir("D:/ShapesPruebasSegmentacionUrbana/AEU/CroquisUrbanoAEU")

    #shutil.rmtree("D:/ShapesPruebasSegmentacionUrbana/Croquis/")
    lista_directorios=os.listdir("D:/ShapesPruebasSegmentacionUrbana/AEU/CroquisUrbanoAEU/")


    if len(lista_directorios)>0:
        for el in lista_directorios:
            shutil.rmtree("D:/ShapesPruebasSegmentacionUrbana/AEU/CroquisUrbanoAEU/"+str(el))



    where_expression = UBIGEO.ExpresionUbigeos(ubigeos)

    with arcpy.da.SearchCursor("zonas", ['UBIGEO', 'ZONA'],where_expression) as cursor:
        for row in cursor:
            os.mkdir("D:/ShapesPruebasSegmentacionUrbana/AEU/CroquisUrbanoAEU/Zona"+str(row[0])+str(row[1]))




def Exportar_Croquis_Urbano_AEU(ubigeos):
    arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbana"
    #ZONA_AEU = "D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/zona_aeu"
    #ZONA_CENSAL=r"D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp"
    #MZS_AEU="D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/MZS_AEU.dbf"
    #MZS_FINAL="D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_FINAL.shp"
    #MZS_TRABAJO = "D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbana\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    RUTAS_LINEAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS.shp"
    #RUTAS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbana/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"
    AEUS = "D:/ShapesPruebasSegmentacionUrbana/AEU/Renumerar/TB_AEUS.dbf"
    TB_MZS_shp = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    ZONA_CENSAL  = "D:/ShapesPruebasSegmentacionUrbana/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    #arcpy.Dissolve_management(MZS_TRABAJO,MZS_FINAL,["UBIGEO","ZONA","AEU_FINAL"],[["IDMANZANA","FIRST"]])

    #arcpy.MakeTableView_management(ZONA_AEU, "zona_aeu_x")
    #arcpy.MakeTableView_management(MZS_AEU, "mzs_aeu")
    #arcpy.MakeFeatureLayer_management(ZONA_CENSAL,"zonas")
    #arcpy.MakeFeatureLayer_management(RUTAS_LINEAS, "rutas")
    #arcpy.MakeFeatureLayer_management(RUTAS_PUNTOS, "rutas")
    arcpy.MakeTableView_management(AEUS, "aeus")

    where_expression=UBIGEO.ExpresionUbigeos(ubigeos)




    for row in arcpy.da.SearchCursor(AEUS, ["UBIGEO", "ZONA",  "AEU_FINAL","CANT_VIV"],where_expression):
        where_segundo = ' "UBIGEO"=\'' + str(row[0]) + '\' AND "ZONA" =\'' + str(row[1]) + '\' AND AEU_FINAL=' + str(row[2])
        where_zona =' "UBIGEO"=\'' + str(row[0]) + '\' AND "ZONA" =\'' + str(row[1]) + '\' '

        i=0
        where_temporal=""
        where_temporal2 = ""


        for row1 in arcpy.da.SearchCursor(MZS_AEU_dbf, ["IDMANZANA"],where_segundo):
            if (i == 0):

                where_temporal = ' "IDMANZANA"=\'' + str(row1[0]) + '\''
                #where_temporal2 = ' "MANZANA"=\'' + str(row1[2][11:]) + '\''
            else:
                where_temporal = where_temporal + ' OR "IDMANZANA"=\'' + str(row1[0]) + '\''
                #where_temporal2 = where_temporal2 + ' OR "MANZANA"=\'' + str(row1[2][11:]) + '\''

            i = i + 1

        where_rutas = where_segundo
        where_mapa = ' "UBIGEO"=\'' + str(int(row[0])) + '\' AND "ZONA" =\'' + str(int(row[1])) + '\' AND AEU_FINAL=' + str(int(row[2]))
        where_viviendas = where_segundo + ' AND ( USOLOCAL=1 OR USOLOCAL=3 ) '
        where_manzanas=where_temporal



        mxd = arcpy.mapping.MapDocument(
            r"D:/ShapesPruebasSegmentacionUrbana/AEU/Mxd/CroquisSegmentacionUrbanoFinal.mxd")
        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]


        arcpy.MakeFeatureLayer_management(TB_MZS_shp, "manzanas", where_manzanas)
        # arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp", "manzanas",where)
        arcpy.MakeFeatureLayer_management(RUTAS_LINEAS, "rutas_lineas", where_rutas)
        #arcpy.MakeFeatureLayer_management(RUTAS_PUNTOS, "rutas_puntos", where_rutas)

        arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS,"viviendas",where_viviendas)


        lyrFile1 = arcpy.mapping.Layer("rutas_lineas")
        lyrFile4 = arcpy.mapping.Layer("rutas_puntos")
        lyrFile2 = arcpy.mapping.Layer("viviendas")
        lyrFile3 = arcpy.mapping.Layer("manzanas")

        arcpy.ApplySymbologyFromLayer_management(lyrFile1,
                                                 "D:/ShapesPruebasSegmentacionUrbana/AEU/Layers/rutas_lineas.lyr")
        arcpy.ApplySymbologyFromLayer_management(lyrFile2,
                                                 "D:/ShapesPruebasSegmentacionUrbana/AEU/Layers/vivienda_final.lyr")
        arcpy.ApplySymbologyFromLayer_management(lyrFile3,
                                                 "D:/ShapesPruebasSegmentacionUrbana/AEU/Layers/manzana_final.lyr")
        arcpy.ApplySymbologyFromLayer_management(lyrFile4,
                                                 "D:/ShapesPruebasSegmentacionUrbana/AEU/Layers/rutas_puntos.lyr")
        arcpy.mapping.AddLayer(df, lyrFile1)
        arcpy.RefreshActiveView()

#       if lyrFile2.supports("LABELCLASSES"):
#           for lblclass in lyrFile2.labelClasses:
#               # lblclass.className = "[ORDEN]"
#               lblclass.expression = "[OR_VIV_AEU]"
#               lblclass.showClassLabels = False

#       lyrFile2.showLabels = False
        arcpy.RefreshActiveView()
        arcpy.mapping.AddLayer(df, lyrFile2)
        arcpy.RefreshActiveView()
        arcpy.mapping.AddLayer(df, lyrFile3)
        arcpy.RefreshActiveView()

        arcpy.mapping.AddLayer(df, lyrFile4)
        arcpy.RefreshActiveView()


        viv_aeu = int(row[3])
        #seccion = "0" * (3 - len(str(row1[3]))) + str(row1[3])
        aeu = "0" * (3 - len(str(row[2]))) + str(row[2])
        ubigeo = str(row[0])
        zona = UBIGEO.EtiquetaZona(str(row[1]))

        TextElement1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDD")[0]
        TextElement2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCPP")[0]
        TextElement3 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDI")[0]
        TextElement4 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DEPARTAMENTO")[0]
        TextElement5 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "PROVINCIA")[0]
        TextElement6 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DISTRITO")[0]
        TextElement7 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "NOMCCPP")[0]
        TextElement8 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "ZONA")[0]

        TextElement9 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "AEU")[0]
        #TextElement10 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "SECCION")[0]
        TextElement11 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "VIV_AEU")[0]

        TextElement1.text = ubigeo[0:2]
        TextElement2.text = ubigeo[2:4]
        TextElement3.text = ubigeo[4:6]
        TextElement8.text = zona
        TextElement9.text = str(aeu)
        #TextElement10.text = seccion
        TextElement11.text = str(viv_aeu)


        for row4 in arcpy.da.SearchCursor(ZONA_CENSAL, ['DEPARTAMEN', 'PROVINCIA', 'DISTRITO', 'NOMCCPP'],where_zona):
            TextElement4.text = str(row4[0])
            TextElement5.text = row4[1]
            TextElement6.text = row4[2]
            TextElement7.text = row4[3]


        ddp = mxd.dataDrivenPages
        indexLayer = ddp.indexLayer

        arcpy.SelectLayerByAttribute_management(indexLayer, "NEW_SELECTION", where_mapa)

        for indexPage in ddp.selectedPages:
            ddp.currentPageID = indexPage
           #arcpy.mapping.ExportToJPEG(mxd, r"D:/ShapesPruebasSegmentacionUrbana/AEU/CroquisUrbanoAEU/Zona" + str(
           #    row[0]) + str(
           #    row[1]) + "/Imagen" + str(row[0]) + str(row[1]) + str(row[2]) + ".jpeg", df,
           #                           df_export_width=1024,
           #                           df_export_height=1024,
           #                           resolution=1600, world_file=True)

            ddp.exportToPDF(r"D:/ShapesPruebasSegmentacionUrbana/AEU/CroquisUrbanoAEU/Zona"+str(row[0])+str(row[1])+"/Croquis"+str(row[0])+str(row[1])+str(row[2])+".pdf", "CURRENT")

        # arcpy.mapping.ExportToPNG(mxd,"D:/ShapesPruebasSegmentacionUrbana/Croquis/CroquiseEJEMPLO.png")
        # arcpy.mapping.PrintMap(mxd, r"\\pincullo\CANONiR4051-OEDS", df)
        arcpy.mapping.RemoveLayer(df, lyrFile1)
        arcpy.mapping.RemoveLayer(df, lyrFile2)
        arcpy.mapping.RemoveLayer(df, lyrFile3)

        # arcpy.mapping.RemoveLayer(df,lyrFile3)

        del mxd
        del df


            #Exportar_Croquis_Urbano_Zona_AEU(str(fila[0]),str(fila[1]))


#def Exportar_Croquis_Urbano_Zona_AEU(ubigeo, zona):
#    ZONAS = r"D:/ShapesPruebasSegmentacionUrbana/Zones/TB_ZONAS.shp"
#    MZS = "D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"
#    where_inicial = ' "UBIGEO"=\'' + str(ubigeo) + '\' AND "ZONA"=\'' + str(zona) + '\''
#
#    with arcpy.arcpy.da.SearchCursor("aeus", ['UBIGEO', 'ZONA', 'AEU_FINAL', 'SECCION', 'SUM_VIV_AE'],
#                                     where_inicial) as cursor1:
#        for row1 in cursor1:
#            where_segundo = ' "UBIGEO"=\'' + str(row1[0]) + '\' AND "ZONA" =\'' + str(
#                row1[1]) + '\' AND AEU_FINAL=' + str(row1[2])
#            where_expression_zona = ' "UBIGEO"=\'' + str(row1[0]) + '\' AND "ZONA"=\'' + str(row1[1]) + '\''
#            print  where_segundo
#            where_rutas = where_segundo
#            where_viviendas = where_segundo + ' AND ( USOLOCAL=1 OR USOLOCAL=3 ) '
#
#            i = 0
#            viv_aeu = int(row1[4])
#            seccion = "0" * (3 - len(str(row1[3]))) + str(row1[3])
#            aeu = "0" * (3 - len(str(row1[2]))) + str(row1[2])
#            ubigeo = str(row1[0])
#            zona = UBIGEO.EtiquetaZona(str(row1[1]))
#
#            with arcpy.arcpy.da.SearchCursor("mzs_aeu",
#                                             ['UBIGEO', 'ZONA', 'IDMANZANA', 'AEU_FINAL', 'VIV_AEU'],
#                                             where_segundo) as cursor3:
#                for row3 in cursor3:
#
#                    if i == 0:
#
#                        where_temporal = ' "IDMANZANA"=\'' + str(row3[2]) + '\''
#                        where_temporal2 = ' "MANZANA"=\'' + str(row3[2][11:]) + '\''
#                    else:
#                        where_temporal = where_temporal + ' OR "IDMANZANA"=\'' + str(row3[2]) + '\''
#                        where_temporal2 = where_temporal2 + ' OR "MANZANA"=\'' + str(row3[2][11:]) + '\''
#
#                    i = i + 1
#
#                    # viv_aeu=int(row3[4])+viv_aeu
#
#            where = where_temporal
#            where_rutas = where_rutas
#            where_viviendas = where_viviendas
#
#            where_mapa = ' "UBIGEO"=\'' + str(int(row1[0])) + '\' AND "ZONA" =\'' + str(
#                int(row1[1])) + '\' AND AEU_FINAL=' + str(int(row1[2]))
#            print where_mapa
#            # where_viviendas=' UBIGEO=\'021806\' AND "ZONA" =\'00800\' AND "MANZANA"=\'001O\' AND ( USOLOCAL=1 OR USOLOCAL=3 ) '
#            mxd = arcpy.mapping.MapDocument(
#                r"D:/ShapesPruebasSegmentacionUrbana/mxd/CroquisSegmentacionUrbano.mxd")
#            df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
#
#            arcpy.MakeFeatureLayer_management(MZS, "manzanas", where)
#            # arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp", "manzanas",where)
#            arcpy.MakeFeatureLayer_management("rutas", "rutas2", where_rutas)
#            arcpy.MakeFeatureLayer_management(
#                r"D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp", "viviendas",
#                where_viviendas)
#            arcpy.MakeFeatureLayer_management(ZONAS, "zonas", where_expression_zona)
#            TextElement1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDD")[0]
#            TextElement2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCPP")[0]
#            TextElement3 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDI")[0]
#            TextElement4 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DEPARTAMENTO")[0]
#            TextElement5 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "PROVINCIA")[0]
#            TextElement6 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DISTRITO")[0]
#            TextElement7 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "NOMCCPP")[0]
#            TextElement8 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "ZONA")[0]
#            # TextElement8 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CATEGORIACCPP")[0]
#            TextElement9 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "AEU")[0]
#            TextElement10 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "SECCION")[0]
#            TextElement11 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "VIV_AEU")[0]
#            # TextElement.text =str(row1[0])[0:2]
#            # -*- coding: 850 -*-
#
#            TextElement1.text = ubigeo[0:2]
#            TextElement2.text = ubigeo[2:4]
#            TextElement3.text = ubigeo[4:6]
#            TextElement8.text = zona
#            TextElement9.text = str(aeu)
#            TextElement10.text = seccion
#            TextElement11.text = str(viv_aeu)
#
#            for row4 in arcpy.da.SearchCursor("zonas", ['DEPARTAMEN', 'PROVINCIA', 'DISTRITO', 'NOMCCPP']):
#                TextElement4.text = str(row4[0])
#                TextElement5.text = row4[1]
#                TextElement6.text = row4[2]
#                TextElement7.text = row4[3]
#
#            lyrFile1 = arcpy.mapping.Layer("rutas2")
#            lyrFile2 = arcpy.mapping.Layer("viviendas")
#            lyrFile3 = arcpy.mapping.Layer("manzanas")
#            arcpy.ApplySymbologyFromLayer_management(lyrFile1,
#                                                     "D:/ShapesPruebasSegmentacionUrbana/Layers/rutas_final.lyr")
#            arcpy.ApplySymbologyFromLayer_management(lyrFile2,
#                                                     "D:/ShapesPruebasSegmentacionUrbana/Layers/vivienda_final.lyr")
#            arcpy.ApplySymbologyFromLayer_management(lyrFile3,
#                                                     "D:/ShapesPruebasSegmentacionUrbana/Layers/manzana_final.lyr")
#            arcpy.mapping.AddLayer(df, lyrFile1)
#            arcpy.RefreshActiveView()
#
#            if lyrFile2.supports("LABELCLASSES"):
#                for lblclass in lyrFile2.labelClasses:
#                    # lblclass.className = "[ORDEN]"
#                    lblclass.expression = "[OR_VIV_AEU]"
#                    lblclass.showClassLabels = False
#
#            lyrFile2.showLabels = False
#            arcpy.RefreshActiveView()
#            arcpy.mapping.AddLayer(df, lyrFile2)
#            arcpy.RefreshActiveView()
#            arcpy.mapping.AddLayer(df, lyrFile3)
#            arcpy.RefreshActiveView()
#
#            # for el in arcpy.mapping.ListDataFrames(mxd):
#            #    print el.name
#            # for el2 in arcpy.mapping.ListLayers(mxd):
#            #    print el2.name
#            ddp = mxd.dataDrivenPages
#            indexLayer = ddp.indexLayer
#
#            arcpy.SelectLayerByAttribute_management(indexLayer, "NEW_SELECTION", where_mapa)
#
#            # mxd = arcpy.mapping.MapDocument(r"C:\Project\Project.mxd")
#
#
#
#            # df_mapa = arcpy.mapping.ListDataFrames(mxd, "Mapa")[0]
#
#
#
#
#
#            for indexPage in ddp.selectedPages:
#                ddp.currentPageID = indexPage
#                arcpy.mapping.ExportToJPEG(mxd, r"D:/ShapesPruebasSegmentacionUrbana/Croquis/Zona" + str(
#                    row1[0]) + str(
#                    row1[1]) + "/Imagen" + str(row1[0]) + str(row1[1]) + str(row1[2]) + ".jpeg", df,
#                                           df_export_width=1024,
#                                           df_export_height=1024,
#                                           resolution=1600, world_file=True)
#
#                # ddp.exportToPDF(r"D:/ShapesPruebasSegmentacionUrbana/Croquis/Zona"+str(row1[0])+str(row1[1])+"/Croquis"+str(row1[0])+str(row1[1])+str(row1[2])+".pdf", "CURRENT")
#
#            # arcpy.mapping.ExportToPNG(mxd,"D:/ShapesPruebasSegmentacionUrbana/Croquis/CroquiseEJEMPLO.png")
#            # arcpy.mapping.PrintMap(mxd, r"\\pincullo\CANONiR4051-OEDS", df)
#            arcpy.mapping.RemoveLayer(df, lyrFile1)
#            arcpy.mapping.RemoveLayer(df, lyrFile2)
#            arcpy.mapping.RemoveLayer(df, lyrFile3)
#
#            # arcpy.mapping.RemoveLayer(df,lyrFile3)
#
#            del mxd
#            del df
#

ubigeos = ["020601","021806","110204"]
conx.ActualizarCantViviendasMzs()
print "ActualizarCantViviendasMzs"
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
#Ruta="D:\ShapesPruebasSegmentacionUrbana\AEU\MatrizAdyacencia"
#Lista_adyacencia="lista_adyacencia.dbf"
#ie.Importar_Lista_ADYACENCIA(Ruta,Lista_adyacencia)
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
##CrearRutasPuntos(ubigeos)
##print "CrearRutasPuntos"



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
#
#CrearLineasAEUPrimeraPasada()
#print "CrearLineasAEUPrimeraPasada"
#print datetime.today()
#
#ActualizarRutasViviendasMenoresIguales16()
#print "ActualizarRutasViviendasMenoresIguales16"
#print datetime.today()
#
#CrearLineasAEUFinal()
#print "CrearLineasAEUFinal"
#print datetime.today()
#
##CrearLineasAEUSegundaPasada()
##print "CrearLineasAEUSegundaPasada"
#
#
##ActualizarRutasViviendasMenoresIguales16()
##print "ActualizarRutasViviendasMenoresIguales16"
##print datetime.today()
#
#CrearTablaSegundaPasada()
#print "CrearTablaSegundaPasada"
#print datetime.today()
##ActualizarRutasAEUSegundaPasada()
##print "ActualizarRutasAEUSegundaPasada"
##print datetime.today()
#
#Renumerar_AEU()
#print "Renumerar_AEU"
#print datetime.today()
#RenumerarRutas()
#print "RenumerarRutas"
#print datetime.today()
#CrearMarcosCroquis(ubigeos)
#print "CrearMarcosCroquis"
#print datetime.today()
#CrearTB_AEUS()
#print "CrearTB_AEUS"
#print datetime.today()
#


SegmEspSeccion.EnumerarSecciones()
print "EnumerarSecciones"
SegmEspSeccion.CrearMarcosSecciones()
print "CrearMarcosSecciones"




#print "CrearTB_AEUS"
#print datetime.today()
#

#Crear_Carpetas_Croquis_AEU(ubigeos)
#print "Crear_Carpetas_Croquis_AEU"
#Exportar_Croquis_Urbano_AEU(ubigeos)
#print "Exportar_Croquis_Urbano_AEU"










#ie.Importar_Lista_ADYACENCIA()