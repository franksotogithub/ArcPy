import random
import arcpy
import math
import numpy as np
from decimal import *

arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"

def OrdenarComponentesViviendas(manzanas):
    a = np.array(manzanas)
    b=a[a[:, 1].astype(int).argsort()]
    #print "sin ordenar"
    #print a
    #print "ordenado"
    #print b
    rs=b.tolist()
    rs_final=[]
    #print rs


    manzanasx=manzanas[:]
    #print manzanasx
    for el2 in rs:
        for el in manzanasx:
            if (el[0]==el2[0]):
                rs_final.append(el)
                break
    return  rs_final




def OrdenarManzanas_Cant_Viviendas_XY(manzanasx):
    a = np.array(manzanasx)
    # a = np.array([[3, 2], [6, 2], [3, 6], [3, 4], [5, 3]])
    idx = np.lexsort((a[:, 3].astype(float), a[:, 4].astype(float) * -1, a[:, 1].astype(int)))
    b = a[idx]
    rs = b.tolist()
    rs_final = []

    for el2 in rs:
        for el in manzanasx:
            if (el[0] == el2[0]):
                rs_final.append(el)
                break
    return rs_final
    # print a[:,1].astype(int)
    # print "sin ordenar"
    # print a
    # print "ordenado"
    # print rs_final


def OrdenarManzanas_XY(manzanasx):
    a = np.array(manzanasx)
    # a = np.array([[3, 2], [6, 2], [3, 6], [3, 4], [5, 3]])
    idx = np.lexsort((a[:, 3].astype(float), a[:, 4].astype(float) * -1))
    b = a[idx]
    rs = b.tolist()
    rs_final = []

    for el2 in rs:
        for el in manzanasx:
            if (el[0] == el2[0]):
                rs_final.append(el)
                break

    # print a[:,1].astype(int)

    return rs_final



#def OrdenarManzanasXY_CantidadViviendas(manzanas):


#
#
#def OrdenarManzanasXY(manzanas):
#    a = np.array(manzanas)
#    b = a[a[:, 1].astype(int).argsort()]
#    # print "sin ordenar"
#    # print a
#    # print "ordenado"
#    # print b
#    rs = b.tolist()
#    rs_final = []


def Total_Viviendas(manzanas):
    tot=0
    for el in manzanas:
        tot=el[1]+tot

    return tot

def SolucionInicial(manzanas):


    #fc = zona
    solucion_inicial = []
    manzanas_temporal=[]
    #manzanas = []

    cant_viv_estandar=14
    grupos=[]

    cant_aeus_no_asignados=0


    total_viv=0
    cant_manzanas_sin_asignar=0
    manzanas_asignadas=[]


    #manzanas = []

    manzanas_adyacentes = []

    #fieldName1 = "GRUPO"


    #arcpy.AddField_management(fc, fieldName1, "SHORT")

#    where=' "VIV_MZ"<16 '
#    for row1 in arcpy.da.SearchCursor(fc, ["IDMANZANA", "VIV_MZ", "AREA", "xCentroid", "yCentroid"],where):
#        manzana = []
#        total_viv = row1[1] + total_viv
#        cant_manzanas_sin_asignar = 1 + cant_manzanas_sin_asignar
#
#        manzana = [str(row1[0]), int(row1[1]), float(row1[2]), float(row1[3]),float(row1[4])]
#        manzanas.append(manzana)
#    del row1



    cant_manzanas_sin_asignar=len(manzanas)
    manzanas_temporal=manzanas[:]

    total_viv=Total_Viviendas(manzanas_temporal)



    cant_aeus=int(math.ceil(float(total_viv)/float(cant_viv_estandar)))
    cant_aeus_no_asignados=cant_aeus

    #print len(manzanas)

    cant_grupos=0


    for i in range(cant_aeus):
        tamanio_temporal = len(manzanas_temporal)
        #print tamanio_temporal
        k = random.randint(0, tamanio_temporal - 1)
        manzana_temporal = manzanas_temporal[k]
        grupo=[]
        grupo.append(manzana_temporal)
        manzanas_asignadas.append(manzana_temporal)  # se aumente la cantidad de manzanas asiganndasd
        cant_manzanas_sin_asignar = cant_manzanas_sin_asignar - 1  # se disminuye la cantidad de manzanas sin asignar
        manzanas_temporal.remove(manzana_temporal)  # se remueve del temporal la manzana ya asiganda






        where_expression = ' "IDMANZANA"=\'' + str(manzana_temporal[0]) + '\' AND "TOT_VIV_AD"<16 '


        for row3 in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
                                          ["IDMANZ_ADY","TOT_VIV_AD","AREA_ADY","X_ADY","Y_ADY"], where_expression):
            #manzanas_adyacentes.append(str(row3[0]))
            manzana_adyacente = [str(row3[0]), int(row3[1]), float(row3[2]), float(row3[3]), float(row3[4])]

            if cant_manzanas_sin_asignar > cant_aeus_no_asignados:
                if  (manzana_adyacente not in manzanas_asignadas) and (manzana_adyacente in manzanas):
                    grupo.append(manzana_adyacente) # se agrega al grupo
                    manzanas_asignadas.append(manzana_adyacente) # se aumenta la cantidad de manzanas asignadas
                    cant_manzanas_sin_asignar=cant_manzanas_sin_asignar-1# se disminuye la cantidad de manzanas sin asignar
                    manzanas_temporal.remove(manzana_adyacente) # se remueve del temporal la manzana ya asiganda




        cant_aeus_no_asignados=cant_aeus_no_asignados-1

        solucion_inicial.append(grupo)


    tamanio_temp=len(manzanas_temporal)

    find=False

    while tamanio_temp>0:
        find = False
        k = random.randint(0, tamanio_temp - 1)


        manzana_temporal=manzanas_temporal[k]

        where_expression = ' "IDMANZANA"=\'' + str(manzana_temporal[0]) + '\'  AND "TOT_VIV_AD"<16 '

        for row4 in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
                                          ["IDMANZ_ADY","TOT_VIV_AD","AREA_ADY","X_ADY","Y_ADY"], where_expression):

            manzanax=[str(row4[0]), int(row4[1]), float(row4[2]), float(row4[3]), float(row4[4])]
            grupo_temporal=[]
            for grupo_temporal in solucion_inicial:

                if (manzanax in grupo_temporal) and (manzanax in manzanas):
#                    grupo_temporal2=[]

#                    for el in grupo_temporal:
#                        grupo_temporal2.append(el)
#
#                    grupo_temporal2.append(manzana_temporal)

                    solucion_inicial.remove(grupo_temporal)
                    grupo_temporal.append(manzana_temporal)
                    solucion_inicial.append(grupo_temporal)

                    find=True

                    #solucion_vecina.remove(grupo_temporal)
                    #grupo_temporal.append(manzana_escogida)
                    #solucion_vecina.append(grupo_temporal)



                    break

            if find==True:
                break
        #del row4

        manzanas_temporal.remove(manzana_temporal)
        tamanio_temp = len(manzanas_temporal)

    #resultado = []
    #resultado.append(solucion_inicial)
    #resultado.append(manzanas)

    return solucion_inicial






def Manzanas_menores_iguales_16(zona):
   fc=zona
   total_viv = 0

   manzanas = []

   where = ' "VIV_MZ"<=16 '
   for row1 in arcpy.da.SearchCursor(fc, ["IDMANZANA", "VIV_MZ", "AREA", "xCentroid", "yCentroid"], where):
       manzana = [str(row1[0]), int(row1[1]), float(row1[2]), float(row1[3]), float(row1[4])]
       manzanas.append(manzana)
   del row1

   return  manzanas


def Componentes_conexas(lista_adyacencia,manzanas):
    manzanas_temporal=manzanas[:]
    componentes_conexas=[]

    componente_conexa=[]
    manzana_temporal=[]
    V=[]

    while (len(manzanas_temporal)>0):
        componente_conexa = []
        manzana_temporal=manzanas_temporal[0]
        where_expression = ' "IDMANZANA"=\'' + str(manzana_temporal[0]) + '\'  AND "TOT_VIV_AD"<=16 '



        V = []

        manzanas_temporal.remove(manzana_temporal)
        componente_conexa.append(manzana_temporal)

        for row4 in arcpy.da.SearchCursor(lista_adyacencia,
                                          ["IDMANZ_ADY","TOT_VIV_AD","AREA_ADY","X_ADY","Y_ADY"], where_expression):
            fila=[]
            fila=[str(row4[0]),int(row4[1]),float(row4[2]),float(row4[3]),float(row4[4])]
            if fila in manzanas:
                V.append(fila)
                manzanas_temporal.remove(fila)
                componente_conexa.append(fila)






        while (len(V)>0):
            manzana_temporal2=V[0]
            where_expression2 = ' "IDMANZANA"=\'' + str(manzana_temporal2[0]) + '\'  AND "TOT_VIV_AD"<=16 '
            for row5 in arcpy.da.SearchCursor(
                    lista_adyacencia,
                    ["IDMANZ_ADY", "TOT_VIV_AD", "AREA_ADY", "X_ADY", "Y_ADY"], where_expression2):
                fila2 = []
                fila2=[str(row5[0]), int(row5[1]), float(row5[2]), float(row5[3]), float(row5[4])]
                if fila2 in manzanas:
                    if fila2 not in componente_conexa:
                        V.append(fila2)
                        manzanas_temporal.remove(fila2)
                        componente_conexa.append(fila2)
            V.remove(manzana_temporal2)

        componentes_conexas.append(componente_conexa)


    return componentes_conexas



def Componentes_conexas2(lista_adyacencia,manzanas):
    manzanas_temporal=manzanas[:]
    componentes_conexas=[]

    componente_conexa=[]
    manzana_temporal=[]
    V=[]

    while (len(manzanas_temporal)>0):
        componente_conexa = []
        manzana_temporal=manzanas_temporal[0]
        where_expression = ' "IDMANZANA"=\'' + str(manzana_temporal[0]) + '\'  AND "TOT_VIV_AD"<=16 '



        V = []

        manzanas_temporal.remove(manzana_temporal)
        componente_conexa.append(manzana_temporal)

        for row4 in arcpy.da.SearchCursor(lista_adyacencia,
                                          ["IDMANZ_ADY","TOT_VIV_AD","AREA_ADY","X_ADY","Y_ADY"], where_expression):
            fila=[]
            fila=[str(row4[0]),int(row4[1]),float(row4[2]),float(row4[3]),float(row4[4])]
            if fila in manzanas:
                V.append(fila)
                manzanas_temporal.remove(fila)
                componente_conexa.append(fila)






        while (len(V)>0):
            manzana_temporal2=V[0]
            where_expression2 = ' "IDMANZANA"=\'' + str(manzana_temporal2[0]) + '\'  AND "TOT_VIV_AD"<=16 '
            for row5 in arcpy.da.SearchCursor(
                    lista_adyacencia,
                    ["IDMANZ_ADY", "TOT_VIV_AD", "AREA_ADY", "X_ADY", "Y_ADY"], where_expression2):
                fila2 = []
                fila2=[str(row5[0]), int(row5[1]), float(row5[2]), float(row5[3]), float(row5[4])]
                if fila2 in manzanas:
                    if fila2 not in componente_conexa:
                        V.append(fila2)
                        manzanas_temporal.remove(fila2)
                        componente_conexa.append(fila2)
            V.remove(manzana_temporal2)

        componentes_conexas.append(componente_conexa)


    return componentes_conexas


def Componentes_conexas_cantidad_viv(manzanas,cant_max_viviendas=16):
    if len(manzanas)>1:
        manzanas_temporal = OrdenarComponentesViviendas(manzanas)[:]
    else:
        manzanas_temporal =manzanas

    componentes_conexas = []
    componente_conexa = []
    manzana_temporal = []
    cant_max_viviendas=16

    V = []

    cant_viv=0
    while (len(manzanas_temporal) > 0):
        componente_conexa = []
        manzana_temporal = manzanas_temporal[0]
        where_expression = ' "IDMANZANA"=\'' + str(manzana_temporal[0]) + '\'  AND "TOT_VIV_AD"<=16 '
        V = []
        manzanas_temporal.remove(manzana_temporal)
        componente_conexa.append(manzana_temporal)

        cant_viv=0
        cant_viv=manzana_temporal[1]+cant_viv

        for row4 in arcpy.da.SearchCursor(
                "D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
                ["IDMANZ_ADY", "TOT_VIV_AD", "AREA_ADY", "X_ADY", "Y_ADY"], where_expression):
            fila = []
            fila = [str(row4[0]), int(row4[1]), float(row4[2]), float(row4[3]), float(row4[4])]

            if (fila in manzanas_temporal) and ((cant_viv+fila[1])<=cant_max_viviendas):
                V.append(fila)
                manzanas_temporal.remove(fila)
                componente_conexa.append(fila)
                cant_viv=cant_viv+fila[1]

        while (len(V) > 0):

            manzana_temporal2 = V[0]
            where_expression2 = ' "IDMANZANA"=\'' + str(manzana_temporal2[0]) + '\'  AND "TOT_VIV_AD"<=16 '
            for row5 in arcpy.da.SearchCursor(
                    "D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
                    ["IDMANZ_ADY", "TOT_VIV_AD", "AREA_ADY", "X_ADY", "Y_ADY"], where_expression2):
                fila2 = []
                fila2 = [str(row5[0]), int(row5[1]), float(row5[2]), float(row5[3]), float(row5[4])]
                if (fila2 in manzanas_temporal) and ((cant_viv+fila2[1])<=cant_max_viviendas):
                    if fila2 not in componente_conexa:
                        V.append(fila2)
                        manzanas_temporal.remove(fila2)
                        componente_conexa.append(fila2)
                        cant_viv=cant_viv+fila2[1]
            V.remove(manzana_temporal2)
            if(len(V)>1):
                V=OrdenarComponentesViviendas(V)[:]

        if len(manzanas_temporal) > 1:
            manzanas_temporal=OrdenarComponentesViviendas(manzanas_temporal)[:]

        componentes_conexas.append(componente_conexa)

    #print np.array(componentes_conexas)
    return componentes_conexas




def Agrupacion(manzanas,cant_max_viviendas=16):
    if len(manzanas)>1:
        manzanas_temporal = OrdenarManzanas_XY(manzanas)[:]
    else:
        manzanas_temporal =manzanas

    componentes_conexas = []
    componente_conexa = []
    manzana_temporal = []
    cant_max_viviendas=16

    V = []

    cant_viv=0
    while (len(manzanas_temporal) > 0):
        componente_conexa = []
        manzana_temporal = manzanas_temporal[0]
        where_expression = ' "IDMANZANA"=\'' + str(manzana_temporal[0]) + '\'  AND "TOT_VIV_AD"<=16 '
        V = []
        manzanas_temporal.remove(manzana_temporal)
        componente_conexa.append(manzana_temporal)

        cant_viv=0
        cant_viv=manzana_temporal[1]+cant_viv

        for row4 in arcpy.da.SearchCursor(
                "D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
                ["IDMANZ_ADY", "TOT_VIV_AD", "AREA_ADY", "X_ADY", "Y_ADY"], where_expression):
            fila = []
            fila = [str(row4[0]), int(row4[1]), float(row4[2]), float(row4[3]), float(row4[4])]

            if (fila in manzanas_temporal) and ((cant_viv+fila[1])<=cant_max_viviendas):
                V.append(fila)
                manzanas_temporal.remove(fila)
                componente_conexa.append(fila)
                cant_viv=cant_viv+fila[1]

        while (len(V) > 0):
            if(len(V)>1):
                V=OrdenarManzanas_XY(V)[:]
            manzana_temporal2 = V[0]
            where_expression2 = ' "IDMANZANA"=\'' + str(manzana_temporal2[0]) + '\'  AND "TOT_VIV_AD"<=16 '
            for row5 in arcpy.da.SearchCursor(
                    "D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
                    ["IDMANZ_ADY", "TOT_VIV_AD", "AREA_ADY", "X_ADY", "Y_ADY"], where_expression2):
                fila2 = []
                fila2 = [str(row5[0]), int(row5[1]), float(row5[2]), float(row5[3]), float(row5[4])]
                if (fila2 in manzanas_temporal) and ((cant_viv+fila2[1])<=cant_max_viviendas):
                    if fila2 not in componente_conexa:
                        V.append(fila2)
                        manzanas_temporal.remove(fila2)
                        componente_conexa.append(fila2)
                        cant_viv=cant_viv+fila2[1]
            V.remove(manzana_temporal2)


        if len(manzanas_temporal) > 1:
            manzanas_temporal=OrdenarManzanas_XY(manzanas_temporal)[:]

        componentes_conexas.append(componente_conexa)

    #print np.array(componentes_conexas)
    return componentes_conexas





#resultado = []
#resultado.append(solucion_inicial)
#resultado.append(manzanas)

#return resultado
#manzanass=Manzanas_menores_16("D:/ShapesPruebasSegmentacionUrbana/Zones/Shape020601001000001.shp")
#print manzanass

#print Componentes_conexas(manzanass)

#print Componentes_conexas(manzanass)
#[
#    [['02060100100002A', 1, 6974.02, -77.64796604746, -9.27717130724], ['02060100100002C', 3, 8991.75, -77.64774810321, -9.27671177438], ['02060100100003', 11, 25882.38, -77.64831341561, -9.2779636248], ['02060100100006A', 14, 2426.82, -77.64713267431, -9.27796053189], ['02060100100007A', 6, 976.08, -77.64681330164, -9.27749053408], ['02060100100002B', 9, 3732.87, -77.64856364605, -9.27582546135], ['02060100100017', 15, 3106.22, -77.64831734371, -9.27892918472], ['02060100100018', 13, 3267.25, -77.6489079174, -9.27837475553], ['02060100100007', 11, 2774.05, -77.6467956581, -9.27792742648], ['02060100100004', 13, 4036.89, -77.64738349487, -9.27922782288], ['02060100100016', 10, 3382.55, -77.64768866138, -9.27952701083], ['02060100100025B', 13, 2903.56, -77.64891830393, -9.27956969879], ['02060100100026', 10, 3503.08, -77.64801436769, -9.27984577051], ['02060100100019', 6, 2078.01, -77.64939758749, -9.2779057933], ['02060100100024', 14, 3298.55, -77.64922314319, -9.27871534673], ['02060100100015', 14, 2992.93, -77.64706447125, -9.28012537091], ['02060100100027', 0, 2504.99, -77.64833792274, -9.28006821005], ['02060100100030', 10, 3666.43, -77.64738311753, -9.28043809628], ['02060100100022E', 10, 2148.09, -77.65047996988, -9.27853124908], ['02060100100037', 14, 4260.82, -77.64976991749, -9.2793382606], ['02060100100014', 6, 2816.89, -77.64647552001, -9.28067727897], ['02060100100028', 0, 436.36, -77.64820643693, -9.28037709219], ['02060100100029', 11, 3403.85, -77.64769097785, -9.28072768707], ['02060100100022C', 8, 1749.96, -77.65109749309, -9.27894285044], ['02060100100040', 0, 568.1, -77.64960752861, -9.28006925456], ['02060100100034', 1, 3557.15, -77.64800975671, -9.28103021418], ['02060100100022G', 0, 7779.74, -77.65167327703, -9.27832473719], ['02060100100033', 11, 3506.38, -77.64739944982, -9.28158617318], ['02060100100043', 8, 3387.64, -77.64832646898, -9.28133579638], ['02060100100022F', 1, 32570.4, -77.65254879353, -9.27850255719], ['02060100100032', 12, 3639.07, -77.64674376106, -9.28221453229], ['02060100100042', 14, 2927.82, -77.64896666492, -9.28075063113]]
#    , [['02060100100009', 0, 2607.73, -77.6455099662, -9.27976542932], ['02060100100010A', 0, 999.64, -77.64563529772, -9.280090282]]
#    , [['02060100100010B', 10, 2110.56, -77.6460875685, -9.27997993296]]
#    , [['02060100100021', 5, 3780.24, -77.65084864166, -9.27615686214]]
#    , [['02060100100046', 11, 3560.43, -77.64735426863, -9.28282571664]]
#    , [['02060100100050', 1, 2721.74, -77.64953618962, -9.28140666084]]
#    , [['02060100100052', 0, 1480.49, -77.6500373972, -9.28067208974]]]





#[
# [['02060100100002A', 1, 6974.02, -77.64796604746, -9.27717130724], ['02060100100002C', 3, 8991.75, -77.64774810321, -9.27671177438], ['02060100100003', 11, 25882.38, -77.64831341561, -9.2779636248], ['02060100100006A', 14, 2426.82, -77.64713267431, -9.27796053189], ['02060100100007A', 6, 976.08, -77.64681330164, -9.27749053408], ['02060100100002B', 9, 3732.87, -77.64856364605, -9.27582546135], ['02060100100017', 15, 3106.22, -77.64831734371, -9.27892918472], ['02060100100018', 13, 3267.25, -77.6489079174, -9.27837475553], ['02060100100007', 11, 2774.05, -77.6467956581, -9.27792742648], ['02060100100004', 13, 4036.89, -77.64738349487, -9.27922782288], ['02060100100016', 10, 3382.55, -77.64768866138, -9.27952701083], ['02060100100025B', 13, 2903.56, -77.64891830393, -9.27956969879], ['02060100100026', 10, 3503.08, -77.64801436769, -9.27984577051], ['02060100100019', 6, 2078.01, -77.64939758749, -9.2779057933], ['02060100100024', 14, 3298.55, -77.64922314319, -9.27871534673], ['02060100100015', 14, 2992.93, -77.64706447125, -9.28012537091], ['02060100100027', 0, 2504.99, -77.64833792274, -9.28006821005], ['02060100100030', 10, 3666.43, -77.64738311753, -9.28043809628], ['02060100100022E', 10, 2148.09, -77.65047996988, -9.27853124908], ['02060100100037', 14, 4260.82, -77.64976991749, -9.2793382606], ['02060100100014', 6, 2816.89, -77.64647552001, -9.28067727897], ['02060100100028', 0, 436.36, -77.64820643693, -9.28037709219], ['02060100100029', 11, 3403.85, -77.64769097785, -9.28072768707], ['02060100100022C', 8, 1749.96, -77.65109749309, -9.27894285044], ['02060100100040', 0, 568.1, -77.64960752861, -9.28006925456], ['02060100100034', 1, 3557.15, -77.64800975671, -9.28103021418], ['02060100100022G', 0, 7779.74, -77.65167327703, -9.27832473719], ['02060100100033', 11, 3506.38, -77.64739944982, -9.28158617318], ['02060100100043', 8, 3387.64, -77.64832646898, -9.28133579638], ['02060100100022F', 1, 32570.4, -77.65254879353, -9.27850255719], ['02060100100032', 12, 3639.07, -77.64674376106, -9.28221453229], ['02060100100042', 14, 2927.82, -77.64896666492, -9.28075063113]],
# [['02060100100009', 0, 2607.73, -77.6455099662, -9.27976542932], ['02060100100010A', 0, 999.64, -77.64563529772, -9.280090282], ['02060100100010B', 10, 2110.56, -77.6459356501, -9.28007347183]],
# [['02060100100021', 5, 3780.24, -77.65084864166, -9.27615686214]],
# [['02060100100046', 11, 3560.43, -77.64735426863, -9.28282571664]],
# [['02060100100050', 1, 2721.74, -77.64953618962, -9.28140666084]],
# [['02060100100052', 0, 1480.49, -77.6500373972, -9.28067208974]]
#
# ]





# [[['02060100100002A', 1, 6974.02, -77.64796604746, -9.27717130724], ['02060100100002C', 3, 8991.75, -77.64774810321, -9.27671177438], ['02060100100003', 11, 25882.38, -77.64831341561, -9.2779636248], ['02060100100006A', 14, 2426.82, -77.64713267431, -9.27796053189], ['02060100100007A', 6, 976.08, -77.64681330164, -9.27749053408], ['02060100100002B', 9, 3732.87, -77.64856364605, -9.27582546135], ['02060100100017', 15, 3106.22, -77.64831734371, -9.27892918472], ['02060100100018', 13, 3267.25, -77.6489079174, -9.27837475553], ['02060100100007', 11, 2774.05, -77.6467956581, -9.27792742648], ['02060100100004', 13, 4036.89, -77.64738349487, -9.27922782288], ['02060100100016', 10, 3382.55, -77.64768866138, -9.27952701083], ['02060100100025B', 13, 2903.56, -77.64891830393, -9.27956969879], ['02060100100026', 10, 3503.08, -77.64801436769, -9.27984577051], ['02060100100019', 6, 2078.01, -77.64939758749, -9.2779057933], ['02060100100024', 14, 3298.55, -77.64922314319, -9.27871534673], ['02060100100015', 14, 2992.93, -77.64706447125, -9.28012537091], ['02060100100027', 0, 2504.99, -77.64833792274, -9.28006821005], ['02060100100030', 10, 3666.43, -77.64738311753, -9.28043809628], ['02060100100022E', 10, 2148.09, -77.65047996988, -9.27853124908], ['02060100100037', 14, 4260.82, -77.64976991749, -9.2793382606], ['02060100100014', 6, 2816.89, -77.64647552001, -9.28067727897], ['02060100100028', 0, 436.36, -77.64820643693, -9.28037709219], ['02060100100029', 11, 3403.85, -77.64769097785, -9.28072768707], ['02060100100022C', 8, 1749.96, -77.65109749309, -9.27894285044], ['02060100100040', 0, 568.1, -77.64960752861, -9.28006925456], ['02060100100034', 1, 3557.15, -77.64800975671, -9.28103021418], ['02060100100022G', 0, 7779.74, -77.65167327703, -9.27832473719], ['02060100100033', 11, 3506.38, -77.64739944982, -9.28158617318], ['02060100100043', 8, 3387.64, -77.64832646898, -9.28133579638], ['02060100100022F', 1, 32570.4, -77.65254879353, -9.27850255719], ['02060100100032', 12, 3639.07, -77.64674376106, -9.28221453229], ['02060100100042', 14, 2927.82, -77.64896666492, -9.28075063113]],
#  [['02060100100009', 0, 2607.73, -77.6455099662, -9.27976542932], ['02060100100010A', 0, 999.64, -77.64563529772, -9.280090282], ['02060100100010B', 10, 2110.56, -77.6459356501, -9.28007347183]],
#  [['02060100100021', 5, 3780.24, -77.65084864166, -9.27615686214]],
#  [['02060100100046', 11, 3560.43, -77.64735426863, -9.28282571664]],
#  [['02060100100050', 1, 2721.74, -77.64953618962, -9.28140666084]],
#  [['02060100100052', 0, 1480.49, -77.6500373972, -9.28067208974]]]




#mzs=[['02060100100002A', 1, 6974.02, -77.64796604746, -9.27717130724], ['02060100100003', 11, 25882.38, -77.64831341561, -9.2779636248],['02060100100007A', 6, 976.08, -77.64681330164, -9.27749053408], ['02060100100002B', 9, 3732.87, -77.64856364605, -9.27582546135]]
#print Componentes_conexas(mzs)





#[[['02060100100002A', 1, 6974.02, -77.64796604746, -9.27717130724], ['02060100100003', 11, 25882.38, -77.64831341561, -9.2779636248], ['02060100100007A', 6, 976.08, -77.64681330164, -9.27749053408]],
# [['02060100100002B', 9, 3732.87, -77.64856364605, -9.27582546135]]]



#manzanass=[
#['02060100100043', 8, 3387.64, -77.64832646898, -9.28133579638],
##['02060100100034', 1, 3557.15, -77.64800975671, -9.28103021418],
#['02060100100028', 0, 436.36, -77.64820643693, -9.28037709219],
#['02060100100027', 0, 2504.99, -77.64833792274, -9.28006821005],
#['02060100100026', 10, 3503.08, -77.64801436769, -9.27984577051]
#]
#
#print Componentes_conexas(manzanass)




#[[['02060100100043', 8, 3387.64, -77.64832646898, -9.28133579638], ['02060100100034', 1, 3557.15, -77.64800975671, -9.28103021418], ['02060100100028', 0, 436.36, -77.64820643693, -9.28037709219], ['02060100100027', 0, 2504.99, -77.64833792274, -9.28006821005], ['02060100100026', 10, 3503.08, -77.64801436769, -9.27984577051]]]



#[[['02060100100043', 8, 3387.64, -77.64832646898, -9.28133579638]], [['02060100100028', 0, 436.36, -77.64820643693, -9.28037709219], ['02060100100027', 0, 2504.99, -77.64833792274, -9.28006821005], ['02060100100026', 10, 3503.08, -77.64801436769, -9.27984577051]]]

#mzs=[['02060100100007A', 6, 976.08, -77.64681330164, -9.27749053408], ['02060100100002B', 9, 3732.87, -77.64856364605, -9.27582546135], ['02060100100002C', 3, 8991.75, -77.64774810321, -9.27671177438]]
#print Componentes_conexas(mzs)

#print OrdenarComponentesViviendas2(mzs)

#mzs=[['02060100100002A', 1, 6974.02, -77.64796604746, -9.27717130724], ['02060100100002C', 3, 8991.75, -77.64774810321, -9.27671177438], ['02060100100003', 11, 25882.38, -77.64831341561, -9.2779636248], ['02060100100006A', 14, 2426.82, -77.64713267431, -9.27796053189], ['02060100100007A', 6, 976.08, -77.64681330164, -9.27749053408], ['02060100100002B', 9, 3732.87, -77.64856364605, -9.27582546135], ['02060100100017', 15, 3106.22, -77.64831734371, -9.27892918472], ['02060100100018', 13, 3267.25, -77.6489079174, -9.27837475553], ['02060100100007', 11, 2774.05, -77.6467956581, -9.27792742648], ['02060100100004', 13, 4036.89, -77.64738349487, -9.27922782288], ['02060100100016', 10, 3382.55, -77.64768866138, -9.27952701083], ['02060100100025B', 13, 2903.56, -77.64891830393, -9.27956969879], ['02060100100026', 10, 3503.08, -77.64801436769, -9.27984577051], ['02060100100019', 6, 2078.01, -77.64939758749, -9.2779057933], ['02060100100024', 14, 3298.55, -77.64922314319, -9.27871534673], ['02060100100015', 14, 2992.93, -77.64706447125, -9.28012537091], ['02060100100027', 0, 2504.99, -77.64833792274, -9.28006821005], ['02060100100030', 10, 3666.43, -77.64738311753, -9.28043809628], ['02060100100022E', 10, 2148.09, -77.65047996988, -9.27853124908], ['02060100100037', 14, 4260.82, -77.64976991749, -9.2793382606], ['02060100100014', 6, 2816.89, -77.64647552001, -9.28067727897], ['02060100100028', 0, 436.36, -77.64820643693, -9.28037709219], ['02060100100029', 11, 3403.85, -77.64769097785, -9.28072768707], ['02060100100022C', 8, 1749.96, -77.65109749309, -9.27894285044], ['02060100100040', 0, 568.1, -77.64960752861, -9.28006925456], ['02060100100034', 1, 3557.15, -77.64800975671, -9.28103021418], ['02060100100022G', 0, 7779.74, -77.65167327703, -9.27832473719], ['02060100100033', 11, 3506.38, -77.64739944982, -9.28158617318], ['02060100100043', 8, 3387.64, -77.64832646898, -9.28133579638], ['02060100100022F', 1, 32570.4, -77.65254879353, -9.27850255719], ['02060100100032', 12, 3639.07, -77.64674376106, -9.28221453229], ['02060100100042', 14, 2927.82, -77.64896666492, -9.28075063113]]
#print OrdenarComponentesViviendas(mzs)
#print Componentes_conexas_cantidad_viv(mzs,16)






def Agrupacion2(lista_adyacencia,manzanas,cant_max_viviendas=16):
    if len(manzanas)>1:
        manzanas_temporal = OrdenarManzanas_XY(manzanas)[:]
    else:
        manzanas_temporal =manzanas

    componentes_conexas = []
    componente_conexa = []
    manzana_temporal = []
    cant_max_viviendas=16

    V = []

    cant_viv=0
    while (len(manzanas_temporal) > 0):
        componente_conexa = []
        manzana_temporal = manzanas_temporal[0]
        where_expression = ' "IDMANZANA"=\'' + str(manzana_temporal[0]) + '\'  AND "TOT_VIV_AD"<=16 '
        V = []
        manzanas_temporal.remove(manzana_temporal)
        componente_conexa.append(manzana_temporal)

        cant_viv=0
        cant_viv=manzana_temporal[1]+cant_viv

        for row4 in arcpy.da.SearchCursor(
                lista_adyacencia,
                ["IDMANZ_ADY", "TOT_VIV_AD", "AREA_ADY", "X_ADY", "Y_ADY"], where_expression):
            fila = []
            fila = [str(row4[0]), int(row4[1]), float(row4[2]), float(row4[3]), float(row4[4])]

            if (fila in manzanas_temporal) and ((cant_viv+fila[1])<=cant_max_viviendas):
                V.append(fila)
                manzanas_temporal.remove(fila)
                componente_conexa.append(fila)
                cant_viv=cant_viv+fila[1]

        while (len(V) > 0):
            if(len(V)>1):
                V=OrdenarManzanas_XY(V)[:]
            manzana_temporal2 = V[0]
            where_expression2 = ' "IDMANZANA"=\'' + str(manzana_temporal2[0]) + '\'  AND "TOT_VIV_AD"<=16 '
            for row5 in arcpy.da.SearchCursor(
                    lista_adyacencia,
                    ["IDMANZ_ADY", "TOT_VIV_AD", "AREA_ADY", "X_ADY", "Y_ADY"], where_expression2):
                fila2 = []
                fila2 = [str(row5[0]), int(row5[1]), float(row5[2]), float(row5[3]), float(row5[4])]
                if (fila2 in manzanas_temporal) and ((cant_viv+fila2[1])<=cant_max_viviendas):
                    if fila2 not in componente_conexa:
                        V.append(fila2)
                        manzanas_temporal.remove(fila2)
                        componente_conexa.append(fila2)
                        cant_viv=cant_viv+fila2[1]
            V.remove(manzana_temporal2)


        if len(manzanas_temporal) > 1:
            manzanas_temporal=OrdenarManzanas_XY(manzanas_temporal)[:]

        componentes_conexas.append(componente_conexa)

    #print np.array(componentes_conexas)
    return componentes_conexas