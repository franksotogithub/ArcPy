import arcpy
import os
arcpy.env.workspace = r"D:/ArcGisShapes/"

desc= arcpy.Describe("TIN_TO_EDGE.shp")

print desc.name

#arcpy.AddField_management("sprueba.DBO.departamentos","limites_buffer","TEXT","10")
#arcpy.Buffer_analysis("sprueba.DBO.departamentos","sprueba.DBO.departamentos_buffer",'10 miles')

inFeatures = "TIN_TO_EDGE.shp"
fieldName1 = "EndX"
fieldName2 = "EndY"
fieldPrecision = 18
fieldScale = 11


# Add fields
arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE",
                          fieldPrecision, fieldScale)
arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE",
                          fieldPrecision, fieldScale)

# Calculate Points
arcpy.CalculateField_management(inFeatures, fieldName1,
                                "!SHAPE.lastPoint.X!",
                                "PYTHON_9.3")
arcpy.CalculateField_management(inFeatures, fieldName2,
                                "!SHAPE.lastPoint.Y!",
                                "PYTHON_9.3")



field_names = [f.name for f in arcpy.ListFields("TIN_TO_EDGE.shp")]

print field_names


with arcpy.da.SearchCursor("TIN_TO_EDGE.shp",field_names,' "IDDIST" = \'150132\' ') as cursor:
    for row in sorted(cursor):
        print row
