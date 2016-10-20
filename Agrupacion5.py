import random
import ComparacionParticiones as a
import arcpy
#import  CalculateCircle as c

particiones = []

manzanas = []

manzanas_adyacentes = [["a", 20], ["b", 19], ["c", 15], ["d", 20], ["e", 15], ["f", 16]]
manzanas_temporal_2 = [["a", 20], ["b", 19], ["c", 15], ["d", 20], ["e", 15], ["f", 16]]
max_viviendas = 40

arcpy.env.workspace = r"D:/ArcGisShapesPruebas"

manzana_temporal = []

for row1 in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/Zones/Shape15013300200.dbf", ["IDMANZANA", "TOT_VIV"]):
    manzana = []
    manzana.append(str(row1[0]))
    manzana.append(row1[1])
    manzanas.append(manzana)
    # where_expression = ' "IDMANZANA"=%s' % (str(row1[0]))
#print manzanas
del row1


for t in range(1,2):

    manzanas_agrupadas=[]
    manzanas_temporal_2 = []  #primero se pone la mazanza en 0
    for manzana_temp in manzanas:
        manzanas_temporal_2.append(manzana_temp)  # se copia todos los elementos de las manazanas

    #cant_iteraciones = 0

    #particion = [] # se deja la particion en 0

    #tamanio = len(manzanas)
    #j = random.randint(0, tamanio - 1)

    #manzana = manzanas[j]
    particion=[]
    manzanas_adyacentes = []
    tamanio_temporal_2 = len(manzanas_temporal_2)

    #if manzana in manzanas_temporal_2:
    #    manzanas_temporal_2.remove(manzana)
    #    manzanas_agrupadas.append(manzana)

       # if manzana in manzanas_temporal:
       #     manzanas_temporal.remove(manzana)

    m=0


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
            for row3 in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/LISTA_ADYACENCIA_MANZANA.dbf",
                                             ["IDMANZ_ADY", "TOT_VIV_AD"], where_expression):
                manzana_temp = []
                manzana_temp.append(str(row3[0]))
                manzana_temp.append(row3[1])
                manzanas_adyacentes.append(manzana_temp)
            del row3

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
                    #print "Manzana:" + str(manzana2)
                    #print "Lista temporal mazanas:" + str(manzanas_temporal_2)
                    grupo.append(manzana2)
                    manzanas_agrupadas.append(manzana2)
                    manzana_temporal=[]

                    for row4 in manzana2:
                        manzana_temporal.append(row4)
                    del row4
                    #manzana_temporal=manzana2

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


    print particion



print len(particiones)


#for particion in particiones:
#    print particion




    #print "particion: "+str(particion)


        #cant_viviendas=manzana2+cant_viviendas

        #tamanio_temporal = len(manzanas_temporal)

            # print tamanio_temporal
            # print manzana2
            # print manzanas_temporal
            # print  manzanas_temporal_2



        # print "Grupo: "+str(grupo)

    #particion.append(grupo)
        # manzanas_temporal_2.remove(manzana)

    # Aqui discriminanmos los conjuntos repetidos



        # print particion

# particion1=[[["b","15"],["a","20"]],[["d","19"],["c","18"]]]
# particion2=[[["a","20"],["b","15"]],[["c","18"],["d","19"]]]

# a.CompararConjuntos_nivel2()

#for particion in particiones:
#    print "particion :" + str(particion)



# manzana temporal define las manzanas con las cuales puede relacionarse
# manzana_temporal_2 define las manzanas del listado original , esta lista temporal se va a modificar a lo largo del tiempo, a medida que los
# elementos de esta se eliminan de la lista

