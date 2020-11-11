import pandas as pd
import matplotlib.pyplot as plt

# donde está la info?
ruta_lectura = 'Data/'
ruta_catalogo = ruta_lectura + 'Catalogo.xlsx'
ruta_diarios = ruta_lectura + 'Datos_Diarios.xlsx'
ruta_mensuales = ruta_lectura + 'Datos_mensuales.xlsx'

#Lectura del Catalogo de Estaciones
cat = pd.read_excel(ruta_catalogo, index_col=0, parse_dates=['Start', 'End'])
print(cat.to_string())
print((cat['End'] - cat['Start']) / 365.25 )

# Lectura de Datos diarios
dd = pd.read_excel(ruta_diarios, index_col='Fecha', parse_dates=['Fecha'])
print(dd)

# Lectura de Datos mensuales
dm = pd.read_excel(ruta_mensuales, index_col='Fecha', parse_dates=['Fecha'] )
print(dm.to_string())

# Una miradita a los datos mensuales.
dm.plot(subplots=True, legend=True, layout=(4,3), fontsize=6)
plt.show()
