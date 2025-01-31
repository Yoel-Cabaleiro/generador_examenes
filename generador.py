from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph, Frame
from PIL import Image
import os

def crear_examen(pdf_path, preguntas, instrucciones, logo_nombre, logo_width=200, logo_height=60):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    
    # Insertar Logo
    logo_path = os.path.join("logos", logo_nombre)
    if os.path.exists(logo_path):
        try:
            img = Image.open(logo_path)
            aspect_ratio = img.width / img.height
            if logo_width is None:
                logo_width = logo_height * aspect_ratio
            if logo_height is None:
                logo_height = logo_width / aspect_ratio
            x_position = (letter[0] - logo_width) / 2
            y_position = letter[1] - logo_height  # Pegado a la parte superior
            c.drawImage(logo_path, x_position, y_position, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"Error al cargar el logo: {e}")
    
    # Estilo de título y color de letra general
    def titulo(texto, y):
        c.setFont("Helvetica-Bold", 14)  # Tipo de letra del titulo y tamaño
        c.setFillColor(colors.grey) # Color de fondo de los titulos
        c.rect(50, y - 10, 500, 25, fill=1, stroke=0)
        c.setFillColor(colors.white) # Color de letra de los titulos
        c.drawCentredString(300, y, texto)
        c.setFillColor(colors.black) # Color de letra general
        return y - 40
    
    # Función para verificar si es necesario un salto de página
    def verificar_salto_de_pagina(y, espacio_necesario):
        if y - espacio_necesario < 100:  # Si no hay suficiente espacio para la próxima pregunta
            c.showPage()  # Crea una nueva página
            return 750  # Resetea la posición 'y' en la nueva página (a un valor adecuado)
        return y
    
    # Página 1: Formulario del alumno
    y = titulo("Formulario del Alumno", 660) # Aqui puedes cambiar el título de la sección
    c.setFont("Helvetica", 12) # Tipo y tamaño de letra del formulario del alumno
    
    # Aqui cambias los campos del formulario.
    # El primer parámetro es como lo ve el usuario y el segundo el valor.
    # Dale valores como en el ejemplo que ves, siempre en minuscula, sin acentos y sin espacios, usa _
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
        c.drawString(100, y, label)
        c.acroForm.textfield(name=name, x=250, y=y-5, width=200, height=15)
        y -= 40
        y = verificar_salto_de_pagina(y, 40)  
    
    # Sección de Instrucciones
    y = titulo("Instrucciones", y) # Aqui puedes cambiar el título de la sección
    for i, instruccion in enumerate(instrucciones, start=1):
        c.setFont("Helvetica", 12) # Tipo y tamaño de letra de la lista de instrucciones
        c.drawString(120, y, f"{i}. {instruccion}") 
        y -= 20
        y = verificar_salto_de_pagina(y, 20)  # Verifica si es necesario un salto de página
    
    c.showPage()  # Nueva página
    
    # Página 2: Preguntas
    y = titulo("Preguntas", 750) # Aqui puedes cambiar el título de la sección
    for i, (pregunta, opciones) in enumerate(preguntas.items(), start=1):
        # Primero calculamos el espacio necesario para la pregunta
        espacio_pregunta = 20  # Espacio de título de la pregunta
        espacio_respuestas = 20 * len(opciones)  # Cada opción ocupa 20 unidades de altura
        
        # Verificar si la pregunta y sus respuestas caben en la página
        y = verificar_salto_de_pagina(y, espacio_pregunta + espacio_respuestas)
        
        c.setFont("Helvetica-Bold", 12) # Tipo y tamaño de letra del enunciado
        c.drawString(100, y, f"{i}. {pregunta}")
        c.setFont("Helvetica", 12) # Tipo y tamaño de letra de las respuestas
        y -= 20
        
        # Dibujar las opciones de respuesta
        for j, opcion in enumerate(opciones):
            c.drawString(120, y, f"({chr(65 + j)}) {opcion}")
            c.acroForm.checkbox(name=f"q{i}_opt{j}", x=100, y=y-2, size=12)
            y -= 20
        
        y -= 10  # Espaciado entre preguntas, las puedes separar mas o menos con este número
        y = verificar_salto_de_pagina(y, 10)  # Verifica si es necesario un salto de página
    
    c.save()

# Datos del examen. Aquí cambias los datos del examen. Tiene que estar SIEMPRE en este formato.
# Todo es imprtante. Las palabras y frases tienen que estar siempre entre comillas "" / Las lineas tienen que estar separadas por ,
# Las Preguntas y las respuestas tienen que estar separadas por :
# Las respuestas van en una lista []
# Las palabras o frases dentro de la lista [] de respuestas tienen que estar separadas por , (no se pone coma despues de la última palabra de la lista) 
# Puedes poner el número de respuestas que quieras por pregunta y el número de preguntas que quieras.
# Cada linea separada por , de las instrucciones se crea como una lista visual. 
# NO cambies las palabras "preguntas" e "instrucciones".
datos_examen = {
    "preguntas": {
        "¿Cuál es la capital de Francia?": ["París", "Madrid", "Berlín", "Roma"],
        "¿Cuánto es 2 + 2?": ["3", "4", "5", "6"],
        "¿Cuál es la capital de España?": ["París", "Madrid", "Berlín", "Roma"],
        "¿Cuánto es 2 + 3?": ["3", "4", "5", "6"],
    },
    "instrucciones": [
        "Lee atentamente cada pregunta antes de responder.",
        "Marca la respuesta correcta en cada pregunta.",
        "Entrega el examen una vez finalizado.",
    ]
}

# Generar el PDF. Aquí cambias tanto el nombre del pdf final (primer argumento), 
# como los parametros del logo (últimos 3 argumentos: nombre, ancho y alto). El nombre tiene que estar escrito exactamente igual.
# EL logo tiene que estar dentro de la carpeta logos.
crear_examen("examen_interactivo1231.pdf", datos_examen["preguntas"], datos_examen["instrucciones"], "logo proyecto.png", logo_width=400, logo_height=120)

# Se imprime un mensaje en la consola diciendote que el proceso ha acabado.
print("PDF generado exitosamente.")
