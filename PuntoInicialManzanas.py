import arcpy
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

#def CrearVertices():
