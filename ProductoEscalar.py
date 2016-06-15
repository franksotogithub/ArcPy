import arcpy
import numpy as np

arcpy.env.workspace = r"D:/ArcGisShapesPruebas/"

desc="Shape07010100100.shp"
fc="D:/ArcGisShapesPruebas/Intersections/"+desc
fields=['FirstX_1','FirstY_1','LastX_1','LastY_1','FirstX_2','FirstY_2','LastX_2','LastY_2','FID']
#a=np.array([2, 4, 6, 8])
#b = np.array([2, 4, 6, 8])

j=0
with arcpy.arcpy.da.UpdateCursor(fc, fields) as cursor:
    for row in cursor:
        a1=row[0]-row[2] #ax
        a2=row[1]-row[3] #ay  a=(a1,a2)
        b1=row[4]-row[6] #bx
        b2=row[5]-row[7]  # bx b =(b1,b2)

        a = np.array([a1, a2])
        b = np.array([b1, b2])

        producto_escalar = np.dot(a,b)  # a.b=a1*b1 + a2*b2
        coseno=abs(producto_escalar)/(np.linalg.norm(a)*np.linalg.norm(b))

        #print  str(row[8])+":"+str(coseno)

        if (j % 2)==1:
            cursor.deleteRow()

        if coseno>=0.005:
            cursor.deleteRow()


        j=j+1
        print j
