from gost import *

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

llave = my_GOST.set_key(key)

for i in range(num):
    cifr = my_GOST.cifrado(cif)

p = desc + llave + cifr
