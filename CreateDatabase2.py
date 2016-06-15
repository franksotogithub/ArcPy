# Name: CreateDatabase.py
# Description: Connects to a point in time in the geodatabase in
#              PostgreSQL using database authentication.

# Import system modules
import arcpy
import os

# Run the tool
#path="d:/ArcGisConexiones"
#file_sde="Prueba6.sde"
#conection_sde=path+"/"+ file_sde


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


#arcpy.env.workspace = "" # Release hold on enterprise geodatabase workspace created in previous steps.

# Execute he Clear Workspace Cache tool
#arcpy.ClearWorkspaceCache_management() # If you do not specify a connection, all enterprise geodatabase workspaces will be removed from the Cache

arcpy.env.workspace = r"Database Connections/Prueba6.sde"

datasets=arcpy.ListDatasets()



for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path=os.path.join(arcpy.env.workspace,ds,fc)
        print path





#datasetList = arcpy.ListDatasets()

#print datasetList







#arcpy.env.workspace=""



#arcpy.ClearWorkspaceCache_management()

#arcpy.ClearWorkspaceCache_management()
#arcpy.Delete_management("Prueba6.sde")
#os.remove("C:\\Users\\fsoto\\AppData\\Roaming\\ESRI\\Desktop10.3\\ArcCatalog\Prueba6.sde")



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