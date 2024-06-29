# -- coding: utf-8 --
from supabase import create_client, Client
from dotenv import load_dotenv
import estilosfil_form
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configura tu URL de Supabase y tu clave API desde variables de entorno
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Crear cliente Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def alta_usuario(email, clave):
    data = {"email": email, "clave": clave}
    response = supabase.table('usuarios').insert(data).execute()
    if response.status_code == 201:
        print("Usuario registrado exitosamente.")
    else:
        print("Error al registrar usuario: {response.data}")

def get_user(email):
    response = supabase.table('usuarios').select('*').eq('email', email).execute()
    print(response)
    if response.data:
        return response.data[0]
    return None

def get_users():
    response = supabase.table('usuarios').select('*').execute()
    return response

def eliminar_usuario(email):
    response = supabase.table('usuarios').delete().eq('email', email).execute()
    if response.status_code == 200:
        print("Usuario eliminado exitosamente.")
    else:
        print("Error al eliminar usuario: {response.data}")

def modificar_password(email, nueva_clave):
    data = {"clave": nueva_clave}
    response = supabase.table('usuarios').update(data).eq('email', email).execute()
    if response.status_code == 200:
        print("Contraseña modificada exitosamente.")
    else:
        print("Error al modificar contraseña: {response.data}")

def modificar_usuario(email, clave, nombre):
    data = {"nombre": nombre, "email": email}
    response = supabase.table('usuarios').update(data).eq('clave', clave).execute()
    if response.status_code == 200:
        print("Usuario modificado exitosamente.")
    else:
        print("Error al modificar usuario: {response.data}")

# Funciones para la gestión de alumnos, secciones y resultados, adaptadas a Supabase

def get_student(email, clave):
    response = supabase.table('alumnos').select('*').eq('email', email).eq('password', clave).execute()
    if response.data:
        return response.data[0]
    return None

def obtener_alumnos():
    response = supabase.table('alumnos').select('*').execute()
    return response.data

def register_student(email, clave, nombre):
    data = {"email": email, "password": clave, "name": nombre}
    response = supabase.table('alumnos').insert(data).execute()
    if response.status_code == 201:
        print("Alumno registrado exitosamente.")
    else:
        print("Error al registrar alumno: {response.data}")

def create_section(seccion, curso, especialidad, correoMaestro, anio):
    data = {
        "section": seccion,
        "course": curso,
        "specialty": especialidad,
        "email_teacher": correoMaestro,
        "year": anio
    }

    response = supabase.table('secciones').insert(data).execute()
    if response:
        print("Sección creada exitosamente.")
    else:
        print("Error al crear sección: {response.data}")

def get_sections():
    response = supabase.table('secciones').select('*').execute()
    return response.data

def get_sections_by_teacher(correo):
    response = supabase.table('secciones').select('*').eq('email_teacher', correo).execute()
    return response.data

def actualizar_seccion(seccion_id, seccion, curso, especialidad, correoMaestro, anio):
    data = {
        "seccion": seccion,
        "curso": curso,
        "especialidad": especialidad,
        "correoMaestro": correoMaestro,
        "año": anio
    }
    response = supabase.table('secciones').update(data).eq('id', seccion_id).execute()
    if response.status_code == 200:
        print("Sección actualizada exitosamente.")
    else:
        print("Error al actualizar sección: {response.data}")

def create_section_responses(resultado, seccion, especialidad, anio, correo):
    data = {
        "result": resultado,
        "section": seccion,
        "specialty": especialidad,
        "year": anio,
        "email": correo
    }
    response = supabase.table('resultados').insert(data).execute()
    if response:
        print("Respuestas registradas exitosamente.")
    else:
        print("Error al registrar respuestas: {response.data}")

def get_results_by_section(seccion, especialidad, anio):
    response = supabase.table('resultados').select('result','email').eq('section', seccion).eq('specialty', especialidad).eq('year', anio).execute()
    resultados = response.data
    if not resultados:
        return "No hay resultados en esta sección"
    else:
        auxiliar = []
        for i in resultados:
            auxiliar.append(genera_array_resp(i['result'], i['email'], True))
        return auxiliar

def get_results_by_student(seccion, especialidad, anio):
    response = supabase.table('resultados').select('*').eq('section', seccion).eq('specialty', especialidad).eq('year', anio).execute()
    resultados = response.data
    auxiliar = []
    for i in resultados:
        auxiliar.append(genera_array_resp(i['result'], True))
    return auxiliar

def get_individual_results(respuestas):
    data, R_, y = estilosfil_form.estilosfil_form(respuestas)
    response_object = {
        'Activo': str(round((1 - data[0][0]) * 100, 0))     + "%",
        'Reflexivo': str(round((1 - data[0][1]) * 100, 0))  + "%",
        'Teórico': str(round((1 - data[0][2]) * 100, 0))    + "%",
        'Pragmático': str(round((1 - data[0][3]) * 100, 0)) + "%",
    }
    return response_object

def modificar_seccion(seccion, curso):
    data = {"seccion": seccion}
    response = supabase.table('secciones').update(data).eq('curso', curso).execute()
    if response.status_code == 200:
        print("Sección modificada exitosamente.")
    else:
        print("Error al modificar sección: {response.data}")

def genera_array_resp(respuesta_string, email="Ninguno", individual = False):
    if individual:
        arreglo = [int(char) for char in respuesta_string]
    else:
        arreglo = [[int(caracter) for caracter in fila[0]] for fila in respuesta_string]

    data, R_ , y = estilosfil_form.estilosfil_form(arreglo)

    response_object = {
            'Activo': str(round((1 - data[0][0])*100, 0))+'%',
            'Reflexivo': str(round((1-data[0][1])*100, 0))+'%',
            'Teórico': str(round((1 - data[0][2])*100, 0))+'%',
            'Pragmático': str(round((1 - data[0][3])*100, 0))+'%',
            'Email': email
    }
    return response_object

if __name__ == '__main__':
    alta_usuario('galeanoterlyn@gmail.com', '2222')
