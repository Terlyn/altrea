import pymysql
import estilosfil_form
import sqlite3
def dame_conexion():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='24junio98',
        db='base'
    )

def alta_usuario(email, clave):
    conexion = dame_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO usuarios(email,clave) VALUES (%s,%s)", (email, clave)
        )

        conexion.commit()
        conexion.close()   

def obtener_usuario(email):
    conexion = dame_conexion()
    usuario = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT email, clave, type FROM usuarios WHERE email = %s", (email) 
        )
        usuario = cursor.fetchone()
        conexion.close()
    return usuario
    
def obtener_usuarios():
    conexion = dame_conexion()
    usuarios = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM usuarios"
        )
        usuarios = cursor.fetchall()
        #print(usuarios)  
    conexion.close()
    return usuarios

def eliminar_usuario(email):
    conexion = dame_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "DELETE FROM usuarios WHERE email = %s", (email,)
            )
        conexion.commit()
        print("Usuario eliminado exitosamente.")
    except Exception as e:
        print("Error al eliminar usuario:", e)
    finally:
        conexion.close()

def modificar_contraseña(email, nueva_clave):
    conexion = dame_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE usuarios SET clave = %s WHERE email = %s", (nueva_clave, email)
            )
        conexion.commit()
        print("Usuario modificado exitosamente.")
    except Exception as e:
        print("Error al modificar usuario:", e)
        raise  # Re-levanta la excepción para que pueda ser manejada en la vista
    finally:
        conexion.close()
        
        
def modificar_usuario(email, clave, nombre):
    conexion = dame_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE usuarios SET nombre = %s, email =%s WHERE clave = %s", (nombre, email, clave)
            )
        conexion.commit()
        print("Usuario modificado exitosamente.")
    except Exception as e:
        print("Error al modificar usuario:", e)
        raise  # Re-levanta la excepción para que pueda ser manejada en la vista
    finally:
        conexion.close()
        
    def borrar_usuario(self, email):
        try:
            conn = self.obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE email = ?", (email,))
            conn.commit()
            cursor.close()
            conn.close()
            print(f"Usuario con email {email} borrado exitosamente.")
        except sqlite3.Error as e:
            print(f"Error al borrar usuario: {e}")
            
            
def crear_tabla():
    conexion = dame_conexion()
    try:
        with conexion.cursor() as cursor:
            # Define la consulta SQL para crear la tabla
            sql = """
            CREATE TABLE IF NOT EXISTS MiTabla (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255),
                edad INT
            )
            """
            # Ejecuta la consulta SQL
            cursor.execute(sql)
            print("Tabla creada exitosamente.")
        # Confirma los cambios en la base de datos
        conexion.commit()
    finally:
        # Cierra la conexión
        conexion.close()



############################################################
######################base datos############################
######################estudiantes###########################
############################################################

def obtener_alumno(email,clave):
    conexion = dame_conexion()
    alumno = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM alumnos WHERE correo = %s and contraseña = %s", (email, clave)
        )
        alumno = cursor.fetchone()
        conexion.close()
        return alumno


def obtener_alumnos():
    conexion = dame_conexion()
    alumnos = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM alumnos"
        )
        alumnos = cursor.fetchall()
        print(alumnos)  # Imprime los usuarios en la consola para verificar
    conexion.close()
    return alumnos

def alta_alumno(email, clave, nombre):
    conexion = dame_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO alumnos(correo, contraseña, nombre) VALUES (%s, %s,%s)", (email, clave, nombre)
        )
        conexion.commit()
    conexion.close()

############################################################
######################base datos############################
#######################secciones###########################
############################################################
def crear_seccion(seccion, curso, especialidad, correoMaestro, año):
    conexion = dame_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO secciones(seccion, curso, especialidad, correoMaestro, año) VALUES (%s, %s,%s,%s,%s)", (seccion, curso, especialidad, correoMaestro, año)
        )
        conexion.commit()
    conexion.close()


def obtener_secciones():
    conexion = dame_conexion()
    secciones = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM secciones"
        )
        secciones = cursor.fetchall()
    conexion.close()
    print(secciones)
    return secciones

#obtener secciones por correo de maestro
def obtener_secciones_por_maestro(correo):
    conexion = dame_conexion()
    resultados = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM secciones WHERE correoMaestro = %s ",
            (correo)
        )
        resultados = cursor.fetchall()
    conexion.close()
    return resultados

######modal de editar seccion ##########################
def actualizar_seccion(seccion_id, seccion, curso, especialidad, correoMaestro, año):
    conexion = dame_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE secciones SET seccion = %s, curso = %s, especialidad = %s, correoMaestro = %s, año = %s WHERE id = %s",
            (seccion, curso, especialidad, correoMaestro, año, seccion_id)
        )
        conexion.commit()
    conexion.close()
############################################################
######################base datos############################
#############respuestas por secciones#######################
############################################################
def crear_respuestas_por_secciones(resultado, seccion,  especialidad, año, correo):
    print(resultado)
    print(correo)
    print(especialidad)
    conexion = dame_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO resultados(resultado, seccion,  especialidad, año,correo) VALUES (%s, %s,%s,%s,%s)", (resultado, seccion,  especialidad, año, correo)
        )
        conexion.commit()
    conexion.close()

#######################estoy trabajando aqui####################################
def genera_array_resp(respuesta_string, individual = False):
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
    }
    return response_object
        
 #esta función muestra todos los resultados por sección   
def obtener_resultados_por_seccion(seccion, especialidad, año):
    conexion = dame_conexion()
    resultados = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT resultado FROM resultados WHERE seccion = %s AND especialidad = %s AND año = %s" ,
            (seccion, especialidad, año)
        )
        resultados = cursor.fetchall()
    conexion.close()
    if resultados == ():
        resultado = "No hay resultados en esta sección"
    else:
        resultado = genera_array_resp(resultados)
    return resultado

#esta función muestra los resultados historicos por alumno
def obtener_resultados_por_alumno(seccion, especialidad, año):
    conexion = dame_conexion()
    resultados = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT resultado, seccion, especialidad, año FROM resultados WHERE seccion = %s AND especialidad = %s AND año = %s",
            (seccion, especialidad, año)
        )
        resultados = cursor.fetchall()
    conexion.close()
    auxiliar = []
    for i in resultados:
        auxiliar.append(genera_array_resp(i[0], True))
        
    return auxiliar

def obtener_resultados_ind(respuestas):
    data, R_ , y = estilosfil_form.estilosfil_form(respuestas)
    response_object = {
            'Activo': str(round((1 - data[0][0])*100, 0))+'%',
            'Reflexivo': str(round((1-data[0][1])*100, 0))+'%',
            'Teórico': str(round((1 - data[0][2])*100, 0))+'%',
            'Pragmático': str(round((1 - data[0][3])*100, 0))+'%',
        }

    return response_object

#################################editar seccion#######
def modificar_seccion(seccion, curso):
    conexion = dame_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE secciones SET seccion = %s WHERE curso = %s", (seccion, curso)
            )
        conexion.commit()
        print("sección modificada exitosamente.")
    except Exception as e:
        print("Error al modificar la seccion:", e)
        raise  # Re-levanta la excepción para que pueda ser manejada en la vista
    finally:
        conexion.close()

if __name__ == '__main__':
    alta_usuario('anto@gmail.com', 'sdfsf')