
"""
Created on Wed Sep 17 13:23:23 2022

@author: Marcos Jesus Nicolas
"""
import pandas as pd
import math as m

def imprimir_matriz(A):
	for F in A:
		for e in F:
			print('{:12.5f}'.format(e), end = ' ')
		print()

def dist_eu(x1:list,x2:list)->float:
    if len(x1) == len(x2):
        suma = 0
        for i in range(len(x1)):
            suma += (x1[i]-x2[i])**2
        return m.sqrt(suma)
    else:
        return -1

def matriz_dist(DATOS:list)->list:
    M_dist = []
    for i in range(len(DATOS)):
        M_dist.append([0]*len(DATOS))
    for c in range(len(DATOS)):
        for r in range(len(DATOS)):
            if c == r:
                M_dist[r][c] = 0
            else:
                M_dist[r][c] = dist_eu(DATOS[r], DATOS[c])
    return M_dist

def busca_menor(matriz:pd.core.frame.DataFrame,clust:list)->tuple:
    x = clust[0]
    y = clust[1]
    menor = matriz.loc[x][y]
    for i in clust:
        for k in clust:
            if i != k:
                if menor > matriz.loc[k][i]:
                    menor = matriz.loc[k][i]
                    x = k
                    y = i
    return (x,y)

def cal_new_dist(matriz:pd.core.frame.DataFrame,obj1:str,obj2:str,metodo:str,clust:list)->tuple:
    col_nv = []
    reg_nv = []
    for i in clust:
        if obj1 != i:
            if obj2 != i:
                if metodo == 'Simple':
                    col_nv.append(min(matriz.loc[obj1][i],matriz[obj2][i]))
                    reg_nv.append(min(matriz.loc[obj1][i],matriz[obj2][i]))
                elif metodo == 'Completo':
                    col_nv.append(max(matriz.loc[obj1][i],matriz[obj2][i]))
                    reg_nv.append(max(matriz.loc[obj1][i],matriz[obj2][i]))
                elif metodo == 'Promedio':
                    col_nv.append((matriz.loc[obj1][i]+matriz[obj2][i])/2)
                    reg_nv.append((matriz.loc[obj1][i]+matriz[obj2][i])/2)
    reg_nv.append(0)
    return (col_nv,reg_nv)

def clusters_jerarquicos(DATOS:list, n:int, metodo:str):
    # Checamos que hayan ingresado metodos validos
    METODOS = ['Simple', 'Completo','Promedio']
    if METODOS.count(metodo) == -1:
        return 'Metodo no valido, vuelva a intentar'
    
    # Crea el arreglo de Clusters
    clusters = []
    for i in range(1,len(DATOS)+1):
        clusters.append(str(i))
    
    # Crear matriz de distancias. Se utiliza la metrica Euclidiana
    M = matriz_dist(DATOS)
    M = pd.DataFrame(M, index=clusters, columns=clusters)
    # Numero actual de clusters
    m = len(DATOS)
    while m > n:
        # Encontramos la menor distancia
        obj1, obj2 = busca_menor(M,clust = clusters)
        # Realizamos una copia de la matriz de distancias
        K = M.copy()
        # Quitamos los renglones de los cluster que se uniran
        M = M.drop([obj1,obj2],axis = 0)
        M = M.drop([obj1,obj2],axis = 1)
        # Calulamos las distancias al nuevo cluster
        col, reg = cal_new_dist(K, obj1, obj2,metodo,clusters)
        # Construimos la nueva matriz de distancias
        M[obj1+obj2] = col
        M.loc[obj1+obj2] = reg
        # Juntamos los clusters
        clusters.pop(clusters.index(obj1))
        clusters.pop(clusters.index(obj2))
        clusters.append(obj1+obj2)
        # Reducimos el numero de clusters en uno
        m -= 1
    return clusters

# Prueba
datos = [[30,42,51],[30,40,50],[28,45,53],[28,41,55],[29,39,51],[30,43,51]]
print("Los clusters con metodo Completo son: ",clusters_jerarquicos(datos, 2, 'Completo'))
print("Los clusters con metodo Simple son: ",clusters_jerarquicos(datos, 2, 'Simple'))
print("Los clusters con metodo Promedio son: ",clusters_jerarquicos(datos, 2, 'Promedio'))
