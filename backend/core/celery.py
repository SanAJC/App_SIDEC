import os
from celery import Celery

# Configurar Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Usar configuración de Django con namespace 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-descubrir tareas en todas las apps instaladas
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')