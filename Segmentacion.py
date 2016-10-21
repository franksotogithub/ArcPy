import  SegmTabAEU
import  SegmTabSeccion
import  SegmTabExportarCroquis as CroquisTabular
import  SegmEspAEU
import SegmEspSeccion
import SegmEspExportarCroquis as CroquisEsp
import  datetime
import  ConectionSQL as conx
import  ImportarExportarSQL as ie
from datetime import *


def Importar_Tablas(ubigeos):
    print datetime.today()
    conx.ActualizarCantViviendasMzs()
    print "ActualizarCantViviendasMzs"
    print datetime.today()
    SegmEspAEU.ImportarTablasTrabajo(ubigeos)
    print "ImportarTablasTrabajo"
    print datetime.today()

def SegmentacionEspacial(ubigeos):
    Ruta = "D:\ShapesPruebasSegmentacionUrbana\AEU\MatrizAdyacencia"
    Lista_adyacencia = "lista_adyacencia.dbf"
    print datetime.today()
    SegmEspAEU.CrearMatrizAdyacencia(ubigeos)
    print "CrearMatrizAdyacencia"
    print datetime.today()

    SegmEspAEU.ExportarTablasAdyacencia()
    print "ExportarTablasAdyacencia"
    print datetime.today()

    conx.InsertarAdyacencia()
    print "InsertarAdyacencia"
    print datetime.today()
    ie.Importar_Lista_ADYACENCIA(Ruta, Lista_adyacencia)
    print "ImportarAdyacencia"
    print datetime.today()
    SegmEspAEU.CrearViviendasOrdenadas()
    print "CrearViviendasOrdenadas"
    print datetime.today()
    SegmEspAEU.EnumerarAEUEnViviendasDeManzanasCantVivMayores16(ubigeos)
    print "EnumerarAEUEnViviendasDeManzanasCantVivMayores16"
    print datetime.today()
    SegmEspAEU.AgruparManzanasCantVivMenoresIguales16(ubigeos)
    print "AgruparManzanasCantVivMenoresIguales16"
    print datetime.today()
    SegmEspAEU.EnumerarAEUEnViviendasDeManzanasCantVivMenoresIguales16(ubigeos)
    print "EnumerarAEUEnViviendasDeManzanasCantVivMenoresIguales16"
    print datetime.today()
    SegmEspAEU.CrearMZS_AEU(ubigeos)
    print "CrearMZS_AEU"
    print datetime.today()
    SegmEspAEU.CrearRutasPreparacion()
    print "CrearRutasPreparacion"
    print datetime.today()
    SegmEspAEU.PrimeraViviendaPorAEU()
    print "PrimeraViviendaPorAEU"
    print datetime.today()
    SegmEspAEU.SegundaViviendaPorAEU()
    print "SegundaViviendaPorAEU"
    print datetime.today()

    SegmEspAEU.RelacionarRutasLineasConAEUSegundaVivienda()
    print "RelacionarRutasLineasConAEUSegundaVivienda"
    print datetime.today()

    SegmEspAEU.ActualizarRutasViviendasMenoresIguales16()
    print "ActualizarRutasViviendasMenoresIguales16"
    print datetime.today()

    SegmEspAEU.CrearLineasAEUFinal()
    print "CrearLineasAEUFinal"
    print datetime.today()

    SegmEspAEU.CrearTablaSegundaPasada()
    print "CrearTablaSegundaPasada"
    print datetime.today()

    SegmEspAEU.ActualizarRutasAEUSegundaPasada()
    print "ActualizarRutasAEUSegundaPasada"
    print datetime.today()

    SegmEspAEU.Renumerar_AEU(ubigeos)
    print "Renumerar_AEU"
    print datetime.today()

    SegmEspAEU.RenumerarRutas()
    print "RenumerarRutas"
    print datetime.today()

    SegmEspAEU.CrearTB_AEUS()
    print "CrearTB_AEUS"
    print datetime.today()

    SegmEspAEU.CrearMarcosCroquis(ubigeos)
    print "CrearMarcosCroquis"
    print datetime.today()

    SegmEspSeccion.EnumerarSecciones(ubigeos)
    print "EnumerarSecciones"
    print datetime.today()

    SegmEspSeccion.CrearSecciones(ubigeos)
    print "CrearSecciones"
    print datetime.today()

    SegmEspSeccion.CrearMarcosSecciones()
    print "CrearMarcosSecciones"
    print datetime.today()
    SegmEspAEU.ModelarTablas(ubigeos)
    print "ModelarTablas"
    print datetime.today()

    conx.LimpiarRegistrosSegmentacionEspUbigeo(ubigeos)
    print "LimpiarRegistros"
    print datetime.today()
    SegmEspAEU.InsertarRegistros(ubigeos)
    print "InsertarRegistros"
    print datetime.today()
    conx.ActualizarEstadoAEUSegmEsp(ubigeos)
    print "ActualizarEstadoAEUSegmEsp"
    print datetime.today()

def SegmentacionTabular(ubigeos):
    print datetime.today()
    SegmTabAEU.CopiarTablas()
    print "CopiarTablas"
    print datetime.today()
    SegmTabAEU.OrdenarManzanasFalsoCod()
    print "OrdenarManzanasFalsoCod"
    print datetime.today()
    SegmTabAEU.CrearViviendasOrdenadas()
    print "CrearViviendasOrdenadas"
    print datetime.today()
    SegmTabAEU.EnumerarAEUEnViviendasDeManzanas(ubigeos)
    print "EnumerarAEUEnViviendasDeManzanas"
    print datetime.today()
    SegmTabAEU.CrearMZS_AEU(ubigeos)
    print "CrearMZS_AEU"
    print datetime.today()#

    SegmTabAEU.RenumerarViviendasMzsMenores16(ubigeos)
    print "RenumerarViviendasMzsMenores16"
    print datetime.today()  #

    SegmTabAEU.CrearRutasPreparacion(ubigeos)
    print "CrearRutasPreparacion"
    print datetime.today()
    SegmTabAEU.PrimeraViviendaPorAEU()
    print "PrimeraViviendaPorAEU"
    print datetime.today()
    SegmTabAEU.SegundaViviendaPorAEU()
    print "SegundaViviendaPorAEU"
    print datetime.today()
    SegmTabAEU.RelacionarRutasLineasConAEUSegundaVivienda()
    print "RelacionarRutasLineasConAEUSegundaVivienda"
    print datetime.today()
    SegmTabAEU.ActualizarRutasViviendasMenoresIguales16()
    print "ActualizarRutasViviendasMenoresIguales16"
    print datetime.today()
    SegmTabAEU.CrearLineasAEUFinal()
    print "CrearLineasAEUFinal"
    print datetime.today()
    SegmTabAEU.CrearTB_AEUS()
    print "CrearTB_AEUS"
    print datetime.today()
    SegmTabAEU.CrearMarcosCroquis(ubigeos)
    print "CrearMarcosCroquis"
    print datetime.today()
    SegmTabSeccion.EnumerarSecciones(ubigeos)
    print "EnumerarSecciones"
    print datetime.today()
    SegmTabSeccion.CrearSecciones(ubigeos)
    print "CrearSecciones"
    print datetime.today()
    SegmTabSeccion.CrearMarcosSecciones()
    print "CrearMarcosSecciones"
    print datetime.today()
    SegmTabAEU.ModelarTablas(ubigeos)
    print "ModelarTablas"
    print datetime.today()
    conx.LimpiarRegistrosSegmentacionTabularUbigeo(ubigeos)
    print "LimpiarRegistros"
    print datetime.today()
    SegmTabAEU.InsertarRegistros(ubigeos)
    print "InsertarRegistros"
    print datetime.today()
    conx.ActualizarEstadoAEUSegmTab(ubigeos)
    print "ActualizarEstadoAEUSegmTab"
    print datetime.today()

def ExportarSegmTab(ubigeos):
    for ubigeo in ubigeos:
        CroquisTabular.CrearCarpetasCroquisSegmTab([ubigeo])
        CroquisTabular.ExportarCroquisUrbanoAEU([ubigeo])
        CroquisTabular.ExportarCroquisUrbanoSeccion([ubigeo])
        CroquisTabular.ExportarCroquisUrbanoZona([ubigeo])
def ExportarSegmEsp(ubigeos):
    for ubigeo in ubigeos:
        CroquisEsp.CrearCarpetasCroquisSegmEsp([ubigeo])
        CroquisEsp.ExportarCroquisUrbanoAEU([ubigeo])
        CroquisEsp.ExportarCroquisUrbanoSeccion([ubigeo])
        CroquisEsp.ExportarCroquisUrbanoZona([ubigeo])









#ubigeos=["030602",
#"050507",
#"050601",
#"050617"
# ]
#
#
#Importar_#Tablas(ubigeos)
#SegmentacionEspacial(ubigeos)
#SegmentacionTabular(ubigeos)
#
#ubigeos=["030602",
#"050507",
#"050601",
#"050617"
# ]
#ExportarSegmEsp(ubigeos)
#ExportarSegmTab(ubigeos)




#ubigeos=["020601"]
#SegmEspAEU.EnumerarAEUEnViviendasDeManzanasCantVivMenoresIguales16(ubigeos)


#ubigeos=["020601","021509"]
#SegmTabAEU.CrearViviendasOrdenadas()
#SegmTabAEU.EnumerarAEUEnViviendasDeManzanas(ubigeos)

#SegmEspAEU.PrimeraPuertaPorAEU()
#SegmEspAEU.RelacionarRutasLineasConAEUSegundaVivienda()
#
#ubigeos=["020601",
#"021509",
#"021806",
#"022001"
# ]
#
#
#SegmEspAEU.CrearRutasPreparacion()
#SegmEspAEU.RelacionarRutasLineasConAEUSegundaVivienda()
#SegmEspAEU.RelacionarRutasLineasConAEUPrimeraPuerta()


