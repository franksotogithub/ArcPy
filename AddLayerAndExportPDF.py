import arcpy

arcpy.env.overwriteOutput = True  #sirve para sobreescribir los elementos



for i in range(1,2):
    mxd = arcpy.mapping.MapDocument(r"D:/ArcGisProgramas/segmentacion.mxd")
    df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

#    print i
    where_expression_1 = "AER= " + str(i)
    where_expression_2 = "AER= \'" + str(i) +"\' "

    arcpy.MakeFeatureLayer_management(r"D:/ArcGisSegmentacion/routes/rutas_final.shp", "rutas_temporal",where_expression_1)
    arcpy.MakeFeatureLayer_management(r"D:/ArcGisSegmentacion/vivienda_censal_1.shp", "viviendas_temporal",where_expression_2)
    #arcpy.MakeFeatureLayer_management(r"D:/ArcGisSegmentacion/rutas_final.lyr", "rutas_temporal_2",
    #                                  where_expression_1)

   #lyrFile=arcpy.SelectLayerByAttribute_management("rutas_temporal","NEW_SELECTION",where_expression_2)



    #lyrFile=arcpy.mapping.Layer(r"D:/ArcGisSegmentacion/routes/rutas_final_dissolve.shp")
    arcpy.SelectLayerByAttribute_management("rutas_temporal","NEW_SELECTION",where_expression_1)

    arcpy.SelectLayerByAttribute_management("viviendas_temporal","NEW_SELECTION",where_expression_2)
    #arcpy.SelectLayerByAttribute_management("rutas_temporal_2", "NEW_SELECTION", where_expression_1)

    #arcpy.SelectLayerByAttribute_management(r"D:/ArcGisSegmentacion/rutas_final.lyr", "NEW_SELECTION", where_expression_1)


    lyrFile1=arcpy.mapping.Layer("rutas_temporal")
    lyrFile2=arcpy.mapping.Layer("viviendas_temporal")
    #lyrFile3 = arcpy.mapping.Layer("rutas_temporal_2")

    arcpy.ApplySymbologyFromLayer_management(lyrFile1, "D:/ArcGisSegmentacion/rutas_final.lyr")
    arcpy.mapping.AddLayer(df,lyrFile1)
    #arcpy.mapping.AddLayer(df, lyrFile3)


    if lyrFile2.supports("LABELCLASSES"):
        for lblclass in lyrFile2.labelClasses:
            #lblclass.className = "[ORDEN]"
            lblclass.expression = "[ORDEN]"
            lblclass.showClassLabels = True


    lyrFile2.showLabels = True

    arcpy.RefreshActiveView()

    arcpy.mapping.AddLayer(df,lyrFile2)
    arcpy.RefreshActiveView()

    #for el in arcpy.mapping.ListDataFrames(mxd):
    #    print el.name

    #for el2 in arcpy.mapping.ListLayers(mxd):
    #    print el2.name

    ddp = mxd.dataDrivenPages
    indexLayer = ddp.indexLayer


    arcpy.SelectLayerByAttribute_management(indexLayer,"NEW_SELECTION",where_expression_2)


    for indexPage in ddp.selectedPages:
        ddp.currentPageID = indexPage
        ddp.exportToPDF(r"D:/ArcGisPDFSegmentacion/Page" + str(indexPage) + ".pdf", "CURRENT")
        #arcpy.mapping.PrintMap(mxd, r"\\pincullo\CANONiR4051-OEDS", df)
    arcpy.mapping.RemoveLayer(df,lyrFile1)
    arcpy.mapping.RemoveLayer(df,lyrFile2)
    #arcpy.mapping.RemoveLayer(df,lyrFile3)

    del mxd
    del df
    #arcpy.mapping.ExportToPDF(mxd,r"D:/ArcGisPDFSegmentacion/pruebaPDF.pdf")

    #print df
    #print df[0]
    #arcpy.SelectLayerByAttribute_management("rutas_temporal")


    #arcpy.mapping.ExportToPDF(mxd,r"D:/ArcGisPDFSegmentacion/pruebaPDF.pdf", "CURRENT")







