# -*- coding: utf-8 -*-
import numpy as np
import math as mt

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


# ******************* Funciones Auxiliares *************************
# Calculo del estadístico de Kolmogorov
def ckolmo(obs):
# implementa p(lamda)
# Obs es el valor de lamda empirico
# Definicion de los niveles de significancia
    # vns = [0.4000, 0.3000, 0.2000, 0.1000, 0.0500, 0.0250, 0.0100, 0.0050, 0.0010, 0.0005]
    vns = [obs]
    lvns = len(vns)
    ckd = []
    for i in range(lvns):
        ckd.append([0])
    for i in range (lvns):
        ckd[i] = (-np.log(vns[i]/2.0)/np.log(mt.e)/2.0)**(1/2.0)
    return ckd


# Aplica la prueba de Kolmogorov
def testKolmogorov(pe, pt, alfa):
    # pe prob excedencia empirica
    # pt prob excedencia teorica
    # alfa nivel de significacion de la prueba
    # res = 1 la hipotesis no se rechaza; res = 0 La hipotesis se rechaza
    D=np.max(np.abs(pe-pt))
    lamda=D*np.sqrt(np.size(pe,axis=0))
    # lamda es el lamda empirico
    lamdat=ckolmo(alfa)
    if lamda<=lamdat:
        res=1
    else:
        res=0
    return res
