# Name: CreateDatabase.py
# Description: Connects to a point in time in the geodatabase in
#              PostgreSQL using database authentication.

# Import system modules
import arcpy
import os




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




arcpy.env.workspace = r"Database Connections/Prueba6.sde/sprueba.DBO.base_urbana"

desc= arcpy.Describe("sprueba.DBO.manzana_censal")

print desc.name

#arcpy.AddField_management("sprueba.DBO.departamentos","limites_buffer","TEXT","10")
#arcpy.Buffer_analysis("sprueba.DBO.departamentos","sprueba.DBO.departamentos_buffer",'10 miles')

inFeatures = "sprueba.DBO.manzana_censal"
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



