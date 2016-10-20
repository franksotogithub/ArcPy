import arcpy
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

arcpy.env.workspace = r"Database Connections/Prueba6.sde/sprueba.DBO.base_urbana"

desc= arcpy.Describe("sprueba.DBO.manzana_censal")

print desc.name


#arcpy.CopyFeatures_management("sprueba.DBO.manzana_censal", r"Database Connections/Prueba6.sde/sprueba.DBO.base_urbana/sprueba.DBO.manzana_censal_viviendas")

inFeatures=r"Database Connections/Prueba6.sde/sprueba.DBO.base_urbana/sprueba.DBO.manzana_censal_viviendas"
arcpy.AddField_management(inFeatures, "Shape_area", "DOUBLE")
exp = "!SHAPE.AREA@METERS!"
arcpy.CalculateField_management(inFeatures, "Shape_area", exp, "PYTHON_9.3")