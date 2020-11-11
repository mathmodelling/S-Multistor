__author__ = 'Profesor Efraín. Domínguez Calle'
import numpy as np
import pandas as pd

__author__ = 'Profesor Efraín. Domínguez Calle, PhD.'
__copyright__ = "Copyright 2020, Mathmodelling"
__credits__ = ["None"]
__license__ = "Uso académico estudiantes de la Pontificia Universidad Javeriana"
__version__ = "1.0"
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
# El archivo de salida contiene una tabla de resultados explicando que meses se pueden considerar o no grupos aleatorios
# para la variable analizada. Se guarda una tabla por pestaña, la pestaña identifica a la estación

# Primer paso: Definición de rutas para lectura y guardado de archivos de Excel
excel_entrada = 'Precipitación_Complementadas.xlsx'
excel_salida = 'Precipitaciones_Prueba_de_Rachas.xlsx'
# Leemos el libro de Excel
libro = pd.ExcelFile(excel_entrada)
# Establecemos la lista de pestañas y leemos cada una de ellas en un ciclo
pestanas = libro.sheet_names
print(pestanas)

# Pasos preparativos:
# Dataframe para guardar los resultados
Rachas_Test = pd.DataFrame()
Resumen_Rachas = pd.DataFrame()
# Libro para guardar resultado de la prueba de Rachas
libro = pd.ExcelWriter(excel_salida)

# Paso 2: Ciclo de lectura de datos por pestañas y aplicación prueba de rachas
for p in pestanas:
    print('Trabajando pestaña:', p)
    datos = pd.read_excel(excel_entrada, sheet_name=p, index_col=0)
    mindex = datos.index.values
    print('mindex', mindex)
    # Paso 2.1 De acuerdo con la prueba de rachas obtenemos los promedios para cada mes
    promedios = datos.mean()

    # Paso 2.2 Obtenemos un data frame cambiando datos por signos[Si el dato es mayor o igual que el promedio del mes este sa cambia por un "+"]
    # de lo contrario el dato se cambia por un "-"
    # Para comparar se imprime el dataframe antes del cambio
    print(datos.to_string())
    # El cambio se hace en dos tiempos, primero los menores a la media se ponen cómo "-"
    signos = datos.where(datos >= promedios, other='-')
    # Segundo cambio los mayores o iguales a la media se ponen cómo "+"
    signos = signos.where(datos < promedios, other='+')
    # Se imprime el data frame de signos para verifica que el cambio quedo bien hecho
    print(signos.to_string())

    # Paso 2.3. Conteo de rachas empiricas
    # selecciono las filas de la inicial a la penultima
    signos_ini = signos[0:-1]
    #signos_ini.set_index()
    # Selecciono las filas de la segunda a la última
    signos_fin = signos[1:]
    # Guardo columnas
    cols = signos_ini.columns
    # Cálculo del numero de rachas empíricas
    Re = pd.DataFrame(np.where(signos_fin.values != signos_ini.values,1, 0), columns=cols).sum() + 1

    # Paso 2.4. Cálculo del intervalo de confianza
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