from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image
import os

def crear_examen(pdf_path, preguntas, instrucciones, logo_nombre, logo_width=200, logo_height=60):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    
    # Configuración de estilos
    styles = getSampleStyleSheet()

    # Cambiar aqui estilo de preguntas
    estilo_pregunta = ParagraphStyle(
        'pregunta',
        parent=styles['Normal'],
        fontSize=12, # Tamaño letra enunciado
        leading=14,
        leftIndent=0,
        spaceBefore=0,
        spaceAfter=6, 
        fontName='Helvetica-Bold' # Tipo de letra enunciado
    )
    estilo_respuesta = ParagraphStyle(
        'respuesta',
        parent=styles['Normal'],
        fontSize=12, # Tamaño letra de respuestas
        leading=14,
        leftIndent=0,
        spaceBefore=0,
        spaceAfter=0,
        fontName='Helvetica' # Tipo de letra respuestas
    )

    
    # Insertar Logo
    logo_path = os.path.join("logos", logo_nombre)
    if os.path.exists(logo_path):
        try:
            img = Image.open(logo_path)
            aspect_ratio = img.width / img.height
            logo_width = logo_height * aspect_ratio if logo_width is None else logo_width
            logo_height = logo_width / aspect_ratio if logo_height is None else logo_height
            x_position = (letter[0] - logo_width) / 2
            y_position = letter[1] - logo_height
            c.drawImage(logo_path, x_position, y_position, 
                       width=logo_width, height=logo_height, 
                       preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"Error al cargar el logo: {e}")

    # Función para títulos y color de letra general
    def titulo(texto, y):
        c.setFont("Helvetica-Bold", 14) # Tipo de letra y tamaño de titulos
        c.setFillColor(colors.grey) # Color de fondo titulos
        c.rect(50, y - 10, 500, 25, fill=1, stroke=0)
        c.setFillColor(colors.white) # Color letra titulos
        c.drawCentredString(300, y, texto)
        c.setFillColor(colors.black) # Color letra general
        return y - 40

    # Función mejorada de salto de página
    def verificar_salto(y_necesario, y_actual, titulo_seccion=None):
        if y_actual - y_necesario < 50: # El numero es el espacio minimo entre la última linea y el final de la página
            c.showPage()
            nuevo_y = 750
            if titulo_seccion:
                nuevo_y = titulo(titulo_seccion, nuevo_y)
            return nuevo_y
        return y_actual

    # Página 1: Formulario del alumno
    y = titulo("Formulario del Alumno", 660) # Aqui puedes cambiar el titulo de la sección (No cambies el num)
    c.setFont("Helvetica", 12) # Tipo y tamaño de letra del formulario
    
    campos = [
        ("Acción formativa:", "accion_formativa"),
        ("Fecha:", "fecha"),
        ("Docente:", "docente"),
        ("Alumno/a:", "alumno"),
        ("NIF Alumno/a:", "nif"),
        ("Calificación:", "calificacion"),
        ("Firma Alumno/a:", "firma_alumno"),
        ("Firma Docente:", "firma_docente"),
    ]
    
    for label, name in campos:
        y = verificar_salto(40, y)
        c.drawString(100, y, label)
        c.acroForm.textfield(name=name, x=250, y=y-5, width=200, height=15)
        y -= 40

    # Instrucciones
    y = titulo("Instrucciones", y) # Aqui puedes cambiar el titulo de la sección (No cambies la y)
    for i, instruccion in enumerate(instrucciones, 1):
        y = verificar_salto(20, y)
        para = Paragraph(f"{i}. {instruccion}", estilo_respuesta) # Las Instrucciones tienen el mismo estilo que las respuestas.
        w, h = para.wrap(400, 1000)
        para.drawOn(c, 120, y - h)
        y -= h + 15

    # Preguntas
    c.showPage()
    y = titulo("Preguntas", 750) # Aqui puedes cambiar el titulo de la sección (No cambies el num)
    
    for i, (pregunta_texto, opciones) in enumerate(preguntas.items(), 1):
        # Calcular alturas
        pregunta_para = Paragraph(f"{i}. {pregunta_texto}", estilo_pregunta)
        w_preg, h_preg = pregunta_para.wrap(500, 1000)
        
        respuestas = []
        for opcion in opciones:
            resp_para = Paragraph(opcion, estilo_respuesta)
            w_resp, h_resp = resp_para.wrap(450, 1000)
            respuestas.append((resp_para, h_resp))
        
        total_altura = h_preg + sum(h_resp + 15 for h_resp in [h for _, h in respuestas]) + 20
        
        # Verificar espacio
        y = verificar_salto(total_altura, y, "Preguntas")
        
        # Dibujar pregunta
        pregunta_para.drawOn(c, 100, y - h_preg)
        y -= h_preg + 15
        
        # Dibujar respuestas
        for j, (resp_para, h_resp) in enumerate(respuestas):
            c.acroForm.checkbox(name=f"q{i}_opt{j}", x=100, y=y - 12, size=12)
            resp_para.drawOn(c, 120, y - h_resp)
            y -= h_resp + 15
        
        y -= 40 # Espacio entre preguntas (cambia el num)

    c.save()



# CAMBIA AQUI LOS DATOS DEL EXAMEN

# Sigue siempre el mismo esquema.

# No cambies las palabras "preguntas" ni "instrucciones". Tampoco el nombre de la variable datos_examen

# datos_examen es un objeto {}. Los objetos {} estan compuestos de pares clave: valor. Cada par clave: valor se separa por comas.
# ejemplo de objeto:    persona = {nombre: Samuel, apellido: Elcure}.    persona es un objeto {} con las claves nombre y apellido y sus respectivos valores.

# "preguntas" e "instrucciones" son claves del objeto datos_examen: datos_examen = {"preguntas": {}, "instrucciones": []}
# Como puedes ver el valor de preguntas  es otro objeto {} y el de instrucciones una lista [].

# el objeto preguntas {}, tiene como clave el enunciado de la pregunta entre "". El valor es una lista [] de respuestas.
# Cada palabra en una lista [] tiene que ir con "" y separada por coma.

# ejemplo preguntas:     {"preguntas": {"enunciado": ["respuesaA", "respuestaB"], "enunciado2": ["respuestaA", "RespuestaB"]}}
# objeto preguntas ->                   |__clave__|: |__________valor__________|
# objeto datos_examen->   |__clave__|: |________________________________________valor_________________________________________|


# instrucciones es directamente una lista []. Cada frase o parrafo en la lista se separa por comas.

# Para que entiendas bien el formato de lo de abajo, si quitamos todo seria asi: 
#                                                    datos_examen = {"preguntas": {"enunciado1": ["RespuestaA", "RespuestaB"], "enunciado2": ["RespuestaA", "RespuestaB"]}, "instrucciones": ["Instruccion1", "Instrucción2"]}
# Claves: valores de preguntas ->                                                  |__clave___|: |_________valor____________|,  |__clave__|: |______________valor_______|
# Claves: valores de datos_examen ->                                |___clave__|: |_________________________________________valor________________________________________|, |____clave____|: |__________valor________________|


# Puedes poner el numero de respuestas por pregunta que quieras y el numero de preguntas que quieras. Tambien de instrucciones.


datos_examen = { # Se abre el objeto datos_examen.
    "preguntas": { # Se crea la clave "preguntas" y se le da un valor de objeto {} que se abre aquí
        "Explique en detalle el proceso de fotosíntesis y su importancia ecológica:": [ # "Enunciado de la pregunta": Se abre la lista respuestas []
            "Proceso biológico que convierte energía lumínica en química usando clorofila, agua y dióxido de carbono, liberando oxígeno como subproducto.", # pongo una , entre respuestas
            "Mecanismo fundamental para la vida en la Tierra que sustenta las cadenas tróficas y regula el clima global.",
            "Proceso metabólico inverso a la respiración celular que ocurre exclusivamente en organismos autótrofos.",
            "Sistema complejo de intercambio gaseoso que varía según las condiciones ambientales y la especie vegetal." # No se pone coma en la ultima respuesta
        ], # pongo una , entre preguntas y se cierra la lista respuestas []
        "Describa los principales factores que influyen en el cambio climático global:": [
            "Aumento de gases de efecto invernadero por actividades humanas como quema de combustibles fósiles y deforestación.",
            "Variaciones en la órbita terrestre y actividad solar que modifican los patrones climáticos a largo plazo.",
            "Cambios en los usos del suelo y prácticas agrícolas intensivas que afectan los ecosistemas naturales.",
            "Interacciones complejas entre sistemas oceánicos y atmosféricos que regulan la temperatura planetaria." # No se pone coma en la ultima respuesta
        ], 
        "Pregunta 3": [
            "RespuestaA", 
            "RespuestaB"
        ],
        "Pregunta 4": ["Respuesta A", "Respuesta B"] # No se pone coma al final de la última pregunta
    }, # Se cierra el objeto preguntas {} y pongo , para separarlo de instrucciones
    "instrucciones": [ # Se crea la clave "instrucciones y se le da valor de lista [] que se abre aqui.
        "Instrucción 1", # Cada apartado de instrucciones va entre "" y se separa por una coma.
        "Instrucción 2",
        "Instrucción 3: Puede ser perfectamente una linea larga o un párrafo.",
        "Instrucción 4: etc",
    ] # Se cierra lista instrucciones.
}

crear_examen("examen_avanzado11.pdf", # Cambiar aqui el nombre del pdf creado. Si guardas los pdfs aqui, cambia el nombre cada vez pq te dará fallo si intenta crear uno que ya existe.
            datos_examen["preguntas"], 
            datos_examen["instrucciones"], 
            "logo proyecto.png", # Nombre completo del archivo del logo entre "" (tiene que estar en la carpeta logos)
            logo_width=400, # Largo del logo (cambia el num)
            logo_height=120) # Alto del logo (cambia el num)

print("PDF generado con éxito!")