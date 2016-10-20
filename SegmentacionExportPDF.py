import arcpy
mxd = arcpy.mapping.MapDocument(r"D:/ArcGisProgramas/segmentacion.mxd")

arcpy.MakeFeatureLayer_management("D:/ArcGisSegmentacion/routes/rutas_final_dissolve.shp", "rutas_temporal")

df=arcpy.mapping.ListDataFrames(mxd,"Layers")[0]

#print df
#arcpy.SelectLayerByAttribute_management("rutas_temporal")

i=1

where_expression_2 = "AER= \'" + str(i) +"\' "

puntos=arcpy.SelectLayerByAttribute_management("D:/ArcGisSegmentacion/routes/rutas_final_dissolve.shp","NEW_SELECTION",where_expression_2)

arcpy.mapping.AddLayer(df,"D:/ArcGisSegmentacion/layers/rutaAER1021806003010290.lyr","AUTO_ARRANGE")



ddp = mxd.dataDrivenPages
indexLayer = ddp.indexLayer

#where_expression_2 = "AER= \'" + str(i) +"\' "


arcpy.SelectLayerByAttribute_management(indexLayer,"NEW_SELECTION",where_expression_2)




for indexPage in ddp.selectedPages:
    ddp.currentPageID = indexPage
    ddp.exportToPDF(r"D:/ArcGisPDFSegmentacion/Page" + str(indexPage) + ".pdf", "CURRENT")

del mxd

