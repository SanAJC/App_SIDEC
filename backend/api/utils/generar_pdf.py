from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.conf import settings
import os
from api.models import Denuncia

def generar_pdf_denuncia(denuncia: Denuncia) -> bytes:
    """
    Genera el PDF de la denuncia y retorna los bytes, sin guardar aún.
    """
    from io import BytesIO
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin = 50

    if denuncia.entidad.logo:
        logo_path = denuncia.entidad.logo.path
        try:
            c.drawImage(logo_path, margin, height - margin - 50, width=100, height=50, preserveAspectRatio=True)
        except Exception as e:
            pass

    # Escribir encabezados
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin + 110, height - margin - 20, denuncia.entidad.nombre)
    c.setFont("Helvetica", 12)
    c.drawString(margin, height - margin - 80, f"Asunto: {denuncia.asunto}")
    c.drawString(margin, height - margin - 100, f"Usuario denunciante (email): {denuncia.email_usuario}")

    # Detalles del cuerpo
    text_object = c.beginText()
    text_object.setTextOrigin(margin, height - margin - 140)
    text_object.setFont("Helvetica", 11)
    for line in denuncia.cuerpo.splitlines():
        text_object.textLine(line)
    c.drawText(text_object)

    # Pie de página
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(margin, 40, f"Fecha de creación: {denuncia.fecha_creacion.strftime('%Y-%m-%d %H:%M')}")
    c.drawString(margin, 25, f"Radicado ID: {denuncia.id}")

    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
