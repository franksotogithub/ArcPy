#import arcpy
#path= "d:/ArcGisShapes/Departamentos"
#arcpy.env.workspace=path
#arcpy.env.overwriteOutput = True
#arcpy.Buffer_analysis("departamentos2014.shp","departamentos2014_Buffer.shp",'10 miles')


import arcpy
path= "D:/ShapesPruebasSegmentacionUrbana"
arcpy.env.workspace=path
arcpy.env.overwriteOutput = True
arcpy.Buffer_analysis("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp","D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO_BUFFER.shp",'0.30 METERS','FULL','FLAT')

