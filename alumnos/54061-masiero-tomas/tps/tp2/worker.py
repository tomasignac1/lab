import os
import array
import fmanager
import time
import globales
import threading

def filter(geometria,nombre_archivo,fd_old,fd_new,size,list_messege,i,barrera):
    width, height, maxval,comentario,off,interleave,l_total = geometria
    j = 1
    globales.posicion_palabra = 0
    len_total = 0
    print("Hilo:" + str(i))
    poli = 0
    rojo = 0
    verde = 0
    azul = 0
    # print("i: " +str(i))
    print("Escribo el cuerpo del archivo")
    globales.global_palabra = list_messege
    while len_total < (width * height * 3):
        globales.buffer = os.read(fd_old,size)
        globales.buffer = globales.buffer
        len_total = len_total + len(globales.buffer)
        # print(len_total)
        if(j - (3*globales.posicion_buffer) == 1):
            if(len(globales.global_palabra[globales.posicion_palabra]) > 0):
                print(str(globales.global_palabra[globales.posicion_palabra]))
                globales.buffer = array.array('B',globales.buffer)
                #en un string 'color'
                if(i == 0 and poli == 0):
                    rojo = rojo + 1
                    globales.candado.acquire()
                    fd_new.write(logica_color(globales.buffer,globales.global_palabra[globales.posicion_palabra],globales.posicion_palabra))
                    globales.candado.release()
                if(i == 1 and poli == 1):
                    verde = verde + 1
                    globales.candado.acquire()
                    fd_new.write(logica_color(globales.buffer,globales.global_palabra[globales.posicion_palabra + 1],globales.posicion_palabra))
                    globales.candado.release()
                if(i == 2 and poli == 2):
                    azul = azul + 1
                    globales.candado.acquire()
                    fd_new.write(logica_color(globales.buffer,globales.global_palabra[globales.posicion_palabra + 1],globales.posicion_palabra))
                    globales.candado.release()
                # print("poli" +str(poli))
                poli = poli + 1
                if(poli == 3):
                    poli = 0
                globales.posicion_buffer = globales.posicion_buffer + 1
            # else:
            #     fd_new.write(globales.buffer)
        j = j + 1
        if size > len(globales.buffer):
            break

    # try:
    #     ident = globales.barrera.wait()
    #     print(str(i), 
    #     'Ejecutando después de la espera',
    #     ident)
    # except threading.BrokenBarrierError:
    #     print(str(i), 'Cancelando')
    # print("len_total: " +str(len_total))
    time = 0
    print("Rojo: "+str(rojo))
    print("Verde:"+str(verde))
    print("Azul: " +str(azul))
    return time

def logica_color(data, messege,r):
    # print("valor:" + str(r))
    color = int.from_bytes(data, byteorder='big')  # convierte los bytes en enteros
    color_bin = bin(color)[2:].zfill(8) #Toda la data a string binario
    if(((7*r)+r-1) == r):#Bytes menos significativo
        globales.poli_rojo = color_bin[r]
        globales.poli_rojo = messege
        rta = bytes(int(globales.poli_rojo[i : i + 8], 2) for i in range(0, len(color_bin), 8))
        globales.posicion_palabra = globales.posicion_palabra + 1
    else:
        print("no cumple")
        rta = bytes(int(color_bin[i : i + 8], 2) for i in range(0, len(color_bin), 8))
    return rta
