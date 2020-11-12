import numpy as np
import pandas as pd


__author__ = "Efraín Antonio Domínguez Calle"
__copyright__ = "Efraín Antonio Domínguez Calle"
__credits__ = ["None"]
__license__ = "GNU GENERAL PUBLIC LICENSE"
__version__ = "2.0"
__maintainer__ = "Efraín Antonio Domínguez Calle"
__email__ = 'e.dominguez@javeriana.edu.co, edoc@mathmodelling.org'
__status__ = "En desarrollo"


# Curso de Hidroclimatología
# Versión del curso: Segundo semestre del 2020
# Los scripts están orientados a los datos de la CAR Resolución Mensual
# Pontificia Universidad Javeriana - Facultad de Estudios Ambientales y Rurales
# Departamento de Ecología y Territorio
# El script es sólo para uso académico de los estudiantes del curso

# Este script aplica la prueba de Rachas a datos hidrometeorológicos descargados de la CAR
# Para aplicarlo se debe leer el archivo de Excel que resulta de aplicar el script 03_Complementar_Promedio
# El archivo de salida contiene una tabla de resultados explicando que meses se pueden considerar o no
# grupos aleatorios para la variable analizada. Se guarda una tabla por pestaña, la pestaña identifica a la estación


def evaluar_rachas(xls_in, xls_out):
    """Esta función nos permite evaluar la aleatoriedad de conjuntos estadisticos dispuestos por columnas
    en una pestaña de Excel. Si el libro de Excel al que apunta xls_in tiene varias pestañas, todas son evaluadas
    Parámetros:
    xls_in: Una cadena de carácteres especificando la ruta a un Excel que contiene la información a evaluar dispuesta
    por columnas
    xls_out: Una cadena de carácteres especificando la ruta en la que se guarda el Excel con los resultados de
    Aleatoriedad"""

    # Pasos preparativos:

    # Leemos el libro de Excel
    libro = pd.ExcelFile(xls_in)
    # Establecemos la lista de pestañas y leemos cada una de ellas en un ciclo
    pestanas = libro.sheet_names
    print(pestanas)

    # Dataframe para guardar los resultados
    Rachas_Test = pd.DataFrame()
    Resumen_Rachas = pd.DataFrame()
    # Libro para guardar resultado de la prueba de Rachas
    libro = pd.ExcelWriter(xls_out)

    # Paso 1: Ciclo de lectura de datos por pestañas y aplicación prueba de rachas
    for p in pestanas:
        print('Trabajando pestaña:', p)
        datos = pd.read_excel(xls_in, sheet_name=p, index_col=0)
        mindex = datos.index.values
        print('mindex', mindex)
        # Paso 2.1 De acuerdo con la prueba de rachas obtenemos los promedios para cada mes
        promedios = datos.mean()

        # Paso 1.2 Obtenemos un data frame cambiando datos por signos[Si el dato es mayor o igual que el
        # promedio del mes este sa cambia por un "+"]
        # de lo contrario el dato se cambia por un "-"
        # Para comparar se imprime el dataframe antes del cambio
        print(datos.to_string())
        # El cambio se hace en dos tiempos, primero los menores a la media se ponen cómo "-"
        signos = datos.where(datos >= promedios, other='-')
        # Segundo cambio los mayores o iguales a la media se ponen cómo "+"
        signos = signos.where(datos < promedios, other='+')
        # Se imprime el data frame de signos para verifica que el cambio quedo bien hecho
        print(signos.to_string())

        # Paso 1.3. Conteo de rachas empiricas
        # selecciono las filas de la inicial a la penultima
        signos_ini = signos[0:-1]
        #signos_ini.set_index()
        # Selecciono las filas de la segunda a la última
        signos_fin = signos[1:]
        # Guardo columnas
        cols = signos_ini.columns
        # Cálculo del numero de rachas empíricas
        Re = pd.DataFrame(np.where(signos_fin.values != signos_ini.values,1, 0), columns=cols).sum() + 1

        # Paso 1.4. Cálculo del intervalo de confianza
        n = datos.count()
        print('**********'),
        print ('Tamaño del grupo:', n, np.size(n))
        Rt = (n + 1)/2.0
        Std_Rt = np.sqrt(n - 1)/2
        talfa = 1.96
        res_Test = np.logical_and(Re >= Rt - talfa*Std_Rt, Re <= Rt + talfa*Std_Rt)
        res_Test = np.where(res_Test, 'ACEPTADA', 'RECHAZADA')
        Rachas_Test['n'] = n
        Rachas_Test['Re'] = Re
        Rachas_Test['Rt'] = Rt
        Rachas_Test['Std_Rt'] = Std_Rt
        Rachas_Test['Limite Inferior'] = Rt - talfa*Std_Rt
        Rachas_Test['Limite Superior'] = Rt + talfa*Std_Rt
        Rachas_Test['Ho'] = res_Test
        Rachas_Test.to_excel(libro, sheet_name=p, merge_cells=False)
        print(Rachas_Test.to_string())
        Resumen_Rachas[p] = res_Test
    Resumen_Rachas.index = Rachas_Test.index
    print(Resumen_Rachas.to_string())
    Resumen_Rachas.to_excel(libro, sheet_name='Resumen Aleatoriedad', merge_cells=False)
    libro.save()
    return


if __name__ == "__main__":
    # execute only if run as a script
    # Primer paso: Definición de rutas para lectura y guardado de archivos de Excel
    excel_entrada1 = 'Data/serie_mensual_caudales.xlsx'
    excel_salida1 = 'Data/rachas_caudales_serie_mensual.xlsx'
    evaluar_rachas(excel_entrada1, excel_salida1)

    excel_entrada2 = 'Data/grupos_mensuales.xlsx'
    excel_salida2 = 'Data/rachas_grupos_mensuales.xlsx'
    evaluar_rachas(excel_entrada2, excel_salida2)

