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


arcpy.Buffer_analysis("sprueba.DBO.departamentos","sprueba.DBO.departamentos_buffer",'10 miles')


#arcpy.env.workspace = r"Database Connections/Prueba6.sde/sprueba.DBO.base_limites_nacionales/sprueba.DBO.departamentos"




field_names = [f.name for f in arcpy.ListFields("sprueba.DBO.departamentos")]

print field_names

with arcpy.da.SearchCursor("sprueba.DBO.departamentos",("IDDPTO","NOM_DPTO")) as cursor:
    for row in sorted(cursor):
        print("departamento id: " + row[0])
        print("departamento name: " + row[1])

