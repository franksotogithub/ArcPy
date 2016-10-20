import pyodbc

#def get_conexion():
#    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.200.250;DATABASE=CPV_SEGMENTACION;UID=sde;PWD=$deDEs4Rr0lLo')
#    return cnxn

def ejecutar():
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=192.168.200.250;DATABASE=CPV_SEGMENTACION;UID=sde;PWD=$deDEs4Rr0lLo')

    cursor = cnxn.cursor()
    cursor.execute("""

DELETE LISTA_ADYACENCIA

INSERT LISTA_ADYACENCIA
SELECT A.IDMANZANA_FIRST ,A.TOT_VIV_FIRST,A.AREA_FIRST,A.X_FIRST,A.Y_FIRST,B.IDMANZANA IDMANZANA_LAST,B.VIV_MZ TOT_VIV_LAST,B.AREA AREA_LAST,B.xCentroid X_LAST,B.yCentroid Y_LAST
FROM(
select b.*,a.IDMANZANA IDMANZANA_FIRST,a.VIV_MZ TOT_VIV_FIRST,a.AREA AREA_FIRST,a.xCentroid X_FIRST,a.yCentroid Y_FIRST
from (SELECT * FROM TB_MZS_TRABAJO   ) a
inner join ADYACENCIA  b on a.xCentroid=b.FirstX and a.yCentroid=b.FirstY
)a
inner join
(SELECT * FROM TB_MZS_TRABAJO )
 b on a.LastX=b.xCentroid and a.LastY=b.yCentroid


      """)



    cursor.commit()
    cursor2 = cnxn.cursor()
    cursor2.execute(
        """


delete LISTA_ADYACENCIA_POR_MANZANA
DECLARE @ID VARCHAR(20)


DECLARE TMP1 CURSOR
FOR SELECT DISTINCT A.IDMANZANA

FROM
(
SELECT DISTINCT IDMANZANA_FIRST IDMANZANA FROM LISTA_ADYACENCIA
UNION
SELECT DISTINCT IDMANZANA_LAST IDMANZANA FROM LISTA_ADYACENCIA
) AS A


OPEN TMP1

FETCH NEXT FROM TMP1
INTO @ID

WHILE @@FETCH_STATUS=0
BEGIN
 INSERT LISTA_ADYACENCIA_POR_MANZANA
 SELECT DISTINCT @ID,A.ID,A.VIV,A.AREA,A.X,A.Y
 FROM
 (
 SELECT DISTINCT IDMANZANA_LAST ID,TOT_VIV_LAST  VIV,AREA_LAST AREA,X_LAST X,Y_LAST Y FROM LISTA_ADYACENCIA WHERE  IDMANZANA_FIRST=@ID
 UNION
 SELECT DISTINCT IDMANZANA_FIRST ID,TOT_VIV_FIRST VIV,AREA_FIRST AREA,X_FIRST X,Y_FIRST Y FROM LISTA_ADYACENCIA WHERE  IDMANZANA_LAST=@ID
 )A
FETCH NEXT FROM TMP1
INTO @ID
END
CLOSE TMP1
DEALLOCATE TMP1
        """
    )
    cursor2.commit()
    #rows = cursor.fetchall()
    #return rows

ejecutar()
#datos_croquis=leer_datos_croquis_urbano_aeu(cxn)
#print  datos_croquis