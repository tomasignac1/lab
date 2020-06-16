import os
import array
import fmanager
import time

def filter_red (geometria,nombre_archivo,fd_old,fd_new,size,messege,i):
    print("red")
    width, height, maxval,comentario,off,interleave,l_total = geometria
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

    j = 1
    r = 0
    len_total = 0
    print("Escribo el cuerpo del archivo")
    while len_total < (width * height * 3):
        leido = os.read(fd_old,size)
        len_total = len_total + len(leido)
        print(len_total)
        if(j - (3*r) == 1):
            if(len(list_messege[r]) > 0):
                leido = array.array('B',leido) 
                fd_new.write(logica_color(leido,list_messege[r],r))
                #aca deberia estar la 
                # sincronizacion
                fd_new.write(b'\x00')#este no deberia
                fd_new.write(b'\x00')#este no deberia
                r = r+1
            else:
                fd_new.write(leido)
        j = j + 1
    print("len_total: " +str(len_total))
    return i;

def logica_color(data, messege,r):
    print("valor:" + str(r))
    color = int.from_bytes(data, byteorder='big')  # convierte los bytes en enteros
    color_bin = bin(color)[2:].zfill(8)
    # lista_colores = list(color_bin)
    # lista_colores = array.array('i',lista_colores)
    # print("Largo:" +str(len(lista_colores)))
    # contador = 0
    # for lista_colores in range(len(lista_colores)):
    #     lista_colores[((7*contador)+contador-1)] = messege
    # listado = ''.join(str(e) for e in lista_colores)
    # print("Muestro: " +color_bin[7])
    if(r == 0):
        print("Color: " +color_bin[8])
        print("Mensaje: " +messege)
        color_bin[7] = messege
    else:
        color_bin[((7*r)+r-1)] = messege[r]
    rta = bytes(int(color_bin[i : i + 8], 2) for i in range(0, len(color_bin), 8))
    # color_con_intensidad = intensidad_.to_bytes((intensidad_.bit_length(
    # ) + 7) // 8, 'big') or b'\0'  #vuelvo a bytes
    # return bytearray(color_bin.encode())
    return rta
