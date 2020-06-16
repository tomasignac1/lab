import os
import array
import fmanager
import time

def filter_green (geometria,nombre_archivo,fd_old,fd_new,size,messege,i):
    print("green")
    width, height, maxval,comentario,off,interleave,l_total = geometria
    #print(geometria)
    #print(nombre_archivo)
    ppm_header = fmanager.crea_encabezado(geometria)
    #print(ppm_header)
    return i;
