def fibo(n,a=0,b=1):
    while n!=0:
      return fibo(n-1,b,a+b)
    return a

for i in range(0,10):
    print(fibo(i))


#De la linea 1 a la 4 se define una funcion llamada Fibo que recibe 3 parámetros (n,a,b), 
#   en el cual "a" esta igualada a 0 y "b" igualado a 1.
#   Dentro de esta funcion hay un bucle while, como lo indica la palabra: desde que "n" sea distinto de 0
# si esto se cumple:
#   va a devolver la llamada a si misma pero con n-1 valores, "a" con el valor de "b" y "b" con el valor de "a + b"
#       Una vez terminado el bucle devuelve el valor de "a"
# sino se cumple
#   devuelve valor de "a"

#Luego hay un bucle for con un indice "i" y recorre en un rango del 0 al 10.
#Es decir i va desde 0,1,2,3,4,5,6,7,8,9
#   Dentro de este bucle imprime por pantalla la respuesta de la funcion "fibo" pasandole el valor de n. Primero n vale 0, luego vale 1
#   y asi susesivamente hasta llegar al 9 que es el rango del bucle for.

# Dando como resultado la serie Fibbonachi
