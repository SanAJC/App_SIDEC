from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from api.models import Denuncia
from api.utils.generar_pdf import generar_pdf_denuncia

#Celery task para enviar correo
@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def enviar_correo_denuncia(self, denuncia_id: int):
    try:
        denuncia = Denuncia.objects.get(id=denuncia_id)
    except Denuncia.DoesNotExist:
        return f"Denuncia con ID {denuncia_id} no encontrada."
    
    # Generar PDF
    pdf_bytes = generar_pdf_denuncia(denuncia)
    
    # Configurar correo
    email = EmailMessage(
        subject=f"Denuncia {denuncia.id}",
        body="Adjunto se encuentra la denuncia solicitada.",
        from_email=settings.EMAIL_HOST_USER,
        to=[denuncia.correo_destino],
        reply_to=[denuncia.email_usuario],
    )
    email.attach(f"denuncia_{denuncia.id}.pdf", pdf_bytes, "application/pdf")
    
    # Enviar correo
    email.send()
    return f"Correo enviado a {denuncia.correo_destino} con éxito."
