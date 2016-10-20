import arcpy
import os
import shutil
import sys


def EtiquetaZona(zona):
    rango_equivalencia=[[1,'A'],[2,'B'],[3,'C'],[4,'D'],[5,'E'],[6,'F'],[7,'G'],[8,'H'],[9,'I'],[10,'J'],[11,'K'],[12,'L'],[13,'M'],[14,'N'],[15,'O'],[16,'P'],[17,'Q']]

    #zona='001001'

    zona_temp=zona[0:3]
    zona_int=int(zona[3:])
    zona_int_eq=""
    # busacar equivalencia
    for el in rango_equivalencia:
        if (el[0]==zona_int):
            zona_int_eq=el[1]

    zona_temp=zona_temp+str(zona_int_eq)

    return zona_temp

print EtiquetaZona('001001')
