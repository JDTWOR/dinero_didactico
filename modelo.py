import flet as ft
from supabase import create_client, Client

# Configura Supabase
SUPABASE_URL = "https://efxmvuksosbuqhshflya.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVmeG12dWtzb3NidXFoc2hmbHlhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk1NjE0NTcsImV4cCI6MjA1NTEzNzQ1N30.DVcQzJzr9L2rRkum_6NuN1vk451dWV6iL5x-aqGz7ws"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Función para registrar un usuario
def registrar_usuario(usuario, contrasena):
    data, error = supabase.table("users").insert({
        "nombre": usuario,
        "password": contrasena,  # 🔴 En producción, usa hashing (bcrypt)
    }).execute()
    return error is None

# Función para iniciar sesión
def iniciar_sesion(nombre, contrasena):
    usuario = supabase.table("users").select("*").eq("nombre", nombre).eq("password", contrasena).execute()
    return usuario.data[0] if usuario.data else None

# Función para obtener saldo
def obtener_dinero(id_usuario):
    user = supabase.table("users").select("balance").eq("id", id_usuario).execute()
    return user.data[0]["balance"] if user.data else 0

# Función para transferir dinero
def transferir_dinero(from_id, to_username, amount):
    to_user = supabase.table("users").select("*").eq("username", to_username).execute()
    if not to_user.data:
        return "Usuario no encontrado"

    to_id = to_user.data[0]["id"]
    from_balance = get_balance(from_id)

    if from_balance < amount:
        return "Saldo insuficiente"

    # Realizar la transacción
    supabase.table("users").update({"balance": from_balance - amount}).eq("id", from_id).execute()
    supabase.table("users").update({"balance": to_user.data[0]["balance"] + amount}).eq("id", to_id).execute()
    
    return "Transferencia exitosa"