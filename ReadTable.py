import arcpy
arcpy.env.workspace = r"D:/ArcGisShapesPruebas"



manzana_temporal=[]

for row1 in  arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/Zones/Shape15013300200.dbf", ["IDMANZANA"]):
    manzana_temporal = []
    print row1[0]
    #where_expression = ' "IDMANZANA"=%s' % (str(row1[0]))
    where_expression =' "IDMANZANA"=\'' + str(row1[0])+'\'  '
    print where_expression
    for row  in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/LISTA_ADYACENCIA_MANZANA.dbf", ["IDMANZ_ADY","TOT_VIV_AD"],where_expression):
        manzana_temporal.append(row)
        #print manzana_temporal=[]
    print manzana_temporal

