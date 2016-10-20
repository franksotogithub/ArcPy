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


arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/segmentacion.gdb/urbano/vivienda_censal_1", "vivienda_censal_temporal")
arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/segmentacion.gdb/urbano/vivienda_censal_1", "vivienda_censal_temporal2")
arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/AER_MANZANA.dbf", "aer_manzana")

# Set environment settings
output_dir = "D:/ShapesPruebasSegmentacionUrbana"
# The NA layer's data will be saved to the workspace specified here
env.workspace = os.path.join(output_dir, "segmentacion.gdb")
env.overwriteOutput = True
arcpy.CheckOutExtension("network")
# Set local variables

input_gdb = "D:/ShapesPruebasSegmentacionUrbana/segmentacion.gdb"

network = "D:/ShapesPruebasSegmentacionUrbana/segmentacion.gdb/urbano/urbano_ND2"
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


try:
    for i in range(1,10):


        where_expression = "AER=\'" + str(i)+"\'"
    #where_expression = " AER= '1' "
    #arcpy.SelectLayerByAttribute_management("vivienda_censal_temporal", "NEW_SELECTION")
    #arcpy.SelectLayerByAttribute_management("aer_manzana", "NEW_SELECTION",where_expression)

        with arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/AER_MANZANA.dbf", ["IDMANZANA"],where_expression) as cursor2:
            for fila in cursor2:
                where_expression_2 = "AER= \'" + str(i) +"\' "+ " AND IDMANZANA =\'"+str(fila[0])+"\'"
                #print where_expression_2
                puntos=arcpy.SelectLayerByAttribute_management("vivienda_censal_temporal","NEW_SELECTION",where_expression_2)


                #for f in puntos:
                #    print f

            #Get the layer object from the result object. The closest facility layer can
            #now be referenced using the layer object.

            #print layer_object

            #Get the names of all the sublayers within the closest facility layer.


            #Load the warehouses as Facilities using the default field mappings and
            #search tolerance

            #puntos="D:/ShapesPruebasSegmentacionUrbana/segmentacion.gdb/urbano/vivienda_censal_3"

            #arcpy.na.AddLocations(layer_object, "Facilities",puntos,"","","ORDEN")


                arcpy.na.AddLocations(layer_object, stops_layer_name,puntos,"","","ORDEN","","","CLEAR")
                arcpy.na.Solve(layer_object)
                #                    facilities, "", "")

            #Load the stores as Incidents. Map the Name property from the NOM field
            #using field mappings
                #field_mappings = arcpy.na.NAClassFieldMappings(layer_object,
                 #                                           incidents_layer_name)
                #field_mappings["Name"].mappedFieldName = "NOM"
                #arcpy.na.AddLocations(layer_object, incidents_layer_name, incidents,
                 #                 field_mappings, "")

            #Solve the closest facility layer


                #print arcpy.mapping.ListLayers(layer_object, routes_layer_name)




                RoutesSubLayer = arcpy.mapping.ListLayers(layer_object, routes_layer_name)[0]
                #StopsSubLayer = arcpy.mapping.ListLayers(layer_object, stops_layer_name)[0]




                name_file_route="rutaAER"+str(i)+str(fila[0])+".shp"
                #stops_file_route = "stopsAER" + str(i) + str(fila[0]) + ".shp"
                arcpy.CopyFeatures_management(RoutesSubLayer, "D:/ShapesPruebasSegmentacionUrbana/routes/"+name_file_route)
                #arcpy.CopyFeatures_management(StopsSubLayer, "D:/ShapesPruebasSegmentacionUrbana/stops/"+stops_file_route)
                outLayerFile = "rutaAER" + str(i) + str(fila[0]) + ".lyrx"



                #arcpy.management.SaveToLayerFile(outNALayer, outLayerFile, "RELATIVE")
                #outNALayer --> shape
                #outLayerFile --> ruta del archivo

                arcpy.management.SaveToLayerFile(layer_object, "D:/ShapesPruebasSegmentacionUrbana/layers/"+outLayerFile, "RELATIVE")


                inFeatures = "D:/ShapesPruebasSegmentacionUrbana/routes/"+name_file_route
                fieldName1 = "AER"
                fieldName2 = "IDMANZANA"


            # Add fields
                arcpy.AddField_management(inFeatures, fieldName1, "SHORT")
                arcpy.AddField_management(inFeatures, fieldName2, "TEXT")
                fields = ['AER', 'IDMANZANA']

            # Create update cursor for feature class
                with arcpy.da.UpdateCursor(inFeatures, fields) as cursor:
                    for row in cursor:
                        row[0] = i
                        row[1] = fila[0]
                        cursor.updateRow(row)
                del cursor


            #print RoutesSubLayer
                lista_nombres_archivos.append(inFeatures)
    del cursor2

    arcpy.Merge_management(lista_nombres_archivos, "D:/ShapesPruebasSegmentacionUrbana/routes/rutas_final.shp")
    arcpy.Dissolve_management("D:/ShapesPruebasSegmentacionUrbana/routes/rutas_final.shp", "D:/ShapesPruebasSegmentacionUrbana/routes/rutas_final_dissolve.shp","AER")



    print("Script completed successfully")

except Exception as e:
            # If an error occurred, print line number and error message
    import traceback, sys
    tb = sys.exc_info()[2]
    print("An error occured on line %i" % tb.tb_lineno)
    print(str(e))





