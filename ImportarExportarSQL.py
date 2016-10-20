import arcpy
import sys


def Importar_Zona():
    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/Zone"
    if arcpy.Exists ("D:/ShapesPruebasSegmentacionUrbana/Zone/zona_censal.shp"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Zone/zona_censal.shp")


    arcpy.env.workspace="Database Connections/PruebaSegmentacion.sde"

    arcpy.FeatureClassToFeatureClass_conversion("CPV_SEGMENTACION.dbo.TB_ZONA_CENSAL",
                                                "D:/ShapesPruebasSegmentacionUrbana/Zone/",
                                                'zona_censal.shp')

def Importar_TB_MZ():
    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/Manzanas"
    if arcpy.Exists ("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp")


    arcpy.env.workspace="Database Connections/PruebaSegmentacion.sde"

    arcpy.FeatureClassToFeatureClass_conversion("CPV_SEGMENTACION.sde.TB_MZS",
                                                "D:/ShapesPruebasSegmentacionUrbana/Manzanas/",
                                                'TB_MZS.shp')


def Importar_TB_MZ_TRABAJO():
    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/Manzanas"
    if arcpy.Exists ("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp")


    arcpy.env.workspace="Database Connections/PruebaSegmentacion.sde"

    arcpy.FeatureClassToFeatureClass_conversion("CPV_SEGMENTACION.sde.TB_MZS_TRABAJO",
                                                "D:/ShapesPruebasSegmentacionUrbana/Manzanas/",
                                                'TB_MZS_TRABAJO.shp')



def Importar_Lista_ADYACENCIA(RUTA,Lista_adyacencia):
    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana"
    ruta_lista_adyacencia=RUTA+"/"+Lista_adyacencia

    if arcpy.Exists (ruta_lista_adyacencia):
        arcpy.Delete_management(ruta_lista_adyacencia)


    arcpy.env.workspace="Database Connections"
    if arcpy.Exists ("PruebaSegmentacion.sde")==False:

        arcpy.CreateDatabaseConnection_management("Database Connections",
                                              "PruebaSegmentacion.sde",
                                              "SQL_SERVER",
                                              "192.168.200.250",
                                              "DATABASE_AUTH",
                                              "sde",
                                              "$deDEs4Rr0lLo",
                                              "#",
                                              "CPV_SEGMENTACION",
                                              "#",
                                              "#",
                                              "#",
                                              "#")



    arcpy.env.workspace="Database Connections/PruebaSegmentacion.sde"
    arcpy.TableToTable_conversion("CPV_SEGMENTACION.sde.LISTA_ADYACENCIA_POR_MANZANA", RUTA, Lista_adyacencia)



def Importar_Lista_MZS_AEU():
    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/ShapesFinal"
    if arcpy.Exists ("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/MZS_AEU.dbf"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/MZS_AEU.dbf")


    arcpy.env.workspace="Database Connections"
    if arcpy.Exists ("PruebaSegmentacion.sde")==False:

        arcpy.CreateDatabaseConnection_management("Database Connections",
                                              "PruebaSegmentacion.sde",
                                              "SQL_SERVER",
                                              "192.168.200.250",
                                              "DATABASE_AUTH",
                                              "sde",
                                              "$deDEs4Rr0lLo",
                                              "#",
                                              "CPV_SEGMENTACION",
                                              "#",
                                              "#",
                                              "#",
                                              "#")



    arcpy.env.workspace="Database Connections/PruebaSegmentacion.sde"

    arcpy.TableToTable_conversion("CPV_SEGMENTACION.dbo.MZS_AEU", "D:\\ShapesPruebasSegmentacionUrbana\\ShapesFinal", "MZS_AEU.dbf")




def Exportar_TB_MZS_TRABAJO():
    #fc = "D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO.shp"
    #arcpy.env.workspace = "D:/ShapesPruebasSegmentacionUrbana/ShapesFinal"
    arcpy.env.workspace = "Database Connections"
    if arcpy.Exists("PruebaSegmentacion.sde") == False:
        arcpy.CreateDatabaseConnection_management("Database Connections",
                                                  "PruebaSegmentacion.sde",
                                                  "SQL_SERVER",
                                                  "192.168.200.250",
                                                  "DATABASE_AUTH",
                                                  "sde",
                                                  "$deDEs4Rr0lLo",
                                                  "#",
                                                  "CPV_SEGMENTACION",
                                                  "#",
                                                  "#",
                                                  "#",
                                                  "#")

    arcpy.env.workspace = "Database Connections/PruebaSegmentacion.sde"

    if arcpy.Exists(r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO"):
        arcpy.Delete_management("Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO")

    #arcpy.TableToTable_conversion("CPV_SEGMENTACION.sde.LISTA_ADYACENCIA_POR_MANZANA",
    #                              "D:\\ShapesPruebasSegmentacionUrbana\\ShapesFinal", "LISTA_ADYACENCIA_MANZANA.dbf")


    arcpy.env.workspace = "D:/ShapesPruebasSegmentacionUrbana/Manzanas"

    arcpy.FeatureClassToGeodatabase_conversion(['TB_MZS_TRABAJO.shp'],
                                           'Database Connections/PruebaSegmentacion.sde')

def Exportar_TB_VIVIENDAS_TRABAJO_SORT():
    #fc = "D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO.shp"
    #arcpy.env.workspace = "D:/ShapesPruebasSegmentacionUrbana/ShapesFinal"
    arcpy.env.workspace = "Database Connections"
    if arcpy.Exists("PruebaSegmentacion.sde") == False:
        arcpy.CreateDatabaseConnection_management("Database Connections",
                                                  "PruebaSegmentacion.sde",
                                                  "SQL_SERVER",
                                                  "192.168.200.250",
                                                  "DATABASE_AUTH",
                                                  "sde",
                                                  "$deDEs4Rr0lLo",
                                                  "#",
                                                  "CPV_SEGMENTACION",
                                                  "#",
                                                  "#",
                                                  "#",
                                                  "#")

    arcpy.env.workspace = "Database Connections/PruebaSegmentacion.sde"

    if arcpy.Exists(r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_VIVIENDAS_U_TRABAJO_SORT"):
        arcpy.Delete_management("Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_VIVIENDAS_U_TRABAJO_SORT")

    #arcpy.TableToTable_conversion("CPV_SEGMENTACION.sde.LISTA_ADYACENCIA_POR_MANZANA",
    #                              "D:\\ShapesPruebasSegmentacionUrbana\\ShapesFinal", "LISTA_ADYACENCIA_MANZANA.dbf")


    arcpy.env.workspace = "D:/ShapesPruebasSegmentacionUrbana/Viviendas"

    arcpy.FeatureClassToGeodatabase_conversion(['D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO_SORT.shp'],
                                           'Database Connections/PruebaSegmentacion.sde')


def Importar_Viviendas():

    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/Viviendas"
    if arcpy.Exists ("D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO.shp"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO.shp")



    arcpy.env.workspace = "Database Connections/PruebaSegmentacion.sde"
    # if arcpy.Exists (r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO"):
    #    arcpy.Delete_management("Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO")

    arcpy.FeatureClassToFeatureClass_conversion("CPV_SEGMENTACION.dbo.TB_VIVIENDAS_U",
                                                "D:/ShapesPruebasSegmentacionUrbana/Viviendas/",
                                                'TB_VIVIENDAS_U_TRABAJO.shp')


def Importar_Cortes():
    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/Viviendas"
    if arcpy.Exists ("D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_CORTES.shp"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_CORTES.shp")


    arcpy.env.workspace = "Database Connections/PruebaSegmentacion.sde"
    # if arcpy.Exists (r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO"):
    #    arcpy.Delete_management("Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO")

    where=' "CORTE"=1 '
    arcpy.FeatureClassToFeatureClass_conversion("CPV_SEGMENTACION.dbo.TB_VIVIENDAS_U",
                                                "D:/ShapesPruebasSegmentacionUrbana/Viviendas/",
                                                'TB_VIVIENDAS_CORTES.shp',where)

def Importar_Cortes_Inicio_Fin():
    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/Viviendas"
    if arcpy.Exists ("D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_CORTES_INICIO_FIN.shp"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_CORTES_INICIO_FIN.shp")


    arcpy.env.workspace = "Database Connections/PruebaSegmentacion.sde"
    # if arcpy.Exists (r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO"):
    #    arcpy.Delete_management("Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO")

    where=' "CORTE"=2 '
    arcpy.FeatureClassToFeatureClass_conversion("CPV_SEGMENTACION.dbo.TB_VIVIENDAS_U",
                                                "D:/ShapesPruebasSegmentacionUrbana/Viviendas/",
                                                'TB_VIVIENDAS_CORTES_INICIO_FIN.shp',where)


#Importar_TB_MZ()

#Importar_Viviendas()
#Importar_Cortes()
#Importar_Cortes_Inicio_Fin()

#Importar_TB_MZ_TRABAJO()


#
#def InsertarAdyacencia():
#
#    arcpy.env.workspace="Database Connections"
#    if arcpy.Exists ("PruebaSegmentacion.sde")==False:
#
#        arcpy.CreateDatabaseConnection_management("Database Connections",
#                                              "PruebaSegmentacion.sde",
#                                              "SQL_SERVER",
#                                              "192.168.200.250",
#                                              "DATABASE_AUTH",
#                                              "sde",
#                                              "$deDEs4Rr0lLo",
#                                              "#",
#                                              "CPV_SEGMENTACION",
#                                              "#",
#                                              "#",
#                                              "#",
#                                              "#")
#
#
#
#    egdb_conn = arcpy.ArcSDESQLExecute(r"Database Connections/PruebaSegmentacion.sde")
#
#
#
#
#    try:
#        sql = " exec INSERTAR_LISTA_ADYACENCIA"
#
#        egdb_return = egdb_conn.execute(sql)
#
#
#    except Exception as err:
#        print(err)
#        egdb_return = False
#        #egdb_return2 = False
#
#
#Importar_Lista()
