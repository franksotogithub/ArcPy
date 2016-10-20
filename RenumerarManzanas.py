import random
import arcpy
import math
import numpy as np

arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"


def Listar_Manzanas_Ordenado_ID(ubigeo,zona):
   fc=zona
   total_viv = 0

   manzanas = []
   where='"UBIGEO"=\''+str(ubigeo)+'\' AND "ZONA"=\''+str(zona)+'\' '
   for row1 in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp", ["IDMANZANA"],where):
       manzana = str(row1[0])
       manzanas.append(manzana)
   del row1

   manzanas.sort()
   return  manzanas


def Ordenar_Manzanas_Y(manzanasx):
    a = np.array(manzanasx)
    # a = np.array([[3, 2], [6, 2], [3, 6], [3, 4], [5, 3]])
    idx = np.argsort(a[:, 1].astype(float)*-1)
    b = a[idx]
    rs = b.tolist()
    rs_final = []

    for el2 in rs:
        for el in manzanasx:
            if (el[0] == el2[0]):
                rs_final.append(el[0])
                break
    return rs_final

def Ordenar_Manzanas_Distancia(manzanas):
    manzanasx=manzanas[:]
    a2 = np.array(manzanasx)

    idx2 = np.argsort(a2[:, 2])
    b2 = a2[idx2]
    #print "Sin ordenar:"
    #print a2
    #print "Ordenado:"
    #print b2
    rs = b2.tolist()
    rs_final = []

    for el2 in rs:

        for el in manzanasx:
            if (el[0] == el2[0]):
                rs_final.append(el)
                break
    return rs_final



def Obtener_Manzanas_Adyacentes(manzana,archivo_distancias):
    fc = archivo_distancias
    total_viv = 0

    manzanas_adyacentes = []
    where=' "IDMANZANA"=\''+str(manzana)+'\''

    for row1 in arcpy.da.SearchCursor(fc, ["IDMANZAN_1","yCentroid","DISTANCE"],where):
        manzana = [str(row1[0]),float(row1[1]),float(row1[2])]
        manzanas_adyacentes.append(manzana)
    #del row1


    return manzanas_adyacentes




def Ordenar_Manzanas(zona):
    fc = zona
    manzanas=Listar_Manzanas_Ordenado_ID(zona)[:]

    #print manzanas

    manzanas_adyacentes=[]
    manzanas_adyacentes_ordenadas_distancia = []
    manzanas_adyacentes_ordenadas_y = []

    manzanas_temporal=manzanas[:]
    lista_ordenada=[]

    el = manzanas_temporal[0]
    lista_ordenada.append(el)
    manzanas_temporal.remove(el)
    while len(lista_ordenada)<54:

        manzanas_adyacentes=Obtener_Manzanas_Adyacentes(el,'D:/ShapesPruebasSegmentacionUrbana/Distancias/distancias.dbf')[:]
        #print  manzanas_adyacentes
        manzanas_adyacentes_ordenadas_distancia=Ordenar_Manzanas_Distancia(manzanas_adyacentes)[0:10]
        #print  manzanas_adyacentes_ordenadas_distancia
        manzanas_adyacentes_ordenadas_y=Ordenar_Manzanas_Y(manzanas_adyacentes_ordenadas_distancia)[:]

        while len(manzanas_adyacentes_ordenadas_y)>0:
            manzana_escogida=manzanas_adyacentes_ordenadas_y[0]
            if manzana_escogida in lista_ordenada:
                manzanas_adyacentes_ordenadas_y.remove(manzana_escogida)

            else:
                lista_ordenada.append(manzana_escogida)
                manzanas_temporal.remove(manzana_escogida)
                break

        #manzanas_temporal.remove(el)

        if len(manzanas_adyacentes_ordenadas_y)>0:
            el=lista_ordenada[len(lista_ordenada)-1]
        else:
            el=manzanas_temporal[0]
        print  len(lista_ordenada)


        if len(lista_ordenada)==53:
            print lista_ordenada






def Renumerar_AEU(ubigeos):
    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"

    MZS_AEU_dbf = "D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/MZS_AEU.dbf"
    MIN_AEU = "D:/ShapesPruebasSegmentacionUrbana/Renumerar/MIN_AEU"
    MIN_AEU_SORT = "D:/ShapesPruebasSegmentacionUrbana/Renumerar/MIN_AEU_SORT"
    AEU_CANT_VIV="D:/ShapesPruebasSegmentacionUrbana/Renumerar/AEU_CANT_VIV"


    if arcpy.Exists ("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp")
    if arcpy.Exists ("D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf")
    if arcpy.Exists("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_RUTAS.shp"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_RUTAS.shp")
    if arcpy.Exists("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp")
    if arcpy.Exists(MIN_AEU):
        arcpy.Delete_management(MIN_AEU)
    if arcpy.Exists(MIN_AEU_SORT):
        arcpy.Delete_management(MIN_AEU_SORT)
    if arcpy.Exists(AEU_CANT_VIV):
        arcpy.Delete_management(AEU_CANT_VIV)

    arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/TB_MZS_TRABAJO.shp","D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp" )
    arcpy.AddField_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp", "AEU_FINAL", "SHORT")
    arcpy.Copy_management("D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/MZS_AEU.dbf", "D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf")
    arcpy.AddField_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf", "AEU_FINAL", "SHORT")

    arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/TB_RUTAS.shp", "D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_RUTAS.shp")
    arcpy.AddField_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_RUTAS.shp", "AEU_FINAL", "SHORT")
    arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/TB_VIVIENDAS_U_TRABAJO.shp", "D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp")
    arcpy.AddField_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp", "AEU_FINAL", "SHORT")

    arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/MZS_AEU.dbf", "mzs_aeu")
    arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/MZS_AEU.dbf", "mzs_aeu2")
    arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp",
                                      "tb_mzs")

    arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp",
                                      "zonas")




    arcpy.Statistics_analysis(MZS_AEU_dbf, MIN_AEU, [["IDMANZANA", "MIN"]], ["UBIGEO", "ZONA", "AEU"])
    arcpy.Sort_management(MIN_AEU, MIN_AEU_SORT, ["MIN_IDMANZANA","AEU"])
    arcpy.MakeTableView_management(MIN_AEU_SORT,"min_aeu_sort")
    where_list=ubigeos

    m = 0
    where_expression = ""
    for x in where_list:
        if (m + 1) == len(where_list):
            where_expression = where_expression + ' "UBIGEO"=\'%s\' ' % where_list[m]
        else:
            where_expression = where_expression + ' "UBIGEO"=\'%s\' OR' % (where_list[m])

        m = m + 1

    with arcpy.da.SearchCursor("zonas", ['UBIGEO', 'ZONA'],where_expression) as cursorzona:
        for rowzona in cursorzona:
            Renumerar_AEU_Zona3(str(rowzona[0]),str(rowzona[1]))

    arcpy.Statistics_analysis("D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf", AEU_CANT_VIV, [["VIV_AEU", "SUM"]], ["UBIGEO", "ZONA", "AEU_FINAL"])

 #  arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf",
 #                                    "mzs_aeu_renumerado")



def Listar_MZS_AEU_Reordenado(ubigeo,zona):
    arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/MZS_AEU.dbf", "mzs_aeu")
    arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/MZS_AEU.dbf", "mzs_aeu2")
    manzanas=Listar_Manzanas_Ordenado_ID(ubigeo,zona)
    manzanas_temp= manzanas[:]
    mzs_aeu=[]
    numero_aeu=1




    lista_manzana_aeu=[]
    with arcpy.da.SearchCursor("mzs_aeu", ['UBIGEO', 'ZONA', 'AEU', 'IDMANZANA']) as cursor6:
        for row6 in cursor6:
            lista_manzana_aeu.append([str(row6[3]),int(row6[2])])


#
#    while (len(manzanas_temp) > 0):
#        manzana=manzanas_temp[0]
#        where_x=' "IDMANZANA"=\''+str(manzana)+'\''
#        arcpy.SelectLayerByAttribute_management("mzs_aeu", "NEW_SELECTION", where_x)
#        #mzs_aeu
#
#        i=0
#        with arcpy.da.SearchCursor("mzs_aeu", ['UBIGEO', 'ZONA', 'AEU', 'IDMANZANA']) as cursor6:
#            for row6 in cursor6:
#                where1 = ' "UBIGEO"=\'' + str(row6[0]) + '\' AND "ZONA"=\'' + str(row6[1]) + '\' AND AEU=' + str(row6[2])
#                arcpy.SelectLayerByAttribute_management("mzs_aeu2", "NEW_SELECTION", where1)
#
#                with arcpy.da.SearchCursor("mzs_aeu2", ['IDMANZANA','AEU']) as cursor7:
#                    for row7 in cursor7:
#                        manzanaid=str(row7[0])
#                        manzana_aeu=[str(row7[0]),int(row7[1]),numero_aeu]
#                        mzs_aeu.append(manzana_aeu)
#                        if str(row7[0]) in  manzanas_temp:
#                            manzanas_temp.remove(manzanaid)
#
#                numero_aeu = 1 + numero_aeu
#    return mzs_aeu
#

def Renumerar_AEU_Zona(ubigeo,zona):
    manzanas=Listar_Manzanas_Ordenado_ID(ubigeo,zona)[:]
    #mzs_aeu=Listar_MZS_AEU_Reordenado(ubigeo, zona)[:]
    manzanas_temporal = manzanas[:]


    numero_aeu = 1
    while (len(manzanas_temporal)>0):
        manzana=manzanas_temporal[0]
        where_x=' "IDMANZANA"=\''+str(manzana)+'\''

        #print where_x
        arcpy.SelectLayerByAttribute_management("mzs_aeu", "NEW_SELECTION", where_x)
#
        with arcpy.da.SearchCursor("mzs_aeu", ['UBIGEO','ZONA','AEU','IDMANZANA']) as cursor6:
            for row6 in cursor6:


                where1 = ' "UBIGEO"=\''+str(row6[0])+'\' AND "ZONA"=\''+str(row6[1])+'\' AND AEU=' +str(row6[2])


                arcpy.SelectLayerByAttribute_management("mzs_aeu2", "NEW_SELECTION", where1)

                with arcpy.da.SearchCursor("mzs_aeu2", ['IDMANZANA','AEU']) as cursor7:
                    for row7 in cursor7:
                        where2='  "IDMANZANA"=\''+str(row7[0])+'\' AND AEU=' +str(row7[1])
                        where3 = '  "IDMANZANA"=\'' + str(row7[0]) + '\' '

                        where4 = '"UBIGEO"=\'' + str(row7[0])[0:6] + '\' AND "ZONA" =\'' + str(row7[0])[6:11] + '\' AND "MANZANA"=\'' + str(row7[0])[11:] + '\' AND AEU='+str(row7[1])

                        with arcpy.da.UpdateCursor(r"D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf", ['UBIGEO', 'ZONA', 'AEU','IDMANZANA','AEU_FINAL'],where2) as cursor8:
                            for row8 in cursor8:
                                row8[4]=int(numero_aeu)
                                manzanax = str(row8[3])
                                cursor8.updateRow(row8)

                                #print manzanax
                                if manzanax in manzanas_temporal:
                                    manzanas_temporal.remove(manzanax)
                        del cursor8

                        with arcpy.da.UpdateCursor(r"D:\ShapesPruebasSegmentacionUrbana\Renumerar\TB_RUTAS.shp", ['UBIGEO', 'ZONA', 'AEU','MANZANA','AEU_FINAL'],where4) as cursor9:
                            for row9 in cursor9:
                                row9[4]=int(numero_aeu)
                                cursor9.updateRow(row9)
                        del cursor9
                        with arcpy.da.UpdateCursor(r"D:\ShapesPruebasSegmentacionUrbana\Renumerar\TB_MZS_TRABAJO.shp",
                                                  ['UBIGEO', 'ZONA', 'AEU', 'IDMANZANA','AEU_FINAL'],where3 ) as cursor10:
                           for row10 in cursor10:
                               row10[4] = int(numero_aeu)
                               cursor10.updateRow(row10)
                        del cursor10

                        with arcpy.da.UpdateCursor(r"D:\ShapesPruebasSegmentacionUrbana\Renumerar\TB_VIVIENDAS_U_TRABAJO.shp",
                                      ['UBIGEO', 'ZONA', 'AEU', 'MANZANA','AEU_FINAL'], where4) as cursor11:
                            for row11 in cursor11:
                                row11[4] = int(numero_aeu)
                                cursor11.updateRow(row11)
                        del cursor11

                        #print  numero_aeu

                numero_aeu = numero_aeu + 1

#fc='D:/ShapesPruebasSegmentacionUrbana/Zones/Shape020601001000001.shp'

#ubigeos=["020601","021806","110204"]
#Renumerar_AEU(ubigeos)


def Renumerar_AEU_Zona2(ubigeo,zona):
    #manzanas=Listar_Manzanas_Ordenado_ID(ubigeo,zona)[:]
    mzs_aeu=Listar_MZS_AEU_Reordenado(ubigeo, zona)[:]
    mzs_aeu_temp=mzs_aeu[:]


    for mz in mzs_aeu:
        idmanzana=str(mz[0])
        #where_x = ' "IDMANZANA"=\'' + str(mz[0]) + '\''
        numero_aeu_anterior=str(mz[1])
        numero_aeu_nuevo = int(mz[2])


 #       arcpy.SelectLayerByAttribute_management("mzs_aeu2", "NEW_SELECTION", where_x)
 #       with arcpy.da.SearchCursor("mzs_aeu2", ['IDMANZANA', 'AEU']) as cursor7:
 #           for row7 in cursor7:
        where2 = '  "IDMANZANA"=\'' + idmanzana + '\' AND AEU=' + numero_aeu_anterior
        where3 = '  "IDMANZANA"=\'' + idmanzana + '\' '

        where4 = '"UBIGEO"=\'' + idmanzana[0:6] + '\' AND "ZONA" =\'' + idmanzana[6:11] + '\' AND "MANZANA"=\'' + idmanzana[11:] + '\' AND AEU=' + numero_aeu_anterior
        #print "aeu actual: " +str(numero_aeu) + "IDMANZANA:"+str(row7[0])+str("aeu anterior:") +str(row7[1])
        print  where2
        with arcpy.da.UpdateCursor(r"D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf",
                                   ['UBIGEO', 'ZONA', 'AEU_FINAL', 'IDMANZANA'], where2) as cursor8:
            for row8 in cursor8:
                row8[2] = numero_aeu_nuevo
                #manzanax = str(row8[3])

                cursor8.updateRow(row8)
                # print manzanax

        del cursor8

        with arcpy.da.UpdateCursor(r"D:\ShapesPruebasSegmentacionUrbana\Renumerar\TB_RUTAS.shp",
                                   ['UBIGEO', 'ZONA', 'AEU_FINAL', 'MANZANA'], where4) as cursor9:
            for row9 in cursor9:
                row9[2] = numero_aeu_nuevo
                cursor9.updateRow(row9)
        del cursor9
        with arcpy.da.UpdateCursor(r"D:\ShapesPruebasSegmentacionUrbana\Renumerar\TB_MZS_TRABAJO.shp",
                                   ['UBIGEO', 'ZONA', 'AEU_FINAL', 'IDMANZANA'], where3) as cursor10:
            for row10 in cursor10:
                row10[2] = numero_aeu_nuevo
                cursor10.updateRow(row10)
        del cursor10
        with arcpy.da.UpdateCursor(r"D:\ShapesPruebasSegmentacionUrbana\Renumerar\TB_VIVIENDAS_U_TRABAJO.shp",
                                   ['UBIGEO', 'ZONA', 'AEU_FINAL', 'MANZANA'], where4) as cursor11:
            for row11 in cursor11:
                row11[2] = numero_aeu_nuevo
                cursor11.updateRow(row11)
        del cursor11



def Renumerar_AEU_Zona3(ubigeo,zona):
    #manzanas=Listar_Manzanas_Ordenado_ID(ubigeo,zona)[:]

    where_x = ' "UBIGEO"=\'' + str(ubigeo) + '\' AND "ZONA"=\''+str(zona)+'\''
    arcpy.SelectLayerByAttribute_management("min_aeu_sort", "NEW_SELECTION", where_x)

    numero_aeu_nuevo=1
    for row11 in arcpy.da.SearchCursor("min_aeu_sort",['UBIGEO','ZONA','AEU','MIN_IDMANZANA']):
        aeu_anterior=str(row11[2])
        where11=' "UBIGEO"=\''+row11[0]+'\' AND "ZONA"=\'' +row11[1]+'\' AND AEU='+aeu_anterior

        print "AEU: "+str(aeu_anterior)+" MANZANA: "+str(row11[1])+" aeu_nuevo:"+ str(numero_aeu_nuevo)

        with arcpy.da.UpdateCursor(r"D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf",
                                   ['UBIGEO', 'ZONA', 'AEU_FINAL', 'IDMANZANA'], where11) as cursor8:
            for row8 in cursor8:
                row8[2] = numero_aeu_nuevo
                #manzanax = str(row8[3])

                cursor8.updateRow(row8)
                # print manzanax

        del cursor8

        with arcpy.da.UpdateCursor(r"D:\ShapesPruebasSegmentacionUrbana\Renumerar\TB_RUTAS.shp",
                                   ['UBIGEO', 'ZONA', 'AEU_FINAL', 'MANZANA'], where11) as cursor9:
            for row9 in cursor9:
                row9[2] = numero_aeu_nuevo
                cursor9.updateRow(row9)
        del cursor9
        with arcpy.da.UpdateCursor(r"D:\ShapesPruebasSegmentacionUrbana\Renumerar\TB_MZS_TRABAJO.shp",
                                   ['UBIGEO', 'ZONA', 'AEU_FINAL', 'IDMANZANA'], where11) as cursor10:
            for row10 in cursor10:
                row10[2] = numero_aeu_nuevo
                cursor10.updateRow(row10)
        del cursor10

        with arcpy.da.UpdateCursor(r"D:\ShapesPruebasSegmentacionUrbana\Renumerar\TB_VIVIENDAS_U_TRABAJO.shp",
                                   ['UBIGEO', 'ZONA', 'AEU_FINAL', 'MANZANA'], where11) as cursor11:
            for row11 in cursor11:
                row11[2] = numero_aeu_nuevo
                cursor11.updateRow(row11)
        del cursor11

        numero_aeu_nuevo = 1+numero_aeu_nuevo


ubigeos=["020601","021806","110204"]
Renumerar_AEU(ubigeos)







    #where_segundo = ' "UBIGEO"=\'' + str(row1[0]) + ' \' AND "ZONA" =\'' + str(row1[1])



    #for row1 in arcpy.da.SearchCursor(ZONA_CANT_AEU, ["UBIGEO", "ZONA", "COUNT_AEU"]):






#print Listar_MZS_AEU_Reordenado("020601","00100")



#
#
#    while (len(manzanas_temporal)>0):
#        manzana=manzanas_temporal[0]
#        where_x=' "IDMANZANA"=\''+str(manzana)+'\''
#
#        #print where_x
#        arcpy.SelectLayerByAttribute_management("mzs_aeu", "NEW_SELECTION", where_x)
#
#        with arcpy.da.SearchCursor("mzs_aeu", ['UBIGEO','ZONA','AEU','IDMANZANA']) as cursor6:
#            for row6 in cursor6:
#                where1 = ' "UBIGEO"=\''+str(row6[0])+'\' AND "ZONA"=\''+str(row6[1])+'\' AND AEU=' +str(row6[2])
#
#                arcpy.SelectLayerByAttribute_management("mzs_aeu2", "NEW_SELECTION", where1)
#
#                with arcpy.da.SearchCursor("mzs_aeu2", ['IDMANZANA','AEU']) as cursor7:
#                    for row7 in cursor7:
#                        where2='  "IDMANZANA"=\''+str(row7[0])+'\' AND AEU=' +str(row7[1])
#                        where3 = '  "IDMANZANA"=\'' + str(row7[0]) + '\' '
#
#                        where4 = '"UBIGEO"=\'' + str(row7[0])[0:6] + '\' AND "ZONA" =\'' + str(row7[0])[6:11] + '\' AND "MANZANA"=\'' + str(row7[0])[11:] + '\' AND AEU='+str(row7[1])
#
#                        with arcpy.da.UpdateCursor(r"D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf", ['UBIGEO', 'ZONA', 'AEU','IDMANZANA'],where2) as cursor8:
#                            for row8 in cursor8:
#                                row8[2]=int(numero_aeu)
#                                manzanax = str(row8[3])
#                                cursor8.updateRow(row8)
#
#                                #print manzanax
#                                if manzanax in manzanas_temporal:
#                                    manzanas_temporal.remove(manzanax)
#                        del cursor8
#
#                        with arcpy.da.UpdateCursor(r"D:\ShapesPruebasSegmentacionUrbana\Renumerar\TB_RUTAS.shp", ['UBIGEO', 'ZONA', 'AEU','MANZANA'],where4) as cursor9:
#                            for row9 in cursor9:
#                                row9[2]=int(numero_aeu)
#                                cursor9.updateRow(row9)
#                        del cursor9
#                        with arcpy.da.UpdateCursor(r"D:\ShapesPruebasSegmentacionUrbana\Renumerar\TB_MZS_TRABAJO.shp",
#                                                  ['UBIGEO', 'ZONA', 'AEU', 'IDMANZANA'],where3 ) as cursor10:
#                           for row10 in cursor10:
#                               row10[2] = int(numero_aeu)
#                               cursor10.updateRow(row10)
#                        del cursor10
#                        with arcpy.da.UpdateCursor(r"D:\ShapesPruebasSegmentacionUrbana\Renumerar\TB_VIVIENDAS_U_TRABAJO.shp",
#                                      ['UBIGEO', 'ZONA', 'AEU', 'MANZANA'], where4) as cursor11:
#                            for row11 in cursor11:
#                                row11[2] = int(numero_aeu)
#                                cursor11.updateRow(row11)
#                        del cursor11
#
#                        #print  numero_aeu
#
#                numero_aeu = numero_aeu + 1

#print Listar_MZS_AEU_Reordenado("021806","00500")



#print Listar_Manzanas(fc)
#print Ordenar_Manzanas_Distancia([['02060100100052', -9.2753, 0.005289302071], ['02060100100051', -9.275, 0.00607088824604], ['02060100100050', -9.275384509, 0.00603327842443], ['02060100100049', -9.27538450956, 0.00569832380288], ['02060100100048', -9.27538450956, 0.00694542843751], ['02060100100047', -9.27538450956, 0.00814114319356], ['02060100100046', -9.27538450956, 0.00786541558254], ['02060100100045', -9.27538450956, 0.00768225267149], ['02060100100044', -9.27538450956, 0.00687429566603], ['02060100100043', -9.27538450956, 0.00615642048946], ['02060100100042', -9.27538450956, 0.00544710417205], ['02060100100041', -9.27538450956, 0.00506511928706], ['02060100100040', -9.27538450956, 0.00469401863801], ['02060100100039', -9.27538450956, 0.00463311187778], ['02060100100038', -9.27538450956, 0.00445129885122], ['02060100100037', -9.27538450956, 0.00395597152188], ['02060100100036', -9.27538450956, 0.00459415486326], ['02060100100035', -9.27538450956, 0.005204848208], ['02060100100034', -9.27538450956, 0.00595451486063], ['02060100100033', -9.27538450956, 0.00668772108724], ['02060100100032', -9.27538450956, 0.00752505751822], ['02060100100031', -9.27538450956, 0.0064725895779], ['02060100100030', -9.27538450956, 0.00564674653672], ['02060100100029', -9.27538450956, 0.00578274415931], ['02060100100028', -9.27538450956, 0.00527279077319], ['02060100100027', -9.27538450956, 0.00513738996896], ['02060100100026', -9.27538450956, 0.00484434544945], ['02060100100025B', -9.27538450956, 0.00445966711228], ['02060100100025A', -9.27538450956, 0.00364010167219], ['02060100100024', -9.27538450956, 0.00339940088018], ['02060100100023', -9.27538450956, 0.00259165391858], ['02060100100022H', -9.27538450956, 0.00187699304402], ['02060100100022G', -9.27538450956, 0.00343231508695], ['02060100100022F', -9.27538450956, 0.00408966806788], ['02060100100022E', -9.27538450956, 0.00318391083245], ['02060100100022C', -9.27538450956, 0.00375365572268], ['02060100100022B', -9.27538450956, 0.0039571868532], ['02060100100021', -9.27538450956, 0.00122139994439], ['02060100100020', -9.27538450956, 0.0017455567639], ['02060100100019', -9.27538450956, 0.00257133275798], ['02060100100018', -9.27538450956, 0.00315129415581], ['02060100100017', -9.27538450956, 0.00388294554543], ['02060100100016', -9.27538450956, 0.00469693004984], ['02060100100015', -9.27538450956, 0.00552538303714], ['02060100100014', -9.27538450956, 0.00630533255361], ['02060100100013', -9.27538450956, 0.00622993277191], ['02060100100012', -9.27538450956, 0.00544790104639], ['02060100100011', -9.27538450956, 0.00539393175231], ['02060100100010B', -9.27538450956, 0.00597253665343], ['02060100100010A', -9.27538450956, 0.00635238811554], ['02060100100009', -9.27538450956, 0.00620373455274], ['02060100100008C', -9.27538450956, 0.00579689637834], ['02060100100007A', -9.27538450956, 0.00373873535662], ['02060100100007', -9.27538450956, 0.0042974244792], ['02060100100006A', -9.27538450956, 0.00356071056787], ['02060100100005', -9.27538450956, 0.00471002945897], ['02060100100004', -9.27538450956, 0.00459523272512], ['02060100100003', -9.27538450956, 0.00302933125258], ['02060100100002C', -9.27538450956, 0.00253037896853], ['02060100100002B', -9.27538450956, 0.00149098798245], ['02060100100002A', -9.27538450956, 0.00263482046558]])





