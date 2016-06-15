import arcpy
import arcpy.da
path= r"c:/Users/fsoto/AppData/Roaming/Esri/Desktop10.3/ArcCatalog/Connection to 192.168.201.76.sde"
arcpy.env.workspace=path
fcList = arcpy.ListFeatureClasses()

i=0
for fc in fcList:
    i=i+1
    print fc
    if i>2:
        break
    else:
        fields = arcpy.ListFields(fc)
        for fl in fields:
            print fl.name

#try:
#    fields=arcpy.ListFields("signeg_bd_nac.public.departamentos_2014")



#    for fld in fields:
#        print fld.name
#except Exception as e:
#    print e.message()



#with arcpy.da.SearchCursor("signeg_bd_nac.public.departamentos_2014",("ccdd","nombdep")) as cursor:
#    for row in sorted(cursor):
#         print "Departamento : "+row[1]



#with arcpy.da.SearchCursor("departamentos2014.shp",("ccdd","nombdep")) as cursor:

 #   for row in sorted(cursor):
 #       print "Departamento : "+row[1]


#print arcpy.Exists(path)
#datasetList=arcpy.ListDatasets()
#print datasetList

#fields=arcpy.ListFields("departamentos2014.shp")
#print "Hola"
#for fld in fields:
#    print fld.name

