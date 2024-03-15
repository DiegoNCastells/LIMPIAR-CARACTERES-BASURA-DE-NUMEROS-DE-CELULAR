# %%
import pandas as pd
from sqlalchemy import create_engine
import pyodbc
import logging
import datetime
import re


# %%
df = pd.read_excel('./Base_Numeros.xlsx') 
df.shape

# %% [markdown]
# ELIMINAR GUIONES

# %%
df_filtrado = df  #[df['Telefono']]#.apply(lambda x: len(str(x)) > 10)].copy()  
df.shape

# %%
df_filtrado.head(3)

# %% [markdown]
# USAR DICCIONARIO PARA MAPEAR

# %%

def limpiar_caract(numero):
    # Definir el diccionario de mapeo de caracteres
    mapeo_caract_vacio = {'-': '', '_': '', ')': '', '(': '',' ' : ''}
    numero_str = str(numero)
    # Aplicar el reemplazo utilizando expresiones regulares
    for caracter, reemplazo in mapeo_caract_vacio.items():
        numero_str = re.sub(re.escape(caracter), reemplazo, numero_str)
    
    return numero_str

# Aplicar la función a la columna 'telefono_nuevo'
df_filtrado['telefono_nuevo'] = df_filtrado['Telefono'].map(limpiar_caract)
df_filtrado.head()

# %% [markdown]
# ELIMINA EL +54 O EL 54

# %%
def limpiar_telefono(numero):
    # Eliminar los prefijos especificados y el carácter '-' de los números de teléfono
    filtrar = ['+549', '549','+54', '54']
    numero = str(numero)
    for prefijo in filtrar:
        if numero.startswith(prefijo):
            numero = numero[len(prefijo):] 
    return numero

# Aplicar la limpieza a la columna 'telefono'
df_filtrado['telefono_nuevo_sin_prefijo'] = df_filtrado['telefono_nuevo'].apply(limpiar_telefono)
df_filtrado.head(5)

# %%
def limpiar_primer_cero(numero):
    # Eliminar los prefijos especificados y el carácter '-' de los números de teléfono
    numero = str(numero)
    prefijo = '0'
    if numero.startswith(prefijo):
        numero = numero[len(prefijo):] 
    return numero

# Aplicar la limpieza a la columna 'telefono'
df_filtrado['telefono_nuevo_sin_prefijo_ni_0'] = df_filtrado['telefono_nuevo_sin_prefijo'].apply(limpiar_primer_cero) 
df_filtrado 


# %% [markdown]
# RE VALIDO LOS QUE telefono_nuevo_sin_prefijo_ni_0 SON MAYORES A 10 DIGITOSS

# %%

def eliminar_15(numero):
    # Definir el mapeo de caracteres a reemplazar
    mapeo_caract_vacio = {'15': ''} 
    # Convertir el número a una cadena
    numero_str = str(numero) 
    # Aplicar el reemplazo utilizando expresiones regulares
    if len(numero) > 10:
        for caracter, reemplazo in mapeo_caract_vacio.items():
            numero_str = re.sub(re.escape(caracter), reemplazo, numero_str, count=1)  # El argumento count=1 limita el reemplazo a la primera ocurrencia    
    return numero_str  # Convertir la cadena resultante de nuevo a un número entero y devolverlo


# %%
df_filtrado['telefono_nuevo_sin_prefijo_ni_0_ni_15'] = df_filtrado['telefono_nuevo_sin_prefijo_ni_0'].apply(eliminar_15)

# %%
# Definir la función para determinar el estado del celular
def determinar_estado(telefono):
    if len(str(telefono)) == 10:
        return "valido"
    else:
        return "invalido"

# Aplicar la función a la columna 'telefono_nuevo_sin_prefijo' y crear una nueva columna 'estado_celular'
df_filtrado['estado_celular'] = df_filtrado['telefono_nuevo_sin_prefijo_ni_0_ni_15'].apply(determinar_estado)

# %%
# Definir la función para determinar el estado del celular y agregar el prefijo '549' si es válido
def determinar_estado(telefono):
    if len(str(telefono)) == 10:
        return '549' + str(telefono)
    else:
        return None  # Devolver None para los teléfonos no válidos

# Aplicar la función a la columna 'telefono_nuevo_sin_prefijo_ni_0_ni_15' y crear una nueva columna 'celular_valido'
df_filtrado['celular_valido'] = df_filtrado['telefono_nuevo_sin_prefijo_ni_0_ni_15'].apply(determinar_estado)

# %%
df_final = df_filtrado.loc[:, ['Negocio', 'Marca', 'SKU', 'Descripcion', 'Nombre', 'DNI', 'Email', 'Validacion', 'Numero de caso', 'Garantia', 'Dias de garantia', 'Dias garantia restante', 'Tipo reclamo', 'Estado', 'Telefono', 'celular_valido','estado_celular']]
df_final.to_excel('./BASE_GAREX_CURADO.xlsx', index=True)


# %%
df_final

# %%



