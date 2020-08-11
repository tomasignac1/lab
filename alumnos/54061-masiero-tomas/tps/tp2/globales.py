import threading

global buffer
buffer = []
global global_palabra
global_palabra = []

global poli_rojo
poli_rojo = []
global poli_verde
poli_verde = []
global poli_azulo
poli_azul = []
global posicion_buffer
posicion_buffer = 0
global posicion_palabra
posicion_palabra = 0

#variables para controlar los problemas de concurrencia
global candado
candado = threading.Lock()
global barrera
barrera = threading.Barrier(3)