import arcpy
#arcpy.env.workspace = "D:/ArcGisShapes/"

#arcpy.env.workspace = r"Database Connections/Prueba6.sde/sprueba.DBO.base_limites_nacionales"
#arcpy.FeatureClassToShapefile_conversion(["sprueba.DBO.distritos"],
#                                         "D:/ArcGisShapes/")





arcpy.env.workspace="Database Connections"
if arcpy.Exists ("PruebaSegmentacion.sde")==False:

    arcpy.CreateDatabaseConnection_management("Database Connections",
                                          "PruebaSegmentacion.sde",
                                          "SQL_SERVER",
                                          "192.168.200.250",
                                          "DATABASE_AUTH",
                                          "sde",
                                          "$deDEs4Rr0lLo",
                                          "#",
                                          "CPV_SEGMENTACION",
                                          "#",
                                          "#",
                                          "#",
                                          "#")


#arcpy.ListUsers(conection_sde)

#print arcpy.ListFeatureClasses()

#prueba = "Prueba6.sde"
#desc= arcpy.Describe("Prueba6.sde")
#print desc.name




arcpy.env.workspace = r"Database Connections/PruebaSegmentacion.sde"

#desc= arcpy.Describe("sprueba.DBO.base_limites_nacionales")

#print desc.name

#arcpy.env.workspace = r"Database Connections/Prueba6.sde/sprueba.DBO.base_urbana"

#desc= arcpy.Describe("sprueba.DBO.manzana_censal")

#print desc.name

#arcpy.CopyFeatures_management("sprueba.DBO.manzana_censal", r"Database Connections/Prueba6.sde/sprueba.DBO.base_urbana/sprueba.DBO.manzana_censal_viviendas")

#arcpy.FeatureClassToFeatureClass_conversion("sprueba.DBO.manzana_censal", "Database Connections/Prueba6.sde/sprueba.DBO.base_urbana/", "manzana_censal_vivienda" )


arcpy.CopyFeatures_management("CPV_SEGMENTACION.dbo.TB_MZS", "Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO")