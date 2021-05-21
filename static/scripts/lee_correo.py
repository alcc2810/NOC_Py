import re
import os.path
import sys
from os import strerror

patron_horas = re.compile("\d{2}h\d{2}")
patron_logins = re.compile("^LOGIN.*")


telconet_file = "D:\\Scripts_PY\\NOC_Py\\programados\\telconet.txt"
lumen_file = "D:\\Scripts_PY\\NOC_Py\\programados\\lumen.txt"
cnt_file = "D:\\Scripts_PY\\NOC_Py\\programados\\cnt.txt"

line_cnt = 0

if os.path.isfile(telconet_file):
    print("\n* Telconet :)\n")
elif os.path.isfile(lumen_file):
    print("\n* Lumen :)\n")
elif os.path.isfile(cnt_file):
    print("\n* CNT :)\n")
else:
    print("\n* File does not exist :( Please check and try again.\n")
    sys.exit()


try:
    #Abre el archivo en modo lectura
    stream_telconet = open(telconet_file, "rt")

    # #Coloca el cursor al inicio del archivo
    stream_telconet.seek(0)

    #procesar el contenido
    contenido_telconet = stream_telconet.readlines()

    stream_telconet.close()
except Exception as exc:
    print("No se puede abrir el archivo:", exc)


for linea in contenido_telconet:
    print (linea)

# horas_trabajo = list(filter(re_numtrabajo, contenido_telconet))
# print(list(filter(re_numtrabajo, contenido_telconet)))

str_contenido_telconet = str(contenido_telconet)
x = patron_horas.findall(str_contenido_telconet)

print(x)
if x:
  print("YES! We have a match!")
else:
  print("No match")