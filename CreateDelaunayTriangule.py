#import arcpy


# Set environment settings
#

#arcpy.env.workspace = r"Database Connections/Prueba6.sde/sprueba.DBO.base_urbana"


# Set local variables
#
#inFeatures = "sprueba.DBO.manzana_censal_centroide"
#outFeatureClass = "sprueba.DBO.manzana_censal_poligonos_Voronoi"
#outFields = "ALL"

#desc= arcpy.Describe("sprueba.DBO.manzana_censal")

#print desc.name
# Execute CreateThiessenPolygons
#
#arcpy.CreateThiessenPolygons_analysis(inFeatures, r"Database Connections/Prueba6.sde/sprueba.DBO.base_urbana/sprueba.DBO.manzana_censal_poligonos_Voronoi", outFields)



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

arcpy.env.workspace = r"Database Connections/Prueba6.sde/sprueba.DBO.base_urbana"

desc= arcpy.Describe("sprueba.DBO.manzana_censal")

print desc.name

arcpy.CreateTin_3d("sprueba.DBO.manzana_censal_delanuay", "","sprueba.DBO.manzana_censal_centroide", "Delaunay")