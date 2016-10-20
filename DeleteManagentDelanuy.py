import arcpy
arcpy.env.workspace="Database Connections"
arcpy.env.workspace = r"Database Connections/Prueba6.sde/"
arcpy.env.workspace = r"Database Connections/Prueba6.sde/sprueba.DBO.prueba"



print arcpy.ListFeatureClasses()
print arcpy.Exists (r"Database Connections/Prueba6.sde/sprueba.DBO.prueba/sprueba.DBO.adyancencia")

if arcpy.Exists (r"Database Connections/Prueba6.sde/sprueba.DBO.prueba/sprueba.DBO.adyancencia_1"):

    arcpy.Delete_management("Database Connections/Prueba6.sde/sprueba.DBO.prueba/sprueba.DBO.adyancencia_1")
