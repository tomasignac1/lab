import argparse
import os
import time
import sys
import array
import fmanager
import worker
import worker_blue
import worker_green
from concurrent import futures
import threading

start = time.perf_counter()

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Abrir y leer un imagen .ppm')
  parser.add_argument('-s', '--size', dest="size", help="Size")
  parser.add_argument('-f', '--file', action="store", dest="archivo",metavar='archivo', type=str, required=True, help="Nombre del archivo" )
  parser.add_argument('-m', '--filemessege', action="store", dest="messege",metavar='messege', type=str, required=True, help="Nombre del archivo con el mensaje esteganográfico" )
  parser.add_argument('-t', '--offset', dest="offset", help="Tamaño del header")
  parser.add_argument('-i', '--interleave', dest="interleave", help="interleave de modificacion en pixel")
  parser.add_argument('-o', '--fileoutput', action="store", dest="output",metavar='output', type=str, required=True, help="Estego mensaje" )
  args =  parser.parse_args()

  offset = int(args.offset)
  interleave = int(args.interleave)
  size = int(args.size)
  archivo = args.archivo
  messege = args.messege
  nombre_archivo = args.output

  size = size - (size%3) #reajusta a multiplo de 3
  fd = os.open(archivo, os.O_RDONLY)
  l_total = os.stat(messege).st_size #Tamaño de mi mensaje saludo
  #manejo de info del encabezado en un modulo
  off,width,height,maxval,comentario = fmanager.lee_encabezado(fd)
  os.lseek(fd,off,0) #rebobina al principio del raster
  geometria = [width,height,maxval,comentario,off,interleave,l_total]

  #Logic messege
  fd_messege = os.open(messege, os.O_RDONLY)
  mensaje_leido = os.read(fd_messege,l_total)
  renglon = mensaje_leido.splitlines()
  dimension_mensaje = len (renglon[0]) + 1
  for n in range(0,len(renglon)):
    dimension_mensaje = dimension_mensaje + len(renglon[n]) + 1
    take_messege = renglon[n]
    messege_bin = ' '.join(format(x, 'b') for x in bytearray(take_messege))
    messege_decoded = bytes.decode(take_messege)
    print(str(messege_decoded))
    print(messege_bin)
  list_messege = list(messege_bin)
  res = list_messege[0]
  print("RES: " +str(res))

  #Creamos archivo nuevo
  ppm_header = fmanager.crea_encabezado(geometria)
  # Save the PPM image as a binary file
  fd_new =  open(nombre_archivo, 'wb')
  fd_new.write(bytearray(ppm_header.encode()))

  # barrera
  barrera = 0
  # barrera = threading.Barrier(0)
  #Creamos hilos
  hilos = futures.ThreadPoolExecutor(max_workers=3)
  #resultado_a_futuro = hilos.map(functools.partial(workers.filter, nombre_archivo,seg),geometria)#mapeo
  red = [ hilos.submit(worker.filter,geometria,nombre_archivo,fd,fd_new,size,list_messege,0,barrera)  for i in range(1,0,-1)]
  green = [ hilos.submit(worker.filter,geometria,nombre_archivo,fd,fd_new,size,list_messege,1,barrera)  for i in range(1,0,-1)]
  blue = [ hilos.submit(worker.filter,geometria,nombre_archivo,fd,fd_new,size,list_messege,2,barrera)  for i in range(1,0,-1)]
  for r in futures.as_completed(red):
        print (r.result())
  for g in futures.as_completed(green):
        print (g.result())
  for b in futures.as_completed(blue):
        print (b.result())
  finish = time.perf_counter()
  tt = round(finish-start,3)
  print ("tiempo total = ",tt)
  # NUM_HILOS = 3
  # hilos = [threading.Thread(name='Hilo -%s' % i, 
  #                           target=worker.filter_red, 
  #                           args=(geometria,nombre_archivo,fd,fd_new,size,list_messege,barrera,),
  #                           ) for i in range(NUM_HILOS)]
  # for hilo in hilos:
  #   print(hilo.name, 'Comenzando ejecución')
  #   hilo.start()