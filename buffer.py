import arcpy
path= "d:/ArcGisShapes/Departamentos"
arcpy.env.workspace=path
arcpy.env.overwriteOutput = True
arcpy.Buffer_analysis("departamentos2014.shp","departamentos2014_Buffer.shp",'10 miles')

