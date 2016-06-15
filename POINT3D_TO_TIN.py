import arcpy
from arcpy import env
# Check out any necessary licenses
arcpy.CheckOutExtension("3D")
env.workspace = r"D:/ArcGisShapes/"
# Local variables:
Shapefile = "POINT_TOPOINT3D.shp Shape.Z"
Tin = "TIN_PRUEBA2"

# Process: Create TIN
arcpy.CreateTin_3d(Tin, "", Shapefile, "DELAUNAY")