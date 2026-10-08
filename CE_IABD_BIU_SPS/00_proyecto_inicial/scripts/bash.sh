#!/bin/bash

# 1. Obtener la fecha actual con formato mes_día_año (por ejemplo, 10_06_26)
#    %m: mes (01-12)
#    %d: día (01-31)
#    %y: año en 2 dígitos (ej. 26)
FECHA=$(date +"%m_%d_%y")

# 2. Mostrar esa fecha por pantalla
echo "$FECHA"

# 3 y 4. Copiar ../users/extracted/users.csv a ../users/processed/
#        con el nombre FECHA_processed_users.txt (ej. 10_06_26_processed_users.txt)
cp ../users/extracted/users.csv "../users/processed/${FECHA}_processed_users.txt"

# 5. Ejecutar el script Python python.py
python3 python.py
