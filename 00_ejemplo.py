import pandas as pd
import matplotlib.pyplot as plt

# ¿Donde está la info?
ruta_lectura = 'Data/'
ruta_catalogo = ruta_lectura + 'Catalogo.xlsx'
ruta_mensuales = ruta_lectura + 'Datos_mensuales.xlsx'

# Lectura del catálogo de estaciones
cat = pd.read_excel(ruta_catalogo, index_col=0, parse_dates=['Start', 'End'])
print(cat.to_string())

# Leer Caudales mensuales QL_1
dm = pd.read_excel(ruta_mensuales, sheet_name='QL_1', parse_dates=['Fecha'], index_col='Fecha')
print(dm.to_string())
dm.plot(subplots=True, legend=True, layout=(4, 3), fontsize=8)
plt.show()

# Seleccionar estación de caudales de mi interes
q = dm[[29037020]]
print(type(q))
q.plot()
plt.show()
