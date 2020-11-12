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
dm = pd.read_excel(ruta_mensuales, sheet_name='QL_1', index_col='Fecha')
print(dm.to_string())
# dm.plot(subplots=True, legend=True, layout=(4, 3), fontsize=8)
# plt.show()

# Seleccionar estación de caudales de mi interes
q = pd.DataFrame(dm[29037020])
print(type(q))
# q.plot()
# plt.show()

# Rellenar vacios de forma lineal entre fechas
q = q.interpolate(method='linear')
q = q['1960':]

# Convertir de serie de tiempo a grupos
q['año'] = q.index.year
q['mes'] = q.index.month
print(q.head(20).to_string())
# Crear grupos mensuales
qm = q.pivot(index="año", columns="mes", values=29037020)
print(qm.to_string())

# Por etiqueta PEP8 todas las clausulas para usar import deben ir
# en la parte inicial del script :-(
import statsmodels.api as sm
decomposicion = sm.tsa.seasonal_decompose(q[29037020])
fig = decomposicion.plot()
# plt.show()

qm.columns = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN',
              'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']

qm.to_excel('Data/grupos_mensuales.xlsx', sheet_name='Caudales')

print(q)
q = q.drop(['año', 'mes'], axis=1)
q.to_excel('Data/serie_mensual_caudales.xlsx', sheet_name='29037020')



