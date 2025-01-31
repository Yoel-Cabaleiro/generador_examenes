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
    
    # Estilo de título
    def titulo(texto, y):
        c.setFillColor(colors.grey)
        c.rect(50, y - 10, 500, 25, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.drawCentredString(300, y, texto)
        c.setFillColor(colors.black)
        return y - 40
    
    # Página 1: Formulario del alumno
    y = titulo("Formulario del Alumno", 660)
    c.setFont("Helvetica", 12)
    
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
    
    # Sección de Instrucciones
    y = titulo("Instrucciones", y)
    for i, instruccion in enumerate(instrucciones, start=1):
        c.drawString(120, y, f"{i}. {instruccion}")
        y -= 20
    
    c.showPage()  # Nueva página
    
    # Página 2: Preguntas
    y = titulo("Preguntas", 750)
    for i, (pregunta, opciones) in enumerate(preguntas.items(), start=1):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y, f"{i}. {pregunta}")
        c.setFont("Helvetica", 12)
        y -= 20
        
        for j, opcion in enumerate(opciones):
            c.drawString(120, y, f"({chr(65 + j)}) {opcion}")
            c.acroForm.checkbox(name=f"q{i}_opt{j}", x=100, y=y-2, size=12)
            y -= 20
        
        y -= 10  # Espaciado entre preguntas
    
    c.save()

def hacer_interactivo(pdf_path):
    from pdfrw import PdfReader, PdfWriter, IndirectPdfDict
    pdf = PdfReader(pdf_path)
    for page in pdf.pages:
        if "/Annots" in page:
            for annot in page["/Annots"]:
                annot.update(IndirectPdfDict(Ff=0))  # Hacer los campos editables
    PdfWriter(pdf_path, trailer=pdf).write()

# Datos del examen
datos_examen = {
    "preguntas": {
        "¿Cuál es la capital de Francia?": ["París", "Madrid", "Berlín", "Roma"],
        "¿Cuánto es 2 + 2?": ["3", "4", "5", "6"],
    },
    "instrucciones": [
        "Lee atentamente cada pregunta antes de responder.",
        "Marca la respuesta correcta en cada pregunta.",
        "Entrega el examen una vez finalizado.",
    ]
}

# Generar el PDF con un logo seleccionado y dimensiones ajustables
crear_examen("examen_interactivo9.pdf", datos_examen["preguntas"], datos_examen["instrucciones"], "logo proyecto.png", logo_width=400, logo_height=120)
print("PDF generado exitosamente.")
