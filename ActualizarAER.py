import arcpy
#import  CalculateCircle as c
import math
import CalculoFuncionObjetivo as funcionObjetivo


arcpy.env.workspace = r"D:/ArcGisShapesPruebas"


def ActualizarAER(zona,solucion,manzanas):
    fieldName1 = "AER"
    fc=zona
# fc="D:/ArcGisShapesPruebas/Zones/Shape15013300200.shp"

# fc_circles="D:/ArcGisShapesPruebas/EnvolvesCircles/"+zona
# fc_circles2="D:/ArcGisShapesPruebas/EnvolvesCirclesBuffers/"+zona

    arcpy.AddField_management(fc, fieldName1, "SHORT")


# ordenar manzanas por id
    # obtengo las manzanas
    manzanas_id=[]
    for el in manzanas:
        manzanas_id.append(el[0])

    manzanas_id.sort()


    numero_grupo=1


    solucion_ordenada=[]


    while len(manzanas_id)>0:
        manzana_id=manzanas_id[0]


        for grupo in solucion:
            for mzn in grupo:
                if (mzn[0]==manzana_id):
                    grupo2=grupo[:]
                    solucion_ordenada.append(grupo)

                    for mzn2 in grupo2:
                        manzanas_id.remove(mzn2[0])

                    break
















    #for el2 in manzanas:
    #    el2.append()


# ASIGNAR LOS GRUPOS AL SHAPE



    numero_grupo = 0

    for grupo in solucion_ordenada:
        numero_grupo = numero_grupo + 1
        for manzana in grupo:
            fields = ["AER"]
            where_expression = ' "IDMANZANA"=\'' + str(manzana[0]) + '\'  '
            # print numero_grupo
            # print where_expression
            with arcpy.da.UpdateCursor(fc, fields, where_expression) as cursor:

                for row in cursor:
                    row[0] = numero_grupo
                    cursor.updateRow(row)

