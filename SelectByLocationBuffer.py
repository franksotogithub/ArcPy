import arcpy
arcpy.env.workspace ="D:/ArcGisShapesPruebas2/Zones"
# First, make a layer from the feature class

desc="Shape15013300200.shp"
arcpy.MakeFeatureLayer_management("D:/ArcGisShapesPruebas2/Zones/"+desc, "temporal_manzanas")
arcpy.MakeFeatureLayer_management("D:/ArcGisShapesPruebas2/Buffers/"+desc, "temporal_buffers")
arcpy.MakeFeatureLayer_management("D:/ArcGisShapesPruebas2/Buffers/"+desc, "temporal_buffer")





with arcpy.da.SearchCursor("temporal_buffers",["IDMANZANA"]) as cursor3:

    for row3 in cursor3:
        Suma_areas = 0
        where_expression = " IDMANZANA= \'"+str(row3[0])+"\'"
        arcpy.SelectLayerByAttribute_management("temporal_buffer", "NEW_SELECTION", where_expression)

        #print row3[0]

    #    with arcpy.da.SearchCursor("temporal_circulo" ,"*") as cursor2:
    #        for row2 in cursor2:
    #            print row2

        #arcpy.SelectLayerByAttribute ("temporal", "", ' "GRUPO" = 1 ')

        #select arcpy.da.SearchCursor



        #Calculo de la suma de las areas del grupo y sus viviendas
        arcpy.SelectLayerByAttribute_management("temporal_manzanas", "NEW_SELECTION")


        #print "otros"


        # Then add a selection to the layer based on location to features in another feature class

        # calculo de la suma de las areas que se encuentran  en el circulo
        arcpy.SelectLayerByLocation_management("temporal_manzanas", "INTERSECT",
                                               "temporal_buffer","","NEW_SELECTION")

        print "Manzana buffer:"+str(row3[0] )
        with arcpy.da.SearchCursor("temporal_manzanas", ["IDMANZANA"]) as cursor2:

            for row2 in cursor2:
                if row3[0]<>row2[0]:
                    print  str(row2[0])

        #print "Suma de areas dentro del circulo:" + str(Suma_areas_circulo)
        del cursor2




del cursor3


