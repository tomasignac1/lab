from matplotlib.pylab import hist, show

f = open ('histograma_lista.txt','r')
data = f.read()
print(data)
f.close()

array_lista = [int(k) for k in data.split(',')]

#definimos una lista vacia
lista=[]

for x in range(len(array_lista)):
    lista.append(array_lista[x])

#imprimimos la lista    
print(lista)
data=[]
for i in range(1000):
    data.append(lista)

hist(data,21, (0,20))
show()
