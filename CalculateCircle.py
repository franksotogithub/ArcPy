import arcpy

#arcpy.env.workspace = r"D:/ArcGisShapesPruebas"
arcpy.env.workspace ="D:/ArcGisShapesPruebas/Zones"
#Shape15013300200.dbf

#particion=[[['15013300200066B', 7], ['15013300200020L', 14], ['150133002000220', 7], ['15013300200042A', 8]], [['150133002000290', 24], ['150133002000340', 14], ['150133002000300', 0]], [['150133002000130', 2], ['150133002000060', 15], ['150133002000090', 21]], [['15013300200006A', 4], ['150133002000070', 16], ['150133002000080', 5]], [['150133002000280', 19]], [['150133002000360', 23], ['150133002000380',17]], [['150133002000570', 16], ['150133002000450', 10], ['150133002000440', 10]], [['150133002000510', 1], ['150133002000500', 4], ['15013300200053A', 11], ['150133002000540', 9]], [['150133002000610', 13], ['150133002000620', 24]], [['150133002000170', 22], ['150133002000110', 5], ['150133002000260', 1], ['15013300200032A', 10], ['150133002000250', 0]], [['15013300200042B', 17], ['15013300200042C', 18]], [['150133002000490', 17]], [['150133002000240', 16], ['150133002000230', 21]], [['150133002000100', 18]], [['15013300200065A', 12], ['15013300200065B', 8], ['15013300200065C', 11], ['150133002000640', 3]], [['150133002000310', 3], ['150133002000320', 3], ['150133002000330', 11], ['150133002000350', 15]], [['15013300200020D', 14], ['15013300200020H', 14], ['15013300200067A', 5]], [['15013300200020E', 9], ['15013300200020F', 19]], [['15013300200020G', 24]], [['150133002000420', 15], ['150133002000410', 2], ['150133002000400', 3], ['150133002000390', 19]], [['150133002000600', 3], ['150133002000590', 21], ['150133002000580',4]], [['15013300200020J', 19], ['15013300200020I', 15]], [['15013300200064A', 22]], [['15013300200020K', 24]], [['150133002000180', 17], ['150133002000190', 14]], [['150133002000160', 10]], [['150133002000370', 16], ['150133002000430', 10]], [['150133002000120', 18]], [['150133002000630', 24]], [['15013300200066A', 22]], [['150133002000270', 0]]]
#promx=0
#promy=0
#n=0




def  Calcular_Circulo_Minimo(solucion):
    fc="D:/ArcGisShapesPruebas/Zones/Shape15013300200.shp"
    fc_out="D:/ArcGisShapesPruebas/EnvolvesCircles/Shape15013300200_circles.shp"

    numero_grupo = 0
    for grupo in solucion:
        numero_grupo = numero_grupo+1
        for manzana in grupo:
            #print str(manzana[0])
            fc="D:/ArcGisShapesPruebas/Zones/Shape15013300200.shp"
            fields=["GRUPO"]
            where_expression = ' "IDMANZANA"=\'' + str(manzana[0]) + '\'  '

            with arcpy.da.UpdateCursor(fc, fields,where_expression) as cursor:

                for row in cursor:
                    row[0] = numero_grupo
                    cursor.updateRow(row)


                #promy=promy+row3[1]

    arcpy.MinimumBoundingGeometry_management(fc,fc_out,"CIRCLE", "LIST",["GRUPO"])
    arcpy.Buffer_analysis(fc_out,"Shape15013300200_circles_buffer.shp",'0.5 METERS')