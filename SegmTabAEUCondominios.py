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




def CopiarTablas():
    env.overwriteOutput = True
    lista=[["D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp","D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"],
           ["D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp","D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp"],
           ["D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp","D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"],
           ["D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/PuntosInicio/PUNTOS_INICIO.shp","D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/PuntosInicio/PUNTOS_INICIO.shp"]
          ]

    for el in lista:
        arcpy.Copy_management(el[0],el[1])

def OrdenarManzanasFalsoCod():
    MZS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    MZS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_MZS_ORDENADAS.shp"
    if arcpy.Exists(MZS_ORDENADAS):
        arcpy.Delete_management(MZS_ORDENADAS)
    arcpy.Sort_management(MZS, MZS_ORDENADAS, ["UBIGEO", "ZONA", "FALSO_COD" ])


def CrearViviendasOrdenadas():
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbanaTabularCondominios"
    VIVIENDAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"

    if arcpy.Exists(VIVIENDAS_ORDENADAS):
        arcpy.Delete_management(VIVIENDAS_ORDENADAS)

    arcpy.Sort_management(VIVIENDAS, VIVIENDAS_ORDENADAS, ["UBIGEO", "ZONA", "MANZANA", "ID_REG_OR"])
    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "AEU", "SHORT")
    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "OR_VIV_AEU", "SHORT")
    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "FLG_CORTE", "SHORT")
    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "FLG_MZ", "SHORT")



def EnumerarAEUEnViviendasDeManzanas(ubigeos):
    arcpy.env.overwriteOutput = True
    MZS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_MZS_ORDENADAS.shp"
    VIVIENDAS="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    ZONAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    VIVIENDAS_AEU_OR_MAX="in_memory//VIVIENDAS_AEU_OR_MAX"
    VIVIENDAS_MZS_OR_MAX = "in_memory//VIVIENDAS_MZS_OR_MAX"
    MZS_CONDOMINIOS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS_CONDOMINIOS.dbf"

    where_list=ubigeos
    m = 0
    where_expression = ""
    arcpy.AddField_management(MZS_ORDENADAS, "AEU", "SHORT")
    where_expression=UBIGEO.ExpresionUbigeos(ubigeos)




    for row in arcpy.da.SearchCursor(ZONAS,["UBIGEO", "ZONA"],where_expression):
        where_expression1 = "UBIGEO=\'" + str(row[0]) + "\' AND ZONA=\'" + str(row[1]) + "\' "
        numero_aeu = 1


        cant_vivi_agrupadas=0
        anterior_manzana=0
        cant_viv_anterior_manzana=0
        or_viv_aeu=1



        with arcpy.da.UpdateCursor(MZS_ORDENADAS,["UBIGEO", "ZONA", "MANZANA", "IDMANZANA", "VIV_MZ","MZS_COND" ],where_expression1) as cursor1:
            for row1 in cursor1:
                cant_viv=int(row1[4])



                if (cant_viv>16):

                    where_expression_viv = " UBIGEO=\'" + str(row1[0]) + "\'  AND  ZONA=\'" + str(
                        row1[1]) + "\' AND MANZANA=\'" + str(row1[2]) + "\'"
                    mzs_cond = int(row1[5])

                    #Aqui se hace referencia a la manzana anterior
                    if anterior_manzana==1:  # la anterior manzana es una menor o igual a 16 viviendas
                        if cant_vivi_agrupadas!=0:

                            numero_aeu=numero_aeu+1
                        else:
                            print cant_vivi_agrupadas

                    cant_vivi_agrupadas = 0
                    anterior_manzana = 2  ##si la manzana es con mas de 16 viv entonces 2



                    if (mzs_cond==0):
                        division=float(cant_viv)/16.0
                        cant_aeus=math.ceil(division)
                        residuo=cant_viv%cant_aeus
                        viv_aeu=cant_viv/cant_aeus
                        i=0
                        or_viv_aeu=1

                        #where_expression_viv = " UBIGEO=\'" + str(row1[0]) + "\'  AND  ZONA=\'" + str(row1[1]) + "\' AND MANZANA=\'" + str(row1[2])+"\'"
                        edificacion_anterior=0
                        numero_aeu_anterior=0
                        idmanzana_anterior=""

                        cant_aeus_aux = 0

                        with arcpy.da.UpdateCursor (VIVIENDAS_ORDENADAS, ["UBIGEO", "ZONA", "MANZANA", "ID_REG_OR", "AEU", "OR_VIV_AEU", "P19A",
                                                "P29", "FLG_MZ","P23"],where_expression_viv ) as cursor2:
                            for row2 in cursor2:
                                row2[8] = 1
                                idmanzana = str(row2[0]) + str(row2[1]) + str(row2[2])
                                usolocal = int(row2[7])

                                edificacion = int(row2[6])

                                if (usolocal in [1, 3]):
                                    row2[4] = numero_aeu
                                    row2[5] = or_viv_aeu
                                    or_viv_aeu = or_viv_aeu + 1

                                elif (usolocal == 6):
                                    row2[4] = 0

                                else:
                                    if or_viv_aeu != 1:
                                        row2[4] = numero_aeu
                                    else:
                                        if idmanzana == idmanzana_anterior:
                                            if edificacion == edificacion_anterior:
                                                row2[4] = numero_aeu_anterior
                                            elif (edificacion != edificacion_anterior and cant_aeus_aux == cant_aeus):
                                                row2[4] = numero_aeu_anterior
                                            elif (edificacion == 1 and edificacion_anterior != 1):
                                                row2[4] = numero_aeu_anterior
                                            else:
                                                row2[4] = numero_aeu


                                        else:
                                            row2[4] = numero_aeu
                                            # row2[4] = numero_aeu_anterior

                                if residuo > 0:
                                    if or_viv_aeu > (viv_aeu + 1):
                                        i = 1
                                        edificacion_anterior = edificacion
                                        numero_aeu_anterior = numero_aeu
                                        idmanzana_anterior = idmanzana
                                        numero_aeu = numero_aeu + 1
                                        residuo = residuo - 1
                                        or_viv_aeu = 1
                                        cant_aeus_aux = cant_aeus_aux + 1

                                else:
                                    if or_viv_aeu > (viv_aeu):
                                        edificacion_anterior = edificacion
                                        numero_aeu_anterior = numero_aeu
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

                        # arcpy.Statistics_analysis("condominios", VIVIENDAS_AEU_OR_MAX, [["ID_REG_OR", "MAX"]],["UBIGEO", "ZONA", "MANZANA","AEU"])

                        for condominios in [[str(x[0]), str(x[1]), str(x[2]), int(x[3]), int(x[4])] for x in
                                            arcpy.da.SearchCursor(MZS_CONDOMINIOS,
                                                                  ["UBIGEO", "ZONA", "MANZANA", "CONDOMINIO",
                                                                   "VIV_COND"], where_expression_viv)]:
                            cant_viv_cond = condominios[4]

                            if (cant_viv_cond == 0):
                                cant_aeu_condominio = 1
                                viv_aeu_condominio = 0
                                res_viv_condominio = 0
                            else:
                                ##########cant aeu_condominio es la cantidad de aeus por block ########################
                                cant_aeu_condominio = int(math.ceil(float(condominios[4]) / 16.0))
                                ##########viv_aeu_block es la cantidad de viviendas por block#####################
                                viv_aeu_condominio = int(condominios[4]) / int(cant_aeu_condominio)
                                ##########res_viv_block es el residuo de viviendas por block######################

                                res_viv_condominio = int(condominios[4]) % int(cant_aeu_condominio)



                            or_viv_aeu = 1



                            where_expression_viv_cond = " UBIGEO=\'" + condominios[0] + "\'  AND  ZONA=\'" + \
                                                        condominios[1] + "\' AND MANZANA=\'" + condominios[
                                                            2] + "\' AND  P19A=" + str(condominios[3])

                            print  where_expression_viv_cond

                            with arcpy.da.UpdateCursor(VIVIENDAS_ORDENADAS,
                                                       ["UBIGEO", "ZONA", "MANZANA", "ID_REG_OR", "AEU", "OR_VIV_AEU",
                                                        "P19A",
                                                        "P29", "FLG_MZ", "P23"], where_expression_viv_cond) as cursor2:
                                for row2 in cursor2:
                                    # flg manzana en 1
                                    row2[8] = 1
                                    idmanzana = str(row2[0]) + str(row2[1]) + str(row2[2])
                                    usolocal = int(row2[7])

                                    condominio = int(row2[6])

                                    # condominio=int(row2[9])
                                    # print  bloque
                                    if (usolocal in [1, 3]):
                                        row2[4] = numero_aeu
                                        row2[5] = or_viv_aeu
                                        or_viv_aeu = or_viv_aeu + 1
                                    elif (usolocal == 6):
                                        row2[4] = 0

                                    else:
                                        if or_viv_aeu != 1:
                                            row2[4] = numero_aeu


                                        else:

                                            if condominio == condominio_anterior:
                                                row2[4] = numero_aeu_anterior
                                            else:
                                                row2[4] = numero_aeu


                                    if res_viv_condominio > 0:

                                        if or_viv_aeu > (viv_aeu_condominio + 1):
                                            i = 1
                                            condominio_anterior = condominio
                                            numero_aeu_anterior = numero_aeu
                                            idmanzana_anterior = idmanzana
                                            numero_aeu = numero_aeu + 1
                                            residuo = residuo - 1
                                            or_viv_aeu = 1

                                    else:


                                        if or_viv_aeu > (viv_aeu_condominio):
                                            condominio_anterior = condominio
                                            numero_aeu_anterior = numero_aeu
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

                    anterior_manzana = 1  ##si la manzana es menor igual a 16 viv entonces la anterior manzana tiene valor 1


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






def CrearMZS_AEU(ubigeos):
    arcpy.env.overwriteOutput = True
    MZS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_MZS_ORDENADAS.shp"
    MZS_AEU_1 = "in_memory//MZS_AEU_1"
    MZS_AEU_2 = "in_memory//MZS_AEU_2"
    MZS_AEU = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"
    MZS_MENORES_16="in_memory//MZS_MENORES_16"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
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
    arcpy.Delete_management(MZS_AEU_1)
    arcpy.Delete_management(MZS_AEU_2)




def RenumerarViviendasMzsMenores16(ubigeos):
    arcpy.env.overwriteOutput = True

    MZS_AEU = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"

    MZS_AEU_SELECC = "MZS_AEU_SELECC"
    AEU = "in_memory/AEU"

    AEU_SELECC = "in_memory/AEU_SELECC"
    #where_expression = "("+UBIGEO.ExpresionUbigeos(ubigeos)+")  AND CANT_VIV<=16"
    #print  where_expression
    #arcpy.MakeTableView_management(MZS_AEU,MZS_AEU_SELECC)
    #arcpy.Select_analysis(MZS_AEU,MZS_AEU_SELECC,where_expression)

    arcpy.Statistics_analysis(MZS_AEU, AEU, [["MANZANA", "COUNT"]],
                              ["UBIGEO", "CODCCPP", "ZONA", "AEU"])
    where=" COUNT_MANZANA>1"

    arcpy.MakeTableView_management(AEU, AEU_SELECC,where)

    #where_expression=UBIGEO.ExpresionUbigeos(ubigeos)

    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"

    #arcpy.Sort_management(MZS_AEU, ["UBIGEO", "CODCCPP", "ZONA", "AEU", "AEU"])

    for row1 in arcpy.da.SearchCursor(AEU_SELECC, ["UBIGEO", "ZONA","AEU"]):
        where_expression_viv = " UBIGEO=\'" + str(row1[0]) + "\'  AND  ZONA=\'" + str(
            row1[1]) + "\' AND AEU=" + str(row1[2])
        print where_expression_viv
        or_viv_aeu=1
        with arcpy.da.UpdateCursor(VIVIENDAS_ORDENADAS,
                                   ["UBIGEO", "ZONA", "MANZANA", "ID_REG_OR", "AEU", "OR_VIV_AEU", "EDIFICACIO",
                                    "USOLOCAL", "COND_USOLO", "FLG_CORTE", "FLG_MZ"], where_expression_viv) as cursor2:
            for row2 in cursor2:

                usolocal = int(row2[7])


                #edificacion = int(row2[6])

                if (usolocal in [1, 3]):  # or (usolocal==6 and (usolocal_cond in [1,3])):
                    row2[5] = or_viv_aeu
                    or_viv_aeu = or_viv_aeu + 1

                cursor2.updateRow(row2)




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

    arcpy.Statistics_analysis(VIVIENDAS_ORDENADAS, VIVIENDAS_MZS_MAX_AEU, [["AEU", "MAX"]],
                              ["UBIGEO", "ZONA", "MANZANA"])

    arcpy.AddField_management(TB_VERTICES_FINAL_Layer,"IDMANZANA", "TEXT")
    arcpy.CalculateField_management(TB_VERTICES_FINAL_Layer, "IDMANZANA", "!UBIGEO!+!ZONA!+!MANZANA!","PYTHON_9.3")


    arcpy.AddField_management(VIVIENDAS_MZS_MAX_AEU, "IDMANZANA", "TEXT")
    arcpy.CalculateField_management(VIVIENDAS_MZS_MAX_AEU, "IDMANZANA", "!UBIGEO!+!ZONA!+!MANZANA!", "PYTHON_9.3")



    arcpy.AddJoin_management(TB_VERTICES_FINAL_Layer,"IDMANZANA",VIVIENDAS_MZS_MAX_AEU,"IDMANZANA")

    arcpy.CopyFeatures_management(TB_VERTICES_FINAL_Layer, TB_VERTICES_FINAL_AEU)



    add_field = [["UBIGEO","TEXT"], ["CODCCPP","TEXT"], ["ZONA","TEXT"], ["MANZANA","TEXT"], ["AEU","SHORT"]]

    for el in add_field:
        arcpy.AddField_management(TB_VERTICES_FINAL_AEU,el[0],el[1])

    calculate_field= [["UBIGEO","!TB_VERTICE!"],["ZONA","!TB_VERTI_1!"],["ZONA","!TB_VERTI_2!"],["MANZANA","!TB_VERTI_3!"],["AEU","!tb_vivie_6!"]]


    for el in calculate_field:
        arcpy.CalculateField_management(TB_VERTICES_FINAL_AEU,el[0],el[1],"PYTHON_9.3")



    list_deletefield = ["TB_VERTICE", "tb_viviend"]
    for el in range(1,7):
        list_deletefield.append("TB_VERTI_" + str(el))
    for el in range(1,8):
        list_deletefield.append("tb_vivie_"+str(el))

    arcpy.DeleteField_management(TB_VERTICES_FINAL_AEU, list_deletefield)


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
    AEUS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Renumerar/TB_AEUS.dbf"
    AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    RUTAS_LINEAS = "D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    SECCIONES="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/SECCIONES/EnumerarSecciones/TB_SECCIONES.shp"

    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"

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
    TB_AEUS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Renumerar/TB_AEUS.dbf"
    TB_AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    TB_RUTAS_LINEAS = "D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
    TB_RUTAS="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"
    TB_SECCIONES = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/SECCIONES/EnumerarSecciones/TB_SECCIONES.shp"
    TB_VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    TB_MARCOS_AEUS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Mapas/TB_MARCOS_AEUS.shp"
    TB_MARCOS_SECCIONES = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/SECCIONES/Mapas/TB_MARCOS_SECCIONES.shp"


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




ubigeos=["150116"]
#print datetime.today()
#CopiarTablas()
#print "CopiarTablas"
#print datetime.today()
#OrdenarManzanasFalsoCod()
#print "OrdenarManzanasFalsoCod"
#print datetime.today()
#CrearViviendasOrdenadas()
#print "CrearViviendasOrdenadas"
print datetime.today()
EnumerarAEUEnViviendasDeManzanas(ubigeos)
print "EnumerarAEUEnViviendasDeManzanas"
#print datetime.today()
#CrearMZS_AEU(ubigeos)
#print "CrearMZS_AEU"
#print datetime.today()#
#RenumerarViviendasMzsMenores16(ubigeos)
#print "RenumerarViviendasMzsMenores16"
#print datetime.today()  #
#CrearRutasPuntos()
#print "CrearRutasPuntos"
#print datetime.today()  #
#
#RelacionarVerticeFinalInicioConAEUMax()
#print "RelacionarVerticeFinalInicioConAEUMax"
#print datetime.today()  #
#
#CrearRutasPreparacion()
#print "CrearRutasPreparacion"
#print datetime.today()  #
#
#RelacionarRutasLineasConAEU()
#
#print "CrearRutasPreparacion"
#print datetime.today()  #
#
#CrearTB_AEUS()
#
#print "CrearTB_AEUS"
#print datetime.today()  #