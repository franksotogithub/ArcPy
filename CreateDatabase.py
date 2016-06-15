# Name: CreateDatabase.py
# Description: Connects to a point in time in the geodatabase in
#              PostgreSQL using database authentication.

# Import system modules
import arcpy

# Run the tool
path="d:/ArcGisConexiones"
file_sde="Prueba5.sde"
conection_sde=path+"/"+ file_sde



if arcpy.Exists (conection_sde)==False:

    arcpy.CreateDatabaseConnection_management(path,
                                          file_sde,
                                          "POSTGRESQL",
                                          "192.168.201.76",
                                          "DATABASE_AUTH",
                                          "usSigneg",
                                          "Signeg2605",
                                          "#",
                                          "signeg_bd_nac",
                                          "#",
                                          "#",
                                          "#",
                                          "#")

#arcpy.ListUsers(conection_sde)

#print arcpy.ListFeatureClasses()
featureClass = "d:\\ArcGisConexiones\\Prueba5.sde"
desc= arcpy.Describe(featureClass)
print desc.name









#fieldList = arcpy.ListFields(featureClass)

#for field in fieldList:
#    print field.name





#arcpy.env.workspace=conection_sde
#for ls in arcpy.ListFeatureClasses("*"):
#    print arcpy.Describe(ls)




#datasetList = arcpy.ListDatasets("*", "Feature")
#for dataset in datasetList:
#        print dataset
#        fcList = arcpy.ListFeatureClasses("*", "", dataset)
#        fcList.sort()
#        for fc in fcList:
#            print fc

            #print arcpy.Exists("Prueba5.sde")
#print  arcpy.Exists("signeg_bd_nac.public.a_bd")

#arcpy.ListUsers("d:\ArcGisConexiones\Prueba4.sde")
#print arcpy.DisconnectUser(conection_sde,33)