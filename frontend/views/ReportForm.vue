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
        <p class="muted">Alcaldía Municipal · Complete todos los campos requeridos</p>
      </div>

      <form class="form" @submit.prevent="onSubmit">
        <div class="field">
          <label>Entidad destino <span class="req">*</span></label>
          <select v-model="form.entidad" required>
            <option value="" disabled>Seleccione una entidad</option>
            <option v-for="e in entidades" :key="e.id" :value="String(e.id)">{{ e.nombre }}</option>
          </select>
          <small v-if="!entidades.length" class="muted">No hay entidades para mostrar. Inicie sesión o verifique la conexión.</small>
        </div>

        <div class="field">
          <label>Asunto <span class="req">*</span></label>
          <input v-model="form.asunto" type="text" placeholder="Resuma su denuncia en pocas palabras" required />
        </div>

        <div class="field">
          <label>Cuerpo <span class="req">*</span></label>
          <textarea v-model="form.cuerpo" rows="6" placeholder="Describa los hechos de manera clara y detallada" required></textarea>
        </div>

        <div class="field">
          <label>Correo del Usuario <span class="req">*</span></label>
          <input v-model="form.email_usuario" type="email" placeholder="su_correo@ejemplo.com" required />
        </div>

        <div class="field">
          <label>Detalle</label>
          <textarea v-model="form.detalle" rows="4" placeholder="Información adicional relevante"></textarea>
        </div>

        <div class="field">
          <label>Correo destino</label>
          <input v-model="form.correo_destino" type="email" placeholder="Opcional: sobreescribir correo de la entidad" />
        </div>

        <hr class="divider" />
        <h3 class="section-title">Adjunto</h3>
        <p class="muted small">Adjunte un archivo PDF si corresponde. Máx 10MB.</p>

        <div class="field">
          <label>Archivo PDF</label>
          <input type="file" accept="application/pdf" @change="handlePdf" />
        </div>

        <div class="actions">
          <router-link to="/dashboard" class="btn light">Cancelar</router-link>
          <button type="submit" class="btn primary" :disabled="!entidades.length || !form.entidad || !form.asunto || !form.cuerpo || !form.email_usuario">Enviar Denuncia</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/axios'

const form = ref({
  entidad: '',
  asunto: '',
  cuerpo: '',
  email_usuario: '',
  detalle: '',
  correo_destino: ''
})

const entidades = ref([])
const pdfFile = ref(null)
const API_BASE = '/api'
const route = useRoute()
const DEFAULT_ENTIDADES = [
  { id: 'alcaldia', nombre: 'Alcaldía Municipal' },
  { id: 'personeria', nombre: 'Personería Jurídica' },
  { id: 'salud', nombre: 'Secretaría de Salud' },
  { id: 'consulado', nombre: 'Consulado' },
]

function handlePdf(e){
  const incoming = e.target.files[0]
  if(!incoming) return
  if(incoming.size > 10*1024*1024) return // 10MB
  pdfFile.value = incoming
}

onMounted(async () => {
  try{
    const { data } = await api.get(`${API_BASE}/entidades/`)
    entidades.value = Array.isArray(data) ? data : []
    const key = (route.query.entity || '').toString().toLowerCase()
    if (key && entidades.value.length) {
      const found = entidades.value.find(e => (e.nombre || '').toLowerCase().includes(key))
      if (found) form.value.entidad = String(found.id)
    }
    if (!entidades.value.length) {
      entidades.value = DEFAULT_ENTIDADES
      const key2 = (route.query.entity || '').toString().toLowerCase()
      if (key2) {
        const found2 = entidades.value.find(e => (e.nombre || '').toLowerCase().includes(key2) || String(e.id).toLowerCase() === key2)
        if (found2) form.value.entidad = String(found2.id)
      }
    }
  }catch(err){
    console.error('Error cargando entidades', err)
    entidades.value = DEFAULT_ENTIDADES
    const key = (route.query.entity || '').toString().toLowerCase()
    if (key) {
      const found = entidades.value.find(e => (e.nombre || '').toLowerCase().includes(key) || String(e.id).toLowerCase() === key)
      if (found) form.value.entidad = String(found.id)
    }
  }
})

async function onSubmit(){
  if (isNaN(form.value.entidad)) return
  const fd = new FormData()
  fd.append('entidad', form.value.entidad)
  fd.append('asunto', form.value.asunto)
  fd.append('cuerpo', form.value.cuerpo)
  fd.append('email_usuario', form.value.email_usuario)
  if(form.value.detalle) fd.append('detalle', form.value.detalle)
  if(form.value.correo_destino) fd.append('correo_destino', form.value.correo_destino)
  if(pdfFile.value) fd.append('pdf', pdfFile.value)

  try{
    const { data } = await api.post(`${API_BASE}/denuncias/`, fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    alert('Denuncia enviada correctamente')
    console.log('denuncia creada', data)
  }catch(err){
    console.error('Error enviando denuncia', err)
    alert('Error al enviar la denuncia. Verifique los datos e intente nuevamente.')
  }
}
</script>

<style scoped>
.report-page{ background:#f6f7f9; min-height:100vh; padding: 24px 0 48px; }
.container{ max-width: 1080px; margin: 0 auto; padding-left: 30px; padding-right: 30px; }
.topbar{ margin-bottom: 6px; display:flex; justify-content: space-between; align-items:center; }
.brand{ display:flex; align-items:center; gap:8px; }
.brand-logo{ width:100%; height:30px; display:block; object-fit: cover; }
.brand-text{ font-weight:800; letter-spacing: 1.1px; color: #111; }
.top-actions{ display:flex; gap:10px; }

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
.small{ font-size: 0.92rem; }

.form{ display:flex; flex-direction:column; gap:14px; margin-top: 14px; }
.field{ display:flex; flex-direction:column; gap:6px; }
label{ font-weight:700; font-size:0.95rem; }
.req{ color:#ef4444; }
input, textarea{
  border: 1.5px solid #cfd4dc;
  border-radius: 8px;
  padding: 10px 12px;
  background:#fff;
  outline:none;
}
input:focus, textarea:focus{ border-color:#2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,.12); }

.divider{ border: none; border-top:1px solid #e5e7eb; margin: 10px 0; }
.section-title{ font-size:1.05rem; font-weight:800; margin: 4px 0 6px; }

.uploader{ border: 1.5px dashed #cbd5e1; border-radius: 12px; background:#fafbfc; }
.uploader-inner{ padding: 22px; text-align: center; color:#475569; cursor: pointer; }
.uploader-icon{ font-size: 22px; margin-bottom: 6px; }
.file-input{ display:none; }

.previews{ display:flex; flex-wrap: wrap; gap: 10px; margin-top: 12px; }
.thumb{ position: relative; width: 120px; height: 90px; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,.08); }
.thumb img{ width:100%; height:100%; object-fit: cover; display:block; }
.thumb .remove{ position:absolute; top:4px; right:4px; border:none; background: rgba(0,0,0,.6); color:#fff; width:22px; height:22px; border-radius: 50%; cursor:pointer; }

.actions{ display:flex; gap:10px; justify-content: flex-end; margin-top: 8px; }
.btn{ display:inline-flex; align-items:center; justify-content:center; padding: 10px 16px; border-radius: 8px; font-weight:800; cursor:pointer; text-decoration:none; }
.btn.light{ background:#eef1f5; color:#111; }
.btn.primary{ background:#2563eb; color:#fff; border:none; }

@media (max-width: 720px){
  .container{ padding-left: 16px; padding-right: 16px; }
}
</style>