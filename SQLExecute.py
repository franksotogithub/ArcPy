import arcpy
import sys


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



egdb_conn = arcpy.ArcSDESQLExecute(r"Database Connections/Prueba6.sde")


tbl = "sprueba.DBO.departamentos"

try:
    sql = "select IDDPTO,NOM_DPTO from {0}".format(tbl)
    print("Attempt to execute SQL Statement: {0}".format(sql))
    egdb_return = egdb_conn.execute(sql)
    #print egdb_return
    for row in egdb_return:
        print "id=" + row[0] + " nombre=" + row[1]

except Exception as err:
    print(err)
    egdb_return = False


