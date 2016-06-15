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


#arcpy.ListUsers(conection_sde)

#print arcpy.ListFeatureClasses()

prueba = "Prueba6.sde"
desc= arcpy.Describe("Prueba6.sde")
print desc.name




arcpy.env.workspace = r"Database Connections/Prueba6.sde"

desc= arcpy.Describe("sprueba.DBO.base_limites_nacionales")

print desc.name


#datasets=arcpy.ListDatasets()


arcpy.env.workspace = r"Database Connections/Prueba6.sde/sprueba.DBO.base_limites_nacionales"

desc= arcpy.Describe("sprueba.DBO.departamentos")

print desc.name

#arcpy.AddField_management("sprueba.DBO.departamentos","limites_buffer","TEXT","10")
#arcpy.Buffer_analysis("sprueba.DBO.departamentos","sprueba.DBO.departamentos_buffer",'10 miles')

inFeatures = "sprueba.DBO.departamentos"
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

