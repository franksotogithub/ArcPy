
import random
import arcpy
import SolucionInicialUrbano  as si

arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"
def SolucionVecina(manzanas_temporal,solucion_anterior):

    manzanas_adyacentes=[]
    solucion_vecina=[]

    tamanio_temp = len(manzanas_temporal)


    solucion_vecina=solucion_anterior[:]
    tamanio_solucion=len(solucion_anterior)


    solucion_anterior_escoger=[]

    # escogiendo solo los grupos que tengan mas de un elemento

    for el in solucion_anterior:
        if len(el)>1:
            solucion_anterior_escoger.append(el)

    # escogiendo alguno de estos grupos random que tienen mas de un elemento

    # escogiendo el grupo
    k=random.randint(0, len(solucion_anterior_escoger) - 1)

    grupo_escogido=solucion_anterior_escoger[k]
    tamanio_grupo_escogido = len(grupo_escogido)



    cant_manzanas_adyacentes_no_grupo=0
    cant_manzanas_adyacentes_grupo = 0
    manzanas_adyacentes_grupo=[]
    grupo_temp_escogido=grupo_escogido[:]

    cant_manzanas_grupo=len(grupo_escogido)

    manzana_encontrada=False

    while (len(grupo_temp_escogido)>0):
        cant_manzanas_adyacentes_grupo = 0
        manzanas_adyacentes=[]
        manzanas_adyacentes_grupo = []

        tamanio_grupo_escogido_temp=len(grupo_temp_escogido)
        k = random.randint(0, tamanio_grupo_escogido_temp - 1)

        manzana_escogida = grupo_temp_escogido[k]

        grupo_escogido_temp_1=grupo_temp_escogido[:]

        grupo_escogido_temp_1.remove(manzana_escogida)

        where_expression = ' "IDMANZANA"=\'' + str(manzana_escogida[0]) + '\' AND "TOT_VIV_AD"<16 '

        #while  len(manzanas_adyacentes)==0:
        for row4 in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
                                          ["IDMANZ_ADY", "TOT_VIV_AD", "AREA_ADY", "X_ADY", "Y_ADY"], where_expression):
            fila=[str(row4[0]), int(row4[1]), float(row4[2]), float(row4[3]),float(row4[4])]

            if fila not in grupo_temp_escogido:
                manzanas_adyacentes.append(fila)  # ingresar las manzanas adyacentes a la manzana escogida que no forman parte del grupo escogido

            else:
                manzanas_adyacentes_grupo.append(fila) # inserta las manzanas adyacentes a la manzana que forman parte del grupo
        #        cant_manzanas_adyacentes_grupo = 1+cant_manzanas_adyacentes_grupo


        cant_manzanas_adyacentes_grupo=len(manzanas_adyacentes_grupo)

        contador=0



        # evalua si las manznas adyacentes a la manzana escogida dentro del grupo siguen siendo adyacentes entre si cuando se elimina la manzana escogida del grupo.
        if(len(grupo_escogido_temp_1)>1):

            for manzana_adyacente_grupo in manzanas_adyacentes_grupo:

                where_expression = ' "IDMANZANA"=\'' + str(manzana_adyacente_grupo[0]) + '\' AND "TOT_VIV_AD"<16 '

                # while  len(manzanas_adyacentes)==0:
                for row5 in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
                                                  ["IDMANZ_ADY", "TOT_VIV_AD", "AREA_ADY", "X_ADY", "Y_ADY"],
                                                  where_expression):
                    fila2 = [str(row5[0]), int(row5[1]), float(row5[2]), float(row5[3]), float(row5[4])]
                    if fila2 in grupo_escogido_temp_1:  # existe aunque sea una manzana dentro del grupo que es adyacente a la manzana adyacente a la manzana escogida
                       contador=contador+1
                       break



        #manzanas_adyacentes_grupo
        #cantidad de manzanas adyacentes a la manzana escogida dentro del

        if (len(manzanas_adyacentes)>0) and ((cant_manzanas_adyacentes_grupo==contador) or (len(grupo_escogido_temp_1)==1) ) :   # si existen manzanas adyacentes fuera del grupo y que la cantidad de manzanas adyacentes dentro del grupo es menor que 1
            manzana_encontrada=True
            #print str(manzana_encontrada)
            break
        else:
            grupo_temp_escogido.remove(manzana_escogida)


    #print "grupo escogido: "+str(grupo_escogido)
    #print "manzana escogida:" + str(manzana_escogida)



#   for grupo_temporal in solucion_anterior:

#       if manzana_escogida in grupo_temporal:
#           print "Grupo de la manzana escogida:" + str(grupo_temporal)


#           #solucion_vecina.remove(grupo_temporal)
#           grupo_temporal.remove(manzana_escogida)
#           solucion_vecina[indice] = grupo_temporal
#           #solucion_vecina.append(grupo_temporal)
#           break

#       indice=indice+1



    #print "manzanas adyacentes" + str(manzanas_adyacentes)





    #print "Manzana adyacente seleccionada: "+ str(manzana_adyacente)


    #el grupo donde se encontraba la manzana escogida es eliminada y se inserta otro grupo donde



    indice2 = 0

    #print "Manzana escogida: " + str(manzana_escogida)
    #print "Manzana adyacente escogida: " + str(manzana_adyacente)
    # se obtiene la manzanas adyacente y si su  grupo y



    if manzana_encontrada==True:
        find = False
        tamanio_adyacentes = len(manzanas_adyacentes)
        j = random.randint(0, tamanio_adyacentes - 1)
        manzana_adyacente = manzanas_adyacentes[j]

        for grupo_temporal in solucion_anterior:
            if (manzana_adyacente in grupo_temporal) and (manzana_adyacente not in grupo_escogido) :
                grupo_temporal2=[]
                index = solucion_anterior.index(grupo_temporal)
                indice2=solucion_anterior.index(grupo_temporal)
                grupo_temporal2=grupo_temporal[:]
                grupo_temporal2.append(manzana_escogida)
                solucion_vecina[indice2]=grupo_temporal2
                find=True
                break
         # se captura la manzana y se retira del grupo
        if find==True:
            indice = solucion_anterior.index(grupo_escogido)
            grupo_escogido_temp = grupo_escogido[:]
            grupo_escogido_temp.remove(manzana_escogida)
            solucion_vecina[indice] = grupo_escogido_temp[:]

    return solucion_vecina
    #return [solucion_vecina,indice,indice2]




#manzanas=[['02060100100002A', 1, 6974.02, -77.64796604746, -9.27717130724], ['02060100100002B', 9, 3732.87, -77.64856364605, -9.27582546135], ['02060100100002C', 3, 8991.75, -77.64774810321, -9.27671177438], ['02060100100003', 11, 25882.38, -77.64831341561, -9.2779636248], ['02060100100004', 13, 4036.89, -77.64738349487, -9.27922782288], ['02060100100006A', 14, 2426.82, -77.64713267431, -9.27796053189], ['02060100100007', 11, 2774.05, -77.6467956581, -9.27792742648], ['02060100100007A', 6, 976.08, -77.64681330164, -9.27749053408], ['02060100100009', 0, 2607.73, -77.6455099662, -9.27976542932], ['02060100100010A', 0, 999.64, -77.64563529772, -9.280090282], ['02060100100010B', 10, 2110.56, -77.6460875685, -9.27997993296], ['02060100100014', 6, 2816.89, -77.64647552001, -9.28067727897], ['02060100100015', 14, 2992.93, -77.64706447125, -9.28012537091], ['02060100100016', 10, 3382.55, -77.64768866138, -9.27952701083], ['02060100100017', 15, 3106.22, -77.64831734371, -9.27892918472], ['02060100100018', 13, 3267.25, -77.6489079174, -9.27837475553], ['02060100100019', 6, 2078.01, -77.64939758749, -9.2779057933], ['02060100100021', 5, 3780.24, -77.65084864166, -9.27615686214], ['02060100100022C', 8, 1749.96, -77.65109749309, -9.27894285044], ['02060100100022E', 10, 2148.09, -77.65047996988, -9.27853124908], ['02060100100022F', 1, 32570.4, -77.65254879353, -9.27850255719], ['02060100100022G', 0, 7779.74, -77.65167327703, -9.27832473719], ['02060100100024', 14, 3298.55, -77.64922314319, -9.27871534673], ['02060100100025B', 13, 2903.56, -77.64891830393, -9.27956969879], ['02060100100026', 10, 3503.08, -77.64801436769, -9.27984577051], ['02060100100027', 0, 2504.99, -77.64833792274, -9.28006821005], ['02060100100028', 0, 436.36, -77.64820643693, -9.28037709219], ['02060100100029', 11, 3403.85, -77.64769097785, -9.28072768707], ['02060100100030', 10, 3666.43, -77.64738311753, -9.28043809628], ['02060100100032', 12, 3639.07, -77.64674376106, -9.28221453229], ['02060100100033', 11, 3506.38, -77.64739944982, -9.28158617318], ['02060100100034', 1, 3557.15, -77.64800975671, -9.28103021418], ['02060100100037', 14, 4260.82, -77.64976991749, -9.2793382606], ['02060100100040', 0, 568.1, -77.64960752861, -9.28006925456], ['02060100100042', 14, 2927.82, -77.64896666492, -9.28075063113], ['02060100100043', 8, 3387.64, -77.64832646898, -9.28133579638], ['02060100100046', 11, 3560.43, -77.64735426863, -9.28282571664], ['02060100100050', 1, 2721.74, -77.64953618962, -9.28140666084], ['02060100100052', 0, 1480.49, -77.6500373972, -9.28067208974]]
#solucion_inicial=[[['02060100100027', 0, 2504.99, -77.64833792274, -9.28006821005], ['02060100100025B', 13, 2903.56, -77.64891830393, -9.27956969879], ['02060100100026', 10, 3503.08, -77.64801436769, -9.27984577051], ['02060100100028', 0, 436.36, -77.64820643693, -9.28037709219]], [['02060100100009', 0, 2607.73, -77.6455099662, -9.27976542932], ['02060100100010A', 0, 999.64, -77.64563529772, -9.280090282]], [['02060100100016', 10, 3382.55, -77.64768866138, -9.27952701083], ['02060100100004', 13, 4036.89, -77.64738349487, -9.27922782288], ['02060100100015', 14, 2992.93, -77.64706447125, -9.28012537091], ['02060100100017', 15, 3106.22, -77.64831734371, -9.27892918472]], [['02060100100034', 1, 3557.15, -77.64800975671, -9.28103021418], ['02060100100029', 11, 3403.85, -77.64769097785, -9.28072768707], ['02060100100033', 11, 3506.38, -77.64739944982, -9.28158617318], ['02060100100043', 8, 3387.64, -77.64832646898, -9.28133579638]], [['02060100100050', 1, 2721.74, -77.64953618962, -9.28140666084]], [['02060100100002C', 3, 8991.75, -77.64774810321, -9.27671177438], ['02060100100002A', 1, 6974.02, -77.64796604746, -9.27717130724], ['02060100100002B', 9, 3732.87, -77.64856364605, -9.27582546135], ['02060100100007A', 6, 976.08, -77.64681330164, -9.27749053408]], [['02060100100010B', 10, 2110.56, -77.6460875685, -9.27997993296]], [['02060100100052', 0, 1480.49, -77.6500373972, -9.28067208974]], [['02060100100022F', 1, 32570.4, -77.65254879353, -9.27850255719], ['02060100100022G', 0, 7779.74, -77.65167327703, -9.27832473719]], [['02060100100022C', 8, 1749.96, -77.65109749309, -9.27894285044], ['02060100100022E', 10, 2148.09, -77.65047996988, -9.27853124908]], [['02060100100030', 10, 3666.43, -77.64738311753, -9.28043809628]], [['02060100100040', 0, 568.1, -77.64960752861, -9.28006925456]], [['02060100100042', 14, 2927.82, -77.64896666492, -9.28075063113]], [['02060100100024', 14, 3298.55, -77.64922314319, -9.27871534673]], [['02060100100032', 12, 3639.07, -77.64674376106, -9.28221453229]], [['02060100100037', 14, 4260.82, -77.64976991749, -9.2793382606]], [['02060100100046', 11, 3560.43, -77.64735426863, -9.28282571664]], [['02060100100014', 6, 2816.89, -77.64647552001, -9.28067727897]], [['02060100100019', 6, 2078.01, -77.64939758749, -9.2779057933]], [['02060100100007', 11, 2774.05, -77.6467956581, -9.27792742648]], [['02060100100021', 5, 3780.24, -77.65084864166, -9.27615686214]], [['02060100100003', 11, 25882.38, -77.64831341561, -9.2779636248], ['02060100100006A', 14, 2426.82, -77.64713267431, -9.27796053189], ['02060100100018', 13, 3267.25, -77.6489079174, -9.27837475553]]]

#solucion_vecina=SolucionVecina(manzanas,solucion_inicial)[:]


#tamanio=len(solucion_inicial)

#for i in range(0, tamanio - 1):
#    if len(solucion_inicial[i]) <> len(solucion_vecina[i]):
#        print "Indice del Grupo de S0:" + str(i)
#        print "Tamanio Grupo de S0:" + str(len(solucion_inicial[i]))
#        print "Tamanio Grupo de S1:" + str(len(solucion_vecina[i]))




def SolucionVecina2(manzanas_temporal,solucion_anterior):

    cant_comp_conx=0
    grupo_escogido_sin_manzana=[]


    manzanas_adyacentes=[]
    solucion_vecina=[]

    tamanio_temp = len(manzanas_temporal)


    solucion_vecina=solucion_anterior[:]
    tamanio_solucion=len(solucion_anterior)


    solucion_anterior_escoger=[]

    # escogiendo solo los grupos que tengan mas de un elemento

    for el in solucion_anterior:
        if len(el)>1:
            solucion_anterior_escoger.append(el)

    # escogiendo alguno de estos grupos random que tienen mas de un elemento

    # escogiendo el grupo
    k=random.randint(0, len(solucion_anterior_escoger) - 1)

    grupo_escogido=solucion_anterior_escoger[k]
    tamanio_grupo_escogido = len(grupo_escogido)



    cant_manzanas_adyacentes_no_grupo=0
    cant_manzanas_adyacentes_grupo = 0
    manzanas_adyacentes_grupo=[]
    grupo_temp_escogido=grupo_escogido[:]

    cant_manzanas_grupo=len(grupo_escogido)

    manzana_encontrada=False

    while (len(grupo_temp_escogido)>0):
        cant_manzanas_adyacentes_grupo = 0
        manzanas_adyacentes=[]
        manzanas_adyacentes_grupo = []

        tamanio_grupo_escogido_temp=len(grupo_temp_escogido)

        k = random.randint(0, tamanio_grupo_escogido_temp - 1)

        manzana_escogida = grupo_temp_escogido[k]
        grupo_escogido_temp_1=[]
        grupo_escogido_temp_1=grupo_temp_escogido[:]

        grupo_escogido_temp_1.remove(manzana_escogida)



        if len(si.Componentes_conexas(grupo_escogido_temp_1))==1:
            grupo_escogido_sin_manzana = grupo_escogido_temp_1[:]
            cant_comp_conx=len(si.Componentes_conexas(grupo_escogido_temp_1))






            where_expression = ' "IDMANZANA"=\'' + str(manzana_escogida[0]) + '\' AND "TOT_VIV_AD"<16 '

            for row4 in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",["IDMANZ_ADY", "TOT_VIV_AD", "AREA_ADY", "X_ADY", "Y_ADY"], where_expression):
                filax=[str(row4[0]), int(row4[1]), float(row4[2]), float(row4[3]),float(row4[4])]

                if (filax not in grupo_escogido) and (filax in manzanas_temporal):
                    manzanas_adyacentes.append(filax)  # ingresar las manzanas adyacentes a la manzana escogida que no forman parte del grupo escogido

            if len(manzanas_adyacentes)>0:
                manzana_encontrada = True
                break
            else:
                manzana_encontrada = False
                grupo_temp_escogido.remove(manzana_escogida)
        else:
            manzana_encontrada = False
            grupo_temp_escogido.remove(manzana_escogida)




#        where_expression = ' "IDMANZANA"=\'' + str(manzana_escogida[0]) + '\' AND "TOT_VIV_AD"<16 '
#
#        #while  len(manzanas_adyacentes)==0:
#        for row4 in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
#                                          ["IDMANZ_ADY", "TOT_VIV_AD", "AREA_ADY", "X_ADY", "Y_ADY"], where_expression):
#            fila=[str(row4[0]), int(row4[1]), float(row4[2]), float(row4[3]),float(row4[4])]
#
#            if fila not in grupo_temp_escogido:
#                manzanas_adyacentes.append(fila)  # ingresar las manzanas adyacentes a la manzana escogida que no forman parte del grupo escogido
#
#            else:
#                manzanas_adyacentes_grupo.append(fila) # inserta las manzanas adyacentes a la manzana que forman parte del grupo
#        #        cant_manzanas_adyacentes_grupo = 1+cant_manzanas_adyacentes_grupo
#
#
#        cant_manzanas_adyacentes_grupo=len(manzanas_adyacentes_grupo)
#
#        contador=0
#
#
#
#        # evalua si las manznas adyacentes a la manzana escogida dentro del grupo siguen siendo adyacentes entre si cuando se elimina la manzana escogida del grupo.
#        if(len(grupo_escogido_temp_1)>1):
#
#            for manzana_adyacente_grupo in manzanas_adyacentes_grupo:
#
#                where_expression = ' "IDMANZANA"=\'' + str(manzana_adyacente_grupo[0]) + '\' AND "TOT_VIV_AD"<16 '
#
#                # while  len(manzanas_adyacentes)==0:
#                for row5 in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
#                                                  ["IDMANZ_ADY", "TOT_VIV_AD", "AREA_ADY", "X_ADY", "Y_ADY"],
#                                                  where_expression):
#                    fila2 = [str(row5[0]), int(row5[1]), float(row5[2]), float(row5[3]), float(row5[4])]
#                    if fila2 in grupo_escogido_temp_1:  # existe aunque sea una manzana dentro del grupo que es adyacente a la manzana adyacente a la manzana escogida
#                       contador=contador+1
#                       break
#


        #manzanas_adyacentes_grupo
        #cantidad de manzanas adyacentes a la manzana escogida dentro del

#        if (len(manzanas_adyacentes)>0) and ((cant_manzanas_adyacentes_grupo==contador) or (len(grupo_escogido_temp_1)==1) ) :   # si existen manzanas adyacentes fuera del grupo y que la cantidad de manzanas adyacentes dentro del grupo es menor que 1
#            manzana_encontrada=True
#            #print str(manzana_encontrada)
#            break
#        else:
#            grupo_temp_escogido.remove(manzana_escogida)


    #print "grupo escogido: "+str(grupo_escogido)
    #print "manzana escogida:" + str(manzana_escogida)



#   for grupo_temporal in solucion_anterior:

#       if manzana_escogida in grupo_temporal:
#           print "Grupo de la manzana escogida:" + str(grupo_temporal)


#           #solucion_vecina.remove(grupo_temporal)
#           grupo_temporal.remove(manzana_escogida)
#           solucion_vecina[indice] = grupo_temporal
#           #solucion_vecina.append(grupo_temporal)
#           break

#       indice=indice+1



    #print "manzanas adyacentes" + str(manzanas_adyacentes)





    #print "Manzana adyacente seleccionada: "+ str(manzana_adyacente)


    #el grupo donde se encontraba la manzana escogida es eliminada y se inserta otro grupo donde



    indice2 = 0

    #print "Manzana escogida: " + str(manzana_escogida)
    #print "Manzana adyacente escogida: " + str(manzana_adyacente)
    # se obtiene la manzanas adyacente y si su  grupo y



    if manzana_encontrada==True:
        find = False
        tamanio_adyacentes = len(manzanas_adyacentes)
        j = random.randint(0, tamanio_adyacentes - 1)
        manzana_adyacente = manzanas_adyacentes[j]

        for grupo_temporal in solucion_anterior:
            if (manzana_adyacente in grupo_temporal) and (manzana_adyacente not in grupo_escogido) :
                grupo_temporal2=[]
                index = solucion_anterior.index(grupo_temporal)
                indice2=solucion_anterior.index(grupo_temporal)
                grupo_temporal2=grupo_temporal[:]
                grupo_temporal2.append(manzana_escogida)
                solucion_vecina[indice2]=grupo_temporal2
                find=True
                break
         # se captura la manzana y se retira del grupo
        if find==True:
            indice = solucion_anterior.index(grupo_escogido)
            grupo_escogido_temp = grupo_escogido[:]
            grupo_escogido_temp.remove(manzana_escogida)
            solucion_vecina[indice] = grupo_escogido_temp[:]

        manzana_ejemplo=['02060100100002B', 9, 3732.87, -77.64856364605, -9.27582546135]

        if manzana_ejemplo in grupo_escogido:
            print "manzana escogida:"+str(manzana_escogida)
            print "grupo solucion inicial: "+str(grupo_escogido)
            print "grupo solucion vecina: "+str(solucion_vecina[solucion_anterior.index(grupo_escogido)])
            print "grupo escogido sin manzana: "+str(grupo_escogido_sin_manzana)
            print "cantidad de componenetes conexas: "+str(cant_comp_conx)
    return solucion_vecina












