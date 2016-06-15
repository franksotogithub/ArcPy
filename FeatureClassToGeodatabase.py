import arcpy
arcpy.env.workspace = "D:/ArcGisShapes/"


arcpy.FeatureClassToGeodatabase_conversion(['TIN_EDGE.shp'],
                                           'Database Connections/Prueba6.sde/sprueba.DBO.base_urbana')