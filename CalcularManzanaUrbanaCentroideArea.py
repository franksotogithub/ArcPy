# Name: CreateDatabase.py
# Description: Connects to a point in time in the geodatabase in
#              PostgreSQL using database authentication.

# Import system modules
import arcpy
import os




#arcpy.env.workspace="Database Connections"
#if arcpy.Exists ("PruebaSegmentacion.sde")==False:
#    arcpy.CreateDatabaseConnection_management("Database Connections",
#                                              "PruebaSegmentacion.sde",
#                                              "SQL_SERVER",
#                                              "192.168.200.250",
#                                              "DATABASE_AUTH",
#                                              "sde",
#                                              "$deDEs4Rr0lLo",
#                                              "#",
#                                              "CPV_SEGMENTACION",
#                                              "#",
#                                              "#",
#                                              "#",
#                                              "#")
#




#arcpy.env.workspace = r"D:/PruebaSegmentacion.sde"

arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana/Manzanas"
#desc= arcpy.Describe("CPV_SEGMENTACION.DBO.TB_MZS")

#print desc.name

#arcpy.AddField_management("sprueba.DBO.departamentos","limites_buffer","TEXT","10")
#arcpy.Buffer_analysis("sprueba.DBO.departamentos","sprueba.DBO.departamentos_buffer",'10 miles')

inFeatures = "TB_MZS.shp"
fieldName1 = "xCentroid"
fieldName2 = "yCentroid"
fieldPrecision = 18
fieldScale = 11

# Add fields

arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE",
                          fieldPrecision, fieldScale)
arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE",
                          fieldPrecision, fieldScale)

# Calculate centroid
arcpy.CalculateField_management(inFeatures, fieldName1,
                                "!SHAPE.CENTROID.X!",
                                "PYTHON_9.3")
arcpy.CalculateField_management(inFeatures, fieldName2,
                                "!SHAPE.CENTROID.Y!",
                                "PYTHON_9.3")


arcpy.AddField_management(inFeatures, "AREA", "DOUBLE")
exp = "!SHAPE.AREA@METERS!"
arcpy.CalculateField_management(inFeatures, "AREA", exp, "PYTHON_9.3")


