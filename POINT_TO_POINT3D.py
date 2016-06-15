# Name: CreateDatabase.py
# Description: Connects to a point in time in the geodatabase in
#              PostgreSQL using database authentication.

# Import system modules
import arcpy
import os




arcpy.env.workspace="Database Connections"
if arcpy.Exists ("Prueba7.sde")==False:

    arcpy.CreateDatabaseConnection_management("Database Connections",
                                          "Prueba7.sde",
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




#poligon to point
arcpy.env.workspace = r"Database Connections/Prueba6.sde/sprueba.DBO.base_urbana"

desc= arcpy.Describe("sprueba.DBO.manzana_censal")


fc="sprueba.DBO.manzana_censal"

fc_new="manzana_censal_centroide3.shp"

if arcpy.Exists (fc_new)==False:
    arcpy.CreateFeatureclass_management(r"Database Connections/Prueba6.sde/prueba.DBO.base_urbana",
                                    fc_new,
                                    "POINT",
                                    "",
                                    "",
                                    "",
                                    "")



#cursor= arcpy.da.InsertCursor("sprueba.DBO.manzana_censal_centroide",["SHAPE@"])

if arcpy.Exists (fc_new)==False:
    cursor = arcpy.da.InsertCursor(fc_new, ["SHAPE@"])
    for row in arcpy.da.SearchCursor(fc, ["SHAPE@"]):
        rowArray = []
        rowArray.append(row[0].centroid)
        cursor.insertRow(rowArray)
        print row[0].centroid

else:
    cursor = arcpy.da.UpdateCursor(fc_new, ["SHAPE@"])
    for row in arcpy.da.SearchCursor(fc, ["SHAPE@"]):
        rowArray = []
        rowArray.append(row[0].centroid)
        cursor.updateRow(rowArray)
        print row[0].centroid


arcpy.AddField_management(fc_new, 'Z', "SHORT")
arcpy.CalculateField_management(fc_new,'Z',1)


arcpy.FeatureTo3DByAttribute_3d(fc_new, 'sprueba.DBO.manzana_censal_3d', 'Z')





# arcpy.CalculateField_management(fc,fieldName1,1)


#fieldName1='Z'
#fieldPrecision = 18
#fieldScale = 11




#arcpy.AddField_management(fc, fieldName1, "SHORT",
#                          fieldPrecision, fieldScale)

#arcpy.CalculateField_management(fc,fieldName1,1)

#arcpy.FeatureTo3DByAttribute_3d(fc, 'sprueba.DBO.manzana_censal_3d', fieldName1)


#arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE",
#                          fieldPrecision, fieldScale)
#arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE",
#                          fieldPrecision, fieldScale)

# Calculate centroid
#arcpy.CalculateField_management(inFeatures, fieldName1,
#                                "!SHAPE.CENTROID.X!",
#                                "PYTHON_9.3")
#arcpy.CalculateField_management(inFeatures, fieldName2,
#                                "!SHAPE.CENTROID.Y!",
#                                "PYTHON_9.3")



