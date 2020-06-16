import os
import array
import fmanager
import time

def filter_blue (geometria,nombre_archivo,fd_old,fd_new,size,messege,i):
    print("blue")
    width, height, maxval,comentario,off,interleave,l_total = geometria
    #print(geometria)
    #print(nombre_archivo)
    ppm_header = fmanager.crea_encabezado(geometria)
    return i;
