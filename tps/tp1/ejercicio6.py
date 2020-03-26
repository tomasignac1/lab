print('Ejercicio 6')
numero = str(input("\nIngresa la lista de numero separadas por coma "))
print(numero)

array_lista = [int(k) for k in numero.split(',')]
array_lista.append(3)
array_lista.sort(reverse=True)
array_lista.pop(2)
print(array_lista)