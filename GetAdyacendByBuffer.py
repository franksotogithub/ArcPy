import arcpy
import numpy as np



num_max_zonas=2
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

desc= arcpy.Describe("sprueba.DBO.base_urbana")

print desc.name


arcpy.env.workspace = r"Database Connections/Prueba6.sde/sprueba.DBO.prueba"

#arcpy.Exists ("Prueba6.sde")==False:
if arcpy.Exists (r"Database Connections/Prueba6.sde/sprueba.DBO.prueba/sprueba.DBO.adyacencia"):
    arcpy.Delete_management("Database Connections/Prueba6.sde/sprueba.DBO.prueba/sprueba.DBO.adyacencia")





arcpy.env.workspace = r"Database Connections/Prueba6.sde/sprueba.DBO.base_urbana"

desc= arcpy.Describe("sprueba.DBO.zona_censal")

print desc.name

where_list=["150133","002"]
where_expression=' "IDDIST"=%s AND "CODZONA"=%s ' % (where_list[0],where_list[1])

#IDIST='150133'
#CODZONA='002'

#arcpy.FeatureClassToFeatureClass_conversion("sprueba.DBO.zona_censal", "D:/ArcGisShapesPruebas22/", 'zona_censal.shp' ,' "IDDIST" = \'150133\' ')
arcpy.FeatureClassToFeatureClass_conversion("sprueba.DBO.zona_censal", "D:/ArcGisShapesPruebas2/", 'zona_censal.shp' ,where_expression)


#crear el shape que  va a contener toda lainformacion






#se crean los shapes para estos efectos se utiliza solo hasta el numer4o 10

i=1
for row  in arcpy.da.SearchCursor("sprueba.DBO.zona_censal", ["IDDIST","CODZONA","SUFZONA"],where_expression):
    print row[0] + " " + row[1]+" "+row[2]
    desc="Shape"+str(row[0])+""+str(row[1])+""+str(row[2])
    where_clause= ' "IDDIST"=%s AND "CODZONA"=%s AND "SUFZONA"=%s' % (row[0],row[1],row[2])


    arcpy.FeatureClassToFeatureClass_conversion("sprueba.DBO.manzana_censal_viviendas", "D:/ArcGisShapesPruebas2/Zones/", desc,where_clause)


    print i
    i=i+1

    if i==num_max_zonas:
        break



#Obtenemos los nombres de los shapes que se han creado y le sacamos su centroide
#arcpy.env.workspace = r"D:/ArcGisShapesPruebas2"
#arcpy.env.workspace = r"D:/ArcGisShapesPruebas2"

arcpy.env.workspace = r"D:/ArcGisShapesPruebas2"
arcpy.env.overwriteOutput = True

if arcpy.Exists ("D:/ArcGisShapesPruebas2/ShapesFinal/adyacencia.shp")==False:
    arcpy.CreateFeatureclass_management("D:/ArcGisShapesPruebas2/ShapesFinal/",
                                    "adyacencia.shp",
                                    "POLYLINE",
                                    "",
                                    "",
                                    "ENABLED",
                                    "")

    fieldName1 = "FirstX"
    fieldName2 = "FirstY"

    fieldName3 = "LastX"
    fieldName4 = "LastY"

    fieldPrecision = 20
    fieldScale = 11


    inFeatures = "D:/ArcGisShapesPruebas2/ShapesFinal/adyacencia.shp"

    # Add fields inicio
    arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE",
                              fieldPrecision, fieldScale)
    arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE",
                              fieldPrecision, fieldScale)
    # Add fields inicio
    arcpy.AddField_management(inFeatures, fieldName3, "DOUBLE",
                              fieldPrecision, fieldScale)
    arcpy.AddField_management(inFeatures, fieldName4, "DOUBLE",
                              fieldPrecision, fieldScale)

else:
    with arcpy.arcpy.da.UpdateCursor("D:/ArcGisShapesPruebas2/ShapesFinal/adyacencia.shp" ) as cursor:
          cursor.deleteRow()

    del cursor


i=1
for row  in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas2/zona_censal.shp", ["IDDIST","CODZONA","SUFZONA"]):

    desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])+".shp"

# convertimos a buffer envolvente





    arcpy.Buffer_analysis("D:/ArcGisShapesPruebas2/Zones/"+desc, "D:/ArcGisShapesPruebas2/Buffers/"+desc, '15 METERS')





    i=i+1
    if i==num_max_zonas:
        break






