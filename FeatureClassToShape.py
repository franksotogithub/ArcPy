import arcpy
#arcpy.env.workspace = "D:/ArcGisShapes/"

#arcpy.env.workspace = r"Database Connections/Prueba6.sde/sprueba.DBO.base_limites_nacionales"
#arcpy.FeatureClassToShapefile_conversion(["sprueba.DBO.distritos"],
#                                         "D:/ArcGisShapes/")





arcpy.env.workspace="Database Connections"
if arcpy.Exists ("Prueba6.sde")==False:

    arcpy.CreateDatabaseConnection_management("Database Connections",
                                          "Prueba6.sde",
                                          "SQL_SERVER",
                                          "192.168.200.250",
                                          "DATABASE_AUTH",
                                          "sde",
                                          "$deDEs4Rr0lLo",
                                          "#",
                                          "sprueba",
                                          "#",
                                          "#",
                                          "#",
                                          "#")


#arcpy.ListUsers(conection_sde)

#print arcpy.ListFeatureClasses()

prueba = "Prueba6.sde"
desc= arcpy.Describe("Prueba6.sde")
print desc.name




arcpy.env.workspace = r"Database Connections/Prueba6.sde"

desc= arcpy.Describe("sprueba.DBO.base_limites_nacionales")

print desc.name

arcpy.env.workspace = r"Database Connections/Prueba6.sde/sprueba.DBO.base_limites_nacionales"

desc= arcpy.Describe("sprueba.DBO.distritos")

print desc.name



arcpy.FeatureClassToFeatureClass_conversion("sprueba.DBO.distritos", "D:/ArcGisShapes/", "distritos_prueba2" ,' "IDDIST" = \'150132\' ')