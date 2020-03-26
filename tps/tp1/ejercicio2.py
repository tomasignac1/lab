print('Ejercicio 2')
numero = int(input("\nIngresa un número entero, por favor: "))
cantidad_suma = int(input("\nIngrese cuantas veces desea sumar, por favor: "))
parseo = str(numero)
if cantidad_suma < 0:
    print(f"La suma entre ellos es {numero}.")
else:
    suma = 0
    rta = int(parseo)
    for i in range(1,cantidad_suma):
        suma = suma + 1
        parseo += str(numero)
        rta = int(parseo) + rta
    print(f"La suma entre ellos es {rta}.")
   