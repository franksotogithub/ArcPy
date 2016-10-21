
import SegmEspAEU as AEU
import SegmEspSeccion as Seccion

import arcpy
import  SolucionInicialUrbano as s
from arcpy import env
import ActualizarAEU as a
import  SegmEspExportarCroquis as Croquis
import  threading

import ImportarExportarSQL as ie
import  UBIGEO
import EliminarAdyacencias
import ConectionSQL as conx
from datetime import *

Ruta="D:\ShapesPruebasSegmentacionUrbana\AEU\MatrizAdyacencia"
Lista_adyacencia="lista_adyacencia.dbf"

ubigeos=["020601",
"021509",
"021806",
"022001"
]
#



conx.ActualizarCantViviendasMzs()
print "ActualizarCantViviendasMzs"
print datetime.today()
AEU.ImportarTablasTrabajo(ubigeos)
print "ImportarTablasTrabajo"
print datetime.today()
AEU.CrearMatrizAdyacencia(ubigeos)
print "CrearMatrizAdyacencia"
print datetime.today()
conx.InsertarAdyacencia()
print "InsertarAdyacencia"
print datetime.today()
ie.Importar_Lista_ADYACENCIA(Ruta,Lista_adyacencia)
print "ImportarAdyacencia"
print datetime.today()

AEU.CrearViviendasOrdenadas()
print "CrearViviendasOrdenadas"
print datetime.today()
AEU.EnumerarAEUEnViviendasDeManzanasCantVivMayores16(ubigeos)
print "EnumerarAEUEnViviendasDeManzanasCantVivMayores16"
print datetime.today()
AEU.AgruparManzanasCantVivMenoresIguales16(ubigeos)
print "AgruparManzanasCantVivMenoresIguales16"
print datetime.today()
AEU.EnumerarAEUEnViviendasDeManzanasCantVivMenoresIguales16(ubigeos)
print "EnumerarAEUEnViviendasDeManzanasCantVivMenoresIguales16"
print datetime.today()



AEU.CrearMZS_AEU(ubigeos)
print "CrearMZS_AEU"
print datetime.today()

AEU.CrearRutasPreparacion()
print "CrearRutasPreparacion"
print datetime.today()
AEU.PrimeraViviendaPorAEU()
print "PrimeraViviendaPorAEU"
print datetime.today()
AEU.SegundaViviendaPorAEU()
print "SegundaViviendaPorAEU"
print datetime.today()


AEU.RelacionarRutasLineasConAEUSegundaVivienda()
print "RelacionarRutasLineasConAEUSegundaVivienda"
print datetime.today()


AEU.ActualizarRutasViviendasMenoresIguales16()
print "ActualizarRutasViviendasMenoresIguales16"
print datetime.today()


AEU.CrearLineasAEUFinal()
print "CrearLineasAEUFinal"
print datetime.today()


AEU.CrearTablaSegundaPasada()
print "CrearTablaSegundaPasada"
print datetime.today()

AEU.ActualizarRutasAEUSegundaPasada()
print "ActualizarRutasAEUSegundaPasada"
print datetime.today()

ubigeos=["021509","022001","030602","050601"]
print datetime.today()
AEU.Renumerar_AEU(ubigeos)
print "Renumerar_AEU"
print datetime.today()

AEU.RenumerarRutas()
print "RenumerarRutas"
print datetime.today()
AEU.CrearTB_AEUS()
print "CrearTB_AEUS"
print datetime.today()


#ubigeos=["090208",
#"150407",
#"080407",
#"090301",
#"150705",
#"150604",
#"080302"]
#
#ubigeos = [
#    #"090208",
#    #"150407",
#    #"021509",
#    #"030602",
#    #"050601",
#    #"080407",
#    #"090301",
#    #"150705",
#    "050619",
#    #"150604",
#    #"022001",
#    #"050617",
#    #"080302"
#]
#
#print datetime.today()
#


AEU.CrearMarcosCroquis(ubigeos)
print "CrearMarcosCroquis"
print datetime.today()


print datetime.today()
#
#ubigeos=["090208",
#"150407",
#"021509",
#"030602",
#"050601",
#"080407",
#"090301",
#"150705",
#"050619",
#"150604",
#"022001",
#"050617",
#"080302"]
#
#
#Seccion.EnumerarSecciones(ubigeos)
#print "EnumerarSecciones"
#print datetime.today()

#Seccion.CrearSecciones(ubigeos)
#print "CrearSecciones"
#print datetime.today()
##
##
#Seccion.CrearMarcosSecciones()
#print "CrearMarcosSecciones"
#print datetime.today()
#AEU.ModelarTablas(ubigeos)
#print "ModelarTablas"
#print datetime.today()


#ubigeos=[
#"021509",
#"022001",
#"030602",
#"050601",
#]

conx.LimpiarRegistrosSegmentacionEspUbigeo(ubigeos)
print "LimpiarRegistros"
print datetime.today()
AEU.InsertarRegistros(ubigeos)
print "InsertarRegistros"
print datetime.today()
conx.ActualizarEstadoAEUSegmEsp(ubigeos)
print "ActualizarEstadoAEUSegmEsp"
print datetime.today()


Croquis.CrearCarpetasCroquisSegmEsp(ubigeos)
print "CrearCarpetas"
#ubigeos=[
#"021806",
#"022001"
#]
#
#Croquis.Exportar_Croquis_Urbano_AEU(ubigeos)
#print "Exportar_Croquis_Urbano_AEU"
#ubigeos=["020601",
#"021509",
#"021806",
#"022001"
#]
#
#Croquis.Exportar_Croquis_Urbano_Seccion(ubigeos)
#print "Exportar_Croquis_Urbano_Seccion"
#ubigeos=["020601",
#"021509",
#"021806",
#"022001"
#]
#Croquis.Exportar_Croquis_Urbano_Zona(ubigeos)
#print "Exportar_Croquis_Urbano_Zona"

#
#
#ubigeos=[
#"090208",
#"150407",
#"021509",
#"030602",
#"050601",
#"080407",
#"090301",
#"150705",
#"050619",
#"150604",
#"022001",
#"050617",
#"080302"
#]
#
#
#ubigeos=[#"021509","022001",
#         "030602","050601"]
#
#for el in ubigeos:
#    ubigeo=[el]
#    print ubigeo
#    Croquis.Exportar_Croquis_Urbano_AEU(ubigeo)
#    print "ExportarCroquisUrbanoAEU"
#    print datetime.today()
#
#    Croquis.Exportar_Croquis_Urbano_Seccion(ubigeo)
#
#    print "ExportarCroquisUrbanoSeccion"
#    print datetime.today()
#
#    Croquis.Exportar_Croquis_Urbano_Zona(ubigeo)
#    print "ExportarCroquisUrbanoZona"
#    print datetime.today()
#
#
#
