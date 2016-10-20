
import random
import arcpy

#def SolucionVecina(manzanas_temporal,solucion_anterior):
#
#    manzanas_adyacentes=[]
#    solucion_vecina=[]
#
#    tamanio_temp = len(manzanas_temporal)
#
#
#    solucion_vecina=solucion_anterior[:]
#
#
#    tamanio_solucion=len(solucion_anterior)
#
#
#    solucion_anterior_escoger=[]
#
#    # escogiendo solo los grupos que tengan mas de un elemento
#
#    for el in solucion_anterior:
#        if len(el)>1:
#            solucion_anterior_escoger.append(el)
#
#    # escogiendo un elemento de alguno de estos grupos random
#
#    # escogiendo el grupo
#    k=random.randint(0, len(solucion_anterior_escoger) - 1)
#    grupo_escogido=solucion_anterior[k]
#
#    tamanio_grupo_escogido=len(grupo_escogido)
#
#    k = random.randint(0, tamanio_grupo_escogido - 1)
#
#    manzana_escogida = grupo_escogido[k]
#
#    where_expression = ' "IDMANZANA"=\'' + str(manzana_escogida) + '\'  '
#
#
#
#    #while  len(manzanas_adyacentes)==0:
#    for row4 in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
#                                  ["IDMANZ_ADY"], where_expression):
#        manzanas_adyacentes.append(row4[0])
#
#
#
#
#
#    #print "manzana escogida:" + str(manzana_escogida)
#
#
#    for grupo_temporal in solucion_anterior:
#        if manzana_escogida in grupo_temporal:
#            #print "Grupo de la manzana escogida:" + str(grupo_temporal)
#            solucion_vecina.remove(grupo_temporal)
#            grupo_temporal.remove(manzana_escogida)
#            solucion_vecina.append(grupo_temporal)
#            break
#
#
#
#
#    #print "manzanas adyacentes" + str(manzanas_adyacentes)
#
#
#
#    tamanio_adyacentes=len(manzanas_adyacentes)
#    j= random.randint(0,tamanio_adyacentes-1)
#
#    manzana_adyacente=manzanas_adyacentes[j]
#
#    #print "Manzana adyacente seleccionada: "+ str(manzana_adyacente)
#
#
#    #el grupo donde se encontraba la manzana escogida es eliminada y se inserta otro grupo donde
#
#
#
#
#    for grupo_temporal in solucion_anterior:
#        if (manzana_adyacente in grupo_temporal) and (manzana_escogida not in grupo_temporal) :
#            #print "Grupo Adyacente Seleccionado: " + str(grupo_temporal)
#             #solucion_vecina
#            solucion_vecina.remove(grupo_temporal)
#            grupo_temporal.append(manzana_escogida)
#            solucion_vecina.append(grupo_temporal)
#
#
#            break
#
#
#
#    return solucion_vecina








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

    while True:
        cant_manzanas_adyacentes_grupo = 0
        manzanas_adyacentes=[]
        manzanas_adyacentes_grupo = []

        tamanio_grupo_escogido_temp=len(grupo_temp_escogido)
        k = random.randint(0, tamanio_grupo_escogido_temp - 1)

        manzana_escogida = grupo_temp_escogido[k]

        grupo_escogido_temp_1=grupo_temp_escogido[:]

        grupo_escogido_temp_1.remove(manzana_escogida)

        where_expression = ' "IDMANZANA"=\'' + str(manzana_escogida[0]) + '\'  '

        #while  len(manzanas_adyacentes)==0:
        for row4 in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
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

                where_expression = ' "IDMANZANA"=\'' + str(manzana_adyacente_grupo[0]) + '\'  '

                # while  len(manzanas_adyacentes)==0:
                for row5 in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
                                                  ["IDMANZ_ADY", "TOT_VIV_AD", "AREA_ADY", "X_ADY", "Y_ADY"],
                                                  where_expression):
                    fila2 = [str(row5[0]), int(row5[1]), float(row5[2]), float(row5[3]), float(row5[4])]
                    if fila2 in grupo_escogido_temp_1:  # existe aunque sea una manzana dentro del grupo que es adyacente a la manzana adyacente a la manzana escogida
                       contador=contador+1
                       break



        #manzanas_adyacentes_grupo
        #cantidad de manzanas adyacentes a la manzana escogida dentro del

        if (len(manzanas_adyacentes)>0) and ((cant_manzanas_adyacentes_grupo==contador) or (len(grupo_escogido_temp_1)==1)) :   # si existen manzanas adyacentes fuera del grupo y que la cantidad de manzanas adyacentes dentro del grupo es menor que 1
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



    tamanio_adyacentes=len(manzanas_adyacentes)
    j= random.randint(0,tamanio_adyacentes-1)

    manzana_adyacente=manzanas_adyacentes[j]

    #print "Manzana adyacente seleccionada: "+ str(manzana_adyacente)


    #el grupo donde se encontraba la manzana escogida es eliminada y se inserta otro grupo donde



    indice2 = 0

    #print "Manzana escogida: " + str(manzana_escogida)
    #print "Manzana adyacente escogida: " + str(manzana_adyacente)
    # se obtiene la manzanas adyacente y si su  grupo y

    find=False
    for grupo_temporal in solucion_anterior:

        if (manzana_adyacente in grupo_temporal) and (manzana_adyacente not in grupo_escogido) :
            grupo_temporal2=[]
            index = solucion_anterior.index(grupo_temporal)
            #print "indice del grupo adyacente seleccionado: " +str(index)
            #print "Grupo Adyacente Seleccionado: " + str(grupo_temporal)
            #print "Tamanio del grupo adyacente seleccionado: " + str(len(grupo_temporal))
             #solucion_vecina

            #solucion_vecina.remove(grupo_temporal)
            #grupo_temporal.append(manzana_escogida)
            #solucion_vecina.append(grupo_temporal)

            indice2=solucion_anterior.index(grupo_temporal)
            grupo_temporal2=grupo_temporal[:]

            grupo_temporal2.append(manzana_escogida)


            solucion_vecina[indice2]=grupo_temporal2
            #print "grupo final:" + str(solucion_vecina[indice2])
            find=True
            break


     # se captura la manzana y se retira del grupo
    if find==True:
        indice = solucion_anterior.index(grupo_escogido)
        #print "Indice el grupo escogido: " + str(indice)
        #print "Grupo escodigo: " + str(grupo_escogido)
        #print "Tamanio del Grupo escodigo: " + str(len(grupo_escogido))
        grupo_escogido_temp = grupo_escogido[:]

        grupo_escogido_temp.remove(manzana_escogida)

        solucion_vecina[indice] = grupo_escogido_temp[:]

    return solucion_vecina
    #return [solucion_vecina,indice,indice2]