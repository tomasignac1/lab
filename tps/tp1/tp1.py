import argparse
import os
import multiprocessing
import time
import sys
import array


class ArgsError(Exception):
    pass

def agrego_intensidad(data, intensidad):
  color = int.from_bytes(data, byteorder='big')  # convierte los bytes en int
  intensidad_ = color*intensidad #le doy intensidad al color
  if(intensidad_ > 255):  
    intensidad_ = 255 #en caso de que sea mayor la intensidad obligo  a tener el maximo
  color_con_intensidad = intensidad_.to_bytes((intensidad_.bit_length(
  ) + 7) // 8, 'big') or b'\0'  #vuelvo a bytes
  return color_con_intensidad

def write_image(archivo_imagen,imagen):
  print("Escribo header del archivo")
  for x in range(len(imagen)):
    os.write(archivo_imagen, imagen[x])
    
def logistica(body,header,color,q,i):
  q.put(body)

  if i == 0:
    cambio_color(header,color,q,i)
  if i == 1:
    cambio_color(header,color,q,i)
  if i == 2:
    cambio_color(header,color,q,i)

def cambio_color(header,color,q,i):
  cola = q.get()
  nombre_archivo = "dog"+str(i)+".ppm"
  archivo_imagen = os.open(nombre_archivo, os.O_RDWR|os.O_CREAT)
  print("Intensidad: {}".format(color))
  print("Imagen: {}".format(i))

  #Encabezado
  write_image(archivo_imagen,header)
      
  j = 1
  r = 0
  print("Escribo el cuerpo del archivo")
  for l in cola:
    if(j - (3*r) == 1):
      if i == 0:
        os.write(archivo_imagen,agrego_intensidad(l,color))
        os.write(archivo_imagen,b'\x00')
        os.write(archivo_imagen,b'\x00')
      if i == 1:
        os.write(archivo_imagen,b'\x00')
        os.write(archivo_imagen,agrego_intensidad(l,color))
        os.write(archivo_imagen,b'\x00')
      if i == 2:
        os.write(archivo_imagen,b'\x00')
        os.write(archivo_imagen,b'\x00')
        os.write(archivo_imagen,agrego_intensidad(l,color))
      r = r+1
    j = j + 1

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

  try:
    if red < 0 or green < 0 or blue < 0 or size < 0:
          raise ArgsError
  except ArgsError:
    print("\nERROR\nError al ingresar las intensidades de los colores y/o lectura de tamaño \n")
    exit(-1)

  color = []
  color.append(red)
  color.append(green)
  color.append(blue)

  imagen1 = []
  imagen2 = []
  imagen3 = []
  imagen1_header = []
  imagen2_header = []
  imagen3_header = []

  fp = os.open(args.archivo,os.O_RDWR)

  contador = 0
  while True:
    line = os.read(fp,size)
    if contador <= 30:
      #Save header
      imagen1_header.append(line)
      imagen2_header.append(line)
      imagen3_header.append(line)
    else:
      #Save body
      imagen1.append(line)
      imagen2.append(line)
      imagen3.append(line)
    contador += 1
    if size > len(line):
          break

  imagen_body = []
  imagen_body.append(imagen1)
  imagen_body.append(imagen2)
  imagen_body.append(imagen3)

  imagen_header = []
  imagen_header.append(imagen1_header)
  imagen_header.append(imagen2_header)
  imagen_header.append(imagen3_header)

  proc = []
  q = multiprocessing.Queue()
  for i in range(3):
    proc.append(multiprocessing.Process(target=logistica,args= (imagen_body[i],imagen_header[i],color[i],q,i) ))
    proc[i].start()

  print(proc)

  for i in range(3):
    proc[i].join()