import arcpy
import numpy as np

arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"

def MasNorOeste():
    fc1=r"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO_VERTICES_SORT.shp"
    fc2=r"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"

    with arcpy.arcpy.da.SearchCursor(fc2, ['IDMANZANA']) as cursor2:
        for row2 in cursor2:
            where_expression = " IDMANZANA=\'" + str(row2[0])+"\'"

            contador=0
            with arcpy.arcpy.da.UpdateCursor(fc1, ['FID'],where_expression) as cursor1:
                for row1 in cursor1:

                    if(contador>0):
                        #print row1[0]
                        cursor1.deleteRow()

                    #cursor1.deleteRow()
                    contador=contador+1

def MasNorOeste2():
    arcpy.env.overwriteOutput = True
    fc1 = r"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO_VERTICES_SORT.shp"
    fc2 = r"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"
    f3=r"D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_VERTICES.shp"
    f4 = r"D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/"
    arcpy.MakeFeatureLayer_management(fc1, "vertice_temporal")
    archivos=[]

    with arcpy.arcpy.da.SearchCursor(fc2, ['IDMANZANA']) as cursor2:
        for row2 in cursor2:
            where_expression = " IDMANZANA=\'" + str(row2[0]) + "\'"

            contador = 0
            with arcpy.arcpy.da.SearchCursor(fc1, ['FID'], where_expression) as cursor1:
                for row1 in cursor1:
                    if (contador == 0):
                        where_expression2 = " FID=" + str(row1[0])
                        arcpy.SelectLayerByAttribute_management("vertice_temporal", "", where_expression2)

                        f5=f4+"Vertice"+str(row2[0])+str(row1[0])+".shp"

                        arcpy.CopyFeatures_management("vertice_temporal",f5 )
                        archivos.append(f5)
                        break

                contador=contador+1
                    # cursor1.deleteRow()

    arcpy.Merge_management(archivos,f3)




MasNorOeste2()