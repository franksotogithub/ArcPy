import arcpy
arcpy.MakeFeatureLayer_management(
    r"Database Connections/Prueba6.sde/sprueba.DBO.base_urbana",
    "sprueba.DBO.manzana_censal_centroide")

# Create a Describe object from the feature layer.
#
desc = arcpy.Describe("mainlines_layer")