import argparse
import os
import time
import sys
import array
import fmanager
import worker_red
import worker_blue
import worker_green
from concurrent import futures
#import functools

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

  #Creamos archivo nuevo
  ppm_header = fmanager.crea_encabezado(geometria)
  # Save the PPM image as a binary file
  fd_new =  open(nombre_archivo, 'wb')
  fd_new.write(bytearray(ppm_header.encode()))

  #Creamos hilos
  hilos = futures.ThreadPoolExecutor(max_workers=6)
  #resultado_a_futuro = hilos.map(functools.partial(workers.filter, nombre_archivo,seg),geometria)#mapeo
  red = [ hilos.submit(worker_red.filter_red,geometria,nombre_archivo,fd,fd_new,size,messege,1)  for i in range(1,0,-1)]
  green = [ hilos.submit(worker_green.filter_green,geometria,nombre_archivo,fd,fd_new,size,messege,2)  for i in range(1,0,-1)]
  blue = [ hilos.submit(worker_blue.filter_blue,geometria,nombre_archivo,fd,fd_new,size,messege,3)  for i in range(1,0,-1)]
  for r in futures.as_completed(red):
    print (r.result())
  for g in futures.as_completed(green):
    print (g.result())
  for b in futures.as_completed(blue):
    print (b.result())
  