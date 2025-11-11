# SIDEC - Sistema de Denuncias y Quejas Ciudadanas

Una plataforma web segura y transparente que permite a los ciudadanos denunciar abusos o malas prácticas de funcionarios públicos de forma confidencial y sencilla.

## 🚀 Características Principales

### Frontend (Vue.js)
- **Interfaz moderna y responsiva** construida con Vue 3 y Composition API
- **Diseño intuitivo** con componentes reutilizables y estilos CSS modernos
- **Gestión de estado** con sistema de autenticación reactivo
- **Formularios dinámicos** para creación de denuncias con generación de PDF
- **Dashboard personalizado** para gestión de denuncias del usuario
- **Navegación inteligente** que adapta el contenido según el estado de autenticación

### Backend (Django REST Framework)
- **API RESTful** robusta y bien documentada
- **Autenticación segura** con JWT y cookies HTTP-only
- **Gestión de usuarios** con perfiles y permisos diferenciados
- **Sistema de denuncias** con estado de seguimiento (pendiente, enviado, error)
- **Generación de PDFs** automática para cada denuncia
- **Envío de correos** asíncrono con Celery y Redis

## 🔧 Tecnologías Utilizadas

### Frontend
- **Vue.js 3** - Framework progresivo de JavaScript
- **Vue Router** - Sistema de enrutamiento
- **Axios** - Cliente HTTP para comunicación con el backend
- **jsPDF** - Generación de documentos PDF en el cliente
- **CSS3** - Estilos modernos y responsivos

### Backend
- **Django 4** - Framework web de alto nivel
- **Django REST Framework** - Toolkit para construir APIs web
- **PostgreSQL** - Base de datos relacional
- **Redis** - Almacenamiento en caché y cola de mensajes
- **Celery** - Sistema de procesamiento asíncrono
- **Simple JWT** - Autenticación con tokens JWT

### Servicios Externos
- **Servidor SMTP** - Para envío de correos electrónicos
- **Almacenamiento en la nube** - Para archivos adjuntos (configurable)

## 📋 Módulos del Sistema

### 1. Autenticación (`authentication/`)
```python
# Modelos principales
- User: Usuario del sistema con email como identificador principal
- UserProfile: Perfil extendido con información adicional

# Endpoints principales
- POST /api/auth/register/ - Registro de nuevos usuarios
- POST /api/auth/login/ - Inicio de sesión
- POST /api/auth/logout/ - Cierre de sesión
- GET /api/auth/profile/ - Obtener perfil del usuario
- PUT /api/auth/profile/ - Actualizar perfil
- POST /api/auth/refresh/ - Refrescar token JWT
```

**Características de seguridad:**
- Tokens JWT con expiración configurable
- Cookies HTTP-only para almacenar refresh tokens
- Protección CSRF implementada
- Validación de contraseñas seguras
- Rate limiting en endpoints críticos

### 2. API de Denuncias (`api/`)
```python
# Modelos principales
- Entidad: Instituciones gubernamentales destinatarias
- Denuncia: Formulario de denuncia con estado de seguimiento

# Endpoints principales
- GET /api/entidades/ - Listar entidades disponibles
- GET /api/denuncias/ - Listar denuncias del usuario
- POST /api/denuncias/ - Crear nueva denuncia
- GET /api/denuncias/{id}/ - Detalles de denuncia específica
```

**Características del módulo:**
- Validación de datos de entrada
- Generación automática de PDFs
- Envío de correos asíncrono
- Historial de cambios de estado
- Filtros por fecha y estado

### 3. Servicios de Notificación (`services/`)
```python
# Sistema de colas con Celery
- enviar_correo_denuncia: Envía email con PDF adjunto
- generar_pdf_denuncia: Genera PDF de la denuncia
- actualizar_estado_denuncia: Actualiza estado y notifica
```

**Características del servicio:**
- Procesamiento asíncrono de tareas pesadas
- Reintentos automáticos en caso de fallo
- Monitoreo de estado de tareas
- Logs detallados de operaciones

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+

### Backend (Django)
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/App_SIDEC.git
cd App_SIDEC/backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor de desarrollo
python manage.py runserver

# Ejecutar worker de Celery (en terminal separada)
celery -A core worker -l info

# Ejecutar scheduler de Celery (en terminal separada)
celery -A core beat -l info
```

### Frontend (Vue.js)
```bash
# Navegar al directorio frontend
cd App_SIDEC/frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env
# Editar .env con la URL del backend

# Ejecutar servidor de desarrollo
npm run serve

# Construir para producción
npm run build
```

## 📊 Flujo de Trabajo

### 1. Registro de Usuario
```
Usuario → Formulario de Registro → Validación → Creación de Cuenta → Email de Bienvenida
```

### 2. Creación de Denuncia
```
Usuario Autenticado → Formulario de Denuncia → Validación → Generación PDF → Envío Email → Confirmación
```

### 3. Procesamiento de Denuncia
```
Denuncia Creada → Estado: Pendiente → Envío Asíncrono → Estado: Enviado/Error → Notificación
```

## 🔐 Seguridad

### Medidas Implementadas
- **Encriptación de contraseñas** con bcrypt
- **Validación de entrada** en todos los formularios
- **Rate limiting** para prevenir ataques de fuerza bruta
- **CORS configurado** para dominios específicos
- **Headers de seguridad** HTTP implementados(para produccion)
- **Sanitización** de datos antes de almacenarlos

### Privacidad de Datos
- Los correos electrónicos se almacenan de forma segura
- Los documentos adjuntos se procesan de forma segura
- No se comparte información personal con terceros
- Cumplimiento con regulaciones de protección de datos

## 📈 Monitoreo y Mantenimiento

### Logs y Auditoría
- Registro de todas las operaciones críticas
- Monitoreo de intentos de acceso fallidos
- Auditoría de cambios en denuncias
- Trazabilidad completa de acciones

### Métricas Disponibles
- Número de denuncias por período
- Tasa de éxito en envío de correos
- Tiempo promedio de procesamiento
- Usuarios activos por mes

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Contacto

Para soporte o consultas:
- Email: soporte@sidec.gob.mx
- Teléfono: +52 (55) 1234-5678
- Dirección: Av. Principal 123, Ciudad de México

## 🙏 Agradecimientos

- Equipo de desarrollo de SIDEC
- Comunidad de código abierto
- Colaboradores y testers beta

---

**Nota**: Este sistema fue desarrollado para promover la transparencia y la rendición de cuentas en el sector público. Su uso debe estar alineado con los principios de legalidad, objetividad y respeto a los derechos humanos.