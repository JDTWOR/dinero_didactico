import bcrypt
from modelo import *
import flet as ft

def main(page: ft.Page):
    page.title = "DINERO DIDACTICO"

    def pantalla_principal(usuario):
        
        page.clean()
        def refrescar(e):
            dinero = obtener_dinero(usuario["id"])
            saldo.value = f"Saldo: $ {dinero}"
            print(usuario)
            saldo.update()
        dinero = obtener_dinero(usuario["id"])
        boton_actualizar_saldo = ft.Button(text="Refrescar", on_click=refrescar)        
        saldo = ft.Text(value=f"Saldo: $ {dinero}")
        page.add(saldo, boton_actualizar_saldo)

    def validar_inicio_sesion(e):
        usuario = iniciar_sesion(nombre_usuario.value, contraseña_usuario.value)
        if usuario:
            estado_ingreso.value = "Inicio de sesion correcto"
            pantalla_principal(usuario)
        else:
            estado_ingreso.value = "Usuario o contraseña incorrectos"
            page.update()


    nombre_usuario = ft.TextField(hint_text="Ingrese su usuario")
    contraseña_usuario = ft.TextField(hint_text="Ingrese su contraseña")
    boton_iniciar_sesion = ft.TextButton(text="INICIAR SESION", on_click=validar_inicio_sesion) 
    boton_crear_cuenta = ft.TextButton(text="CREAR CUENTA")
    estado_ingreso = ft.Text()
    page.add(nombre_usuario, contraseña_usuario, estado_ingreso, ft.Row(controls=[boton_iniciar_sesion, boton_crear_cuenta]))

ft.app(target=main)
