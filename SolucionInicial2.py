import random
import ComparacionParticiones as a
import arcpy
#import  CalculateCircle as c
import math
import CalculoFuncionObjetivo as funcionObjetivo


arcpy.env.workspace = r"D:/ArcGisShapesPruebas"


def SolucionInicial2(zona):
    fc = zona

    solucion_inicial = []
    manzanas_temporal=[]
    manzanas = []

    cant_viv_estandar=14
    grupos=[]

    cant_aeus_no_asignados=0

    #manzanas_adyacentes = [["a", 20], ["b", 19], ["c", 15], ["d", 20], ["e", 15], ["f", 16]]
    #manzanas_temporal_2 = [["a", 20], ["b", 19], ["c", 15], ["d", 20], ["e", 15], ["f", 16]]

    #manzana_temporal = []
    total_viv=0
    cant_manzanas_sin_asignar=0
    manzanas_asignadas=[]


    manzanas = []

    manzanas_adyacentes = []

    fieldName1 = "GRUPO"

    # fc="D:/ArcGisShapesPruebas/Zones/Shape15013300200.shp"

    # fc_circles="D:/ArcGisShapesPruebas/EnvolvesCircles/"+zona
    # fc_circles2="D:/ArcGisShapesPruebas/EnvolvesCirclesBuffers/"+zona

    arcpy.AddField_management(fc, fieldName1, "SHORT")
    #arcpy.AddField_management(fc, "Shape_area", "DOUBLE")
    #exp = "!SHAPE.AREA@METERS!"
    #arcpy.CalculateField_management(fc, "Shape_area", exp, "PYTHON_9.3")


    for row1 in arcpy.da.SearchCursor(fc, ["IDMANZANA", "TOT_VIV", "Shape_area", "xCentroid", "yCentroid"]):
        manzana = []
        total_viv = row1[1] + total_viv
        cant_manzanas_sin_asignar = 1 + cant_manzanas_sin_asignar

        manzana = [str(row1[0]), int(row1[1]), float(row1[2]), float(row1[3]),float(row1[4])]
        manzanas.append(manzana)
    del row1

    manzanas_temporal=manzanas[:]





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






        where_expression = ' "IDMANZANA"=\'' + str(manzana_temporal[0]) + '\'  '


        for row3 in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
                                          ["IDMANZ_ADY","TOT_VIV_AD","AREA_ADY","X_ADY","Y_ADY"], where_expression):
            #manzanas_adyacentes.append(str(row3[0]))
            manzana_adyacente = [str(row3[0]), int(row3[1]), float(row3[2]), float(row3[3]), float(row3[4])]

            if cant_manzanas_sin_asignar > cant_aeus_no_asignados:
                if  manzana_adyacente not in manzanas_asignadas:
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

        where_expression = ' "IDMANZANA"=\'' + str(manzana_temporal[0]) + '\'  '

        for row4 in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf",
                                          ["IDMANZ_ADY","TOT_VIV_AD","AREA_ADY","X_ADY","Y_ADY"], where_expression):

            manzanax=[str(row4[0]), int(row4[1]), float(row4[2]), float(row4[3]), float(row4[4])]
            grupo_temporal=[]
            for grupo_temporal in solucion_inicial:

                if manzanax in grupo_temporal:
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

    resultado = []
    resultado.append(solucion_inicial)
    resultado.append(manzanas)

    return resultado
#resultado = []
#resultado.append(solucion_inicial)
#resultado.append(manzanas)

#return resultado
#print SolucionInicial2("D:/ArcGisShapesPruebas/Zones/Shape15013300200.shp")