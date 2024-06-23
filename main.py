# -- coding: utf-8 --
from flask import Flask, redirect, request, url_for, render_template, flash, session
import basedatos

app = Flask(__name__)
app.secret_key = 'miclavesecreta'

@app.before_request
def antes_de_todo():
    ruta = request.path
    if not 'usuario' in session and ruta != "/entrar" and ruta != "/login" and ruta != "/salir" and ruta != "/registro":
        flash("Inicia sesión para continuar")
        #return redirect("/inicio")
        inicio()

@app.route("/dentro")
def dentro():
    return render_template("index.html", usuarios = obtener_usuarios())


@app.route("/entrar")
def entrar():
    return render_template("entrar.html")

@app.route("/")
@app.route("/inicio")
def inicio():
    return render_template("inicio.html")

@app.route("/sobreNosotros")
def sobreNosotros():
    return render_template("sobreNosotros.html")

@app.route("/loginEstudiante")
def loginEstudiante():
    return render_template("loginEstudiante.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    contraseña = request.form['contraseña']

    try:
        usuario = basedatos.obtener_usuario(email)
    except Exception as e:
        flash("Error al obtener usuario")
        
    if usuario:
        if usuario[1] == contraseña:
            session['usuario'] = email
            basedatos.obtener_usuarios()
            secciones = basedatos.obtener_secciones_por_maestro(email)
            return render_template("index.html", usuarios = obtener_usuarios(), secciones = secciones, user=usuario[2])
        else:
            flash("Acceso denegado")
            return redirect("/entrar")
    else:
        flash("Usuario no registrado")
    return redirect("/entrar")

def imprimir_Resultado( resultado ):
    return resultado

@app.route("/salir")
def salir():
    session.pop("usuario", None)
    flash("Sesión cerrada")

    return redirect("/entrar")

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/registrar", methods=['POST'])
def registrar():
    email = request.form['email']
    contraseña = request.form['contraseña']

    try:
        basedatos.alta_usuario(email, contraseña)
        flash("Bienvenido")
    except Exception as e:
        flash("Error al registrar usuario")
    finally:
        return redirect("/entrar")

#@app.route("/obtener_usuarios")
def obtener_usuarios():
    try:
        usuarios = basedatos.obtener_usuarios()
        return(usuarios)  # Imprime los usuarios en la consola para verificar
        #return render_template('index.html', usuarios=usuarios)
    except Exception as e:
        print("Error al obtener usuarios:", e)
        return 0 # Imprime cualquier error en la consola
        #return render_template('error')  # Puedes crear una plantilla 'error.html' para mostrar mensajes de error al usuario

@app.route('/modificar_contraseña', methods=['POST'])
def modificar_contraseña():
    if request.method == 'POST':
        try:
            email = request.form['email']
            nueva_clave = request.form['nueva_clave']
            basedatos.modificar_contraseña(email, nueva_clave)
            flash("Usuario modificado exitosamente.")
        except Exception as e:
            flash("Error al modificar usuario: " + str(e))
    return redirect("/")

@app.route('/modificar_usuario', methods=['POST'])
def modificar_usuario():
    if request.method == 'POST':
        try:
            emails = request.form.getlist('email_')
            claves = request.form.getlist('clave_')
            nombres = request.form.getlist('nombre_')

            # Combinamos los valores en una lista de diccionarios
            combinados = []
            usuarios = basedatos.obtener_usuarios()
            for email, clave, nombre in zip(emails, claves, nombres):
                combinados.append({'email': email, 'clave': clave, 'nombre': nombre})
                basedatos.modificar_usuario(email, clave, nombre)
            flash("Usuario modificado exitosamente.")
            
        except Exception as e:
            flash("Error al modificar usuario: " + str(e))
    return render_template("/index.html")

@app.route('/borrar_usuario', methods=['POST'])
def borrar_usuario():
    if request.method == 'POST':
        try:
            emails = request.form.getlist('email_')

            # Borramos los usuarios con los correos electrónicos especificados
            for email in emails:
                basedatos.borrar_usuario(email)
            
            flash("Usuario(s) borrado(s) exitosamente.")
            
        except Exception as e:
            flash("Error al borrar usuario(s): " + str(e))
    return render_template("/index.html")

############################################################
######################base datos############################
######################estudiantes###########################
############################################################
@app.route("/registrarEstudiante", methods=['POST'])
def registrarEstudiante():
    email      = request.form['emailRegistro']
    contraseña = request.form['contraseñaRegistro']
    nombre     = request.form['nombreRegistro']

    try:
        basedatos.alta_alumno(email, contraseña, nombre)
        flash("Bienvenido")
    except Exception as e:
        flash("Error al registrar usuario")
    finally:
        return redirect("/loginEstudiante")
    
    
@app.route("/loginEstudiante1", methods=["POST"])
def loginEstudiante1():
    email = request.form['email']
    contraseña = request.form['contraseña']

    alumno = basedatos.obtener_alumno(email,contraseña)
    if alumno:
        if alumno[2] == contraseña:
            #return email
            array_preguntas = mostrar_formulario_()
            #return redirect("/formulario/login")
            return render_template('formulario.html', preguntas=array_preguntas[0], secciones= array_preguntas[1], login= array_preguntas[2], email = email)

        else:
            flash("Acceso denegado")
 
    else:
        flash("Usuario no registrado")
    return redirect("/entrar")


############################################################
######################formulario############################
############################################################

@app.route('/formulario', methods=['GET'])
def mostrar_formulario():
    array_secciones = basedatos.obtener_secciones()
    preguntas = [
        "Tengo fama de decir lo que pienso claramente y sin rodeos",
        "Estoy seguro/a de lo que es bueno y lo que es malo, lo que está bien y lo que está mal.",
        "Muchas veces actúo sin mirar las consecuencias",
        "Normalmente trato de resolver los problemas metódicamente y paso a paso",
        "Creo que los formalismos coartan y limitan la actuación libre de las personas",
        "Me interesa saber cuáles son los sistemas de valores de los demás y con qué criterios actúan",
        "Pienso que el actuar intuitivamente puede ser siempre tan válido como actuar reflexivamente.",
        "Creo que lo más importante es que las cosas funcionen",
        "Procuro estar al tanto de lo que ocurre aquí y ahora",
        "Disfruto cuando tengo tiempo para preparar mi trabajo y realizarlo a conciencia",
        "Estoy a gusto siguiendo un orden en las comidas, en el estudio, haciendo ejercicio regularmente",
        "Cuando escucho una nueva idea enseguida comienzo a pensar cómo ponerla en práctica",
        "Prefiero las ideas originales y novedosas aunque no sean prácticas",
        "Admito y me ajusto a las normas sólo si me sirven para lograr mis objetivos",
        "Normalmente encajo bien con personas reflexivas, y me cuesta sintonizar con personas demasiado espontáneas, imprevisibles",
        "Escucho con más frecuencia que hablo",
        "Prefiero las cosas estructuradas a las desordenadas",
        "Cuando poseo cualquier información, trato de interpretarla bien antes de manifestar alguna conclusión",
        "Antes de hacer algo estudio con cuidado sus ventajas e inconvenientes",
        "Me entusiasmo con el reto de hacer algo nuevo y diferente",
        "Casi siempre procuro ser coherente con mis criterios y sistemas de valores. Tengo principios y los sigo",
        "Cuando hay una discusión no me gusta ir con rodeos",
        "Me disgusta implicarme afectivamente en el ambiente de la escuela. Prefiero mantener relaciones distantes",
        "Me gustan más las personas realistas y concretas que las teóricas",
        "Me cuesta ser creativo/a, romper estructuras",
        "Me siento a gusto con personas espontáneas y divertidas",
        "La mayoría de las veces expreso abiertamente cómo me siento",
        "Me gusta analizar y dar vueltas a las cosas",  
        "Me molesta que la gente no se tome en serio las cosas",  
        "Me atrae experimentar y practicar las últimas técnicas y novedades",  
        "Soy cauteloso/a a la hora de sacar conclusiones",  
        "Prefiero contar con el mayor número de fuentes de información. Cuantos más datos reúna para reflexionar, mejor.",  
        "Tiendo a ser perfeccionista",  
        "Prefiero oír las opiniones de los demás antes de exponer la mía",  
        "Me gusta afrontar la vida espontáneamente y no tener que planificar todo previamente",  
        "En las discusiones me gusta observar cómo actúan los demás participantes",  
        "Me siento incómodo/a con las personas calladas y demasiado analíticas",  
        "Juzgo con frecuencia las ideas de los demás por su valor práctico",  
        "Me agobio si me obligan a acelerar mucho el trabajo para cumplir un plazo",  
        "En las reuniones apoyo las ideas prácticas y realistas",  
        "Es mejor gozar del momento presente que deleitarse pensando en el pasado o en el futuro",  
        "Me molestan las personas que siempre desean apresurar las cosas",  
        "Aporto ideas nuevas y espontáneas en los grupos de discusión",  
        "Pienso que son más consistentes las decisiones fundamentadas en un minucioso análisis que las basadas en la intuición",  
        "Detecto frecuentemente la inconsistencia y puntos débiles en las argumentaciones de los demás",  
        "Creo que es preciso saltarse las normas muchas más veces que cumplirlas",  
        "A menudo caigo en la cuenta de otras formas mejores y más prácticas de hacer las cosas",  
        "En conjunto hablo más que escucho",  
        "Prefiero distanciarme de los hechos y observarlos desde otras perspectivas",  
        "Estoy convencido/a que debe imponerse la lógica y el razonamiento",  
        "Me gusta buscar nuevas experiencias",  
        "Me gusta experimentar y aplicar las cosas",  
        "Pienso que debemos llegar pronto al grano, al meollo de los temas.",  
        "Siempre trato de conseguir conclusiones e ideas claras",
        "Prefiero discutir cuestiones concretas y no perder el tiempo con pláticas superficiales", 
        "Me impaciento cuando me dan explicaciones irrelevantes e incoherentes", 
        "Compruebo antes si las cosas funcionan realmente", 
        "Hago varios borradores antes de la redacción definitiva de un trabajo", 
        "Soy consciente de que en las discusiones ayudo a mantener a los demás centrados en el tema, evitando divagaciones", 
        "Observo que, con frecuencia, soy uno/a de los/as más objetivos/as y desapasionados/as en las discusiones", 
        "Cuando algo va mal, le quito importancia y trato de hacerlo mejor", 
        "Rechazo ideas originales y espontáneas si no las veo prácticas", 
        "Me gusta sopesar diversas alternativas antes de tomar una decisión", 
        "Con frecuencia miro hacia delante para prever el futuro", 
        "En los debates y discusiones prefiero desempeñar un papel secundario antes que ser el/la líder o el/la que más participa", 
        "Me molestan las personas que no actúan con lógica", 
        "Me resulta incómodo tener que planificar y prever las cosas", 
        "Creo que el fin justifica los medios en muchos casos", 
        "Suele reflexionar sobre los asuntos y problemas", 
        "El trabajar a conciencia me llena de satisfacción y orgullo", 
        "Ante los acontecimientos trato de descubrir los principios y teorías en que se basan", 
        "Con tal de conseguir el objetivo que pretendo soy capaz de herir sentimientos ajenos", 
        "No me importa hacer todo lo necesario para que sea efectivo mi trabajo", 
        "Con frecuencia soy una de las personas que más anima las fiestas", 
        "Me aburro enseguida con el trabajo metódico y minucioso", 
        "La gente con frecuencia cree que soy poco sensible a sus sentimientos", 
        "Suele dejarme llevar por mis intuiciones", 
        "Si trabajo en grupo procuro que se siga un método y un orden", 
        "Con frecuencia me interesa averiguar lo que piensa la gente", 
        "Esquivo los temas subjetivos, ambiguos y poco claros"
    ]
    return render_template('formulario.html', preguntas=preguntas, secciones= array_secciones, login=False)

#@app.route('/formulario/login', methods=['GET'])
def mostrar_formulario_():
    array_secciones = basedatos.obtener_secciones()
    preguntas = [
        "Tengo fama de decir lo que pienso claramente y sin rodeos",
        "Estoy seguro/a de lo que es bueno y lo que es malo, lo que está bien y lo que está mal.",
        "Muchas veces actúo sin mirar las consecuencias",
        "Normalmente trato de resolver los problemas metódicamente y paso a paso",
        "Creo que los formalismos coartan y limitan la actuación libre de las personas",
        "Me interesa saber cuáles son los sistemas de valores de los demás y con qué criterios actúan",
        "Pienso que el actuar intuitivamente puede ser siempre tan válido como actuar reflexivamente.",
        "Creo que lo más importante es que las cosas funcionen",
        "Procuro estar al tanto de lo que ocurre aquí y ahora",
        "Disfruto cuando tengo tiempo para preparar mi trabajo y realizarlo a conciencia",
        "Estoy a gusto siguiendo un orden en las comidas, en el estudio, haciendo ejercicio regularmente",
        "Cuando escucho una nueva idea enseguida comienzo a pensar cómo ponerla en práctica",
        "Prefiero las ideas originales y novedosas aunque no sean prácticas",
        "Admito y me ajusto a las normas sólo si me sirven para lograr mis objetivos",
        "Normalmente encajo bien con personas reflexivas, y me cuesta sintonizar con personas demasiado espontáneas, imprevisibles",
        "Escucho con más frecuencia que hablo",
        "Prefiero las cosas estructuradas a las desordenadas",
        "Cuando poseo cualquier información, trato de interpretarla bien antes de manifestar alguna conclusión",
        "Antes de hacer algo estudio con cuidado sus ventajas e inconvenientes",
        "Me entusiasmo con el reto de hacer algo nuevo y diferente",
        "Casi siempre procuro ser coherente con mis criterios y sistemas de valores. Tengo principios y los sigo",
        "Cuando hay una discusión no me gusta ir con rodeos",
        "Me disgusta implicarme afectivamente en el ambiente de la escuela. Prefiero mantener relaciones distantes",
        "Me gustan más las personas realistas y concretas que las teóricas",
        "Me cuesta ser creativo/a, romper estructuras",
        "Me siento a gusto con personas espontáneas y divertidas",
        "La mayoría de las veces expreso abiertamente cómo me siento",
        "Me gusta analizar y dar vueltas a las cosas",  
        "Me molesta que la gente no se tome en serio las cosas",  
        "Me atrae experimentar y practicar las últimas técnicas y novedades",  
        "Soy cauteloso/a a la hora de sacar conclusiones",  
        "Prefiero contar con el mayor número de fuentes de información. Cuantos más datos reúna para reflexionar, mejor.",  
        "Tiendo a ser perfeccionista",  
        "Prefiero oír las opiniones de los demás antes de exponer la mía",  
        "Me gusta afrontar la vida espontáneamente y no tener que planificar todo previamente",  
        "En las discusiones me gusta observar cómo actúan los demás participantes",  
        "Me siento incómodo/a con las personas calladas y demasiado analíticas",  
        "Juzgo con frecuencia las ideas de los demás por su valor práctico",  
        "Me agobio si me obligan a acelerar mucho el trabajo para cumplir un plazo",  
        "En las reuniones apoyo las ideas prácticas y realistas",  
        "Es mejor gozar del momento presente que deleitarse pensando en el pasado o en el futuro",  
        "Me molestan las personas que siempre desean apresurar las cosas",  
        "Aporto ideas nuevas y espontáneas en los grupos de discusión",  
        "Pienso que son más consistentes las decisiones fundamentadas en un minucioso análisis que las basadas en la intuición",  
        "Detecto frecuentemente la inconsistencia y puntos débiles en las argumentaciones de los demás",  
        "Creo que es preciso saltarse las normas muchas más veces que cumplirlas",  
        "A menudo caigo en la cuenta de otras formas mejores y más prácticas de hacer las cosas",  
        "En conjunto hablo más que escucho",  
        "Prefiero distanciarme de los hechos y observarlos desde otras perspectivas",  
        "Estoy convencido/a que debe imponerse la lógica y el razonamiento",  
        "Me gusta buscar nuevas experiencias",  
        "Me gusta experimentar y aplicar las cosas",  
        "Pienso que debemos llegar pronto al grano, al meollo de los temas.",  
        "Siempre trato de conseguir conclusiones e ideas claras",
        "Prefiero discutir cuestiones concretas y no perder el tiempo con pláticas superficiales", 
        "Me impaciento cuando me dan explicaciones irrelevantes e incoherentes", 
        "Compruebo antes si las cosas funcionan realmente", 
        "Hago varios borradores antes de la redacción definitiva de un trabajo", 
        "Soy consciente de que en las discusiones ayudo a mantener a los demás centrados en el tema, evitando divagaciones", 
        "Observo que, con frecuencia, soy uno/a de los/as más objetivos/as y desapasionados/as en las discusiones", 
        "Cuando algo va mal, le quito importancia y trato de hacerlo mejor", 
        "Rechazo ideas originales y espontáneas si no las veo prácticas", 
        "Me gusta sopesar diversas alternativas antes de tomar una decisión", 
        "Con frecuencia miro hacia delante para prever el futuro", 
        "En los debates y discusiones prefiero desempeñar un papel secundario antes que ser el/la líder o el/la que más participa", 
        "Me molestan las personas que no actúan con lógica", 
        "Me resulta incómodo tener que planificar y prever las cosas", 
        "Creo que el fin justifica los medios en muchos casos", 
        "Suele reflexionar sobre los asuntos y problemas", 
        "El trabajar a conciencia me llena de satisfacción y orgullo", 
        "Ante los acontecimientos trato de descubrir los principios y teorías en que se basan", 
        "Con tal de conseguir el objetivo que pretendo soy capaz de herir sentimientos ajenos", 
        "No me importa hacer todo lo necesario para que sea efectivo mi trabajo", 
        "Con frecuencia soy una de las personas que más anima las fiestas", 
        "Me aburro enseguida con el trabajo metódico y minucioso", 
        "La gente con frecuencia cree que soy poco sensible a sus sentimientos", 
        "Suele dejarme llevar por mis intuiciones", 
        "Si trabajo en grupo procuro que se siga un método y un orden", 
        "Con frecuencia me interesa averiguar lo que piensa la gente", 
        "Esquivo los temas subjetivos, ambiguos y poco claros"
    ]
    auxiliar = [preguntas, array_secciones, True]
    return auxiliar
    #return render_template('formulario.html', preguntas=preguntas, secciones= array_secciones, login= True)

@app.route('/procesar_encuesta', methods=['POST'])
def procesar_encuesta():
    respuestas  = {f'pregunta{i}': request.form.get(f'pregunta{i}') for i in range(1, 81)}
    login       = request.form.get('login')
    string_data = request.form['seccion'].strip("()")
    items       = string_data.split(", ")
    
    items = [item.strip("'") if item.startswith("'") and item.endswith("'") else int(item) if item.isdigit() else item for item in items]

    seccion      = items[1]
    especialidad = items[3]
    correo       = request.form.get('email')
    año          = items[5]

    array_respuestas = []
    str_respuesta    = ""

    for respuesta in respuestas.items():
        array_respuestas.append(int(respuesta[1]))
        str_respuesta += respuesta[1]
    try:
        resultados = [basedatos.obtener_resultados_ind( array_respuestas)]  
        if login == "True":
            basedatos.crear_respuestas_por_secciones(str_respuesta, seccion,  especialidad, año, correo)
            resultados = mostrar_resultados(seccion, especialidad, año, correo)            
        #resultados = basedatos.obtener_resultados(seccion, especialidad, año)

    except Exception as e:
        resultados = "Error"
    return render_template('resultados.html', data = resultados)


############################################################
######################base datos############################
######################secciones###########################
############################################################
    
    
@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    # Obtener los valores ingresados en los campos del formulario
    seccion      = request.form['seccion']
    especialidad = request.form['especialidad']
    curso        = request.form['curso']
    correoMaestro= request.form['correoMaestro']
    año          = request.form['año']
    usuario = basedatos.obtener_usuario(correoMaestro)
    try:
        basedatos.crear_seccion(seccion, curso, especialidad, correoMaestro, año)
    except Exception as e:
        flash("Error al registrar usuario")
    finally:
        flash("Sección Creada")
        #return redirect("/formulario")
    # Puedes redirigir a otra página o devolver una respuesta aquí
    return render_template('index.html', curso = curso, seccion = seccion, especialidad = especialidad, user=usuario[2])



############################################################
############Resultados a partir de seccion#######################
###################seccion, curso, año###########################
############################################################

#@app.route('/resultados')
def mostrar_resultados(seccion, especialidad, año, correo):
    #seccion = request.form.get('seccion')
    #especialidad = request.form.get('especialidad')
    #año = request.form.get('año')
    data = basedatos.obtener_resultados_por_alumno(seccion, especialidad, año)
    print(data)
    #return render_template('resultados.html', data=data)
    return data

##############Luego borrar esto porque es solo de prueba###############
###############para la modal visualizar seccion ######################
# Ejemplo de datos
secciones = [
    (1, 'A', 'Matemáticas', 'Profesor 1', 'maestro1@example.com', 2024),
    (2, 'B', 'Ciencias', 'Profesor 2', 'maestro2@example.com', 2024),
]

resultados_seccion = {
    'A': [{'activo': 10, 'reflexivo': 20, 'teorico': 30, 'pragmatico': 40}],
    'B': [{'activo': 15, 'reflexivo': 25, 'teorico': 35, 'pragmatico': 45}]
}

def index():
    secciones = basedatos.obtener_secciones()
    seccion = request.args.get('seccion')
    especialidad = request.args.get('especialidad')
    año = request.args.get('año')
    resultados = []

    if seccion and especialidad and año:
        resultados = basedatos.obtener_resultados_por_seccion(seccion, especialidad, año)

    return render_template('index.html', secciones=secciones, resultados=resultados)

@app.route('/visualizar', methods=['POST'])
def visualizar():
    string_data = request.form['seccion'].strip("()")  # Elimina los paréntesis
    items = string_data.split(", ")  # Divide los elementos por comas

    # Remueve las comillas de los elementos que son cadenas
    items = [item.strip("'") if item.startswith("'") and item.endswith("'") else int(item) if item.isdigit() else item for item in items]

    seccion = items[1]
    especialidad = items[3]
    email = items[4]
    año = items[5]
    resultados = []
    secciones = basedatos.obtener_secciones_por_maestro(email)
    usuario = basedatos.obtener_usuario(email)
    resultados = basedatos.obtener_resultados_por_seccion(seccion, especialidad, año)
    
    return render_template('index2.html',usuarios = obtener_usuarios(), secciones=secciones, resultados=resultados, user=usuario[2])
    #return resultados

@app.route('/actualizar_seccion', methods=['POST'])
def actualizar_seccion():
    # Lógica para actualizar la sección
    return redirect(url_for('index'))

###################################################################################
##################################Editar Secciones##########################
###################################################################################
def obtener_secciones():
    try:
        usuarios = basedatos.obtener_secciones()
        return(secciones)  # Imprime los usuarios en la consola para verificar
        #return render_template('index.html', usuarios=usuarios)
    except Exception as e:
        print("Error al obtener secciones:", e)
        return 0 # Imprime cualquier error en la consola
        #return render_template('error')  # Puedes crear una plantilla 'error.html' para mostrar mensajes de error al usuario
        
        
#modifical el parametro curso
@app.route('/modificar_seccion', methods=['POST'])
def modificar_seccion():
    if request.method == 'POST':
        try:
            curso = request.form['curso']
            seccion = request.form['seccion']
            basedatos.modificar_seccion(curso, seccion)
            flash("Usuario modificado exitosamente.")
        except Exception as e:
            flash("Error al modificar la sección: " + str(e))
    return redirect("/index")

if __name__ == '__main__':
    app.run(debug=True)