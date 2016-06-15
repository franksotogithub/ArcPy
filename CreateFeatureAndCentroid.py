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

if arcpy.Exists ("sprueba.DBO.departamentos_centroide")==False:
    arcpy.CreateFeatureclass_management(r"Database Connections/Prueba6.sde/sprueba.DBO.base_limites_nacionales",
                                    "sprueba.DBO.departamentos_centroide",
                                    "POINT",
                                    "",
                                    "",
                                    "",
                                    "")
#arcpy.AddField_management(outCentroids, 'ORIG_ID', 'LONG')




cursor= arcpy.da.InsertCursor("sprueba.DBO.departamentos_centroide",["SHAPE@"])

for row in arcpy.da.SearchCursor("sprueba.DBO.departamentos", ["SHAPE@"]):
    rowArray = []
    rowArray.append(row[0].centroid)
    cursor.insertRow(rowArray)
    print row[0].centroid







