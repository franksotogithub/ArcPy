import random
import ComparacionParticiones as a
import arcpy
#import  CalculateCircle as c
import math
import CalculoFuncionObjetivo as funcionObjetivo


arcpy.env.workspace = r"D:/ArcGisShapesPruebas"


def SolucionInicial(zona):

    fc = zona

    solucion_inicial = []
    manzanas_temporal=[]
    manzanas = []

    cant_viv_estandar=16
    grupos=[]

    cant_aeus_no_asignados=0

    #manzanas_adyacentes = [["a", 20], ["b", 19], ["c", 15], ["d", 20], ["e", 15], ["f", 16]]
    #manzanas_temporal_2 = [["a", 20], ["b", 19], ["c"-, 15], ["d", 20], ["e", 15], ["f", 16]]

    #manzana_temporal = []
    total_viv=0
    cant_manzanas_sin_asignar=0
    manzanas_asignadas=[]


    manzanas = []

    manzanas_adyacentes = []

    for row1 in arcpy.da.SearchCursor(fc, ["IDMANZANA", "TOT_VIV","Shape_area","xCentroid","yCentroid"]):
        total_viv = row1[1] + total_viv

        manzanas.append(str(row1[0]))

        cant_manzanas_sin_asignar = 1 + cant_manzanas_sin_asignar

        # manzana.append(row1[1])
        # manzanas.append(manzana)
        # where_expression = ' "IDMANZANA"=%s' % (str(row1[0]))
    # print manzanas
    del row1


    # aca se copian los elementos de manzanas a manzanas_temporal
    for l in manzanas:
        manzanas_temporal.append(l)





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






        where_expression = ' "IDMANZANA"=\'' + str(manzana_temporal) + '\'  '


        for row3 in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
                                          ["IDMANZ_ADY"], where_expression):
            #manzanas_adyacentes.append(str(row3[0]))

            if cant_manzanas_sin_asignar > cant_aeus_no_asignados:
                if  row3[0] not in manzanas_asignadas:
                    grupo.append(str(row3[0])) # se agerega al grupo
                    manzanas_asignadas.append(row3[0]) # se aumente la cantidad de manzanas asiganndasd
                    cant_manzanas_sin_asignar=cant_manzanas_sin_asignar-1# se disminuye la cantidad de manzanas sin asignar
                    manzanas_temporal.remove(row3[0]) # se remueve del temporal la manzana ya asiganda




        cant_aeus_no_asignados=cant_aeus_no_asignados-1

        solucion_inicial.append(grupo)

        #cant_grupos=1+cant_grupos



    #print "Solucion inicial:"+str(solucion_inicial)
    #print "Tamanio de la solucion inicial:"+str(len(solucion_inicial))

    #print "Cantidad manzanas asignadas:"+str(len(manzanas_asignadas))

    #print "Manzanas temporal:"+str(manzanas_temporal)

    tamanio_temp=len(manzanas_temporal)

    find=False

    while tamanio_temp>0:
        find = False
        k = random.randint(0, tamanio_temp - 1)


        manzana_temporal=manzanas_temporal[k]

        where_expression = ' "IDMANZANA"=\'' + str(manzana_temporal) + '\'  '

        for row4 in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
                                          ["IDMANZ_ADY"], where_expression):
    # manzanas_adyacentes.append(str(row3[0]))

            grupo_temporal=[]
            for grupo_temporal in solucion_inicial:
                #print grupo_temporal
                if row4[0] in grupo_temporal:
                    grupo_temporal2=[]

                    for el in grupo_temporal:
                        grupo_temporal2.append(el)

                    grupo_temporal2.append(manzana_temporal)

                    solucion_inicial.remove(grupo_temporal)
                    solucion_inicial.append(grupo_temporal2)
                    find=True
                    break

            if find==True:
                break
        #del row4

        manzanas_temporal.remove(manzana_temporal)
        tamanio_temp = len(manzanas_temporal)


    fieldName1 = "GRUPO"

    #fc="D:/ArcGisShapesPruebas/Zones/Shape15013300200.shp"
    
    #fc_circles="D:/ArcGisShapesPruebas/EnvolvesCircles/"+zona
    #fc_circles2="D:/ArcGisShapesPruebas/EnvolvesCirclesBuffers/"+zona

    arcpy.AddField_management(fc, fieldName1, "SHORT")



    arcpy.AddField_management(fc, "Shape_area", "DOUBLE")
    exp = "!SHAPE.AREA@METERS!"
    arcpy.CalculateField_management(fc, "Shape_area", exp, "PYTHON_9.3")




    # ASIGNAR LOS GRUPOS AL SHAPE



    numero_grupo = 0


    for grupo in solucion_inicial:
        numero_grupo = numero_grupo + 1
        for manzana in grupo:
            fields = ["GRUPO"]
            where_expression = ' "IDMANZANA"=\'' + str(manzana) + '\'  '
            #print numero_grupo
            #print where_expression
            with arcpy.da.UpdateCursor(fc, fields, where_expression) as cursor:

                for row in cursor:
                    row[0] = numero_grupo
                    cursor.updateRow(row)

    resultado=[]
    resultado.append(solucion_inicial)
    resultado.append(manzanas)

    return resultado
    #return resultado

#
#
#
#def ListarManzanas(zona):
#    fc = zona
#    manzanas = []
#
#    manzanas_adyacentes = []
#
#    for row1 in arcpy.da.SearchCursor(fc, ["IDMANZANA", "TOT_VIV"]):
#        total_viv = row1[1] + total_viv
#
#        manzanas.append(str(row1[0]))
#
#        cant_manzanas_sin_asignar = 1 + cant_manzanas_sin_asignar
#
#        # manzana.append(row1[1])
#        # manzanas.append(manzana)
#        # where_expression = ' "IDMANZANA"=%s' % (str(row1[0]))
#    # print manzanas
#    del row1
#    return manzanas
#

#print SolucionInicial("Shape15013300200.shp")