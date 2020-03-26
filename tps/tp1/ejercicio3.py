from matplotlib.pylab import hist, show
#definimos una lista vacia
length_list=int(input("Ingrese el tamaño de su lista:"))
lista=[]

for x in range(length_list):
    value=int(input("Ingrese valores: "))
    lista.append(value)

#imprimimos la lista    
print(lista)
data=[]
for i in range(1000):
    data.append(lista)

hist(data,21, (0,20))
show()
