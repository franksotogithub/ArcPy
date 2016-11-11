import random
import math
import numpy as np
import os
import shutil
import arcpy
import  SolucionInicialUrbano as s
from arcpy import env
import  UBIGEO



def CopiarTablas():
    env.overwriteOutput = True
    lista=[["D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp","D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"],
           ["D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp","D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp"],
           ["D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp","D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"],
           ["D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS_CONDOMINIOS.dbf",
            "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_MZS_CONDOMINIOS.dbf"],
           ["D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/PuntosInicio/PUNTOS_INICIO.shp","D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/PuntosInicio/PUNTOS_INICIO.shp"],

          ]

    for el in lista:
        arcpy.Copy_management(el[0],el[1])

    MZS="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    arcpy.DeleteField_management(MZS,["AEU_2"])

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






def EnumerarAEUEnViviendasDeManzanas(where_expression):
    arcpy.env.overwriteOutput = True
    MZS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_MZS_ORDENADAS.shp"
    VIVIENDAS="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    ZONAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    VIVIENDAS_AEU_OR_MAX="in_memory//VIVIENDAS_AEU_OR_MAX"
    VIVIENDAS_MZS_OR_MAX = "in_memory//VIVIENDAS_MZS_OR_MAX"
    MZS_CONDOMINIOS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_MZS_CONDOMINIOS.dbf"

    #where_list=ubigeos
    m = 0
    #where_expression = ""

    #where_expression=UBIGEO.ExpresionUbigeos(ubigeos)

    for row in arcpy.da.SearchCursor(ZONAS,["UBIGEO", "ZONA"],where_expression):
        where_expression1 = "UBIGEO=\'" + str(row[0]) + "\' AND ZONA=\'" + str(row[1]) + "\' "
        numero_aeu = 1


        cant_vivi_agrupadas=0
        anterior_manzana=0
        cant_viv_anterior_manzana=0
        or_viv_aeu=1


        with arcpy.da.UpdateCursor(MZS_ORDENADAS,["UBIGEO", "ZONA", "MANZANA", "FALSO_COD", "VIV_MZ","MZS_COND","AEU" ],where_expression1) as cursor1:
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

                        condominio_anterior = 0
                        numero_aeu_anterior = 0



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


                    with arcpy.da.UpdateCursor(VIVIENDAS_ORDENADAS,
                                               ["UBIGEO", "ZONA", "MANZANA", "ID_REG_OR", "AEU", "OR_VIV_AEU", "P19A",
                                                "P29", "FLG_MZ", "P23"], where_expression_viv) as cursor2:
                        for row2 in cursor2:
                            row2[8] = 0
                            row2[4] = numero_aeu
                            usolocal = int(row2[7])

                            if (usolocal in [1, 3]):
                                row2[5] = or_viv_aeu
                                or_viv_aeu = or_viv_aeu + 1
                            cursor2.updateRow(row2)
                    del cursor2

                    #with arcpy.da.UpdateCursor (VIVIENDAS_ORDENADAS, ["UBIGEO","ZONA","MANZANA","ID_REG_OR","AEU", "OR_VIV_AEU","EDIFICACIO","USOLOCAL","COND_USOLO","FLG_CORTE","FLG_MZ"],where_expression_viv ) as cursor2:
                    #    for row2 in cursor2:
                    #        row2[10] = 0
                    #        usolocal = int(row2[7])
                    #        usolocal_cond = int(row2[8])
                    #        row2[4] = numero_aeu
                    #        edificacion = int(row2[6])
#
                    #        if (usolocal in [1, 3]):  # or (usolocal==6 and (usolocal_cond in [1,3])):
                    #            row2[5] = or_viv_aeu
                    #            or_viv_aeu = or_viv_aeu + 1
#
                    #        cursor2.updateRow(row2)
#
                    #del cursor2

                row1[6]=int(numero_aeu)
                cursor1.updateRow(row1)




def CrearMZS_AEU(where_expression):
    arcpy.env.overwriteOutput = True
    MZS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_MZS_ORDENADAS.shp"
    MZS_AEU_1 = "in_memory//MZS_AEU_1"
    MZS_AEU_2 = "in_memory//MZS_AEU_2"
    MZS_AEU = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"
    MZS_MENORES_16="in_memory//MZS_MENORES_16"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"


    if arcpy.Exists(MZS_AEU):
        arcpy.Delete_management(MZS_AEU)

    #where_expresion= UBIGEO.ExpresionUbigeos(ubigeos)
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
                              ["UBIGEO", "CODCCPP","ZONA", "MANZANA", "AEU","FALSO_COD","VIV_MZ"])
    arcpy.AddField_management(MZS_MENORES_16, "CANT_VIV", "SHORT")
    expression = "!VIV_MZ!"
    arcpy.CalculateField_management(MZS_MENORES_16, "CANT_VIV", expression, "PYTHON_9.3")
    arcpy.DeleteField_management(MZS_MENORES_16, ['FID_','FREQUENCY','COUNT_MANZANA','VIV_MZ'])
    arcpy.Merge_management([MZS_AEU_1, MZS_MENORES_16],MZS_AEU_2 )
    arcpy.Sort_management(MZS_AEU_2, MZS_AEU, ["UBIGEO","CODCCPP","ZONA","FALSO_COD","AEU"])
    arcpy.Delete_management(MZS_AEU_1)
    arcpy.Delete_management(MZS_AEU_2)


def CrearViviendasCortes():
    arcpy.env.overwriteOutput = True
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    VIVIENDAS_AEU_OR_MAX_Stadistics = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/VIVIENDAS_AEU_OR_MAX_Stadistics"
    VIVIENDAS_MZS_OR_MAX_Stadistics = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/VIVIENDAS_MZS_OR_MAX_Stadistics"
    VIVIENDAS_AEU_OR_MAX = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/VIVIENDAS_AEU_OR_MAX.shp"
    VIVIENDAS_MZS_OR_MAX = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/VIVIENDAS_MZS_OR_MAX.shp"

    TB_VIVIENDAS_CORTES_shp = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_VIVIENDAS_CORTES.shp"

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


def RenumerarViviendasMzsMenores16(where_expression):
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
                                   ["UBIGEO", "ZONA", "MANZANA", "ID_REG_OR", "AEU", "OR_VIV_AEU",
                                    "P29"], where_expression_viv) as cursor2:
            for row2 in cursor2:

                usolocal = int(row2[6])


                #edificacion = int(row2[6])

                if (usolocal in [1, 3]):  # or (usolocal==6 and (usolocal_cond in [1,3])):
                    row2[5] = or_viv_aeu
                    or_viv_aeu = or_viv_aeu + 1

                cursor2.updateRow(row2)



def CrearRutasPuntos():
    arcpy.env.overwriteOutput = True
    TB_RUTAS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    PUERTAS_VIVIENDAS_MULTIFAMILIAR = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_PUERTAS_VIVIENDAS_MULTIFAMILIAR.shp"
    VIVIENDAS_ORDENADAS_MULTIFAMILIAR = "VIVIENDAS_ORDENADAS_MULTIFAMILIAR"
    VIVIENDAS_ORDENADAS_MULTIFAMILIAR_2="VIVIENDAS_ORDENADAS_MULTIFAMILIAR_2"
    TB_RUTAS_PUNTOS_MIN = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_MIN.shp"
    TB_RUTAS_PUNTOS_CANT_AEU_IGUAL_1 = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_CANT_AEU_IGUAL_1"
    TB_RUTAS_PUNTOS_AEU_IDENTICOS="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_AEU_IDENTICOS"
    TB_RUTAS_PUNTOS_MIN_SELECT="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_MIN_SELECT.shp"
    spatial_reference = arcpy.Describe(VIVIENDAS_ORDENADAS).spatialReference
    where = "P29=6"
    where2 = "P29M=1 OR P29M=3"
    arcpy.Select_analysis(VIVIENDAS_ORDENADAS, PUERTAS_VIVIENDAS_MULTIFAMILIAR, where)

    arcpy.DeleteIdentical_management(PUERTAS_VIVIENDAS_MULTIFAMILIAR,["UBIGEO","CODCCPP","ZONA","MANZANA","P19A"])
    arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS, VIVIENDAS_ORDENADAS_MULTIFAMILIAR, where2)
    arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS,VIVIENDAS_ORDENADAS_MULTIFAMILIAR_2,where2)

    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"

    AEU_MULTIFAMILIAR = "in_memory/aeu_multifamiliar"
    AEU_MULTIFAMILIAR_ID_REG_OR="in_memory/aeu_multifamiliar_id_reg_or"
    AEU_MULTIFAMILIAR_Layer="AEU_MULTIFAMILIAR_Layer"

    # arcpy.CreateFeatureclass_management(out_path, out_name, geometry_type, template, has_m, has_z, spatial_reference)


    if arcpy.Exists(TB_RUTAS_PUNTOS):
        arcpy.Delete_management(TB_RUTAS_PUNTOS)
    if arcpy.Exists(TB_RUTAS_PUNTOS_MIN):
        arcpy.Delete_management(TB_RUTAS_PUNTOS_MIN)

    if arcpy.Exists(TB_RUTAS_PUNTOS) == False:
        arcpy.CreateFeatureclass_management("D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU",
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

                point = arcpy.Point(row[5][0], row[5][1])
                rowArray = [point, str(row2[0]), str(row2[1]), str(row2[2]), str(row2[3]), str(row2[5]), str(row2[6]),str(row2[7])]
                cursor_insert.insertRow(rowArray)


    sort_fields = [["UBIGEO", "ASCENDING"], ["CODCCPP", "ASCENDING"], ["ZONA", "ASCENDING"],
                               ["MANZANA", "ASCENDING"],
                               ["AEU", "ASCENDING"], ["ID_REG_OR", "ASCENDING"]]



    arcpy.Sort_management(TB_RUTAS_PUNTOS, TB_RUTAS_PUNTOS_MIN, sort_fields)

    arcpy.DeleteIdentical_management(TB_RUTAS_PUNTOS_MIN, ["Shape"])



def RelacionarVerticeFinalInicioConAEUMax():
    arcpy.env.overwriteOutput = True
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    VIVIENDAS_MZS_MAX_AEU = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_MZS_MAX_AEU"
    TB_VERTICES_FINAL = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_VERTICES_FINAL.shp"
    TB_VERTICES_FINAL_Layer="TB_VERTICES_FINAL_Layer"
    TB_VERTICES_FINAL_AEU = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_VERTICES_FINAL_AEU.shp"

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

    TB_VIVIENDAS_ORDENADAS_shp = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    TB_MZS_shp = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    TB_RUTAS_PUNTOS_MIN = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_MIN.shp"
    TB_RUTAS_PUNTOS_MIN_SELECT = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_MIN_SELECT.shp"

    TB_VIVIENDAS_CORTES_shp = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_VIVIENDAS_CORTES.shp"
    TB_MZS_LINE_shp = "in_memory/TB_MZS_LINE"
    TB_MZS_TRABAJO_BUFFER_shp = "in_memory/TB_MZS_TRABAJO_BUFFER"
    PUNTOINICIO_BUFFER_shp = "in_memory/PUNTOINICIO_BUFFER"
    TB_MZS_ERASE_shp = "in_memory/TB_MZS_ERASE"
    PUNTOS_INICIO_shp = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/PuntosInicio/PUNTOS_INICIO.shp"
    TB_SPLIT_shp = "in_memory/TB_SPLIT"
    TB_DISSOLVE_shp = "in_memory/TB_DISSOLVE"
    TB_CORTES_Buffer = "in_memory/TB_VIVIENDAS_CORTES_Buffer"

    TB_RUTAS_DISSOLVE_ERASE_shp_2="in_memory/TB_RUTAS_DISSOLVE_ERASE_2"

    TB_RUTAS_PREPARACION_shp = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PREPARACION.shp"
    TB_VERTICES_FINAL = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_VERTICES_FINAL.shp"
    TB_PUNTOS_CORTE_Merge="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_PUNTOS_CORTE_Merge.shp"

    TB_PUNTOS_CORTE_Merge_Ord="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_PUNTOS_CORTE_Merge_Ord.shp"

    if arcpy.Exists(TB_VERTICES_FINAL):
        arcpy.Delete_management(TB_VERTICES_FINAL)
    if arcpy.Exists(TB_RUTAS_PREPARACION_shp):
        arcpy.Delete_management(TB_RUTAS_PREPARACION_shp)


    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbanaTabularCondominios"

    MZS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    expression_2 = "flg_manzana(!VIV_MZ!)"
    codeblock = """def flg_manzana(VIV_MZ):\n  if (VIV_MZ>16):\n    return 1\n  else:\n    return 0"""

    arcpy.DeleteField_management(MZS,["FLG_MZ"])
    arcpy.AddField_management(MZS, "FLG_MZ","SHORT" )
    arcpy.CalculateField_management(MZS, "FLG_MZ", expression_2, "PYTHON_9.3", codeblock)
    arcpy.Buffer_analysis(TB_MZS_shp, TB_MZS_TRABAJO_BUFFER_shp, "0.31 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")
    arcpy.FeatureToLine_management(TB_MZS_TRABAJO_BUFFER_shp, TB_MZS_LINE_shp, "", "ATTRIBUTES")
    # Process: Merge
    # arcpy.Merge_management("'D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp';'D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp';'D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp'", PUNTOS_INICIO_shp, "IDMANZANA \"IDMANZANA\" true true false 15 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,IDMANZANA,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,IDMANZANA,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,IDMANZANA,-1,-1;OBJECTID \"OBJECTID\" true true false 10 Long 0 10 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,OBJECTID,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,OBJECTID,-1,-1;ORIG_FID \"ORIG_FID\" true true false 10 Long 0 10 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,ORIG_FID,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,ORIG_FID,-1,-1;NEAR_FID \"NEAR_FID\" true true false 10 Long 0 10 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,NEAR_FID,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,NEAR_FID,-1,-1;NEAR_DIST \"NEAR_DIST\" true true false 19 Double 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,NEAR_DIST,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,NEAR_DIST,-1,-1;NEAR_FC \"NEAR_FC\" true true false 254 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,NEAR_FC,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,NEAR_FC,-1,-1;idmax \"idmax\" true true false 254 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,idmax,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,idmax,-1,-1;MIN_NEAR_D \"MIN_NEAR_D\" true true false 19 Double 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,MIN_NEAR_D,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,MIN_NEAR_D,-1,-1;MODIF \"MODIF\" true true false 5 Short 0 5 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_110204.shp,MODIF,-1,-1,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIAL\\P_021806.shp,MODIF,-1,-1;UBIGEO \"UBIGEO\" true true false 6 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,UBIGEO,-1,-1;CODCCPP14 \"CODCCPP14\" true true false 4 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CODCCPP14,-1,-1;MZ_T \"MZ_T\" true true false 4 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,MZ_T,-1,-1;CCDD \"CCDD\" true true false 2 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CCDD,-1,-1;CCPP \"CCPP\" true true false 2 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CCPP,-1,-1;CCDI \"CCDI\" true true false 2 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CCDI,-1,-1;ZONA \"ZONA\" true true false 5 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,ZONA,-1,-1;MANZANA \"MANZANA\" true true false 4 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,MANZANA,-1,-1;CODCCPP \"CODCCPP\" true true false 4 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,CODCCPP,-1,-1;NOMCCPP \"NOMCCPP\" true true false 60 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,NOMCCPP,-1,-1;DEPARTAMEN \"DEPARTAMEN\" true true false 50 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,DEPARTAMEN,-1,-1;PROVNCIA \"PROVNCIA\" true true false 50 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,PROVNCIA,-1,-1;DISTRITO \"DISTRITO\" true true false 50 Text 0 0 ,First,#,D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\RutasTratamiento\\PUNTO INICIO CARHUAZ\\PUNTO INICIO CARHUAZ.shp,DISTRITO,-1,-1")

    # Process: Buffer (2)
    arcpy.Buffer_analysis(PUNTOS_INICIO_shp, PUNTOINICIO_BUFFER_shp, "0.6 Meters", "FULL", "ROUND", "NONE", "",
                          "PLANAR")
    # Process: Erase
    arcpy.Erase_analysis(TB_MZS_LINE_shp, PUNTOINICIO_BUFFER_shp, TB_MZS_ERASE_shp, "")
    arcpy.SplitLine_management(TB_MZS_ERASE_shp, TB_SPLIT_shp)

    # Process: Dissolve
    arcpy.Dissolve_management(TB_SPLIT_shp, TB_DISSOLVE_shp, "UBIGEO;CODCCPP;ZONA;MANZANA;FLG_MZ", "", "MULTI_PART", "DISSOLVE_LINES")
    # Obteniendo los ultimos vertices:
    arcpy.FeatureVerticesToPoints_management(TB_DISSOLVE_shp, TB_VERTICES_FINAL, "END")

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

   # arcpy.Erase_analysis(TB_RUTAS_DISSOLVE_ERASE_shp, TB_CORTES_Buffer, TB_RUTAS_DISSOLVE_ERASE_shp_2, "")
    arcpy.Erase_analysis(TB_DISSOLVE_shp, TB_CORTES_Buffer, TB_RUTAS_DISSOLVE_ERASE_shp_2, "")

    # Process: Multipart To Singlepart
    arcpy.MultipartToSinglepart_management(TB_RUTAS_DISSOLVE_ERASE_shp_2, TB_RUTAS_PREPARACION_shp)





def RelacionarRutasLineasConAEU():
    arcpy.env.overwriteOutput = True
    TB_VIVIENDAS_CORTES_shp = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_VIVIENDAS_CORTES.shp"
    TB_RUTAS_PUNTOS_MIN = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_MIN.shp"
    TB_RUTAS_PUNTOS_MIN_SELECT = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS_MIN_SELECT.shp"
    TB_INTERSECT_RUTAS_1="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_INTERSECT_RUTAS_1.shp"
    TB_INTERSECT_RUTAS_2 = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_INTERSECT_RUTAS_2.shp"
    TB_INTERSECT_RUTAS_3= "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_INTERSECT_RUTAS_3.shp"
    MZS_AEU = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"
    TB_INTERSECT_RUTAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_INTERSECT_RUTAS.shp"
    TB_STADISTICS_INTERSECT_RUTAS="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_STADISTICS_INTERSECT_RUTAS"
    TB_RUTAS_LINEAS="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS.shp"

    TB_RUTAS_PREPARACION = "D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_PREPARACION.shp"
    TB_RUTAS_PREPARACION_Layer="TB_RUTAS_PREPARACION_Layer"
    VIVIENDAS_MZS_OR_MAX = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/VIVIENDAS_MZS_OR_MAX.shp"

    TB_VERTICES_FINAL_AEU = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_VERTICES_FINAL_AEU.shp"
    TB_RUTAS_LINEAS_TEMP="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS_TEMP.shp"
    TB_RUTAS_LINEAS_DISSOLVE="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS_DISSOLVE.shp"
    TB_RUTAS_LINEAS_DISSOLVE_Layer = "TB_RUTAS_LINEAS_DISSOLVE_Layer"
    TB_RUTAS_LINEAS_TEMP_2="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS_TEMP_2.shp"

    arcpy.MakeFeatureLayer_management(TB_RUTAS_PREPARACION,TB_RUTAS_PREPARACION_Layer)

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


    arcpy.Statistics_analysis(TB_INTERSECT_RUTAS,TB_STADISTICS_INTERSECT_RUTAS,[["AEU","MAX"],["ID_REG_OR","MAX"]],["FID_TB_RUT"])

    arcpy.AddJoin_management(TB_RUTAS_PREPARACION_Layer,"FID",TB_STADISTICS_INTERSECT_RUTAS,"FID_TB_RUT")

    arcpy.CopyFeatures_management(TB_RUTAS_PREPARACION_Layer,TB_RUTAS_LINEAS_TEMP)


    add_field = [["UBIGEO","TEXT"], ["CODCCPP","TEXT"], ["ZONA","TEXT"], ["MANZANA","TEXT"],["FLG_MZ","SHORT"] ,["AEU","SHORT"],["ID_REG_OR","SHORT"]]

    for el in add_field:
        arcpy.AddField_management(TB_RUTAS_LINEAS_TEMP,el[0],el[1])

    calculate_field= [["UBIGEO","!TB_RUTAS_P!"],["CODCCPP","!TB_RUTAS_1!"],["ZONA","!TB_RUTAS_2!"],["MANZANA","!TB_RUTAS_3!"],["FLG_MZ","!TB_RUTAS_4!"],["AEU","!tb_stadi_4!"],["ID_REG_OR","!tb_stadi_5!"]]

    for el in calculate_field:
        arcpy.CalculateField_management(TB_RUTAS_LINEAS_TEMP,el[0],el[1],"PYTHON_9.3")

    list_deletefield = ["TB_RUTAS_P","TB_RUTAS_1","TB_RUTAS_2","TB_RUTAS_3","TB_RUTAS_4", "TB_RUTAS_5", "tb_stadist", "tb_stadi_1", "tb_stadi_2", "tb_stadi_3","tb_stadi_4","tb_stadi_5"]


    arcpy.DeleteField_management(TB_RUTAS_LINEAS_TEMP, list_deletefield)



    sort_fields = [["UBIGEO", "ASCENDING"], ["CODCCPP", "ASCENDING"], ["ZONA", "ASCENDING"], ["MANZANA", "ASCENDING"],
                   ["AEU", "ASCENDING"], ["ID_REG_OR", "ASCENDING"]]


    arcpy.Sort_management(TB_RUTAS_LINEAS_TEMP, TB_RUTAS_LINEAS_TEMP_2, sort_fields)



    arcpy.Dissolve_management(TB_RUTAS_LINEAS_TEMP_2, TB_RUTAS_LINEAS_DISSOLVE, ["UBIGEO","CODCCPP","ZONA","MANZANA","FLG_MZ","AEU"],"", "MULTI_PART", "DISSOLVE_LINES")


    arcpy.MakeFeatureLayer_management(TB_RUTAS_LINEAS_DISSOLVE, TB_RUTAS_LINEAS_DISSOLVE_Layer)
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


def CrearTB_AEUS():
    AEUS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Renumerar/TB_AEUS.dbf"
    AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    AEUS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Renumerar/TB_AEUS_PUNTOS.shp"
    RUTAS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS.shp"
    RUTAS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    VIVIENDAS_ORDENADAS="D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\AEU\\EnumerarAEUViviendas\\TB_VIVIENDAS_ORDENADAS.shp"

    if arcpy.Exists (AEUS):
        arcpy.Delete_management(AEUS)

    if arcpy.Exists (AEUS_LINEAS):
        arcpy.Delete_management(AEUS_LINEAS)

    if arcpy.Exists (AEUS_PUNTOS):
        arcpy.Delete_management(AEUS_PUNTOS)

    arcpy.AddField_management(RUTAS_PUNTOS, "AEU_FINAL","SHORT")
    arcpy.AddField_management(RUTAS_LINEAS, "AEU_FINAL","SHORT")
    arcpy.AddField_management(MZS_AEU_dbf, "AEU_FINAL", "SHORT")
    arcpy.AddField_management(VIVIENDAS_ORDENADAS, "AEU_FINAL", "SHORT")

    arcpy.CalculateField_management(RUTAS_PUNTOS, "AEU_FINAL","[AEU]")
    arcpy.CalculateField_management(RUTAS_LINEAS,"AEU_FINAL","[AEU]")
    arcpy.CalculateField_management(MZS_AEU_dbf, "AEU_FINAL", "[AEU]")
    arcpy.CalculateField_management(VIVIENDAS_ORDENADAS, "AEU_FINAL", "[AEU]")

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

def EnumerarSecciones(where_expression):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbanaTabularCondominios"
    MZS_AEU_TEMP = "in_memory\\MZS_AEU_dbf"
    ZONA_CANT_AEU="in_memory\\ZONA_CANT_AEU"
    ZONA_AEU = "in_memory\\ZONA_AEU"
    AEUS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Renumerar/TB_AEUS.dbf"
    AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    AEUS_PUNTOS = "D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\AEU\\Renumerar\\TB_AEUS_PUNTOS.shp"
    MZS_AEU="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"
    RUTAS_LINEAS="D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
    RUTAS_PUNTOS = "D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_PUNTOS.shp"


    arcpy.Sort_management("D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/MZS_AEU.dbf", MZS_AEU_TEMP,
                          ["UBIGEO", "ZONA", "AEU_FINAL"])

    arcpy.Statistics_analysis(MZS_AEU_TEMP,ZONA_AEU , [["CANT_VIV", "SUM"]],
                              ["UBIGEO", "ZONA","AEU_FINAL"])  # SE OBTIENE LAS  AEU'S POR ZONA

    arcpy.Statistics_analysis(ZONA_AEU,ZONA_CANT_AEU, [["AEU_FINAL", "COUNT"]], ["UBIGEO", "ZONA"]) # SE OBTIENE LA  CANTIDAD DE AEU'S POR ZONA


    arcpy.AddField_management(RUTAS_LINEAS, "SECCION", "SHORT")
    arcpy.AddField_management(MZS_AEU, "SECCION", "SHORT")
    arcpy.AddField_management(ZONA_AEU, "SECCION", "SHORT")
    arcpy.AddField_management(AEUS, "SECCION", "SHORT")
    arcpy.AddField_management(AEUS_LINEAS, "SECCION", "SHORT")
    arcpy.AddField_management(AEUS_LINEAS, "ORD_AEU", "SHORT")
    arcpy.AddField_management(AEUS_PUNTOS, "SECCION", "SHORT")
    arcpy.AddField_management(AEUS_PUNTOS, "ORD_AEU", "SHORT")
    arcpy.AddField_management(RUTAS_PUNTOS, "SECCION", "SHORT")
    arcpy.AddField_management(ZONA_CANT_AEU, "CANT_SECC", "SHORT")
    arcpy.AddField_management(ZONA_CANT_AEU, "RESIDUO", "SHORT")
    arcpy.AddField_management(ZONA_CANT_AEU, "CANT_AEU_SEC", "SHORT")

    expression = "math.ceil(float( !COUNT_AEU_FINAL! )/6.0 )"
    arcpy.CalculateField_management(ZONA_CANT_AEU, "CANT_SECC",expression,"PYTHON_9.3" )

    expression2 = "math.floor(!COUNT_AEU_FINAL!/!CANT_SECC!)"
    arcpy.CalculateField_management(ZONA_CANT_AEU, "CANT_AEU_SEC", expression2, "PYTHON_9.3")

    expression3 = "!COUNT_AEU_FINAL!%!CANT_SECC!"
    arcpy.CalculateField_management(ZONA_CANT_AEU, "RESIDUO", expression3,"PYTHON_9.3")

    #where_expression=UBIGEO.ExpresionUbigeos(ubigeos)


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
        ord_aeu=1
        with arcpy.arcpy.da.UpdateCursor(ZONA_AEU, ['AEU_FINAL', 'SECCION'],where_expression2) as cursor2:
            for row2 in cursor2:
                row2[1]=seccion


                where_expression3 = " UBIGEO=\'" + str(row1[0]) + "\'  AND  ZONA=\'" + str(row1[1]) + "\' AND AEU_FINAL="+str(row2[0])

                with arcpy.da.UpdateCursor(AEUS, ['AEU_FINAL', 'SECCION'], where_expression3) as cursor3:
                    for row3 in cursor3:
                        row3[1]=seccion
                        cursor3.updateRow(row3)
                del cursor3


                with arcpy.da.UpdateCursor(RUTAS_PUNTOS, ['AEU_FINAL', 'SECCION'], where_expression3) as cursor5:
                    for row5 in cursor5:
                        row5[1]=seccion
                        cursor5.updateRow(row5)
                del cursor5


                with arcpy.da.UpdateCursor(RUTAS_LINEAS, ['AEU_FINAL', 'SECCION'], where_expression3) as cursor5:
                    for row5 in cursor5:
                        row5[1]=seccion
                        cursor5.updateRow(row5)
                del cursor5


                with arcpy.da.UpdateCursor(AEUS_LINEAS, ['AEU_FINAL', 'SECCION','ORD_AEU'], where_expression3) as cursor6:
                    for row6 in cursor6:
                        row6[1]=seccion
                        row6[2] = ord_aeu
                        cursor6.updateRow(row6)
                del cursor6



                with arcpy.da.UpdateCursor(AEUS_PUNTOS, ['AEU_FINAL', 'SECCION','ORD_AEU'], where_expression3) as cursor5:
                    for row5 in cursor5:
                        row5[1]=seccion
                        row5[2] = ord_aeu
                        cursor5.updateRow(row5)
                del cursor5



                with arcpy.da.UpdateCursor(MZS_AEU, ['AEU_FINAL', 'SECCION'], where_expression3) as cursor7:
                    for row7 in cursor7:
                        row7[1] = seccion
                        cursor7.updateRow(row7)
                del cursor7


                i = i + 1
                ord_aeu = ord_aeu+1


                if residuo_temp>0:
                    if i>(cant_aeu_secc+1):
                        i=1
                        seccion=seccion+1
                        residuo_temp=residuo_temp-1
                        ord_aeu=1

                else:
                    if i > (cant_aeu_secc):
                        i = 1
                        seccion = seccion + 1
                        ord_aeu = 1

                cursor2.updateRow(row2)


 # SE OBTIENE LAS RUTAS COMO UNA SOLA ENTIDAD
    del row1



def CrearSecciones(where_expression):
    arcpy.env.overwriteOutput = True
    AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    AEUS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Renumerar/TB_AEUS_PUNTOS.shp"
    SECCIONES="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/SECCIONES/EnumerarSecciones/TB_SECCIONES.shp"
    ZONA_AEU = "in_memory\\ZONA_AEU_2"
    ZONA_SECCION = "in_memory\\ZONA_SECCION_2"
    MZS_AEU = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"
    MZS_AEU_TEMP = "in_memory\\MZS_AEU_dbf_2"


    if arcpy.Exists(SECCIONES):
        arcpy.Delete_management(SECCIONES)

    arcpy.Sort_management(MZS_AEU, MZS_AEU_TEMP,
                          ["UBIGEO", "CODCCPP","ZONA", "SECCION", "AEU_FINAL"])

    arcpy.Statistics_analysis(MZS_AEU_TEMP, ZONA_AEU, [["CANT_VIV", "SUM"]],
                          ["UBIGEO", "CODCCPP","ZONA","SECCION" ,"AEU_FINAL"])  # SE OBTIENE LAS  AEU'S POR ZONA

    arcpy.Statistics_analysis(ZONA_AEU, ZONA_SECCION, [["SUM_CANT_VIV", "SUM"]],
                              ["UBIGEO", "CODCCPP","ZONA", "SECCION"])  # SE OBTIENE LAS  AEU'S POR ZONA


    arcpy.MakeFeatureLayer_management(AEUS_LINEAS,"aeus_lineas")

    arcpy.MakeFeatureLayer_management(AEUS_PUNTOS, "aeus_puntos")


    #where_expression = UBIGEO.ExpresionUbigeos(ubigeos)
    j=0



    for row1 in arcpy.da.SearchCursor(ZONA_SECCION, ["UBIGEO", "ZONA", "SECCION","SUM_SUM_CANT_VIV","CODCCPP"], where_expression):
        where_expression2 = " UBIGEO=\'" + str(row1[0]) + "\'  AND  ZONA=\'" + str(row1[1])  + "\'  AND  SECCION=" + str(row1[2])
        print where_expression2
        arcpy.SelectLayerByAttribute_management("aeus_lineas", "NEW_SELECTION", where_expression2)
        print arcpy.GetCount_management("aeus_lineas").getOutput(0)
        if (int(arcpy.GetCount_management("aeus_lineas").getOutput(0))>0):

            out_feature_1 = "in_memory/Buffer" + str(row1[0]) + str(row1[1]) + str(row1[2])
            out_feature_2 = "in_memory/FeatureToLine" + str(row1[0]) + str(row1[1]) + str(row1[2])
            out_feature_3 = "in_memory/FeatureToPolygon" + str(row1[0]) + str(row1[1]) + str(row1[2])
            out_feature = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/SECCIONES/Mapas/Dissolve/" + str(row1[0]) + str(
                row1[1]) + str(row1[2]) + ".shp"


            arcpy.Buffer_analysis("aeus_lineas",out_feature_1, '5 METERS','FULL', 'ROUND','LIST',['UBIGEO','ZONA','SECCION'])
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
                arcpy.Append_management(out_feature, SECCIONES,"NO_TEST")
            j = j + 1
            arcpy.Delete_management(out_feature_1)
            arcpy.Delete_management(out_feature_2)
            arcpy.Delete_management(out_feature_3)

        else:

            out_feature = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/SECCIONES/Mapas/Dissolve/" + str(row1[0]) + str(
                row1[1]) + str(row1[2]) + ".shp"

            arcpy.SelectLayerByAttribute_management("aeus_puntos", "NEW_SELECTION", where_expression2)

            arcpy.Buffer_analysis("aeus_puntos",out_feature, '5 METERS','FULL', 'ROUND','LIST',['UBIGEO','CODCCPP','ZONA','SECCION'])
            arcpy.AddField_management(out_feature, "CANT_VIV", "SHORT")
            calculate_expression4 = str(row1[3])
            arcpy.CalculateField_management(out_feature, "CANT_VIV", calculate_expression4, "PYTHON_9.3")


            if (j == 0):
                arcpy.CopyFeatures_management(out_feature, SECCIONES)
            else:
                arcpy.Append_management(out_feature, SECCIONES,"NO_TEST")
            j = j + 1

            arcpy.Delete_management(out_feature)

    del row1



def CrearRutasMultipart():

    RUTAS_LINEAS="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS.shp"
    RUTAS_LINEAS_MULTIPART="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS_MULTIPART.shp"
    arcpy.MultipartToSinglepart_management(RUTAS_LINEAS,RUTAS_LINEAS_MULTIPART)



def ModelarTablas(where_expression):
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



def InsertarRegistros(where_list):
    arcpy.env.workspace = "Database Connections/PruebaSegmentacion.sde"
    TB_AEUS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Renumerar/TB_AEUS.dbf"
    TB_AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    TB_RUTAS_LINEAS = "D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\AEU\\CrearRepresentacionAEU\\TB_RUTAS_LINEAS.shp"
    TB_RUTAS="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/MZS_AEU.dbf"
    TB_SECCIONES = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/SECCIONES/EnumerarSecciones/TB_SECCIONES.shp"
    TB_VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"

    SEGM_ESP_SECCIONES = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_TAB_SECCION"
    SEGM_ESP_AEUS = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_TAB_AEU"
    SEGM_ESP_AEUS_LINEAS = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_TAB_AEU_LINEA"
    SEGM_ESP_RUTAS = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_TAB_RUTA"
    SEGM_ESP_RUTAS_LINEAS = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_TAB_RUTA_LINEA"
    SEGM_ESP_VIVIENDAS_U = "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.SEGM_TAB_VIVIENDA_U"

    #where_list = UBIGEO.ExpresionUbigeos(ubigeos)
    arcpy.MakeFeatureLayer_management(TB_VIVIENDAS_ORDENADAS, "tb_viviendas_ordenadas", where_list)
    arcpy.MakeFeatureLayer_management(TB_SECCIONES, "tb_secciones", where_list)
    arcpy.MakeFeatureLayer_management(TB_AEUS_LINEAS, "tb_aeus_lineas", where_list)
    arcpy.MakeFeatureLayer_management(TB_RUTAS_LINEAS, "tb_rutas_lineas", where_list)
    arcpy.MakeTableView_management(TB_AEUS, "tb_aeus", where_list)
    arcpy.MakeTableView_management(TB_RUTAS, "tb_rutas", where_list)

    arcpy.Append_management("tb_viviendas_ordenadas", SEGM_ESP_VIVIENDAS_U, "NO_TEST")
    arcpy.Append_management("tb_secciones", SEGM_ESP_SECCIONES,"NO_TEST")
    arcpy.Append_management("tb_aeus_lineas", SEGM_ESP_AEUS_LINEAS, "NO_TEST")
    arcpy.Append_management("tb_rutas_lineas", SEGM_ESP_RUTAS_LINEAS, "NO_TEST")
    arcpy.Append_management("tb_aeus", SEGM_ESP_AEUS, "NO_TEST")
    arcpy.Append_management("tb_rutas", SEGM_ESP_RUTAS, "NO_TEST")


    list_deletelayer=["tb_viviendas_ordenadas","tb_secciones","tb_aeus_lineas","tb_rutas_lineas","tb_aeus","tb_rutas","tb_marcos_aeus","tb_marcos_secciones"]

    for el in list_deletelayer:
        arcpy.Delete_management(el)


def CrearCarpetas(data,campos):
    arcpy.env.workspace = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios"
    ZONAS = r"D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    Path_inicial = "\\\srv-fileserver\\CPV2017"


    if os.path.exists(Path_inicial + "\\croquis_segm_tab") == False:
        os.mkdir(Path_inicial + "\\croquis_segm_tab")

    Path_urbano = Path_inicial + "\\croquis_segm_tab\\urbano"

    if os.path.exists(Path_urbano) == False:
        os.mkdir(Path_urbano)

    for el in data:
        if os.path.exists(Path_urbano + "\\" + str(el[0])) == False:
            os.mkdir(Path_urbano + "\\" + str(el[0]))

    where_expression = UBIGEO.Expresion(data, campos)

    with arcpy.da.SearchCursor(ZONAS, ['UBIGEO', 'ZONA'], where_expression) as cursor:
        for row in cursor:
            if os.path.exists(Path_urbano + "\\" + str(row[0]) + "\\" + str(row[1])) == False:
                os.mkdir(Path_urbano + "\\" + str(row[0]) + "\\" + str(row[1]))
            else:
                lista_directorios = os.listdir(Path_urbano + "\\" + str(el[0]) + "\\" + str(el[1]))
                if (len(lista_directorios) > 0):
                    for archivo in lista_directorios:
                        shutil.rmtree(Path_urbano + "\\" + str(el[0]) + "\\" + str(el[1]) + "\\" + str(archivo))
    del row





def ExportarCroquisUrbanoAEU(where_expression):
    arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    RUTAS_LINEAS_MULTIPART = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS_MULTIPART.shp"
    RUTAS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS.shp"
    RUTAS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"
    AEUS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Renumerar/TB_AEUS.dbf"
    TB_MZS_shp = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    ZONA_CENSAL  = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    TB_EJES_VIALES="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_EJES_VIALES.shp"

    #print os.path.dirname(TB_EJES_VIALES) + "/" + os.path.basename(TB_EJES_VIALES)

    Path_inicial = "\\\srv-fileserver\\CPV2017"
    Path_urbano = Path_inicial + "\\croquis_segm_tab\\urbano"
#
    #mxd = arcpy.mapping.MapDocument(
    #    r"D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Mxd/CroquisSegmentacionUrbanoFinal.mxd")
    #df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

    #for lyr in arcpy.mapping.ListLayers(mxd):
    #    if (str(lyr.name)=="TB_EJES_VIALES"):
    #        print lyr.dataSource
    #        lyr.replaceDataSource(TB_EJES_VIALES, "SHAPEFILE_WORKSPACE","ejes_viales", True)
#
    #    if (str(lyr.name)=="TB_MZS"):
    #        lyr.replaceDataSource(TB_MZS_shp, "SHAPEFILE_WORKSPACE",lyr.name, True)
#
    #        #mxd.findAndReplaceWorkspacePaths(lyr.dataSource, TB_MZS_shp, validate=True)
    #mxd.save()
    #del mxd


    #print where_expression
    for row in arcpy.da.SearchCursor(AEUS, ["UBIGEO", "ZONA",  "AEU_FINAL","CANT_VIV","CODCCPP","SECCION"],where_expression):
        where_expression2 = ' "UBIGEO"=\'' + str(row[0]) + '\' AND "ZONA" =\'' + str(row[1]) + '\' AND AEU_FINAL=' + str(row[2])
        where_zona =' "UBIGEO"=\'' + str(row[0]) + '\' AND "ZONA" =\'' + str(row[1]) + '\' '

        i=0
        data=[]


        for row1 in arcpy.da.SearchCursor(MZS_AEU_dbf, ["UBIGEO","ZONA","MANZANA"],where_expression2):

            data.append([str(row1[0]),str(row1[1]),str(row1[2])])


        where_temporal=UBIGEO.Expresion(data,["UBIGEO","ZONA","MANZANA"])

        where_rutas = where_expression2


        where_manzanas=where_temporal


        mxd = arcpy.mapping.MapDocument(
            r"D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Mxd/CroquisSegmentacionUrbanoFinal.mxd")
        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]


        arcpy.MakeFeatureLayer_management(TB_MZS_shp, "manzanas", where_manzanas)
        arcpy.MakeFeatureLayer_management(RUTAS_LINEAS_MULTIPART, "rutas_lineas", where_rutas)
        arcpy.MakeFeatureLayer_management(RUTAS_PUNTOS, "rutas_puntos", where_rutas)



        lyrFile1 = arcpy.mapping.Layer("rutas_lineas")
        lyrFile3 = arcpy.mapping.Layer("manzanas")
        lyrFile4 = arcpy.mapping.Layer("rutas_puntos")

        arcpy.ApplySymbologyFromLayer_management(lyrFile1,
                                                 "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Layers/rutas_lineas.lyr")
        arcpy.ApplySymbologyFromLayer_management(lyrFile3,
                                                 "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Layers/manzana_final.lyr")

        arcpy.ApplySymbologyFromLayer_management(lyrFile4,
                                                 "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Layers/rutas_puntos.lyr")

        arcpy.mapping.AddLayer(df, lyrFile1)
        arcpy.RefreshActiveView()

        arcpy.mapping.AddLayer(df, lyrFile3)
        arcpy.RefreshActiveView()
        arcpy.mapping.AddLayer(df, lyrFile4)
        arcpy.RefreshActiveView()
        viv_aeu = int(row[3])
        seccion = "0" * (3 - len(str(row[5]))) + str(row[5])
        aeu = "0" * (3 - len(str(row[2]))) + str(row[2])
        ubigeo = str(row[0])
        zona = UBIGEO.EtiquetaZona(str(row[1]))
        codigo = str(row[0]) + str(row[1]) + seccion + aeu
        TextElement1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDD")[0]
        TextElement2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCPP")[0]
        TextElement3 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDI")[0]
        TextElement4 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DEPARTAMENTO")[0]
        TextElement5 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "PROVINCIA")[0]
        TextElement6 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DISTRITO")[0]
        TextElement7 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "NOMCCPP")[0]
        TextElement8 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "ZONA")[0]
        TextElement9 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "AEU")[0]
        TextElement10 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "SECCION")[0]
        TextElement11 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "VIV_AEU")[0]
        TextElement12 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "COD_BARRA")[0]
        TextElement13 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "TEXT_COD_BARRA")[0]
        TextElement1.text = ubigeo[0:2]
        TextElement2.text = ubigeo[2:4]
        TextElement3.text = ubigeo[4:6]
        TextElement8.text = zona
        TextElement9.text = str(aeu)
        TextElement10.text = seccion
        TextElement11.text = str(viv_aeu)
        TextElement12.text = "*"+str(codigo)+"*"
        TextElement13.text="*"+str(codigo)+"*"



        for row4 in arcpy.da.SearchCursor(ZONA_CENSAL, ['DEPARTAMEN', 'PROVINCIA', 'DISTRITO', 'NOMCCPP'],where_zona):
            TextElement4.text = str(row4[0])
            TextElement5.text = row4[1]
            TextElement6.text = row4[2]
            TextElement7.text = row4[3]


        df.extent = lyrFile3.getSelectedExtent()
        df.scale = df.scale

        dflinea=arcpy.Polyline(arcpy.Array([ arcpy.Point (df.extent.XMin,df.extent.YMin) ,arcpy.Point(  df.extent.XMax,df.extent.YMax)]),df.spatialReference)
        distancia=dflinea.getLength("GEODESIC","METERS")

        if (float(distancia)<=50):
            df.scale = df.scale*4

        if (float(distancia)>50 and float(distancia)<=100):
            df.scale = df.scale*3

        if (float(distancia)>100 and float(distancia)<=490):
            df.scale = df.scale*2

        if (float(distancia)>490 and float(distancia)<=900):
            df.scale = df.scale*1.5

        if (float(distancia)>900 and float(distancia)<=1200):
            df.scale = df.scale*1.25

        if (float(distancia)>1200 and float(distancia)<=1800):
            df.scale = df.scale*1.10

        if (float(distancia)>1800):
            df.scale = df.scale*1.05

        out = Path_urbano + "\\" + str(row[0]) + "\\" + str(row[1]) + "\\" + codigo + ".pdf"
        print out

        arcpy.mapping.ExportToPDF(mxd,out , "PAGE_LAYOUT")
        arcpy.mapping.RemoveLayer(df, lyrFile1)

        arcpy.mapping.RemoveLayer(df, lyrFile3)
        arcpy.mapping.RemoveLayer(df, lyrFile4)


        del mxd
        del df


def ExportarCroquisUrbanoSeccion(where_expression):
    arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbanaTabularCondominios"
    ZONA_CENSAL = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    AEUS = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Renumerar/TB_AEUS.dbf"
    MZS_AEU="D:\\ShapesPruebasSegmentacionUrbanaTabularCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    SECCIONES = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/SECCIONES/EnumerarSecciones/TB_SECCIONES.shp"
    TB_MZS_shp = "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    Path_inicial = "\\\srv-fileserver\\CPV2017"
    Path_urbano = Path_inicial + "\\croquis_segm_tab\\urbano"


    for row in arcpy.da.SearchCursor(SECCIONES, ['UBIGEO', 'ZONA', 'SECCION','CANT_VIV'],where_expression):
        where_expression1= ' "UBIGEO"=\''+str(row[0])+'\' AND "ZONA"=\''+str(row[1])+'\' AND SECCION=' +str(row[2])
        where_expression_zona = ' "UBIGEO"=\'' + str(row[0]) + '\' AND "ZONA"=\'' + str(row[1]) + '\''

        mxd = arcpy.mapping.MapDocument(r"D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/SECCIONES/Mxd/CroquisSegmentacionUrbanoSecciones.mxd")
        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
        where_expression3=''


        i = 0

        aeu_inicial_temp=0
        aeu_final_temp=0

        data = []

        for row2 in arcpy.da.SearchCursor(AEUS, ['AEU_FINAL'], where_expression1):
            where_expression2 = ' "UBIGEO"=\'' + str(row[0]) + '\' AND "ZONA"=\'' + str(row[1]) + '\' AND AEU_FINAL='+str(row2[0])

            if (i==0):
                aeu_inicial_temp=int(row2[0])
            else:
                aeu_final_temp=int(row2[0])

            i = 0




            for row3 in arcpy.da.SearchCursor(MZS_AEU, ["UBIGEO", "ZONA", "MANZANA"], where_expression2):
                data.append([str(row3[0]), str(row3[1]), str(row3[2])])


        where_expression3 = UBIGEO.Expresion(data, ["UBIGEO", "ZONA", "MANZANA"])



        ubigeo = str(row[0])
        zona = UBIGEO.EtiquetaZona(str(row[1]))
        seccion = "0"*(3-len(str(row[2])))+str(row[2])
        aeu_inicial="0"*(3-len(str(aeu_inicial_temp)))+str(aeu_inicial_temp)
        aeu_final = "0" * (3 - len(str(aeu_final_temp))) + str(aeu_final_temp)
        cant_viv=str(int(row[3]))
        arcpy.MakeFeatureLayer_management(SECCIONES,"secciones_1", where_expression1)
        arcpy.MakeFeatureLayer_management(TB_MZS_shp, "manzanas", where_expression3)
        lyrFile1 = arcpy.mapping.Layer("secciones_1")
        lyrFile2 = arcpy.mapping.Layer("manzanas")
        arcpy.ApplySymbologyFromLayer_management(lyrFile1,
                                                 "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Layers/seccion.lyr")

        arcpy.ApplySymbologyFromLayer_management(lyrFile2,
                                             "D:/ShapesPruebasSegmentacionUrbanaTabularCondominios/AEU/Layers/manzana_final.lyr")
        arcpy.RefreshActiveView()
        arcpy.mapping.AddLayer(df, lyrFile2)
        arcpy.RefreshActiveView()
        arcpy.mapping.AddLayer(df, lyrFile1)
        arcpy.RefreshActiveView()

        codigo=str(row[0]) + str(row[1]) + seccion


        TextElement1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDD")[0]
        TextElement2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCPP")[0]
        TextElement3 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDI")[0]
        TextElement4 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DEPARTAMENTO")[0]
        TextElement5 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "PROVINCIA")[0]
        TextElement6 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DISTRITO")[0]
        TextElement7 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "NOMCCPP")[0]
        TextElement8 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "ZONA")[0]
        TextElement9 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "SECCION")[0]
        TextElement10 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "AEU_INICIAL")[0]
        TextElement11 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "AEU_FINAL")[0]
        TextElement12 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CANT_VIV")[0]
        TextElement13 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "COD_BARRA")[0]
        TextElement14 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "TEXT_COD_BARRA")[0]

        TextElement13.text = "*"+str(codigo)+"*"
        TextElement14.text = "*"+str(codigo)+"*"
        TextElement1.text = ubigeo[0:2]
        TextElement2.text = ubigeo[2:4]
        TextElement3.text = ubigeo[4:6]
        TextElement8.text = zona
        TextElement9.text = seccion
        TextElement10.text = aeu_inicial
        TextElement11.text = aeu_final
        TextElement12.text = cant_viv
        df.extent = lyrFile2.getSelectedExtent()
        df.scale = df.scale *2


        for row4 in arcpy.da.SearchCursor(ZONA_CENSAL, ['DEPARTAMEN','PROVINCIA','DISTRITO','NOMCCPP'],where_expression_zona):
            TextElement4.text=str(row4[0])
            TextElement5.text = row4[1]
            TextElement6.text = row4[2]
            TextElement7.text = row4[3]

        out = Path_urbano + "\\" + str(row[0]) + "\\" + str(row[1]) + "\\" + codigo + ".pdf"
        arcpy.mapping.ExportToPDF(mxd,out , "PAGE_LAYOUT")
        arcpy.mapping.RemoveLayer(df, lyrFile1)
        arcpy.mapping.RemoveLayer(df, lyrFile2)



def ExportarCroquisUrbanoZona(where_expression):
    arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbanaCondominios"
    ZONA_CENSAL = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    ZONA_AEU="D:/ShapesPruebasSegmentacionUrbanaCondominios/EnumerarSecciones/zona_aeu"


    AEUS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Renumerar/TB_AEUS.dbf"
    MZS_AEU="D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"

    SECCIONES = "D:/ShapesPruebasSegmentacionUrbanaCondominios/SECCIONES/EnumerarSecciones/TB_SECCIONES.shp"
    AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    TB_MZS_shp = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    RUTAS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS.shp"
    RUTAS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"
    Path_inicial = "\\\srv-fileserver\\CPV2017"
    Path_urbano = Path_inicial + "\\croquis_segm_tab\\urbano"

    for row in arcpy.da.SearchCursor(ZONA_CENSAL, ['UBIGEO', 'ZONA'], where_expression):
        ubigeo=row[0]
        zona=row[1]

        where_inicial = ' "UBIGEO"=\'' + str(ubigeo) + '\' AND "ZONA"=\'' + str(zona) + '\''
        print where_inicial
        mxd = arcpy.mapping.MapDocument(r"D:/ShapesPruebasSegmentacionUrbanaCondominios/ZONAS/Mxd/CroquisSegmentacionUrbanoZonas.mxd")
        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

        arcpy.MakeFeatureLayer_management(ZONA_CENSAL, "zona_censal",where_inicial)
        lyrFile1 = arcpy.mapping.Layer("zona_censal")
        arcpy.ApplySymbologyFromLayer_management(lyrFile1,
                                                 "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Layers/zonas.lyr")

        i = 0
        aeu_inicial_temp = 0
        aeu_final_temp = 0

        seccion_inicial_temp = 0
        seccion_final_temp = 0


        for row2 in arcpy.da.SearchCursor(RUTAS_LINEAS,
                                          ['AEU_FINAL'], where_inicial):
            aeu_temp = int(row2[0])
            if (i == 0):
                aeu_inicial_temp = aeu_temp
                aeu_final_temp = aeu_temp
            else:
                if aeu_inicial_temp > aeu_temp:
                    aeu_inicial_temp = aeu_temp

                if aeu_final_temp < aeu_temp:
                    aeu_final_temp = aeu_temp

            i = i + 1
        del row2

        i = 0

        cant_viv = 0

        for row3 in arcpy.da.SearchCursor(SECCIONES,
                                           ['SECCION', 'CANT_VIV'], where_inicial):
            seccion_temp = int(row3[0])

            if (i == 0):
                seccion_inicial_temp = seccion_temp
                seccion_final_temp = seccion_temp
            else:
                if seccion_inicial_temp > seccion_temp:
                    seccion_inicial_temp = seccion_temp

                if seccion_final_temp < seccion_temp:
                    seccion_final_temp = seccion_temp

            cant_viv = cant_viv + int(row3[1])
            i = i + 1
        del row3


        aeu_inicial = "0" * (3 - len(str(aeu_inicial_temp))) + str(aeu_inicial_temp)
        aeu_final = "0" * (3 - len(str(aeu_final_temp))) + str(aeu_final_temp)
        seccion_inicial = "0" * (3 - len(str(seccion_inicial_temp))) + str(seccion_inicial_temp)
        seccion_final = "0" * (3 - len(str(seccion_final_temp))) + str(seccion_final_temp)

        codigo = str(ubigeo) + str(zona)
        zona_etiqueta = UBIGEO.EtiquetaZona(zona)
        TextElement1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDD")[0]
        TextElement2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCPP")[0]
        TextElement3 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDI")[0]
        TextElement4 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DEPARTAMENTO")[0]
        TextElement5 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "PROVINCIA")[0]
        TextElement6 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DISTRITO")[0]
        TextElement7 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "NOMCCPP")[0]
        TextElement8 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "ZONA")[0]
        TextElement9 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "SECCION_INICIAL")[0]
        TextElement13 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "SECCION_FINAL")[0]
        TextElement10 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "AEU_INICIAL")[0]
        TextElement11 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "AEU_FINAL")[0]
        TextElement12 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CANT_VIV")[0]
        TextElement14 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "COD_BARRA")[0]
        TextElement15 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "TEXT_COD_BARRA")[0]
        TextElement14.text = "*"+str(codigo)+"*"
        TextElement15.text = "*"+str(codigo)+"*"

        TextElement1.text = ubigeo[0:2]
        TextElement2.text = ubigeo[2:4]
        TextElement3.text = ubigeo[4:6]



        TextElement8.text = zona_etiqueta
        TextElement9.text = seccion_inicial
        TextElement13.text = seccion_final
        TextElement10.text = aeu_inicial
        TextElement11.text = aeu_final
        TextElement12.text = cant_viv

        for row4 in arcpy.da.SearchCursor(ZONA_CENSAL, ['DEPARTAMEN', 'PROVINCIA', 'DISTRITO', 'NOMCCPP'], where_inicial):
            TextElement4.text = str(row4[0])
            TextElement5.text = row4[1]
            TextElement6.text = row4[2]
            TextElement7.text = row4[3]

        arcpy.mapping.AddLayer(df, lyrFile1)
        arcpy.RefreshActiveView()

        df.extent = lyrFile1.getSelectedExtent()
        df.scale = df.scale *1.2
        out = Path_urbano + "\\" + str(row[0]) + "\\" + str(row[1]) + "\\" + codigo + ".pdf"
        arcpy.mapping.ExportToPDF(mxd,out , "PAGE_LAYOUT")
        arcpy.mapping.RemoveLayer(df, lyrFile1)
        del mxd
        del df

    del row



#ubigeos=["150116"]
#print datetime.today()
#CopiarTablas()
#print "CopiarTablas"
#print datetime.today()
#OrdenarManzanasFalsoCod()
#print "OrdenarManzanasFalsoCod"
#print datetime.today()
#CrearViviendasOrdenadas()
#print "CrearViviendasOrdenadas"
#print datetime.today()
#EnumerarAEUEnViviendasDeManzanas(ubigeos)
#print "EnumerarAEUEnViviendasDeManzanas"
##
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
#CrearRutasPreparacion()
#print "CrearRutasPreparacion"
#print datetime.today()  #
#
#RelacionarVerticeFinalInicioConAEUMax()
#print "RelacionarVerticeFinalInicioConAEUMax"
#print datetime.today()  #
#RelacionarRutasLineasConAEU()
##
#print "CrearRutasPreparacion"
#print datetime.today()  #
####
#CrearTB_AEUS()
###
#print "CrearTB_AEUS"
#print datetime.today()  #
#EnumerarSecciones(ubigeos)
#print "EnumerarSecciones"
#print datetime.today()  #
#CrearSecciones(ubigeos)
#print "EnumerarSecciones"
#print datetime.today()  #
#CrearRutasMultipart()
#print "CrearRutasMultipart"
#print datetime.today()  #
#ModelarTablas(ubigeos)
#print "ModelarTablas"
#print datetime.today()  #
#conx.LimpiarRegistrosSegmentacionTabularUbigeo(ubigeos)
#InsertarRegistros(ubigeos)
#print "InsertarRegistros"
#print datetime.today()  #

#data=[
#        ['150116','00100'],
#        ['150116','00200'],
#        ['150116', '00400'],
#        ['150116', '00500'],
#]
#campos=['UBIGEO','ZONA']
#CrearCarpetas(data)



#ExportarCroquisUrbanoAEU(UBIGEO.Expresion(data,campos))
#ExportarCroquisUrbanoSeccion(UBIGEO.Expresion(data,campos))
#ExportarCroquisUrbanoZona(UBIGEO.Expresion(data,campos))