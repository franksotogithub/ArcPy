import arcpy
path= "d:/ArcGisShapes/Departamentos"
arcpy.env.workspace=path
fields=arcpy.ListFields("departamentos2014.shp")
print "Hola"
for fld in fields:
    print fld.name

