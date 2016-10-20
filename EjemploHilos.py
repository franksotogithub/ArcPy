import threading
import  SegmEspExportarCroquis as Croquis


def worker(ubigeo):
    """funcion que realiza el trabajo en el thread"""
    #print ubigeo
    Croquis.Exportar_Croquis_Urbano_AEU([str(ubigeo)])
    return



threads = list()

ubigeos=[
#"020601",
#"021509",
#"021806",
"022001"
]

for ubigeo in ubigeos:
    t = threading.Thread(target=worker,args=(ubigeo,))
    threads.append(t)
    t.start()