import random
import ComparacionParticiones as a
import arcpy
#import  CalculateCircle as c

import ActualizarAEU as b
import numpy as np


arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"


def AgrupacionPrueba(manzanasx):
    particiones = []

    manzanas = []
    manzanas=manzanasx[:]

    manzanas_adyacentes = [["a", 20], ["b", 19], ["c", 15], ["d", 20], ["e", 15], ["f", 16]]
    manzanas_temporal_2 = [["a", 20], ["b", 19], ["c", 15], ["d", 20], ["e", 15], ["f", 16]]
    manzana_temporal = []
    for t in range(1,2):

        manzanas_agrupadas=[]
        manzanas_temporal_2 = []  #primero se pone la mazanza en 0
        for manzana_temp in manzanas:
            manzanas_temporal_2.append(manzana_temp)  # se copia todos los elementos de las manazanas

        particion=[]
        manzanas_adyacentes = []
        tamanio_temporal_2 = len(manzanas_temporal_2)

        #if manzana in manzanas_temporal_2:
        #    manzanas_temporal_2.remove(manzana)
        #    manzanas_agrupadas.append(manzana)

           # if manzana in manzanas_temporal:
           #     manzanas_temporal.remove(manzana)

        m=0
        max_viviendas = 16

        while tamanio_temporal_2 > 0:
        #while m <10:
            manzanas_adyacentes = []
            j = random.randint(0, tamanio_temporal_2 - 1)
            manzana = manzanas_temporal_2[j]
            #for manzana_temp in manzanas_temporal_2:
                #   manzanas_temporal.append(manzana_temp)

            grupo = []

            grupo.append(manzana)
            cant_viviendas = manzana[1]
            manzana_temporal = []

            for row5 in manzana:
                manzana_temporal.append(row5)
            del row5

            manzanas_agrupadas.append(manzana) #se agrega a la lista de manzanas agrupadas
            manzanas_temporal_2.remove(manzana) #se elimina de la lista temporal de manzanas
            i=0
            #print i

            while (cant_viviendas <max_viviendas ): # while de grupos
            #while (i < 3):
                manzanas_adyacentes=[]
                tamanio_temporal=0

                where_expression = ' "IDMANZANA"=\'' + str(manzana_temporal[0]) + '\'  '
                for row3 in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
                                                 ["IDMANZ_ADY", "TOT_VIV_AD","AREA_ADY", "X_ADY", "Y_ADY"], where_expression):
                    manzana_temp = []
                    #manzana_temp.append(str(row3[0]))
                    #manzana_temp.append(int(row3[1]))
                    fila2 = [str(row3[0]), int(row3[1]), float(row3[2]), float(row3[3]), float(row3[4])]

                    if fila2 in manzanas:
                        manzanas_adyacentes.append(fila2)
                #del row3

                #print "Manzanas adyacentes:" +  str(manzanas_adyacentes)
                #print "Manzanas agrupadas:"+ str(manzanas_agrupadas)


                a.diferencia_listas(manzanas_adyacentes,manzanas_agrupadas)

                #print "Manzanas adyacentes diferencia:" + str(manzanas_adyacentes)

                tamanio_temporal=len(manzanas_adyacentes)


                if tamanio_temporal==0:   # si ya no hay ningun elelmento de la lista de adyacencia que pueda enlazarse entonces se termina el bucle
                    break

                #print "Tamanio: "+str(tamanio_temporal)

                while tamanio_temporal>0:
                    k = random.randint(0, tamanio_temporal - 1)

                    manzana2 = manzanas_adyacentes[k]


                    if (manzana2[1]+cant_viviendas)>max_viviendas: # while de posibles adyacencias
                        #print "Manzana:" + str(manzana2)
                        if tamanio_temporal==1 : #esto es si ya ha visto todas las posibles adyacencias y la suma sigue dando mayor entonces sumarlo para que sala del bucle while de grupos y pase a analizar otro grupo
                            cant_viviendas = cant_viviendas + manzana2[1]


                    else:
                        grupo.append(manzana2)
                        manzanas_agrupadas.append(manzana2)
                        manzana_temporal=[]

                        for row4 in manzana2:
                            manzana_temporal.append(row4)
                        del row4


                        cant_viviendas = cant_viviendas + manzana2[1]
                        manzanas_temporal_2.remove(manzana2)
                        break

                    manzanas_adyacentes.remove(manzana2)
                    tamanio_temporal = len(manzanas_adyacentes)

                i = i + 1



            tamanio_temporal_2=len(manzanas_temporal_2)
            #print "tamanio de la lista temporal:"+str(tamanio_temporal_2)
            m=m+1

            #print "grupo: "+str(grupo)

            particion.append(grupo)

        # Aqui discriminanmos los conjuntos repetidos

        res = 0
        if len(particiones) > 0:
            res = 0
            for particion_temporal in particiones:
                res = a.CompararConjuntos_nivel2(particion_temporal, particion)
                if res == 1:
                    break

        if res == 0:
            particiones.append(particion)


        #print particion

    return particiones[0]







#######################################prueba ejemplo
#
#
#
#
#fc="D:/ShapesPruebasSegmentacionUrbana/Zones/Shape020601001000001.shp"
#
#m=[['02060100100002A', 1, 6974.02, -77.64796604746, -9.27717130724], ['02060100100002C', 3, 8991.75, -77.64774810321, -9.27671177438], ['02060100100003', 11, 25882.38, -77.64831341561, -9.2779636248], ['02060100100006A', 14, 2426.82, -77.64713267431, -9.27796053189], ['02060100100007A', 6, 976.08, -77.64681330164, -9.27749053408], ['02060100100002B', 9, 3732.87, -77.64856364605, -9.27582546135], ['02060100100017', 15, 3106.22, -77.64831734371, -9.27892918472], ['02060100100018', 13, 3267.25, -77.6489079174, -9.27837475553], ['02060100100007', 11, 2774.05, -77.6467956581, -9.27792742648], ['02060100100004', 13, 4036.89, -77.64738349487, -9.27922782288], ['02060100100016', 10, 3382.55, -77.64768866138, -9.27952701083], ['02060100100025B', 13, 2903.56, -77.64891830393, -9.27956969879], ['02060100100026', 10, 3503.08, -77.64801436769, -9.27984577051], ['02060100100019', 6, 2078.01, -77.64939758749, -9.2779057933], ['02060100100024', 14, 3298.55, -77.64922314319, -9.27871534673], ['02060100100015', 14, 2992.93, -77.64706447125, -9.28012537091], ['02060100100027', 0, 2504.99, -77.64833792274, -9.28006821005], ['02060100100030', 10, 3666.43, -77.64738311753, -9.28043809628], ['02060100100022E', 10, 2148.09, -77.65047996988, -9.27853124908], ['02060100100037', 14, 4260.82, -77.64976991749, -9.2793382606], ['02060100100014', 6, 2816.89, -77.64647552001, -9.28067727897], ['02060100100028', 0, 436.36, -77.64820643693, -9.28037709219], ['02060100100029', 11, 3403.85, -77.64769097785, -9.28072768707], ['02060100100022C', 8, 1749.96, -77.65109749309, -9.27894285044], ['02060100100040', 0, 568.1, -77.64960752861, -9.28006925456], ['02060100100034', 1, 3557.15, -77.64800975671, -9.28103021418], ['02060100100022G', 0, 7779.74, -77.65167327703, -9.27832473719], ['02060100100033', 11, 3506.38, -77.64739944982, -9.28158617318], ['02060100100043', 8, 3387.64, -77.64832646898, -9.28133579638], ['02060100100022F', 1, 32570.4, -77.65254879353, -9.27850255719], ['02060100100032', 12, 3639.07, -77.64674376106, -9.28221453229], ['02060100100042', 14, 2927.82, -77.64896666492, -9.28075063113]]
#
#
#agrupacion=AgrupacionPrueba(m)[:]
#print agrupacion
#matriz = np.array(agrupacion)
#print matriz
#
#
#
#b.ActualizarAEU2(fc, agrupacion, m)

#############################################























#
#
#for row1 in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/Zones/Shape15013300200.dbf", ["IDMANZANA", "TOT_VIV"]):
#    manzana = []
#    manzana.append(str(row1[0]))
#    manzana.append(row1[1])
#    manzanas.append(manzana)
#    # where_expression = ' "IDMANZANA"=%s' % (str(row1[0]))
##print manzanas
#del row1



#[[[['02060100100019', 6, 2078.01, -77.64939758749, -9.2779057933]], [['02060100100022E', 10, 2148.09, -77.65047996988, -9.27853124908]], [['02060100100032', 12, 3639.07, -77.64674376106, -9.28221453229]], [['02060100100007A', 6, 976.08, -77.64681330164, -9.27749053408], ['02060100100002A', 1, 6974.02, -77.64796604746, -9.27717130724], ['02060100100002C', 3, 8991.75, -77.64774810321, -9.27671177438]], [['02060100100006A', 14, 2426.82, -77.64713267431, -9.27796053189]], [['02060100100016', 10, 3382.55, -77.64768866138, -9.27952701083]], [['02060100100026', 10, 3503.08, -77.64801436769, -9.27984577051], ['02060100100027', 0, 2504.99, -77.64833792274, -9.28006821005], ['02060100100028', 0, 436.36, -77.64820643693, -9.28037709219], ['02060100100034', 1, 3557.15, -77.64800975671, -9.28103021418]], [['02060100100043', 8, 3387.64, -77.64832646898, -9.28133579638]], [['02060100100040', 0, 568.1, -77.64960752861, -9.28006925456], ['02060100100037', 14, 4260.82, -77.64976991749, -9.2793382606]], [['02060100100025B', 13, 2903.56, -77.64891830393, -9.27956969879]], [['02060100100017', 15, 3106.22, -77.64831734371, -9.27892918472]], [['02060100100003', 11, 25882.38, -77.64831341561, -9.2779636248]], [['02060100100022G', 0, 7779.74, -77.65167327703, -9.27832473719], ['02060100100022C', 8, 1749.96, -77.65109749309, -9.27894285044]], [['02060100100004', 13, 4036.89, -77.64738349487, -9.27922782288]], [['02060100100007', 11, 2774.05, -77.6467956581, -9.27792742648]], [['02060100100022F', 1, 32570.4, -77.65254879353, -9.27850255719]], [['02060100100029', 11, 3403.85, -77.64769097785, -9.28072768707]], [['02060100100030', 10, 3666.43, -77.64738311753, -9.28043809628]], [['02060100100024', 14, 3298.55, -77.64922314319, -9.27871534673]], [['02060100100014', 6, 2816.89, -77.64647552001, -9.28067727897]], [['02060100100033', 11, 3506.38, -77.64739944982, -9.28158617318]], [['02060100100018', 13, 3267.25, -77.6489079174, -9.27837475553]], [['02060100100042', 14, 2927.82, -77.64896666492, -9.28075063113]], [['02060100100015', 14, 2992.93, -77.64706447125, -9.28012537091]], [['02060100100002B', 9, 3732.87, -77.64856364605, -9.27582546135]]]]