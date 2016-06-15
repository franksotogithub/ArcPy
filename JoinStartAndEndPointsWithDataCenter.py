
import arcpy
import os
arcpy.env.workspace = r"D:/ArcGisShapes/"

desc= arcpy.Describe("POLIGON_TO_POINT.shp")

print desc.name

#arcpy.AddField_management("sprueba.DBO.departamentos","limites_buffer","TEXT","10")
#arcpy.Buffer_analysis("sprueba.DBO.departamentos","sprueba.DBO.departamentos_buffer",'10 miles')

inFeatures = "POLIGON_TO_POINT.shp"
fieldName1 = "X"
fieldName2 = "Y"
fieldPrecision = 18
fieldScale = 11


# Add fields
#arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE",
#                          fieldPrecision, fieldScale)
#arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE",
#                          fieldPrecision, fieldScale)



arcpy.AddField_management(inFeatures, 'XY', "TEXT","", "",100)
arcpy.AddField_management("TIN_TO_EDGE.shp", 'XYSTART', "TEXT","", "", 100)
arcpy.AddField_management("TIN_TO_EDGE.shp", 'XYEND', "TEXT","", "", 100)

#arcpy.AddField_management("TIN_TO_EDGE.shp", 'IDSTART', "TEXT","", "", 100)
#arcpy.AddField_management("TIN_TO_EDGE.shp", 'IDEND', "TEXT","", "", 100)


field_names = [f.name for f in arcpy.ListFields("POLIGON_TO_POINT.shp")]
print field_names

fc="D:/ArcGisShapes/POLIGON_TO_POINT.shp"
fields=['X','Y','SHAPE@X','SHAPE@Y']
with arcpy.arcpy.da.UpdateCursor(fc, fields) as cursor:
    for row in cursor:
        row[0]=row[2]
        row[1]=row[3]
        cursor.updateRow(row)
del cursor



fields=['X','Y','XY']
with arcpy.arcpy.da.UpdateCursor(fc, fields) as cursor:
    for row in cursor:
        row[2]=str(row[0]) + str(row[1])
        cursor.updateRow(row)
del cursor

fc="D:/ArcGisShapes/TIN_TO_EDGE.shp"
#inFeatures = "TIN_TO_EDGE.shp"
fields = ['StarX', 'StartY', 'XYSTART']
with arcpy.da.UpdateCursor(fc, fields) as cursor:
    for row in cursor:
        row[2] = str(row[0]) + str(row[1])
        cursor.updateRow(row)
del cursor


fields = ['EndX', 'EndY', 'XYEND']
with arcpy.da.UpdateCursor(fc, fields) as cursor:
    for row in cursor:
        row[2] = str(row[0]) + str(row[1])
        cursor.updateRow(row)
del cursor





inFeatures = "TIN_TO_EDGE.shp"
Field = "XYSTART"
joinTable = "POLIGON_TO_POINT.shp"
joinField="XY"
fieldList = ["IDMANZANA", "IDIST","CODZONA","SUFZONA","CODMZNA"]
# Join two feature classes by the zonecode field and only carry
# over the land use and land cover fields
arcpy.JoinField_management (inFeatures, Field, joinTable, joinField, fieldList)
