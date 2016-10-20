import arcpy.mapping as mapping
import os



mxd= mapping.MapDocument(r"D:/ArcGisProgramas/prueba.mxd")
path="D:/ArcGisPDF/prueba2.pdf"


for el in mapping.ListDataFrames(mxd):
    print el.name

for el in mapping.ListLayers(mxd):
    print el.name


for el in mapping.ListLayoutElements(mxd):
    print el
    print el.name

#print os.path.exists("D:/ArcGisPDF")
#print os.path.isfile("D:/ArcGisPDF/prueba2.pdf")

#mapping.ExportToPDF(mxd,path)


horzLine = mapping.ListLayoutElements(mxd,"TEXT_ELEMENT","horzLine")[0]
verLine = mapping.ListLayoutElements(mxd,"TEXT_ELEMENT","horzLine")[0]



print eltable

#df = mapping.ListDataFrames(mxd)[0]
#print df

#table = mapping.ListTableViews(mxd)
#print table




#import os import arcpy  mxd = arcpy.mapping.MapDocument("CURRENT") pdf = str(arcpy.GetParameterAsText(0)) name = str(arcpy.GetParameterAsText(1))
# res = int(arcpy.GetParameterAsText(2)) quality = str(arcpy.GetParameterAsText(3))
# path = os.path.join(pdf, name) if os.path.exists(path):
# os.remove(path) arcpy.mapping.ExportToPDF(mxd, path, "Page_Layout", resolution=res, image_quality=quality)