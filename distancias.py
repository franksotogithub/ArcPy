# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# distancias.py
# Created on: 2016-07-11 18:25:30.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Set the necessary product code
# import arcinfo


# Import arcpy module
import arcpy


# Local variables:
ZONA1 = "ZONA1"
ZONA1_FeatureToPoint = "C:\\Users\\fsoto\\Documents\\ArcGIS\\Default.gdb\\ZONA1_FeatureToPoint"
ZONA1_FeatureToPoint_PointDi = "C:\\Users\\fsoto\\Documents\\ArcGIS\\Default.gdb\\ZONA1_FeatureToPoint_PointDi"
ZONA1_FeatureToPoint_PointDi__2_ = "C:\\Users\\fsoto\\Documents\\ArcGIS\\Default.gdb\\ZONA1_FeatureToPoint_PointDi"

# Process: Feature To Point
arcpy.FeatureToPoint_management(ZONA1, ZONA1_FeatureToPoint, "INSIDE")

# Process: Point Distance
arcpy.PointDistance_analysis(ZONA1_FeatureToPoint, ZONA1_FeatureToPoint, ZONA1_FeatureToPoint_PointDi, "")

# Process: Join Field
arcpy.JoinField_management(ZONA1_FeatureToPoint_PointDi, "INPUT_FID", ZONA1_FeatureToPoint, "OBJECTID", "IDMANZANA;viv")

# Process: Join Field (2)
arcpy.JoinField_management(ZONA1_FeatureToPoint_PointDi__2_, "NEAR_FID", ZONA1_FeatureToPoint, "OBJECTID", "IDMANZANA;viv")


