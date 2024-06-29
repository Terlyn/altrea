# -*- coding: utf-8 -*-
from flask import Flask, redirect, request, url_for, render_template, flash, session
from dotenv import load_dotenv
import basedatos
import os
import json
#source venv/bin/activate 
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1jd2Fxdm93Y2l0aWx0dGFmYW9pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTkxMDE4NzgsImV4cCI6MjAzNDY3Nzg3OH0.mvwNdoier6zEtLbXJhhS5CqBtGYMBM8U3YwRGyY8HLk'
, 'miclavesecreta')

# @app.before_request
# def before_request():
#     route = request.path
#     if 'usuario' not in session and route not in ["/entrar"]:
#         flash("Inicia sesión para continuar")
#         return redirect("/home")

@app.route("/inside")
def inside():
    return render_template("inside.html", usuarios=get_users())

@app.route("/login_page")
def login_page():
    return render_template("login_page.html")

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/student_login_page")
def student_login_page():
    return render_template("student_login_page.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['contraseña']

    try:
        user = basedatos.get_user(email)
    except Exception as e:
        flash("Error al obtener usuario")
        return redirect("/inside")

    if (user != None) and (user['clave'] == password) and (user['email'] == email):
        session['usuario'] = email
        sections = basedatos.get_sections_by_teacher(email)
        return render_template("inside.html", usuarios=get_users(), secciones=sections, user=user['email'])
    else:
        flash("Acceso denegado" if user else "Usuario no registrado")
        return redirect("/login_page")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Sesión cerrada")
    return redirect("/inside")

@app.route("/register_page")
def register_page():
    return render_template("register_page.html")

@app.route("/register", methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['contraseña']

    try:
        basedatos.register_user(email, password)
        flash("Bienvenido")
    except Exception as e:
        flash("Error al registrar usuario")
    return redirect("/inside")

@app.route("/change_password", methods=['POST'])
def change_password():
    try:
        email = request.form['email']
        new_password = request.form['nueva_clave']
        basedatos.change_password(email, new_password)
        flash("Contraseña modificada exitosamente.")
    except Exception as e:
        flash("Error al modificar contraseña: " + str(e))
    return redirect("/")

@app.route("/update_user", methods=['POST'])
def update_user():
    try:
        emails = request.form.getlist('email_')
        passwords = request.form.getlist('clave_')
        names = request.form.getlist('nombre_')

        for email, password, name in zip(emails, passwords, names):
            basedatos.update_user(email, password, name)
        flash("Usuario modificado exitosamente.")
    except Exception as e:
        flash("Error al modificar usuario: " + str(e))
    return redirect("/")

@app.route("/delete_user", methods=['POST'])
def delete_user():
    try:
        emails = request.form.getlist('email_')

        for email in emails:
            basedatos.delete_user(email)
        flash("Usuario(s) borrado(s) exitosamente.")
    except Exception as e:
        flash("Error al borrar usuario(s): " + str(e))
    return redirect("/")

@app.route("/register_student", methods=['POST'])
def register_student():
    email = request.form['emailRegistro']
    password = request.form['contraseñaRegistro']
    name = request.form['nombreRegistro']

    try:
        basedatos.register_student(email, password, name)
        flash("Bienvenido")
    except Exception as e:
        flash("Error al registrar usuario")
    return redirect("/student_login_page")

@app.route("/student_login", methods=["POST"])
def student_login():
    email = request.form['email']
    password = request.form['contraseña']

    student = basedatos.get_student(email, password)
    if student and student['password'] == password:
        questions_data = show_form_()
        return render_template('show_form.html', preguntas=questions_data[0], secciones=questions_data[1], login=questions_data[2], email=email)
    else:
        flash("Acceso denegado" if student else "Usuario no registrado")
    return redirect("/student_login_page")

@app.route('/show_form', methods=['GET'])
def show_form():
    sections = basedatos.get_sections()
    print(sections)
    questions = [
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
        "Me atrae experimentar y practicar las últimas técnicas y novedades",  
        "Soy cauteloso/a a la hora de sacar conclusiones",  
        "Prefiero contar con el mayor número de fuentes de información. Cuantos más datos reúna para reflexionar, mejor.",  
        "Tiendo a ser perfeccionista",  
        "Prefiero oír las opiniones de los demás antes de exponer la mía",  
        "Me gusta afrontar la vida espontáneamente y no tener que planificar todo previamente",  
        "En las discusiones me gusta observar cómo actúan los demás participantes",  
        "Me siento incómodo/a con las personas calladas y demasiado analíticas",  
        "Juzgo con frecuencia las ideas de los demás por su valor práctico",  
        "Me agobio si me obligan a acelerar mucho el trabajo para cumplir un plazo",  
        "En las reuniones apoyo las ideas prácticas y realistas",  
        "Es mejor gozar del momento presente que deleitarse pensando en el pasado o en el futuro",  
        "Me molestan las personas que siempre desean apresurar las cosas",  
        "Aporto ideas nuevas y espontáneas en los grupos de discusión",  
        "Pienso que son más consistentes las decisiones fundamentadas en un minucioso análisis que las basadas en la intuición",  
        "Detecto frecuentemente la inconsistencia y puntos débiles en las argumentaciones de los demás",  
        "Creo que es preciso saltarse las normas muchas más veces que cumplirlas",  
        "A menudo caigo en la cuenta de otras formas mejores y más prácticas de hacer las cosas",  
        "En conjunto hablo más que escucho",  
        "Prefiero distanciarme de los hechos y observarlos desde otras perspectivas",  
        "Estoy convencido/a que debe imponerse la lógica y el razonamiento",  
        "Me gusta buscar nuevas experiencias",  
        "Me gusta experimentar y aplicar las cosas",  
        "Pienso que debemos llegar pronto al grano, al meollo de los temas.",  
        "Siempre trato de conseguir conclusiones e ideas claras",
        "Prefiero discutir cuestiones concretas y no perder el tiempo con pláticas superficiales", 
        "Me impaciento cuando me dan explicaciones irrelevantes e incoherentes", 
        "Compruebo antes si las cosas funcionan realmente", 
        "Hago varios borradores antes de la redacción definitiva de un trabajo", 
        "Soy consciente de que en las discusiones ayudo a mantener a los demás centrados en el tema, evitando divagaciones", 
        "Observo que, con frecuencia, soy uno/a de los/as más objetivos/as y desapasionados/as en las discusiones", 
        "Cuando algo va mal, le quito importancia y trato de hacerlo mejor", 
        "Rechazo ideas originales y espontáneas si no las veo prácticas", 
        "Me gusta sopesar diversas alternativas antes de tomar una decisión", 
        "Con frecuencia miro hacia adelante para prever el futuro", 
        "En los debates y discusiones prefiero desempeñar un papel secundario antes que ser el/la líder o el/la que más participa", 
        "Me molestan las personas que no actúan con lógica", 
        "Me resulta incómodo tener que planificar y prever las cosas", 
        "Creo que el fin justifica los medios en muchos casos", 
        "Suelo reflexionar sobre los asuntos y problemas", 
        "El trabajar a conciencia me llena de satisfacción y orgullo", 
        "Ante los acontecimientos trato de descubrir los principios y teorías en que se basan", 
        "Con tal de conseguir el objetivo que pretendo soy capaz de herir sentimientos ajenos", 
        "No me importa hacer todo lo necesario para que sea efectivo mi trabajo", 
        "Con frecuencia soy una de las personas que más anima las fiestas", 
        "Me aburro enseguida con el trabajo metódico y minucioso", 
        "La gente con frecuencia cree que soy poco sensible a sus sentimientos", 
        "Suelo dejarme llevar por mis intuiciones", 
        "Si trabajo en grupo procuro que se siga un método y un orden", 
        "Con frecuencia me interesa averiguar lo que piensa la gente", 
        "Esquivo los temas subjetivos, ambiguos y poco claros"
    ]
    return render_template('show_form.html', preguntas=questions, secciones=sections, login=False)

def show_form_():
    array_secciones = basedatos.get_sections()
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


@app.route('/process_survey', methods=['POST'])
def process_survey():
    responses = {'pregunta{}'.format(i): request.form.get('pregunta{}'.format(i)) for i in range(1, 81)}
    login = request.form.get('login')
    string_data = request.form['seccion'].strip("()")
    # Reemplazar comillas simples por comillas dobles
    corrected_string = string_data.replace("'", '"')
    json_obj = json.loads(corrected_string)
    # items = string_data.split(", ")
    # items = [item.strip("'") if item.startswith("'") and item.endswith("'") else int(item) if item.isdigit() else item for item in items]

    section = json_obj['section']
    specialty = json_obj['specialty']
    email = request.form.get('email')
    year = json_obj['year']

    response_array = []
    str_response = ""

    for response in responses.items():
        response_array.append(int(response[1]))
        str_response += response[1]
    try:
        results = [basedatos.get_individual_results(response_array)]
        if login == "True":
            basedatos.create_section_responses(str_response, section, specialty, year, email)
            results =  basedatos.get_results_by_student(section, specialty, year)
    except Exception as e:
        results = "Error"

    return render_template('results.html', data=results)

@app.route('/process_form', methods=['POST'])
def process_form():
    section = request.form['seccion']
    specialty = request.form['especialidad']
    course = request.form['curso']
    teacher_email = request.form['correoMaestro']
    year = request.form['año']
    user = basedatos.get_user(teacher_email)

    try:
        basedatos.create_section(section, course, specialty, teacher_email, year)
        flash("Sección Creada")
    except Exception as e:
        flash("Error al crear sección")
    return render_template('inside.html', curso=course, seccion=section, especialidad=specialty, user=user['email'])

@app.route('/visualize', methods=['POST'])
def visualize():
    string_data = request.form['seccion'].strip("()")

    corrected_string = string_data.replace("'", '"')
    json_obj = json.loads(corrected_string)
    section = json_obj['section']
    specialty = json_obj['specialty']
    email = json_obj['email_teacher']
    # email = request.form.get('email')
    year = json_obj['year']

    results = basedatos.get_results_by_section(section, specialty, year)
    sections = basedatos.get_sections_by_teacher(email)
    user = basedatos.get_user(email)

    return render_template('visualize.html', usuarios=get_users(), secciones=sections, resultados=results, user=user['email'])

@app.route('/update_section', methods=['POST'])
def update_section():
    return redirect(url_for('inside'))

@app.route('/modify_section', methods=['POST'])
def modify_section():
    try:
        course = request.form['curso']
        section = request.form['seccion']
        basedatos.modify_section(course, section)
        flash("Sección modificada exitosamente.")
    except Exception as e:
        flash("Error al modificar la sección: " + str(e))
    return redirect("/inside")

def get_users():
    try:
        users = basedatos.get_users()
        return users
    except Exception as e:
        print("Error al obtener usuarios:", e)
        return []

def get_sections():
    try:
        sections = basedatos.get_sections()
        return sections
    except Exception as e:
        print("Error al obtener secciones:", e)
        return []

if __name__ == '__main__':
    app.run(debug=True)
