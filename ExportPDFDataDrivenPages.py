import arcpy
mxd = arcpy.mapping.MapDocument(r"D:/ArcGisProgramas/prueba.mxd")
ddp = mxd.dataDrivenPages
indexLayer = ddp.indexLayer
arcpy.SelectLayerByAttribute_management(indexLayer)
for indexPage in ddp.selectedPages:
    ddp.currentPageID = indexPage
    ddp.exportToPDF(r"D:/ArcGisPDF/Page" + str(indexPage) + ".pdf", "CURRENT")

del mxd


