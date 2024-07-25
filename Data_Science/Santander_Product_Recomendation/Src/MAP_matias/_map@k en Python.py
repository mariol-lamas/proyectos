

# EJEMPLOS DE MAP@K EN PYTHON

import numpy as np

def apk(actual, predicted, k):
    if len(predicted)>k:
        predicted = predicted[:k]
    score = 0.0
    num_hits = 0.0
    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)
    if not actual:
        return 0.0
    return score / min(len(actual), k)


def mapk(actual, predicted, k):    
  return np.mean([apk(a,p,k) for a,p in zip(actual, predicted)])


# Para estos ejemplos, por simplificar, asumiremos que existen los productos: 1, 2, 3, 4, 5 y 6


#EJEMPLO 1
# Imaginad que un cliente contrata los productos 1 y 2, mientras que otro contrata los productos 3, 4 y 5 
actual = [['prod_1','prod_2'], ['prod_3','prod_4','prod_5']]
# Esta es vuestra predicción para ambos los clientes (ordenando los productos según vuestra propensión, de mayor a menor):
predicted = [['prod_2','prod_1','prod_6'], ['prod_5','prod_4','prod_3','prod_1','prod_6']]
# El resultado es perfecto, ya que en el top 2 y top 3 de nuestra predicción (para cada cliente) figuran los 2 y 3 productos que realmente compró cada cliente:
print(mapk(actual, predicted, 4))

#EJEMPLO 2
# Pero… si vuestra predicción fuese:
predicted = [['prod_6','prod_5','prod_4'], ['prod_5','prod_4','prod_3','prod_1','prod_6']]
# La métrica sería 0.5, vuestra predicción es incorrecta en el primer cliente pero perfecta en el segundo:
print(mapk(actual, predicted, 4))


# Si uno manda como predicción todos los productos posibles ordenados de más a menos probable que contrate.
# El valor del MAP@K se reducirá, porque hay clientes que no contratarán nada.
# Al dar una lista de productos cuando la predicción debería ser una lista vacía, reduciremos el MAP@K. 


#EJEMPLO 3
# Imaginad que un cliente contrata los productos 1 y 2, mientras que otro contrata los productos 3, 4 y 5 
actual = [['prod_1','prod_2'], ['prod_3','prod_4','prod_5']]
# Esta es vuestra predicción para ambos los clientes, ordenando todos los productos existentes 
predicted = [['prod_2','prod_1','prod_6','prod_3','prod_4','prod_5'], ['prod_5','prod_4','prod_3','prod_1','prod_6','prod_2']]
# El resultado es perfecto, al igual que en el primer ejemplo. Añadir productos sin alterar el top no ha cambiado el MAP@K:
print(mapk(actual, predicted, 4))


#EJEMPLO 4
# Ahora imaginad que el primer cliente no contrata nada (se puede poner [] o [None])
actual = [[], ['prod_3','prod_4','prod_5']]
predicted = [['prod_2','prod_1','prod_6','prod_3','prod_4','prod_5'], ['prod_5','prod_4','prod_3','prod_1','prod_6','prod_2']]
# La métrica sería 1/2, ya que a predicción del segundo cliente es perfecta.
print(mapk(actual, predicted, 4))


#EJEMPLO 5
# Ahora imaginad que los 5 primeros clientes no contratan nada
actual = [[], [None], [ ], [  ], ['prod_3','prod_4','prod_5']]
predicted = [['prod_2','prod_1','prod_6','prod_3','prod_4','prod_5'], ['prod_4','prod_5','prod_1','prod_6','prod_3','prod_2'], ['prod_1','prod_2','prod_3','prod_6','prod_5','prod_4'], ['prod_6','prod_5','prod_4','prod_1','prod_2','prod_3'], ['prod_5','prod_4','prod_3','prod_1','prod_6','prod_2']]
# La métrica sería 0.2, ya de de los 5 clientes solo 1 compró. 
# Como la predicción del que compró es perfecta, el mejor MAP@K posible pasa de valer 1 a valer 1/5.
print(mapk(actual, predicted, 4))



# Ejemplo de como evaluar en el dataset

import pandas as pd

ejemplo_predicciones = pd.read_csv("ejemplo_predicciones.csv", sep=';', converters={"predicted": lambda x: x.strip("[]").replace("'","").split(", ")})
ejemplo_soluciones = pd.read_csv("ejemplo_soluciones.csv", sep=';')

product_columns = ejemplo_predicciones.columns[1:25]

def get_target_products(row):
    selected_products = product_columns[row == 1]
    return ",".join(selected_products)

def get_sorted_products_string(row):
    sorted_product_names = product_columns[row.argsort()[::-1]]
    return ",".join(sorted_product_names)

y = ejemplo_soluciones[product_columns].apply(lambda row: get_target_products(row), axis=1).str.split(",")
pred_concretas = ejemplo_predicciones['predicted']#.str.split(",")
pred_con_todos_los_productos_ordenados = ejemplo_predicciones[product_columns].apply(lambda row: get_sorted_products_string(row), axis=1).str.split(",")


print("Pred Concretas: MAP@7 Score:", mapk(actual=y, predicted=pred_concretas, k=7))

#Cambiando el valor de @K
for j in [1,2,3,4,5,6,7,8,9,10]:
  print('Mean '+str(np.mean([apk(a,p,k=j) for a,p in zip(y, pred_concretas)]))+' of '+str([apk(a,p,k=j) for a,p in zip(y, pred_concretas)]) )

#Cambiando el valor de @K
print("Pred todas las categorías: MAP@7 Score:", mapk(actual=y, predicted=pred_con_todos_los_productos_ordenados, k=7))
for j in [1,2,3,4,5,6,7,8,9,10]:
  print('Mean '+str(np.mean([apk(a,p,k=j) for a,p in zip(y, pred_con_todos_los_productos_ordenados)]))+' of '+str([apk(a,p,k=j) for a,p in zip(y, pred_con_todos_los_productos_ordenados)]) )

#Cambiando el valor de @K
print("Pred perfecta: MAP@7 Score:", mapk(actual=y, predicted=y, k=7))
for j in [1,2,3,4,5,6,7,8,9,10]:
  print('Mean '+str(np.mean([apk(a,p,k=j) for a,p in zip(y, y)]))+' of '+str([apk(a,p,k=j) for a,p in zip(y, y)]) )











