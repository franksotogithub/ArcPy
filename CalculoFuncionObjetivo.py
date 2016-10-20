import arcpy
arcpy.env.workspace ="D:/ArcGisShapesPruebas"
# First, make a layer from the feature class



def Calculo(zona,circulos):
    arcpy.env.overwriteOutput = True
    arcpy.MakeFeatureLayer_management(zona, "temporal")
    arcpy.MakeFeatureLayer_management(circulos,"temporal_circulos")
    arcpy.MakeFeatureLayer_management(circulos, "temporal_circulo")


    #arcpy.MakeFeatureLayer_management("D:/ArcGisShapesPruebas/Zones/Shape15013300200.shp", "temporal")

    #arcpy.MakeFeatureLayer_management("D:/ArcGisShapesPruebas/EnvolvesCircles/pruebacirclebuffers.shp", "temporal_circulos")
    #arcpy.MakeFeatureLayer_management("D:/ArcGisShapesPruebas/EnvolvesCircles/pruebacirclebuffers.shp", "temporal_circulo")


    Z=0#Valor funcion Objetivo
    p=0.35
    q=0.65
    cant_max_viv=40
    suma_homogeneidad=0
    suma_compacidad=0
    homogeneidad=0
    compacidad=0
    #fields = ["GRUPO"]
    n=0
    with arcpy.da.SearchCursor("temporal_circulos",["GRUPO"]) as cursor3:
        for row3 in cursor3:
            Suma_areas = 0
            where_expression = " GRUPO="+str(row3[0])
            arcpy.SelectLayerByAttribute_management("temporal_circulo", "NEW_SELECTION", where_expression)

            #print row3[0]

        #    with arcpy.da.SearchCursor("temporal_circulo" ,"*") as cursor2:
        #        for row2 in cursor2:
        #            print row2

            #arcpy.SelectLayerByAttribute ("temporal", "", ' "GRUPO" = 1 ')

            #select arcpy.da.SearchCursor








            #Calculo de la suma de las areas del grupo y sus viviendas
            arcpy.SelectLayerByAttribute_management("temporal", "NEW_SELECTION")


            V = 0
            with arcpy.da.SearchCursor("temporal", ["IDMANZANA","Shape_area","TOT_VIV"], where_expression) as cursor1:
                Suma_areas = 0
                for row1 in cursor1:

                    Suma_areas = row1[1] + Suma_areas
                    V = row1[2] + V
            #print "Area en el grupo:" + str(Suma_areas)
            del cursor1

            #print "otros"


            # Then add a selection to the layer based on location to features in another feature class

            # calculo de la suma de las areas que se encuentran  en el circulo
            arcpy.SelectLayerByLocation_management("temporal", "WITHIN",
                                                   "temporal_circulo","","NEW_SELECTION")


            with arcpy.da.SearchCursor("temporal", ["IDMANZANA", "Shape_area"]) as cursor2:
                Suma_areas_circulo = 0
                for row2 in cursor2:
                    Suma_areas_circulo = Suma_areas_circulo + row2[1]

            #print "Suma de areas dentro del circulo:" + str(Suma_areas_circulo)
            del cursor2

            Ar = Suma_areas_circulo - Suma_areas
            A = Suma_areas_circulo

            homogeneidad=pow((V/cant_max_viv)-1,2)
            compacidad=Ar/(A)

            suma_homogeneidad = homogeneidad + suma_homogeneidad
            suma_compacidad=compacidad+suma_compacidad
        del row3
        n=1+n
    del cursor3


    #calculo con la formula

    Z=p*(1.0/float(n))*suma_homogeneidad+ q*(1.0/float(n))*suma_compacidad

    return  Z


#print Calculo("D:/ArcGisShapesPruebas/Zones/Shape15013300200.shp","D:/ArcGisShapesPruebas/EnvolvesCirclesBuffers/Shape15013300200.shp")