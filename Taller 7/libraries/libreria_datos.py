import pandas as pd
import numpy as np
import sympy
import scipy
import os

def imprimir_hola_datos():

	print('Hola Mundo Datos')

def leer_dataframe(path_file):
	if path_file.endswith('.xlsx') or path_file.endswith('.xls'):
		df = pd.read_excel(path_file)
	elif path_file.endswith('.csv') or path_file.endswith('.txt'):
		df = pd.read_csv(path_file,sep = ',') # , ; \t 
		if df.shape[1] == 1:
			df = pd.read_csv(path_file,sep = ';')
			if df.shape[1] == 1:
				df = pd.read_csv(path_file,sep = '\t')
				if df.shape[1] == 1:
					print('No se pudo cargar los datos de forma correcta.')
	else:
		print('No se tiene una lógica desarrollada para cargar este tipo de datos')
		df = pd.DataFrame()
	return(df)