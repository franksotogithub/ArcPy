import arcpy.da
arcpy.env.workspace="d:/ArcGisShapes/Departamentos"
with arcpy.da.SearchCursor("departamentos2014.shp",("ccdd","nombdep")) as cursor:

    for row in sorted(cursor):
        print "Departamento : "+row[1]





