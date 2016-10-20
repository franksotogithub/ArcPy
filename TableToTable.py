import arcpy
import sys

def Importar_Lista():

    #arcpy.env.workspace="D:/ArcGisShapesPruebas"
    #if arcpy.Exists ("LISTA_ADYACENCIA_MANZANA.dbf")==True:
    #    arcpy.Delete_management("LISTA_ADYACENCIA_MANZANA.dbf")


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



    arcpy.env.workspace="Database Connections/Prueba6.sde"

    arcpy.TableToTable_conversion("sprueba.dbo.LISTA_ADYACENCIA_POR_MANZANA", "D:\\ArcGisShapesPruebas\\ShapesFinal", "LISTA_ADYACENCIA_MANZANA.dbf")



Importar_Lista()