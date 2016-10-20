import arcpy
#import  CalculateCircle as c
import math
import CalculoFuncionObjetivo as funcionObjetivo


arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"


def ActualizarAEU(zona,solucion,manzanas):
   # fieldName1 = "AEU"
    fc=zona


# fc="D:/ArcGisShapesPruebas/Zones/Shape15013300200.shp"

# fc_circles="D:/ArcGisShapesPruebas/EnvolvesCircles/"+zona
# fc_circles2="D:/ArcGisShapesPruebas/EnvolvesCirclesBuffers/"+zona

    #arcpy.AddField_management(fc, fieldName1, "SHORT")


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
            fields = ["AEU"]
            where_expression = ' "IDMANZANA"=\'' + str(manzana[0]) + '\'  '
            # print numero_grupo
            # print where_expression
            with arcpy.da.UpdateCursor(fc, fields, where_expression) as cursor:

                for row in cursor:
                    row[0] = numero_grupo
                    cursor.updateRow(row)

            with arcpy.da.UpdateCursor("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp", fields, where_expression) as cursor:

                for row in cursor:
                    row[0] = numero_grupo
                    cursor.updateRow(row)

def ActualizarAEU3(MZS,solucion,manzanas):
    fc=MZS

    numero_grupo = 0

    for grupo in solucion:
        numero_grupo = numero_grupo + 1
        for manzana in grupo:
            fields = ["AEU"]
            where_expression = ' "IDMANZANA"=\'' + str(manzana[0]) + '\'  '
            # print numero_grupo
            # print where_expression
         #   with arcpy.da.UpdateCursor(fc, fields, where_expression) as cursor:
#
         #       for row in cursor:
         #           row[0] = numero_grupo
         #           cursor.updateRow(row)

            with arcpy.da.UpdateCursor(fc, fields, where_expression) as cursor:

                for row in cursor:
                    row[0] = numero_grupo
                    cursor.updateRow(row)



def ActualizarAEU2(zona,solucion,manzanas):
   # fieldName1 = "AEU"
    fc=zona



    numero_grupo = 0

    for grupo in solucion:
        numero_grupo = numero_grupo + 1
        for manzana in grupo:
            fields = ["AEU"]
            where_expression = ' "IDMANZANA"=\'' + str(manzana[0]) + '\'  '
            # print numero_grupo
            # print where_expression
            with arcpy.da.UpdateCursor(fc, fields, where_expression) as cursor:

                for row in cursor:
                    row[0] = numero_grupo
                    cursor.updateRow(row)

            with arcpy.da.UpdateCursor("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp", fields, where_expression) as cursor:

                for row in cursor:
                    row[0] = numero_grupo
                    cursor.updateRow(row)











#ExportarTabla_Agrupada()

                #or_viv_aeu=or_viv_aeu+1
                #print or_viv_aeu


#  fc= "D:/ShapesPruebasSegmentacionUrbana/Zones/" + desc


#  for row10 in arcpy.da.SearchCursor(fc, ["IDMANZANA", "AEU"], where_clause3):
#      where_clause4 = '  ("USOLOCAL"=1 OR "USOLOCAL"=3)   AND "IDMANZANA"=\'%s\' ' % ( row10[0])

#      #or_viv_aeu=1
#      with arcpy.da.UpdateCursor(fc2, ["AEU","OR_VIV_AEU"], where_clause4) as cursor11:
#          for row11 in cursor11:
#              row11[0] = row10[1] + AEU_MAX
#              #row11[1]=or_viv_aeu
#              cursor11.updateRow(row11)
#              #or_viv_aeu=or_viv_aeu+1
#              #print or_viv_aeu

#      #or_viv_aeu = 1
#      with arcpy.da.UpdateCursor(fc3, ["AEU","OR_VIV_AEU"], where_clause4) as cursor12:
#          for row12 in cursor12:
#              row12[0] = row10[1] + AEU_MAX
#              #row12[1] = or_viv_aeu
#              cursor12.updateRow(row12)
#              #or_viv_aeu = or_viv_aeu + 1





#
#
#def ActualizarOrdenAEUViviendas(desc):
#    fc3 = "D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO.shp"
#    fc2 = "D:/ShapesPruebasSegmentacionUrbana/Viviendas/" + desc
#
#    for row10 in arcpy.da.SearchCursor(fc, ["IDMANZANA", "AEU"], where_clause3):
#
#    with arcpy.da.UpdateCursor(fc2, ["IDMANZANA","AEU","OR_VIV_AEU"]) as cursor12:
#            for row12 in cursor12:
#
#

#def ActualizarAEUViviendas()
#ActualizarOrdenAEUViviendas("Shape020601001000001.shp")