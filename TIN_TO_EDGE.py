import arcpy
from arcpy import env
# Check out any necessary licenses
arcpy.CheckOutExtension("3D")
env.workspace = r"D:/ArcGisShapes/"

arcpy.TinEdge_3d('tin_prueba2', 'tin_edge_prueba2.shp', edge_type='DATA')