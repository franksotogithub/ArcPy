import arcpy



mxd = arcpy.mapping.MapDocument(r"D:/ArcGisProgramas/prueba.mxd")
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

for el in arcpy.mapping.ListLayers(mxd):
    print el.name

for table in arcpy.mapping.ListTableViews(mxd,"",df):
    print table.name

mxd.save()
del mxd



#accidentsTable = arcpy.mapping.TableView("sprueba.DBO.departamentos")
#arcpy.mapping.AddTableView(df, accidentsTable)
#mxd.saveACopy(r"D:/ArcGisProgramas/prueba.mxd")
#del mxd#, accidentsTable