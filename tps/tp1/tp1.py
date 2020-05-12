import argparse
import os
import multiprocessing
import time
import sys

def cambiar_color(color,imagen,contador):
  print("Te cambeo el color")
    #Creo archivo imagen 1
  nombre_archivo = "dog"+str(contador)+".ppm"
  a = 0
  imagen_cambiada = []
  for i in range(len(imagen)):
    #de bytes a decimal
    a = int.from_bytes(imagen[i], byteorder='big')
    if i > 80:
      seteoColor = a * color;
      #decimal a bytes
      enteriso_variable = int(seteoColor)
    else:
      enteriso_variable = int(a)
    if(enteriso_variable > 255):
      enteriso_variable = 255
    retorno_bytes = enteriso_variable.to_bytes((enteriso_variable.bit_length() +7 ) // 8, 'big') or b'\0'
    imagen_cambiada.append(retorno_bytes)
  creo_imagen(nombre_archivo,imagen_cambiada)

def creo_imagen(nombre_archivo,imagen):
  print(nombre_archivo)
  archivo_imagen = os.open(nombre_archivo, os.O_RDWR|os.O_CREAT)
  for x in range(len(imagen)):
    os.write(archivo_imagen, imagen[x])
    
def do_nothing(seg,imagen,contador,rojo,verde,azul):
  print("Espero {} seg".format(seg))
  time.sleep(seg)
  print("ya espere")
  if contador == 0:
    cambiar_color(rojo,imagen,contador)
  if contador == 1:
    cambiar_color(verde,imagen,contador)
  if contador == 2:
    cambiar_color(azul,imagen,contador)

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Abrir y leer un imagen .ppm')
  parser.add_argument('-f', '--file', action="store", dest="archivo",metavar='archivo', type=str, required=True, help="Nombre del archivo" )
  parser.add_argument('-s', '--size', dest="size", help="Size")
  parser.add_argument('-r', '--red', dest="red", help="Corresponde al color rojo")
  parser.add_argument('-g', '--green', dest="green", help="Corresponde al color verde")
  parser.add_argument('-b', '--blue', dest="blue", help="Corresponde al color azul")
  args =  parser.parse_args()

  red = int(args.red)
  green = int(args.green)
  blue = int(args.blue)
  size = int(args.size)

  if not os.path.isfile(args.archivo):
    print("File path {} does not exist. Exiting...".format(args.archivo))
    sys.exit()
  imagen1 = []
  imagen2 = []
  imagen3 = []

  fp = os.open(args.archivo,os.O_RDWR)

  while True:
    line = os.read(fp,size)
    imagen1.append(line)
    imagen2.append(line)
    imagen3.append(line)
    if size > len(line):    
      break

  procesar_imagen = []
  procesar_imagen.append(imagen1)
  procesar_imagen.append(imagen2)
  procesar_imagen.append(imagen3)

  #print(procesar_imagen[1])
  proc = []
  contador = 0
  for i in range(3):
    proc.append(multiprocessing.Process(target=do_nothing,args= (3,procesar_imagen[contador],contador,red,green,blue) ))
    proc[i].start()
    contador += 1

  print(proc)

  for i in range(3):
    proc[i].join()