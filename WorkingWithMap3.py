import  arcpy.mapping as mapping
mxd= mapping.MapDocument("d:/ArcGisProgramas/prueba_departamentos_2014.mxd")
layers= mapping.ListLayers(mxd)
for lyr in layers:
    print lyr.name
