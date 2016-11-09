import arcpy
import numpy as np

arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"

def PorCantidadDeIntersecciones(adyacencias, voronoi):
    fields1 = ['FID']
    arcpy.env.overwriteOutput = True

    arcpy.MakeFeatureLayer_management(adyacencias, "temporal_adyacencias")
    arcpy.MakeFeatureLayer_management(voronoi, "temporal_voronoi")
    arcpy.MakeFeatureLayer_management(adyacencias, "temporal_adyacencia")

    # fc1 = "D:/ShapesPruebasSegmentacionUrbana/Edge/" + desc

    # fc2 = "D:/ShapesPruebasSegmentacionUrbana/Intersections/" + desc


    # fc3 = "D:/ShapesPruebasSegmentacionUrbana/IntersectionsInitial/" + desc
    # fields3 = ['FID_Shap_1']

    # arcpy.DeleteIdentical_management(r"D:/ShapesPruebasSegmentacionUrbana/VoronoiSplitLine/" + desc, ["Shape"])

    with arcpy.arcpy.da.UpdateCursor(adyacencias, fields1) as cursor1:
        # contador=0
        for row1 in cursor1:
            # print "ID:" + str(row1[0])
            contador = 0
            where_expression = "FID=" + str(row1[0])
            arcpy.SelectLayerByAttribute_management("temporal_adyacencia", "NEW_SELECTION", where_expression)
            arcpy.SelectLayerByLocation_management("temporal_voronoi", "INTERSECT",
                                                   "temporal_adyacencia", "", "NEW_SELECTION")

            cantidad = 0
            with arcpy.da.SearchCursor("temporal_voronoi", ["FID"]) as cursor2:
                for row2 in cursor2:
                    cantidad = cantidad + 1

            #print "IDVector: " + str(row1[0]) + "cantidad intersecciones:" + str(cantidad)

            if cantidad > 3:
                cursor1.deleteRow()


                ##     with arcpy.arcpy.da.UpdateCursor(fc3, fields3) as cursor2:

                #         for row2 in cursor2:
                #             if row1[0] == row2[0]:
                #                 contador = contador + 1
                #                 # print "contador:" + str(contador)
                #             if contador > 1:
                #                 cursor2.deleteRow()
                #                 contador = contador - 1
                #     del cursor2

                #    if contador>2:

                #        with arcpy.arcpy.da.UpdateCursor(fc3, fields3) as cursor2:
                #            for row2 in cursor2:
                #                if row1[0] == row2[0]:
                #                    cursor2.deleteRow()

                #        del cursor2
                # contador = 1

    del cursor1



def PorCantidadManzanasCruza(manzanas,adyacencias):
    arcpy.env.overwriteOutput = True
    arcpy.MakeFeatureLayer_management(adyacencias, "temporal_adyacencias")
    arcpy.MakeFeatureLayer_management(adyacencias, "temporal_adyacencia")
    arcpy.MakeFeatureLayer_management(manzanas, "temporal_manzanas")
#arcpy.MakeFeatureLayer_management(manzanas, "temporal_circulo")

    with arcpy.da.UpdateCursor(adyacencias, ["FID"]) as cursor3:
        for row3 in cursor3:
            where_expression = " FID=" + str(row3[0])
            arcpy.SelectLayerByAttribute_management("temporal_adyacencia", "NEW_SELECTION", where_expression)

            arcpy.SelectLayerByAttribute_management("temporal_manzanas", "NEW_SELECTION")
            arcpy.SelectLayerByLocation_management("temporal_manzanas", "INTERSECT",
                                                   "temporal_adyacencia", "", "NEW_SELECTION")

            cantidad=0
            with arcpy.da.SearchCursor("temporal_manzanas", ["FID"]) as cursor2:
                for row2 in cursor2:
                    cantidad=cantidad+1



            #print "IDVector: "+ str(row3[0]) + "cantidad intersecciones:" + str(cantidad)

            if cantidad>2:
                cursor3.deleteRow()



def PorZonaCruza(zona,adyacencias):
    arcpy.env.overwriteOutput = True
    arcpy.MakeFeatureLayer_management(adyacencias, "temporal_adyacencias")
    arcpy.MakeFeatureLayer_management(adyacencias, "temporal_adyacencia")
    zona_lineas="in_memory\zona_lineas"

    arcpy.MakeFeatureLayer_management(zona, "temporal_zona")

    arcpy.FeatureToLine_management(zona,zona_lineas)

    arcpy.MakeFeatureLayer_management(zona_lineas, "temporal_zona_lineas")


    with arcpy.arcpy.da.UpdateCursor(adyacencias, ['FID']) as cursor1:
        # contador=0
        for row1 in cursor1:
            # print "ID:" + str(row1[0])
            contador = 0
            where_expression = "FID=" + str(row1[0])
            arcpy.SelectLayerByAttribute_management("temporal_adyacencia", "NEW_SELECTION", where_expression)
            arcpy.SelectLayerByLocation_management("temporal_zona_lineas", "INTERSECT",
                                                   "temporal_adyacencia", "", "NEW_SELECTION")

            cantidad = 0
            with arcpy.da.SearchCursor("temporal_zona_lineas", ["FID"]) as cursor2:
                for row2 in cursor2:
                    cantidad = cantidad + 1


            if (cantidad > 0):
                cursor1.deleteRow()



    del cursor1