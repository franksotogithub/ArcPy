
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




prueba = "Prueba6.sde"
desc= arcpy.Describe("Prueba6.sde")
print desc.name




arcpy.env.workspace = r"Database Connections/Prueba6.sde"

desc= arcpy.Describe("sprueba.DBO.base_limites_nacionales")

print desc.name


#datasets=arcpy.ListDatasets()


arcpy.env.workspace = r"Database Connections/Prueba6.sde/sprueba.DBO.base_urbana"

desc= arcpy.Describe("sprueba.DBO.manzana_censal")

print desc.name



#arcpy.AddField_management(outCentroids, 'ORIG_ID', 'LONG')


if arcpy.Exists ("sprueba.DBO.manzana_censal_centroide2")==False:
    arcpy.CreateFeatureclass_management(r"Database Connections/Prueba6.sde/sprueba.DBO.base_urbana",
                                    "sprueba.DBO.manzana_censal_centroide2",
                                    "POINT",
                                    "",
                                    "",
                                    "ENABLED",
                                    "")




field_names = [f.name for f in arcpy.ListFields("sprueba.DBO.manzana_censal")]
#cursor= arcpy.da.InsertCursor("sprueba.DBO.departamentos_centroide",["SHAPE@"])
print field_names



cursor= arcpy.da.InsertCursor("sprueba.DBO.manzana_censal_centroide2",["SHAPE@"])

#for row in arcpy.da.SearchCursor("sprueba.DBO.manzana_censal", ["SHAPE@"],' "IDDIST" = \'150132\' '):
#    rowArray = []
#    rowArray.append(row[0].centroid)
#    print row[0].centroid


for row in arcpy.da.SearchCursor("sprueba.DBO.manzana_censal", ["SHAPE@XY"],' "IDDIST" = \'150132\' '):

    #print row[0][0]
    point = arcpy.Point(row[0][0], row[0][1],1)
    #print point
    rowArray = []
    rowArray.append(point)
    cursor.insertRow(rowArray)

    #print row[0].centroid

    #rowArray = []
    #rowArray.append(row[0].centroid)
    #print rowArray
    #cursor.insertRow(rowArray)
#    print row[0].centroid
