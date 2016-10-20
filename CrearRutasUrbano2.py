# Name: Solve_Workflow.py
# Description: Solve a closest facility analysis to find the closest warehouse
#              from the store locations and save the results to a layer file on
#              disk.
# Requirements: Network Analyst Extension

#Import system modules
import arcpy
from arcpy import env
import os


arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbana"
#/TB_VIVIENDAS_U_TRABAJO_FINAL
arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp", "manzanas")
arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO.shp", "viviendas")
arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_CORTES.shp", "viviendas_cortes")
arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/MZS_AEU.dbf", "aer_manzana")

# Set environment settings
output_dir = "D:/ShapesPruebasSegmentacionUrbana"
# The NA layer's data will be saved to the workspace specified here
#env.workspace = os.path.join(output_dir, "segmentacion.gdb")
env.overwriteOutput = True
arcpy.CheckOutExtension("network")
# Set local variables



network = "D:/ShapesPruebasSegmentacionUrbana/ManzanasLine/TB_MZS_TRABAJO_LINE_FINAL_ND.nd"
# network = os.path.join(input_gdb, "Transportation", "ParisMultimodal_ND")

layer_name = "RutaTemporal"

# Create a new closest facility analysis layer.
result_object = arcpy.na.MakeRouteLayer(network, layer_name, "Length")
layer_object = result_object.getOutput(0)

sublayer_names = arcpy.na.GetNAClassNames(layer_object)

# Stores the layer names that we will use later
stops_layer_name = sublayer_names["Stops"]
routes_layer_name = sublayer_names["Routes"]
# incidents_layer_name = sublayer_names["Incidents"]



print  sublayer_names

lista_nombres_archivos=[]

cant_aeus=0

try:
    i = 0
    max_zonas = 1

    lista_nombres_archivos = []

    for row1 in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp",
                                     ["UBIGEO", "ZONA"]):

        where_expression = "UBIGEO=\'" + str(row1[0]) + "\' AND ZONA=\'" +str(row1[1])+ "\'"




        for row2 in arcpy.da.SearchCursor("manzanas",
                                         ["MANZANA","IDMANZANA"],where_expression):

            where_expression_2 = "IDMANZANA=\'" + str(row2[1])+"\'"

            cant_aeus=0

            for row21 in arcpy.da.SearchCursor("aer_manzana",
                                         ["AEU"],where_expression_2):
                cant_aeus = cant_aeus+1


        #print aeumax
        #j=0
            where_expression_3="UBIGEO=\'" + str(row1[0]) + "\' AND ZONA=\'" +str(row1[1])+"\' AND MANZANA=\'" +str(row2[0])+ "\'"
            if cant_aeus==1:
                puntos = arcpy.SelectLayerByAttribute_management("viviendas", "NEW_SELECTION",where_expression_3 )



                print len(puntos)


 #      while cant_aeus>=j:
 #          j=j+1
 #          #print j

 #          where_expression_3="UBIGEO=\'" + str(row[0]) + "\' AND ZONA=\'" +str(row[1])+ "\' AND AEU="+str(j)

 #          with arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/MZS_AEU.dbf", ["IDMANZANA"],where_expression_3) as cursor2:
 #              for fila in cursor2:
 #                  where_expression_2 = ' "AEU"= ' + str(j) +'  AND "IDMANZANA" =\''+str(fila[0])+'\''
 #                  print where_expression_2
 #                  #print str(row[1])
 #                  puntos=arcpy.SelectLayerByAttribute_management("viviendas","NEW_SELECTION",where_expression_2)


 #                  #print puntos

 #                  arcpy.na.AddLocations(layer_object, stops_layer_name,puntos,"","","OR_VIV_AEU","","","CLEAR")
 #                  try:
 #                      arcpy.na.Solve(layer_object)
 #                  except Exception as ee:
 #                      continue

 #                  #arcpy.na.Solve(layer_object)




 ##




 #                  RoutesSubLayer = arcpy.mapping.ListLayers(layer_object, routes_layer_name)[0]
 ##




 #                  name_file_route="rutaAEU"+str(row[1])+str(j)+str(fila[0])+".shp"   #zona aeu manzana
 ##
 #                  arcpy.CopyFeatures_management(RoutesSubLayer, "D:/ShapesPruebasSegmentacionUrbana/Rutas/"+name_file_route)
 ##
 #                  outLayerFile = "rutaAEU" + str(row[1])+str(j) + str(fila[0]) + ".lyrx"



 #              #arcpy.management.SaveToLayerFile(outNALayer, outLayerFile, "RELATIVE")
 #              #outNALayer --> shape
 #              #outLayerFile --> ruta del archivo

 #                  arcpy.management.SaveToLayerFile(layer_object, "D:/ShapesPruebasSegmentacionUrbana/RutasLayers/"+outLayerFile, "RELATIVE")
#
#
 #                  inFeatures = "D:/ShapesPruebasSegmentacionUrbana/Rutas/"+name_file_route

 #                  fieldName4 = "UBIGEO"
 #                  fieldName3 = "ZONA"
 #                  fieldName1 = "AEU"
 #                  fieldName2 = "IDMANZANA"


 #          # Add fields
 #                  arcpy.AddField_management(inFeatures, fieldName4, "TEXT")
 #                  arcpy.AddField_management(inFeatures, fieldName3, "TEXT")
 #                  arcpy.AddField_management(inFeatures, fieldName1, "SHORT")
 #                  arcpy.AddField_management(inFeatures, fieldName2, "TEXT")

 #                  fields = ['AEU', 'IDMANZANA','ZONA','UBIGEO']

 #                  with arcpy.da.UpdateCursor(inFeatures, fields) as cursor12:
 #                      for row12 in cursor12:
 #                          row12[0] = j
 #                          row12[1] = fila[0]
 #                          row12[2] = row[1]
 #                          row12[3]=row[0]
 #                          cursor12.updateRow(row12)
 #                  del cursor12

 #                  lista_nombres_archivos.append(inFeatures)


 #      i = i + 1
 #      if i > max_zonas:
 #          break
 #  arcpy.Merge_management(lista_nombres_archivos, "D:/ShapesPruebasSegmentacionUrbana/Rutas/rutas_final.shp")
 #  dissolve_fields=['UBIGEO','ZONA','AEU']
 #  arcpy.Dissolve_management("D:/ShapesPruebasSegmentacionUrbana/Rutas/rutas_final.shp",
 #                            "D:/ShapesPruebasSegmentacionUrbana/Rutas/rutas_final_dissolve.shp", dissolve_fields)

 ##  print("Script completed successfully")

except Exception as e:
            # If an error occurred, print line number and error message
    import traceback, sys
    tb = sys.exc_info()[2]
    print("An error occured on line %i" % tb.tb_lineno)
    print(str(e))


