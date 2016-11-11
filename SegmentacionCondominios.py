import  SegmTabAEUCondominios
#import  SegmTabSeccion
#import  SegmTabExportarCroquis as CroquisTabular
import  SegmEspAEUCondominios
import  datetime
import  ConectionSQL as conx
import  ImportarExportarSQL as ie
from datetime import *
import UBIGEO


def Importar_Tablas(data,campos):
    conx.ActualizarCantViviendasMzsCondominios(data)
    print datetime.today()
    conx.ActualizarCampoMzCondominio(data)
    SegmEspAEUCondominios.ImportarTablasTrabajo(data,campos)
    print "ImportarTablasTrabajo"
    print datetime.today()


def SegmentacionEspacial(data,campos):
    where_expresion=UBIGEO.Expresion(data,campos)
    Ruta = "D:\ShapesPruebasSegmentacionUrbanaCondominios\AEU\MatrizAdyacencia"
    Lista_adyacencia = "lista_adyacencia.dbf"

    SegmEspAEUCondominios.CrearMatrizAdyacencia(where_expresion)
    print "CrearMatrizAdyacencia"
    print datetime.today()
    ##
    SegmEspAEUCondominios.ExportarTablasAdyacencia()
    print "ExportarTablasAdyacencia"
    print datetime.today()

    conx.InsertarAdyacencia()
    print "InsertarAdyacencia"
    print datetime.today()
    ie.Importar_Lista_ADYACENCIA(Ruta, Lista_adyacencia)
    print "ImportarAdyacencia"
    print datetime.today()
    #
    SegmEspAEUCondominios.CrearViviendasOrdenadas()
    print "CrearViviendasOrdenadas"
    print datetime.today()
    SegmEspAEUCondominios.EnumerarAEUEnViviendasDeManzanasCantVivMayores16(where_expresion)
    print "EnumerarAEUEnViviendasDeManzanasCantVivMayores16"
    print datetime.today()
    SegmEspAEUCondominios.AgruparManzanasCantVivMenoresIguales16(where_expresion)
    print "AgruparManzanasCantVivMenoresIguales16"
    print datetime.today()
    SegmEspAEUCondominios.EnumerarAEUEnViviendasDeManzanasCantVivMenoresIguales16(where_expresion)
    print "EnumerarAEUEnViviendasDeManzanasCantVivMenoresIguales16"
    print datetime.today()
    SegmEspAEUCondominios.CrearMZS_AEU(where_expresion)
    print "CrearMZS_AEU"
    print datetime.today()
    ##
    SegmEspAEUCondominios.CrearRutasPuntos()
    print "CrearRutasPuntos"
    print datetime.today()
    SegmEspAEUCondominios.CrearViviendasCortes()
    print "CrearViviendasCortes"
    print datetime.today()
    SegmEspAEUCondominios.CrearRutasPreparacion()
    print "CrearRutasPreparacion"
    print datetime.today()
    SegmEspAEUCondominios.RelacionarVerticeFinalInicioConAEUMax()
    print "RelacionarVerticeFinalInicioConAEUMax"
    print datetime.today()
    SegmEspAEUCondominios.RelacionarRutasLineasConAEU()
    print "RelacionarRutasLineasConAEU"
    print datetime.today()
    SegmEspAEUCondominios.CrearTablaSegundaPasada()
    print "CrearTablaSegundaPasada"
    print datetime.today()
    ####
    ###
    SegmEspAEUCondominios.ActualizarRutasAEUSegundaPasada()
    print "ActualizarRutasAEUSegundaPasada"
    print datetime.today()
    #####
    ####
    SegmEspAEUCondominios.Renumerar_AEU(where_expresion)
    print "Renumerar_AEU"
    print datetime.today()
    #####
    SegmEspAEUCondominios.RenumerarRutas()
    print "RenumerarRutas"
    print datetime.today()
    ###
    ###
    SegmEspAEUCondominios.CrearTB_AEUS()
    print "CrearTB_AEUS"
    print datetime.today()
    ###
    SegmEspAEUCondominios.EnumerarSecciones(where_expresion)
    print "EnumerarSecciones"
    print datetime.today()
    SegmEspAEUCondominios.CrearSecciones(where_expresion)
    print "CrearSecciones"
    SegmEspAEUCondominios.ModelarTablas(where_expresion)
    print "ModelarTablas"
    conx.LimpiarRegistrosSegmentacionEspUbigeo(data)
    print "LimpiarRegistrosSegmentacionEspUbigeo"
    SegmEspAEUCondominios.InsertarRegistros(data)
    print "InsertarRegistros"
    conx.ActualizarEstadoAEUSegmEsp(data)
    print "ActualizarEstadoAEUSegmEsp"
    # print datetime.today()
    SegmEspAEUCondominios.CrearRutasMultipart()
    print "CrearRutasMultipart"
    print datetime.today()

def SegmentacionTabular(data,campos):
    where_expresion=UBIGEO.Expresion(data,campos)
    print datetime.today()
    SegmTabAEUCondominios.CopiarTablas()
    print "CopiarTablas"
    print datetime.today()
    SegmTabAEUCondominios.OrdenarManzanasFalsoCod()
    print "OrdenarManzanasFalsoCod"
    print datetime.today()
    SegmTabAEUCondominios.CrearViviendasOrdenadas()
    print "CrearViviendasOrdenadas"
    print datetime.today()
    SegmTabAEUCondominios.EnumerarAEUEnViviendasDeManzanas(where_expresion)
    print "EnumerarAEUEnViviendasDeManzanas"
    print datetime.today()
    SegmTabAEUCondominios.CrearMZS_AEU(where_expresion)
    print "CrearMZS_AEU"
    print datetime.today()#
    SegmTabAEUCondominios.RenumerarViviendasMzsMenores16(where_expresion)
    print "RenumerarViviendasMzsMenores16"
    print datetime.today()  #
    SegmTabAEUCondominios.CrearRutasPuntos()
    print "CrearRutasPuntos"
    print datetime.today()  #
    SegmTabAEUCondominios.CrearRutasPreparacion()
    print "CrearRutasPreparacion"
    print datetime.today()  #
    SegmTabAEUCondominios.RelacionarVerticeFinalInicioConAEUMax()
    print "RelacionarVerticeFinalInicioConAEUMax"
    print datetime.today()  #
    SegmTabAEUCondominios.RelacionarRutasLineasConAEU()
    print "CrearRutasPreparacion"
    print datetime.today()  #
    SegmTabAEUCondominios.CrearTB_AEUS()
    print "CrearTB_AEUS"
    print datetime.today()  #
    SegmTabAEUCondominios.EnumerarSecciones(where_expresion)
    print "EnumerarSecciones"
    print datetime.today()  #
    SegmTabAEUCondominios.CrearSecciones(where_expresion)
    print "EnumerarSecciones"
    print datetime.today()  #
    SegmTabAEUCondominios.CrearRutasMultipart()
    print "CrearRutasMultipart"
    print datetime.today()  #
    SegmTabAEUCondominios.ModelarTablas(where_expresion)
    print "ModelarTablas"
    print datetime.today()  #
    conx.LimpiarRegistrosSegmentacionTabularUbigeo(where_expresion)
    SegmTabAEUCondominios.InsertarRegistros(where_expresion)
    print "InsertarRegistros"
    print datetime.today()  #

def ExportarSegmEsp(data,campos):
    SegmEspAEUCondominios.CrearCarpetas(data,campos)
    where_expression = UBIGEO.Expresion(data, campos)
    SegmEspAEUCondominios.ExportarCroquisUrbanoAEU(where_expression)
    SegmEspAEUCondominios.ExportarCroquisUrbanoSeccion(where_expression)
    SegmTabAEUCondominios.ExportarCroquisUrbanoZona(where_expression)

def ExportarSegmTab(data,campos):
    SegmTabAEUCondominios.CrearCarpetas(data,campos)
    where_expression = UBIGEO.Expresion(data, campos)
    SegmTabAEUCondominios.ExportarCroquisUrbanoAEU(where_expression)
    SegmTabAEUCondominios.ExportarCroquisUrbanoSeccion(where_expression)
    SegmTabAEUCondominios.ExportarCroquisUrbanoZona(where_expression)











