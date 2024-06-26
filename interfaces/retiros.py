import decimal
import subprocess
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
from customtkinter import *
from PIL import Image

from ConexionMDB import *
from widgets_custom import DashboardMenuCliente, MovimientoWidget

# LISTA DE LOS BOTONES QUE ESTARAN EN EL MENU:
nombreBotonesMenu = ['DEPOSITO', 'TRANSFERENCIA', 'depositar']
DIRECCION_DEPOSITAR = 'assets/depositar.png'

conexion_db = conectar_a_MariaDB()
cursor_db = conexion_db.cursor()

conexion_db = conectar_a_MariaDB()
cursor_db = conexion_db.cursor()

ctk.set_appearance_mode("light") # Fuerza el modo claro
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

root = ctk.CTk()
# COMO INVOCAR EL MENU DEL USUARIO
dashboard_menu = DashboardMenuCliente(root, nombreBotonesMenu, 'USUARIO')
dashboard_menu.grid(row=0, column=0,pady=5, padx=10, ipady=10,ipadx=10, sticky="wsn")

cuerpo_depositar= ctk.CTkFrame(root, fg_color='WHITE', border_width=1)
cuerpo_depositar.grid(row=0, column=1, pady=5, padx=10, ipady=10,ipadx=10, sticky="ewsn")

contenedor_head= ctk.CTkFrame(cuerpo_depositar, fg_color='#EBEBEB', border_width=1)
contenedor_head.grid(row=0, column=0, sticky='ew', pady=10, padx=10)

titulo= ctk.CTkLabel(contenedor_head,text='DEPOSITAR',justify="center",fg_color="transparent",font=("Arial",30))
titulo.grid(row=0, column=0, pady=5, padx=10)

img_logo_deposito = ctk.CTkImage(light_image=Image.open(DIRECCION_DEPOSITAR), size=(100,100))
img = Image.open(DIRECCION_DEPOSITAR)

# Redimensionar la imagen si es necesario
img_resized = img.resize((100, 100))  # Ajusta el tamaño de la imagen según lo necesario

# Crear un CTkImage con la imagen redimensionada
img_logo_deposito = ctk.CTkImage(light_image=img_resized, size=(100, 100))

# Crear un CTkLabel para mostrar la imagen
img_label = ctk.CTkLabel(contenedor_head,text="",justify="center", image=img_logo_deposito)
img_label.grid(row=1, column=0, pady=5, padx=10)

# saldo disponible
contenedor_datos= ctk.CTkFrame(cuerpo_depositar, fg_color='#EBEBEB', border_width=1)
contenedor_datos.grid(row=1, column=0, sticky='new', pady=10, padx=10)
titulo_saldo= ctk.CTkLabel(contenedor_datos,text='saldo disponible',justify="center",fg_color="transparent",font=("Arial",30))
titulo_saldo.grid(row=0, column=0, pady=5, padx=10)

#labels de la cuenta

saldo= ctk.CTkLabel(contenedor_datos,text='saldo: ',fg_color="transparent",font=("Arial",20))
saldo.grid(row=1, column=1, pady=5, padx=10,sticky="e")

#numero de cuenta
numero_cuenta= ctk.CTkLabel(contenedor_datos,text='numero de cuenta:',fg_color="transparent",font=("Arial",20))
numero_cuenta.grid(row=1, column=0, pady=5, padx=10,sticky="w")

def obtener_saldo_cuenta(numero_cuenta, label_saldo):
    query = f"SELECT SALDO FROM CUENTA WHERE NUMERO_CUENTA = '{numero_cuenta}'"
    cursor_db.execute(query)
    saldo = cursor_db.fetchone()
    if saldo:
        label_saldo.configure(text=f"Saldo: ${saldo[0]}")
    else:
        label_saldo.configure(text="Cuenta no encontrada")

def obtener_saldo():
    numero_cuenta = cuenta.get()  # Obtener el número de cuenta ingresado
    if numero_cuenta:
        obtener_saldo_cuenta(numero_cuenta, saldo_disponible)  # Pasar saldo_disponible como argumento

saldo_disponible = ctk.CTkLabel(contenedor_datos, text='saldo', fg_color="transparent", font=("Arial", 20))
saldo_disponible.grid(row=2, column=1, pady=5, padx=10, sticky="w")


# Se obtiene valor de la cuenta
cuenta = ctk.CTkEntry(contenedor_datos)
cuenta.grid(row=2, column=0, pady=5, padx=10, sticky="w")

button_obtener_saldo = ctk.CTkButton(contenedor_datos, text="Obtener Saldo", command=obtener_saldo)
button_obtener_saldo.grid(row=4, column=0, pady=10, padx=10, sticky="")


def obtener_saldo_cuenta(numero_cuenta, label_saldo):
    query = f"SELECT SALDO FROM CUENTA WHERE NUMERO_CUENTA = '{numero_cuenta}'"
    cursor_db.execute(query)
    saldo = cursor_db.fetchone()
    if saldo:
        label_saldo.configure(text=f"Saldo: ${saldo[0]}")
    else:
        label_saldo.configure(text="Cuenta no encontrada")

def obtener_saldo():
    numero_cuenta = cuenta.get()  # Obtener el número de cuenta ingresado
    if numero_cuenta:
        obtener_saldo_cuenta(numero_cuenta, saldo_disponible)  # Pasar saldo_disponible como argumento

saldo_disponible = ctk.CTkLabel(contenedor_datos, text='saldo', fg_color="transparent", font=("Arial", 20))
saldo_disponible.grid(row=2, column=1, pady=5, padx=10, sticky="w")

# Se obtiene valor de la cuenta
cuenta = ctk.CTkEntry(contenedor_datos)
cuenta.grid(row=2, column=0, pady=5, padx=10, sticky="w")

button_obtener_saldo = ctk.CTkButton(contenedor_datos, text="Obtener Saldo", command=obtener_saldo)
button_obtener_saldo.grid(row=4, column=0, pady=10, padx=10, sticky="")




def realizar_deposito():
    numero_cuenta = cuenta.get()  # Obtener el número de cuenta ingresado

    if not numero_cuenta:
        print("Número de cuenta no ingresado.")
        return

    monto_deposito = obtener_monto_deposito()  # Obtener el monto de depósito como Decimal

    if monto_deposito is None:
        print("Monto de depósito inválido.")
        return

    try:
        # Obtener el saldo actual de la cuenta
        query = f"SELECT SALDO FROM CUENTA WHERE NUMERO_CUENTA = '{numero_cuenta}'"
        cursor_db.execute(query)
        saldo_actual = cursor_db.fetchone()

        if saldo_actual is None:
            print("Cuenta no encontrada.")
            return

        saldo_actual = decimal.Decimal(saldo_actual[0])
        nuevo_saldo = saldo_actual + monto_deposito

        # Actualizar el saldo en la base de datos
        update_query = f"UPDATE CUENTA SET SALDO = {nuevo_saldo} WHERE NUMERO_CUENTA = '{numero_cuenta}'"
        cursor_db.execute(update_query)
        conexion_db.commit()

        # Actualizar el texto del saldo disponible en la interfaz
        saldo_disponible.configure(text=f"Saldo: ${nuevo_saldo}")

        print(f"Depósito de ${monto_deposito} realizado en la cuenta {numero_cuenta}.")
    except Exception as e:
        print(f"Error al realizar el depósito: {str(e)}")


#deposito
contenedor_realizar_deposito= ctk.CTkFrame(cuerpo_depositar, fg_color='#EBEBEB', border_width=1)
contenedor_realizar_deposito.grid(row=2, column=0, sticky='new', pady=10, padx=10)
depositar_label= ctk.CTkLabel(contenedor_realizar_deposito,text='deposito',justify="center",fg_color="transparent",font=("Arial",30))
depositar_label.grid(row=0, column=0, pady=5, padx=10)
saldo1= ctk.CTkLabel(contenedor_realizar_deposito,text='saldo que desea depositar: ',fg_color="transparent",font=("Arial",20))
saldo1.grid(row=1, column=0, pady=5, padx=10,sticky="we")




monto_deposito_entry = ctk.CTkEntry(contenedor_realizar_deposito, font=("Arial", 20))
monto_deposito_entry.grid(row=3, column=0, pady=10, padx=10, sticky="")

import decimal


def obtener_monto_deposito():
    monto_ingresado_str = monto_deposito_entry.get()  # Obtener el texto ingresado como cadena

    if monto_ingresado_str:
        try:
            monto_ingresado_decimal = decimal.Decimal(monto_ingresado_str)  # Convertir la cadena a Decimal
            return monto_ingresado_decimal  # Devolver el monto como Decimal
        except decimal.InvalidOperation:
            print("Error: Entrada no válida. Ingrese un número válido.")
    else:
        print("El campo de monto de depósito está vacío.")

# Crear un botón para obtener el monto de deposito

button_obtener_monto = ctk.CTkButton(contenedor_realizar_deposito, text="deposiar", command=realizar_deposito)

button_obtener_monto.grid(row=4, column=0, pady=10, padx=10, sticky="")



def funcion_menu():
    root.destroy()
    subprocess.Popen(['python','inicio_usuario.py'])

button=ctk.CTkButton(cuerpo_depositar, text="Regresar Usuario", command=funcion_menu)

button.grid(row=3, column=0, pady=10, padx=10,sticky="es")

# DISEÑO AUTO AJUSTABLE.

#menu
root.rowconfigure(0, weight=1)  
root.columnconfigure(1, weight=10)

dashboard_menu.rowconfigure(0, weight=1)

# Configurar la expansión del contenido en el contenedor
contenedor_head.columnconfigure(0, weight=1)  # Expandir la columna para centrar el contenido
contenedor_datos.columnconfigure(0, weight=1)
contenedor_datos.rowconfigure(3, weight=10)
contenedor_realizar_deposito.columnconfigure(0, weight=1)
contenedor_realizar_deposito.rowconfigure(3, weight=10)


cuerpo_depositar.columnconfigure(0, weight=1)
cuerpo_depositar.rowconfigure(3, weight=10)
root.mainloop()