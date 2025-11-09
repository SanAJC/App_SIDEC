<template>
  <div class="report-page">
    <div class="topbar container">
      <div class="brand">
        <img src="@/assets/images/logo_max.png" alt="SIDEC" class="brand-logo" />
      </div>
      <div class="top-actions">
        <router-link to="/" class="btn light">Inicio</router-link>
        <router-link to="/dashboard" class="btn light">Volver al Panel</router-link>
      </div>
    </div>

    <div class="card container">
      <div class="card-head">
        <h1>Formulario de Denuncia o Queja</h1>
        <p class="muted">{{ selectedEntityName }} · Complete todos los campos requeridos</p>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="loading-msg">Cargando entidades...</div>

      <!-- Formulario -->
      <form v-else class="form" @submit.prevent="onSubmit">
        <div class="field">
          <label>Entidad destino <span class="req">*</span></label>
          <select v-model="form.entidad_id" @change="onEntityChange" required>
            <option value="" disabled>Seleccione una entidad</option>
            <option v-for="e in entidades" :key="e.id" :value="e.id">
              {{ e.nombre }}
            </option>
          </select>
          <small v-if="selectedEntity" class="info-text">
            📧 Correo de destino: {{ selectedEntity.email }}
            <br>
            📄 El PDF de la denuncia será enviado a este correo
          </small>
        </div>

        <div class="field">
          <label>Asunto <span class="req">*</span></label>
          <input 
            v-model="form.asunto" 
            type="text" 
            placeholder="Resuma su denuncia en pocas palabras" 
            maxlength="255"
            required 
          />
        </div>

        <div class="field">
          <label>Cuerpo <span class="req">*</span></label>
          <textarea 
            v-model="form.cuerpo" 
            rows="6" 
            placeholder="Describa los hechos de manera clara y detallada" 
            required
          ></textarea>
        </div>

        <div class="field">
          <label>Detalle</label>
          <textarea 
            v-model="form.detalle" 
            rows="4" 
            placeholder="Información adicional relevante (opcional)"
          ></textarea>
        </div>

        <div class="actions">
          <router-link to="/dashboard" class="btn light">Cancelar</router-link>
          <button 
            type="submit" 
            class="btn primary" 
            :disabled="submitting || !form.entidad_id || !form.asunto || !form.cuerpo"
          >
            {{ submitting ? 'Generando PDF y enviando...' : 'Enviar Denuncia' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getEntidades, createDenuncia } from '@/api/entities'
import auth from '@/stores/auth'
import jsPDF from 'jspdf'

const route = useRoute()
const router = useRouter()

// Estados
const loading = ref(true)
const submitting = ref(false)
const entidades = ref([])

// Formulario
const form = ref({
  entidad_id: '',
  asunto: '',
  cuerpo: '',
  detalle: ''
})

// Entidad seleccionada
const selectedEntity = computed(() => {
  if (!form.value.entidad_id) return null
  return entidades.value.find(e => e.id === form.value.entidad_id)
})

// Nombre de entidad seleccionada
const selectedEntityName = computed(() => {
  return selectedEntity.value?.nombre || 'Complete todos los campos requeridos'
})

// Cargar entidades al montar
onMounted(async () => {
  await fetchEntidades()
  preselectEntity()
})

// Obtener entidades desde la API
async function fetchEntidades() {
  try {
    loading.value = true
    const response = await getEntidades()
    entidades.value = response.data || []
  } catch (error) {
    console.error('Error al cargar entidades:', error)
    alert('Error al cargar las entidades. Por favor, intente nuevamente.')
    entidades.value = []
  } finally {
    loading.value = false
  }
}

// Pre-seleccionar entidad desde query params
function preselectEntity() {
  const entityParam = route.query.entity
  if (!entityParam || !entidades.value.length) return
  
  // Buscar por ID numérico
  const entityId = parseInt(entityParam)
  if (!isNaN(entityId)) {
    const found = entidades.value.find(e => e.id === entityId)
    if (found) {
      form.value.entidad_id = found.id
      return
    }
  }
  
  // Buscar por nombre (si viene como texto)
  const entityName = entityParam.toString().toLowerCase()
  const found = entidades.value.find(e => 
    e.nombre.toLowerCase().includes(entityName)
  )
  if (found) {
    form.value.entidad_id = found.id
  }
}

// Cuando cambia la entidad seleccionada
function onEntityChange() {
  console.log('Entidad seleccionada:', selectedEntity.value)
}

// Función para generar PDF
function generarPDF() {
  const doc = new jsPDF()
  const pageWidth = doc.internal.pageSize.getWidth()
  const margin = 20
  const maxWidth = pageWidth - (margin * 2)
  let yPos = 20

  // Título
  doc.setFontSize(18)
  doc.setFont(undefined, 'bold')
  doc.text('FORMULARIO DE DENUNCIA', pageWidth / 2, yPos, { align: 'center' })
  yPos += 15

  // Línea separadora
  doc.setLineWidth(0.5)
  doc.line(margin, yPos, pageWidth - margin, yPos)
  yPos += 10

  // Información de la entidad
  doc.setFontSize(12)
  doc.setFont(undefined, 'bold')
  doc.text('ENTIDAD DESTINO:', margin, yPos)
  yPos += 7
  doc.setFont(undefined, 'normal')
  doc.text(selectedEntity.value?.nombre || 'N/A', margin, yPos)
  yPos += 5
  doc.setFontSize(10)
  doc.text(`Correo: ${selectedEntity.value?.email || 'N/A'}`, margin, yPos)
  yPos += 10

  // Usuario denunciante
  doc.setFontSize(12)
  doc.setFont(undefined, 'bold')
  doc.text('DENUNCIANTE:', margin, yPos)
  yPos += 7
  doc.setFont(undefined, 'normal')
  const userEmail = auth.state.user?.email || auth.state.user?.username + '@usuario.com'
  doc.text(`Email: ${userEmail}`, margin, yPos)
  yPos += 7
  const fechaActual = new Date().toLocaleString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
  doc.text(`Fecha: ${fechaActual}`, margin, yPos)
  yPos += 12

  // Asunto
  doc.setFontSize(12)
  doc.setFont(undefined, 'bold')
  doc.text('ASUNTO:', margin, yPos)
  yPos += 7
  doc.setFont(undefined, 'normal')
  const asuntoLines = doc.splitTextToSize(form.value.asunto, maxWidth)
  doc.text(asuntoLines, margin, yPos)
  yPos += (asuntoLines.length * 7) + 8

  // Cuerpo de la denuncia
  doc.setFontSize(12)
  doc.setFont(undefined, 'bold')
  doc.text('DESCRIPCIÓN DE LOS HECHOS:', margin, yPos)
  yPos += 7
  doc.setFont(undefined, 'normal')
  doc.setFontSize(11)
  const cuerpoLines = doc.splitTextToSize(form.value.cuerpo, maxWidth)
  
  // Verificar si necesitamos nueva página
  cuerpoLines.forEach((line) => {
    if (yPos > 270) {
      doc.addPage()
      yPos = 20
    }
    doc.text(line, margin, yPos)
    yPos += 6
  })
  yPos += 8

  // Detalle (si existe)
  if (form.value.detalle && form.value.detalle.trim()) {
    if (yPos > 250) {
      doc.addPage()
      yPos = 20
    }
    doc.setFontSize(12)
    doc.setFont(undefined, 'bold')
    doc.text('INFORMACIÓN ADICIONAL:', margin, yPos)
    yPos += 7
    doc.setFont(undefined, 'normal')
    doc.setFontSize(11)
    const detalleLines = doc.splitTextToSize(form.value.detalle, maxWidth)
    
    detalleLines.forEach((line) => {
      if (yPos > 270) {
        doc.addPage()
        yPos = 20
      }
      doc.text(line, margin, yPos)
      yPos += 6
    })
  }

  // Footer en cada página
  const totalPages = doc.internal.pages.length - 1
  for (let i = 1; i <= totalPages; i++) {
    doc.setPage(i)
    doc.setFontSize(8)
    doc.setTextColor(128)
    doc.text(
      `Página ${i} de ${totalPages} - Generado por SIDEC`,
      pageWidth / 2,
      doc.internal.pageSize.getHeight() - 10,
      { align: 'center' }
    )
  }

  // Retornar el PDF como blob
  return doc.output('blob')
}

// Enviar denuncia
async function onSubmit() {
  // Validar que el usuario esté autenticado
  if (!auth.state.user) {
    alert('Debe iniciar sesión para enviar una denuncia')
    router.push('/login')
    return
  }

  // Validar campos requeridos
  if (!form.value.entidad_id || !form.value.asunto || !form.value.cuerpo) {
    alert('Por favor complete todos los campos requeridos')
    return
  }

  // Validar que tengamos el email del usuario
  const userEmail = auth.state.user.email || auth.state.user.username + '@usuario.com'
  
  try {
    submitting.value = true

    // Generar PDF
    console.log('Generando PDF...')
    const pdfBlob = generarPDF()
    
    // Crear FormData para enviar archivo y datos
    const formData = new FormData()
    formData.append('entidad_id', form.value.entidad_id)
    formData.append('asunto', form.value.asunto.trim())
    formData.append('cuerpo', form.value.cuerpo.trim())
    formData.append('email_usuario', userEmail)
    formData.append('detalle', form.value.detalle.trim() || '')
    formData.append('correo_destino', selectedEntity.value?.email || '')
    
    // Agregar el PDF con nombre descriptivo
    const pdfFileName = `denuncia_${Date.now()}.pdf`
    formData.append('pdf', pdfBlob, pdfFileName)

    console.log('Enviando denuncia con PDF...')

    // Enviar al backend
    const response = await createDenuncia(formData)
    
    console.log('Denuncia creada exitosamente:', response.data)
    
    // Mostrar mensaje de éxito
    alert('✅ Denuncia enviada correctamente con PDF adjunto. Será procesada en breve.')
    
    // Redirigir al dashboard
    router.push('/dashboard')
    
  } catch (error) {
    console.error('Error al enviar denuncia:', error)
    
    // Manejo de errores específicos
    if (error.response) {
      const errorData = error.response.data
      console.error('Detalles del error:', errorData)
      
      if (error.response.status === 401) {
        alert('Su sesión ha expirado. Por favor, inicie sesión nuevamente.')
        router.push('/login')
      } else if (error.response.status === 400) {
        // Errores de validación
        const errorMsg = Object.entries(errorData)
          .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
          .join('\n')
        alert(`Error de validación:\n${errorMsg}`)
      } else {
        alert('Error al enviar la denuncia. Por favor, verifique los datos e intente nuevamente.')
      }
    } else {
      alert('Error de conexión. Verifique su conexión a internet e intente nuevamente.')
    }
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.report-page{ background:#f6f7f9; min-height:100vh; padding: 24px 0 48px; }
.container{ max-width: 1080px; margin: 0 auto; padding-left: 30px; padding-right: 30px; }
.topbar{ margin-bottom: 6px; display:flex; justify-content: space-between; align-items:center; }
.brand{ display:flex; align-items:center; gap:8px; }
.brand-logo{ width:auto; height:30px; display:block; object-fit: cover; }
.top-actions{ display:flex; gap:10px; }

.loading-msg{ 
  text-align:center; 
  padding:60px 20px; 
  color:#6b7280; 
  font-size:1.1rem; 
}

.card{
  margin-top: 12px;
  background:#fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 1px 2px rgba(16,24,40,.04), 0 1px 3px rgba(16,24,40,.06);
  padding: 18px 18px 24px;
}
.card-head h1{ margin:0; font-size: 1.5rem; font-weight: 800; }
.muted{ color:#6b7280; margin: 6px 0 0; }

.form{ display:flex; flex-direction:column; gap:18px; margin-top: 20px; }
.field{ display:flex; flex-direction:column; gap:6px; }
label{ font-weight:700; font-size:0.95rem; color:#111827; }
.req{ color:#ef4444; }

select, input, textarea{
  border: 1.5px solid #d1d5db;
  border-radius: 8px;
  padding: 11px 14px;
  background:#fff;
  outline:none;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.2s;
}

select:focus, input:focus, textarea:focus{ 
  border-color:#2563eb; 
  box-shadow: 0 0 0 3px rgba(37,99,235,.1); 
}

textarea{ 
  resize: vertical; 
  min-height: 100px;
  line-height: 1.5;
}

.info-text{
  color:#6b7280;
  font-size: 0.875rem;
  margin-top: 4px;
  display: block;
}

.actions{ 
  display:flex; 
  gap:12px; 
  justify-content: flex-end; 
  margin-top: 12px; 
  padding-top: 12px;
  border-top: 1px solid #e5e7eb;
}

.btn{ 
  display:inline-flex; 
  align-items:center; 
  justify-content:center; 
  padding: 11px 20px; 
  border-radius: 8px; 
  font-weight:700; 
  cursor:pointer; 
  text-decoration:none; 
  transition: all 0.2s;
  border: none;
  font-size: 0.95rem;
}

.btn.light{ 
  background:#f3f4f6; 
  color:#111827; 
}

.btn.light:hover{ 
  background:#e5e7eb; 
}

.btn.primary{ 
  background:#2563eb; 
  color:#fff; 
}

.btn.primary:hover:not(:disabled){ 
  background:#1d4ed8; 
}

.btn.primary:disabled{
  background:#9ca3af;
  cursor: not-allowed;
  opacity: 0.6;
}

@media (max-width: 720px){
  .container{ padding-left: 16px; padding-right: 16px; }
  .topbar{ flex-direction: column; gap: 12px; align-items: flex-start; }
  .actions{ flex-direction: column-reverse; }
  .btn{ width: 100%; }
}
</style>