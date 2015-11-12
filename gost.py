import random

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


class GOST:
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

with open("gost.py", "rb") as input:
    size = tamano(input)
    print size

tam = str(size) 

if __name__ == '__main__':
    text = int(tam.ljust(23-len(tam),'0'))
    key = random.getrandbits(256)
    my_GOST = GOST()
    my_GOST.set_key(key)

    num = 1000

    for i in range(num):
        text = my_GOST.cifrado(text)
    print hex(text)

    for i in range(num):
        text = my_GOST.descifrado(text)
    print hex(text)
