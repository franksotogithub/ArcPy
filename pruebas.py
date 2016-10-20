import arcpy
import  SolucionInicialUrbano as s
import SolucionVecinaUrbano as v
import  CalculoFuncionObjetivo2 as funcionObjetivo
import ActualizarAEU as a
import AgrupacionPrueba as prueba
import numpy as np

fc = "D:/ShapesPruebasSegmentacionUrbana/Zones/Shape021806005000012.shp"


manzanas = s.Manzanas_menores_16(fc)[:]

matriz = np.array(manzanas)
print "MANZANAS"
print matriz
manzanas1 = manzanas[:]
componentes = s.Componentes_conexas(manzanas1)[:]
matriz2 =np.array(componentes)
print "COMPONENTES"
print matriz2