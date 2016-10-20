import arcpy
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

if arcpy.Exists (r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_VIVIENDAS_U_TRABAJO"):
    arcpy.Delete_management("Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_VIVIENDAS_U_TRABAJO")

arcpy.env.workspace=r"D:/ShapesPruebasSegmentacionUrbana"
arcpy.FeatureClassToGeodatabase_conversion(['D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO.shp'],
                                           'Database Connections/PruebaSegmentacion.sde/')

#arcpy.env.workspace="Database Connections"