

import arcpy
from arcpy import env


env.workspace = r"D:/ArcGisShapes/"

arcpy.PolygonToLine_management("D:/ArcGisShapes/VoronioPolygon",
                               "C:/output/Output.gdb/vegtype_lines",
                               "IGNORE_NEIGHBORS")