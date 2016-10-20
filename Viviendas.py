import arcpy
import numpy as np
import  ImportarExportarSQL as ie


#import SolucionInicial as s
#
#num_max_zonas=7
#
#arcpy.env.workspace="Database Connections"
#
#if arcpy.Exists ("PruebaSegmentacion.sde")==False:
#    arcpy.CreateDatabaseConnection_management("Database Connections",
#                                          "PruebaSegmentacion.sde",
#                                          "SQL_SERVER",
#                                          "192.168.200.250",
#                                          "DATABASE_AUTH",
#                                          "sde",
#                                          "$deDEs4Rr0lLo",
#                                          "#",
#                                          "CPV_SEGMENTACION",
#                                          "#",
#                                          "#",
#                                          "#",
#                                          "#")
#arcpy.env.workspace="Database Connections/PruebaSegmentacion.sde"
##if arcpy.Exists (r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO"):
##    arcpy.Delete_management("Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO")
#
#arcpy.FeatureClassToFeatureClass_conversion("CPV_SEGMENTACION.dbo.TB_VIVIENDAS_U", "D:/ShapesPruebasSegmentacionUrbana/Viviendas/", 'TB_VIVIENDAS_U_TRABAJO.shp' )
##arcpy.FeatureClassToFeatureClass_conversion("CPV_SEGMENTACION.dbo.TB_ZONA_CENSAL", "D:/ShapesPruebasSegmentacionUrbana/Zones/", 'zona_censal.shp' ,where_expression)
#
#arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"
#
#inFeatures="D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO.shp"
#arcpy.AddField_management(inFeatures, "IDMANZANA", "TEXT")
#exp = "!UBIGEO!+!ZONA!+!MANZANA!"
#arcpy.CalculateField_management(inFeatures, "IDMANZANA", exp, "PYTHON_9.3")
#
#arcpy.AddField_management(inFeatures, "OR_VIV_AEU", "SHORT")
#
#i=1
#for row in arcpy.da.SearchCursor(r"D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp", ["UBIGEO","ZONA","CODCCPP"]):
#    print row[0] + " " + row[1]+" "+row[2]
#    desc="Shape"+str(row[0])+""+str(row[1])+""+str(row[2])
#
#    where_clause= ' "UBIGEO"=\'%s\' AND "ZONA"=\'%s\' AND "CODCCPP"=\'%s\' AND  ("USOLOCAL"=1 OR "USOLOCAL"=3)  ' % (row[0],row[1],row[2])
#    print where_clause
#    arcpy.FeatureClassToFeatureClass_conversion("D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO.shp", "D:/ShapesPruebasSegmentacionUrbana/Viviendas/", desc,where_clause)
#
#    i=i+1
#    if i>num_max_zonas:
#        break
#
#

def ReordenarViviendas():
    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/"
    fc3 = r"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"



    if arcpy.Exists ("D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO_SORT.shp"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO_SORT.shp")


    fc1 = r"D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO.shp"
    fc2 = r"D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO_SORT.shp"

    sort_fields = [["UBIGEO","ASCENDING"],["ZONA","ASCENDING"],["MANZANA", "ASCENDING"],["Shape", "ASCENDING"]]
    arcpy.Sort_management(fc1, fc2, sort_fields)

    arcpy.MakeFeatureLayer_management(fc2, "viviendas_temporal")

    with arcpy.arcpy.da.SearchCursor(fc3, ['UBIGEO','ZONA','MANZANA']) as cursor3:
        for row3 in cursor3:

            where_expression = " UBIGEO=\'" + str(row3[0]) + "\'  AND  ZONA=\'" + str(row3[1]) + "\' AND MANZANA=\'"+str(row3[2])+"\'"
            arcpy.SelectLayerByAttribute_management("viviendas_temporal","NEW_SELECTION",where_expression)

            #contador = 0
            orden=1
            with arcpy.arcpy.da.UpdateCursor("viviendas_temporal", ['OR_VIV_AEU']) as cursor1:
                for row1 in cursor1:
                    row1[0]=orden
                    orden = orden + 1
                    cursor1.updateRow(row1)

#ReordenarViviendas()
ie.Exportar_TB_VIVIENDAS_TRABAJO_SORT()



