#import  SegmTabAEUCondominios
#import  SegmTabSeccion
#import  SegmTabExportarCroquis as CroquisTabular
import  SegmEspAEUCondominios
import SegmEspSeccionCondominios
import SegmEspExportarCroquisCondominios as CroquisEsp
import  datetime
import  ConectionSQL as conx
import  ImportarExportarSQL as ie
from datetime import *
import UBIGEO

def Importar_Tablas(ubigeos):



    #conx.ActualizarCantViviendasMzs(ubigeos)
    #conx.ActualizarCantViviendasMzsCondominios(ubigeos)
    #print datetime.today()
    #print "ActualizarCantViviendasMzs"
    #print datetime.today()
    #conx.ActualizarCampoMzCondominio(ubigeos)
    SegmEspAEUCondominios.ImportarTablasTrabajo(ubigeos)
    print "ImportarTablasTrabajo"
    print datetime.today()


def SegmentacionEspacial(ubigeos):
    Ruta = "D:\ShapesPruebasSegmentacionUrbanaCondominios\AEU\MatrizAdyacencia"
    Lista_adyacencia = "lista_adyacencia.dbf"
    print datetime.today()
    SegmEspAEUCondominios.CrearMatrizAdyacencia(ubigeos)
    print "CrearMatrizAdyacencia"
    print datetime.today()

    SegmEspAEUCondominios.ExportarTablasAdyacencia()
    print "ExportarTablasAdyacencia"
    print datetime.today()

    conx.InsertarAdyacencia()
    print "InsertarAdyacencia"
    print datetime.today()
    ie.Importar_Lista_ADYACENCIA(Ruta, Lista_adyacencia)
    print "ImportarAdyacencia"
    print datetime.today()
    SegmEspAEUCondominios.CrearViviendasOrdenadas()
    print "CrearViviendasOrdenadas"
    print datetime.today()
    SegmEspAEUCondominios.EnumerarAEUEnViviendasDeManzanasCantVivMayores16(ubigeos)
    print "EnumerarAEUEnViviendasDeManzanasCantVivMayores16"
    print datetime.today()
    SegmEspAEUCondominios.AgruparManzanasCantVivMenoresIguales16(ubigeos)
    print "AgruparManzanasCantVivMenoresIguales16"
    print datetime.today()
    SegmEspAEUCondominios.EnumerarAEUEnViviendasDeManzanasCantVivMenoresIguales16(ubigeos)
    print "EnumerarAEUEnViviendasDeManzanasCantVivMenoresIguales16"
    print datetime.today()
    SegmEspAEUCondominios.CrearMZS_AEU(ubigeos)
    print "CrearMZS_AEU"
    print datetime.today()
    SegmEspAEUCondominios.CrearRutasPreparacion()
    print "CrearRutasPreparacion"
    print datetime.today()
    SegmEspAEUCondominios.PrimeraViviendaPorAEU()
    print "PrimeraViviendaPorAEU"
    print datetime.today()
    SegmEspAEUCondominios.SegundaViviendaPorAEU()
    print "SegundaViviendaPorAEU"
    print datetime.today()

    SegmEspAEUCondominios.RelacionarRutasLineasConAEUSegundaVivienda()
    print "RelacionarRutasLineasConAEUSegundaVivienda"
    print datetime.today()

    SegmEspAEUCondominios.ActualizarRutasViviendasMenoresIguales16()
    print "ActualizarRutasViviendasMenoresIguales16"
    print datetime.today()

    SegmEspAEUCondominios.CrearLineasAEUFinal()
    print "CrearLineasAEUFinal"
    print datetime.today()

    SegmEspAEUCondominios.CrearTablaSegundaPasada()
    print "CrearTablaSegundaPasada"
    print datetime.today()

    SegmEspAEUCondominios.ActualizarRutasAEUSegundaPasada()
    print "ActualizarRutasAEUSegundaPasada"
    print datetime.today()

    SegmEspAEUCondominios.Renumerar_AEU(ubigeos)
    print "Renumerar_AEU"
    print datetime.today()

    SegmEspAEUCondominios.RenumerarRutas()
    print "RenumerarRutas"
    print datetime.today()

    SegmEspAEUCondominios.CrearTB_AEUS()
    print "CrearTB_AEUS"
    print datetime.today()

    SegmEspAEUCondominios.CrearMarcosCroquis(ubigeos)
    print "CrearMarcosCroquis"
    print datetime.today()

    SegmEspSeccionCondominios.EnumerarSecciones(ubigeos)
    print "EnumerarSecciones"
    print datetime.today()

    SegmEspSeccionCondominios.CrearSecciones(ubigeos)
    print "CrearSecciones"
    print datetime.today()

    SegmEspSeccionCondominios.CrearMarcosSecciones()
    print "CrearMarcosSecciones"
    print datetime.today()
    SegmEspAEUCondominios.ModelarTablas(ubigeos)
    print "ModelarTablas"
    print datetime.today()

    conx.LimpiarRegistrosSegmentacionEspUbigeo(ubigeos)
    print "LimpiarRegistros"
    print datetime.today()
    SegmEspAEUCondominios.InsertarRegistros(ubigeos)
    print "InsertarRegistros"
    print datetime.today()
    conx.ActualizarEstadoAEUSegmEsp(ubigeos)
    print "ActualizarEstadoAEUSegmEsp"
    print datetime.today()



#def SegmentacionTabular(ubigeos):
#    print datetime.today()
#    SegmTabAEU.CopiarTablas()
#    print "CopiarTablas"
#    print datetime.today()
#    SegmTabAEU.OrdenarManzanasFalsoCod()
#    print "OrdenarManzanasFalsoCod"
#    print datetime.today()
#    SegmTabAEU.CrearViviendasOrdenadas()
#    print "CrearViviendasOrdenadas"
#    print datetime.today()
#    SegmTabAEU.EnumerarAEUEnViviendasDeManzanas(ubigeos)
#    print "EnumerarAEUEnViviendasDeManzanas"
#    print datetime.today()
#    SegmTabAEU.CrearMZS_AEU(ubigeos)
#    print "CrearMZS_AEU"
#    print datetime.today()#
#
#    SegmTabAEU.RenumerarViviendasMzsMenores16(ubigeos)
#    print "RenumerarViviendasMzsMenores16"
#    print datetime.today()  #
#
#    SegmTabAEU.CrearRutasPreparacion(ubigeos)
#    print "CrearRutasPreparacion"
#    print datetime.today()
#    SegmTabAEU.PrimeraViviendaPorAEU()
#    print "PrimeraViviendaPorAEU"
#    print datetime.today()
#    SegmTabAEU.SegundaViviendaPorAEU()
#    print "SegundaViviendaPorAEU"
#    print datetime.today()
#    SegmTabAEU.RelacionarRutasLineasConAEUSegundaVivienda()
#    print "RelacionarRutasLineasConAEUSegundaVivienda"
#    print datetime.today()
#    SegmTabAEU.ActualizarRutasViviendasMenoresIguales16()
#    print "ActualizarRutasViviendasMenoresIguales16"
#    print datetime.today()
#    SegmTabAEU.CrearLineasAEUFinal()
#    print "CrearLineasAEUFinal"
#    print datetime.today()
#    SegmTabAEU.CrearTB_AEUS()
#    print "CrearTB_AEUS"
#    print datetime.today()
#    SegmTabAEU.CrearMarcosCroquis(ubigeos)
#    print "CrearMarcosCroquis"
#    print datetime.today()
#    SegmTabSeccion.EnumerarSecciones(ubigeos)
#    print "EnumerarSecciones"
#    print datetime.today()
#    SegmTabSeccion.CrearSecciones(ubigeos)
#    print "CrearSecciones"
#    print datetime.today()
#    SegmTabSeccion.CrearMarcosSecciones()
#    print "CrearMarcosSecciones"
#    print datetime.today()
#    SegmTabAEU.ModelarTablas(ubigeos)
#    print "ModelarTablas"
#    print datetime.today()
#    conx.LimpiarRegistrosSegmentacionTabularUbigeo(ubigeos)
#    print "LimpiarRegistros"
#    print datetime.today()
#    SegmTabAEU.InsertarRegistros(ubigeos)
#    print "InsertarRegistros"
#    print datetime.today()
#    conx.ActualizarEstadoAEUSegmTab(ubigeos)
#    print "ActualizarEstadoAEUSegmTab"
#    print datetime.today()
#def ExportarSegmTab(ubigeos):
#    for ubigeo in ubigeos:
#        CroquisTabular.CrearCarpetasCroquisSegmTab([ubigeo])
#        CroquisTabular.ExportarCroquisUrbanoAEU([ubigeo])
#        CroquisTabular.ExportarCroquisUrbanoSeccion([ubigeo])
#        CroquisTabular.ExportarCroquisUrbanoZona([ubigeo])
def ExportarSegmEsp(ubigeos):
    for ubigeo in ubigeos:
        CroquisEsp.CrearCarpetasCroquisSegmEsp([ubigeo])
        CroquisEsp.ExportarCroquisUrbanoAEU([ubigeo])
        #CroquisEsp.ExportarCroquisUrbanoSeccion([ubigeo])
        #CroquisEsp.ExportarCroquisUrbanoZona([ubigeo])


ubigeos=["150116",
]


data=[
#['150116','00100'],
['150116','00200'],
['150116','00400'],
#['150116','00500'],
]
campos=['UBIGEO','ZONA']



#Importar_Tablas(ubigeos)
#Ruta = "D:\ShapesPruebasSegmentacionUrbanaCondominios\AEU\MatrizAdyacencia"
#Lista_adyacencia = "lista_adyacencia.dbf"
##print datetime.today()
#
#SegmEspAEUCondominios.CrearMatrizAdyacencia(ubigeos)
#print "CrearMatrizAdyacencia"
#print datetime.today()
#
#SegmEspAEUCondominios.ExportarTablasAdyacencia()
#print "ExportarTablasAdyacencia"
#print datetime.today()
###
#conx.InsertarAdyacencia()
#print "InsertarAdyacencia"
#print datetime.today()
#ie.Importar_Lista_ADYACENCIA(Ruta, Lista_adyacencia)
#print "ImportarAdyacencia"
#print datetime.today()
###
###
##
##
#SegmEspAEUCondominios.CrearViviendasOrdenadas()
#print "CrearViviendasOrdenadas"
#print datetime.today()
#SegmEspAEUCondominios.EnumerarAEUEnViviendasDeManzanasCantVivMayores16(ubigeos)
#print "EnumerarAEUEnViviendasDeManzanasCantVivMayores16"
#print datetime.today()
#SegmEspAEUCondominios.AgruparManzanasCantVivMenoresIguales16(ubigeos)
#print "AgruparManzanasCantVivMenoresIguales16"
#print datetime.today()
#SegmEspAEUCondominios.EnumerarAEUEnViviendasDeManzanasCantVivMenoresIguales16(ubigeos)
#print "EnumerarAEUEnViviendasDeManzanasCantVivMenoresIguales16"
#print datetime.today()
#SegmEspAEUCondominios.CrearMZS_AEU(ubigeos)
#print "CrearMZS_AEU"
#print datetime.today()
##
##
#SegmEspAEUCondominios.CrearRutasPuntos()
#print "CrearRutasPuntos"
#print datetime.today()
#SegmEspAEUCondominios.CrearViviendasCortes()
#print "CrearViviendasCortes"
#print datetime.today()
#SegmEspAEUCondominios.CrearRutasPreparacion()
#print "CrearRutasPreparacion"
#print datetime.today()
#SegmEspAEUCondominios.RelacionarVerticeFinalInicioConAEUMax()
#print "RelacionarVerticeFinalInicioConAEUMax"
#print datetime.today()
###
###
#SegmEspAEUCondominios.RelacionarRutasLineasConAEU()
#print "RelacionarRutasLineasConAEU"
#print datetime.today()
##
##
###
###
#SegmEspAEUCondominios.CrearTablaSegundaPasada()
#print "CrearTablaSegundaPasada"
#print datetime.today()
####
###
#SegmEspAEUCondominios.ActualizarRutasAEUSegundaPasada()
#print "ActualizarRutasAEUSegundaPasada"
#print datetime.today()
#####
####
#SegmEspAEUCondominios.Renumerar_AEU(ubigeos)
#print "Renumerar_AEU"
#print datetime.today()
#####
#SegmEspAEUCondominios.RenumerarRutas()
#print "RenumerarRutas"
#print datetime.today()
###
###
#SegmEspAEUCondominios.CrearTB_AEUS()
#print "CrearTB_AEUS"
#print datetime.today()
###
#SegmEspSeccionCondominios.EnumerarSecciones(ubigeos)
#print "EnumerarSecciones"
#print datetime.today()
###
###
#SegmEspAEUCondominios.CrearRutasMultipart()
####ExportarSegmEsp(ubigeos)
###
#SegmEspSeccionCondominios.CrearSecciones(ubigeos)
##
#SegmEspAEUCondominios.ModelarTablas(ubigeos)
#conx.LimpiarRegistrosSegmentacionEspUbigeo(ubigeos)
#

conx.LimpiarRegistrosSegmentacionEspUbigeo(ubigeos)

ubigeos=["150116"]
SegmEspAEUCondominios.InsertarRegistros(ubigeos)
print "InsertarRegistros"
conx.ActualizarEstadoAEUSegmEsp(ubigeos)
print "ActualizarEstadoAEUSegmEsp"
print datetime.today()



#data=[
#       # ['150116','00100'],
#       # ['150116','00200'],
#       # ['150116', '00400'],
#        ['150116', '00500'],
#]
#campos=['UBIGEO','ZONA']
#
#print UBIGEO.Expresion(data,campos)
#
#CroquisEsp.ExportarCroquisUrbanoAEU(UBIGEO.Expresion(data,campos))




#CroquisEsp.ExportarCroquisUrbanoSeccion(UBIGEO.Expresion(data,campos))

#CroquisEsp.ExportarCroquisUrbanoAEU(UBIGEO.Expresion(data,campos))

#CroquisEsp.ExportarCroquisUrbanoZona(UBIGEO.Expresion(data,campos))













