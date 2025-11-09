<template>
  <div class="dashboard-page">
    <div class="container">
      <div class="topbar">
        <div class="brand">
          <img src="@/assets/images/logo_max.png" alt="SIDEC" class="brand-logo" />
        </div>
        <div class="top-actions">
          <router-link to="/" class="btn outline">Inicio</router-link>
          <template v-if="auth.state.user">
            <div class="user-menu">
              <button class="user-trigger" @click.stop="toggleMenu" aria-haspopup="menu" :aria-expanded="menuOpen">
                <span class="avatar">{{ initials }}</span>
                <span class="hamburger" aria-hidden="true">☰</span>
              </button>
              <div v-if="menuOpen" class="dropdown" role="menu">
                <div class="dropdown-header">{{ auth.state.user.username }}</div>
                <button class="dropdown-item" role="menuitem" @click="handleLogout">Cerrar sesión</button>
              </div>
            </div>
          </template>
        </div>
      </div>

      <!-- Loading state para entidades -->
      <div v-if="loadingEntidades" class="loading-msg">Cargando entidades...</div>
      
      <!-- Carousel de entidades -->
      <div v-else-if="entidades.length > 0" class="entity-carousel">
        <button class="nav-btn left" @click="rotate(-1)" aria-label="Anterior">‹</button>
        <TransitionGroup :name="direction === 'next' ? 'slide-left' : 'slide-right'" tag="div" class="entity-row">
          <div v-for="(entidad, i) in visibleEntidades" :key="entidad.id + '-' + startIndex + '-' + i" class="entity-card">
            <h3 class="entity-title">{{ entidad.nombre }}</h3>
            <p class="muted">{{ getEntidadDescription(entidad.nombre) }}</p>
            <router-link :to="{ path: '/report', query: { entity: entidad.id } }" class="btn outline">
              Crear Denuncia
            </router-link>
          </div>
        </TransitionGroup>
        <button class="nav-btn right" @click="rotate(1)" aria-label="Siguiente">›</button>
      </div>

      <div class="records card">
        <div class="records-head">
          <h2>Historial de Radicados</h2>
          <p class="muted">Seguimiento de todas tus denuncias y quejas presentadas</p>
        </div>

        <!-- Loading state para denuncias -->
        <div v-if="loadingDenuncias" class="loading-msg">Cargando denuncias...</div>

        <!-- Tabla de denuncias -->
        <div v-else-if="denuncias.length > 0" class="table-wrap">
          <table class="table">
            <thead>
              <tr>
                <th>Radicado</th>
                <th>Entidad</th>
                <th>Descripción</th>
                <th>Fecha Inicio</th>
                <th>Fecha Cierre</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="denuncia in paginatedDenuncias" :key="denuncia.id">
                <td>{{ formatRadicado(denuncia.id, denuncia.fecha_creacion) }}</td>
                <td>{{ denuncia.entidad?.nombre || 'N/A' }}</td>
                <td>{{ truncate(denuncia.asunto, 50) }}</td>
                <td>{{ formatDate(denuncia.fecha_creacion) }}</td>
                <td>{{ denuncia.fecha_envio ? formatDate(denuncia.fecha_envio) : '-' }}</td>
                <td>
                  <span :class="['pill', 'pill-'+getEstadoKey(denuncia.estado)]">
                    {{ getEstadoLabel(denuncia.estado) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty state -->
        <div v-else class="empty-state">
          <p>No tienes denuncias registradas aún.</p>
        </div>

        <!-- Paginación -->
        <div v-if="totalPages > 1" class="pagination">
          <button class="page-btn" @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">‹</button>
          <button 
            v-for="page in displayedPages" 
            :key="page"
            :class="['page-btn', { active: page === currentPage }]"
            @click="goToPage(page)"
          >
            {{ page }}
          </button>
          <button class="page-btn" @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">›</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import auth from '@/stores/auth'
import { getEntidades, getDenuncias } from '@/api/entities'

// Estados de carga
const loadingEntidades = ref(true)
const loadingDenuncias = ref(true)

// Datos desde la API
const entidades = ref([])
const denuncias = ref([])

// Paginación
const currentPage = ref(1)
const itemsPerPage = 10

// Cargar datos al montar el componente
onMounted(async () => {
  await Promise.all([
    fetchEntidades(),
    fetchDenuncias()
  ])
})

// Obtener entidades desde la API
async function fetchEntidades() {
  try {
    loadingEntidades.value = true
    const response = await getEntidades()
    entidades.value = response.data || []
  } catch (error) {
    console.error('Error al cargar entidades:', error)
    entidades.value = []
  } finally {
    loadingEntidades.value = false
  }
}

// Obtener denuncias desde la API
async function fetchDenuncias() {
  try {
    loadingDenuncias.value = true
    const response = await getDenuncias()
    denuncias.value = response.data || []
  } catch (error) {
    console.error('Error al cargar denuncias:', error)
    denuncias.value = []
  } finally {
    loadingDenuncias.value = false
  }
}

// Descripción por defecto para entidades
function getEntidadDescription(nombre) {
  const descriptions = {
    'Alcaldía Municipal': 'Denuncias sobre servicios públicos, infraestructura y administración',
    'Personería Jurídica': 'Violaciones de derechos humanos y control administrativo',
    'Secretaría de Salud': 'Quejas sobre servicios de salud y medicamentos',
    'Consulado': 'Quejas sobre servicios de notaría y actas'
  }
  return descriptions[nombre] || 'Presenta tu denuncia o queja ante esta entidad'
}

// Lógica del carrusel
const VISIBLE = 3
const startIndex = ref(0)
const direction = ref('next')

const visibleEntidades = computed(() => {
  const src = entidades.value
  if (!src.length) return []
  const n = Math.min(VISIBLE, src.length)
  return Array.from({ length: n }, (_, i) => src[(startIndex.value + i) % src.length])
})

function rotate(dir) {
  const len = entidades.value.length
  if (len <= 1) return
  direction.value = dir > 0 ? 'next' : 'prev'
  startIndex.value = (startIndex.value + (dir > 0 ? 1 : -1) + len) % len
}

// Formateo de datos
function formatRadicado(id, fecha) {
  const year = new Date(fecha).getFullYear()
  return `RAD-${year}-${String(id).padStart(3, '0')}`
}

function formatDate(dateString) {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-CO', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

function truncate(text, maxLength) {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

function getEstadoKey(estado) {
  const estados = {
    'pendiente': 'proceso',
    'enviado': 'finalizado',
    'error_envio': 'revision'
  }
  return estados[estado] || 'proceso'
}

function getEstadoLabel(estado) {
  const labels = {
    'pendiente': 'En proceso',
    'enviado': 'Finalizado',
    'error_envio': 'En revisión'
  }
  return labels[estado] || estado
}

// Paginación
const totalPages = computed(() => Math.ceil(denuncias.value.length / itemsPerPage))

const paginatedDenuncias = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return denuncias.value.slice(start, end)
})

const displayedPages = computed(() => {
  const pages = []
  const maxVisible = 5
  
  if (totalPages.value <= maxVisible) {
    for (let i = 1; i <= totalPages.value; i++) {
      pages.push(i)
    }
  } else {
    if (currentPage.value <= 3) {
      for (let i = 1; i <= 4; i++) pages.push(i)
      pages.push('...')
      pages.push(totalPages.value)
    } else if (currentPage.value >= totalPages.value - 2) {
      pages.push(1)
      pages.push('...')
      for (let i = totalPages.value - 3; i <= totalPages.value; i++) pages.push(i)
    } else {
      pages.push(1)
      pages.push('...')
      pages.push(currentPage.value - 1)
      pages.push(currentPage.value)
      pages.push(currentPage.value + 1)
      pages.push('...')
      pages.push(totalPages.value)
    }
  }
  
  return pages
})

function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

// User menu logic
const router = useRouter()
const menuOpen = ref(false)
const initials = computed(() => {
  const name = auth.state.user?.username || ''
  return name.slice(0,1).toUpperCase()
})

function toggleMenu() { 
  menuOpen.value = !menuOpen.value 
}

function closeMenu() { 
  menuOpen.value = false 
}

async function handleLogout() {
  await auth.logout()
  closeMenu()
  router.push('/login')
}

function onDocClick(e) {
  const menu = document.querySelector('.user-menu')
  if (!menu) return
  if (!menu.contains(e.target)) closeMenu()
}

onMounted(() => document.addEventListener('click', onDocClick))
onBeforeUnmount(() => document.removeEventListener('click', onDocClick))
</script>

<style scoped>
.dashboard-page{ background: var(--bg); min-height: 100vh; padding: 32px 0 56px; }
.container{ max-width: none; width: 100%; margin:0; padding-left:40px; padding-right:40px; }
.topbar{ display:flex; justify-content:space-between; align-items:center; margin-bottom: 20px; }
.brand{ display:flex; align-items:center; gap:10px; }
.brand-logo{ width:auto; height:40px; display:block; object-fit: cover; }
.top-actions{ display:flex; align-items:center; gap:10px; }

.loading-msg{ text-align:center; padding:40px; color:var(--muted); font-size:1.1rem; }
.empty-state{ text-align:center; padding:40px; color:var(--muted); }

.entity-carousel{ position:relative; margin-bottom:30px; }
.entity-row{ display:flex; gap:28px; align-items: stretch; min-height: 200px; }
.entity-row > .entity-card{ flex: 0 0 calc((100% - 56px)/3); }
.entity-card{
  background: var(--surface);
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 26px;
  box-shadow: 0 2px 6px rgba(16,24,40,.06), 0 8px 20px rgba(16,24,40,.06);
  min-height: 200px;
  display: flex;
  flex-direction: column;
}
.nav-btn{ position:absolute; top:50%; transform: translateY(-50%); width:40px; height:40px; border-radius:999px; border:1px solid #e5e7eb; background:#fff; cursor:pointer; font-size: 20px; line-height: 1; display:flex; align-items:center; justify-content:center; box-shadow: 0 4px 12px rgba(16,24,40,.12); z-index: 2; color:#111; }
.nav-btn:hover{ background:#111; color:#fff; border-color:#111; }
.nav-btn:disabled{ opacity:0.3; cursor:not-allowed; }
.nav-btn:disabled:hover{ background:#fff; color:#111; border-color:#e5e7eb; }
.nav-btn.left{ left:-14px; }
.nav-btn.right{ right:-14px; }

/* Transiciones del carrusel */
.slide-left-enter-active, .slide-left-leave-active,
.slide-right-enter-active, .slide-right-leave-active{ transition: transform .25s ease, opacity .25s ease; }
.slide-left-enter-from{ transform: translateX(120%); opacity:0; }
.slide-left-leave-to{ transform: translateX(-120%); opacity:0; }
.slide-right-enter-from{ transform: translateX(-120%); opacity:0; }
.slide-right-leave-to{ transform: translateX(120%); opacity:0; }
.slide-left-move, .slide-right-move{ transition: transform .25s ease; }

.entity-title{ font-size: 2rem; font-weight: 800; margin: 0 0 8px; color: var(--text); }
.muted{ color: var(--muted); margin: 0 0 14px; font-size: 1.05rem; }
.btn.outline{ display:inline-flex; align-items:center; justify-content:center; padding:12px 18px; border-radius:12px; font-weight:800; text-decoration:none; background:transparent; border:2px solid #111; color:#111; font-size: 1.05rem; }
.btn.outline:hover{ background:#111; color:#fff; }

/* user menu styles */
.user-menu { position: relative; }
.user-trigger {
  display:flex; align-items:center; gap:10px;
  background: rgba(0,0,0,0.04);
  border: 1px solid rgba(0,0,0,0.12);
  color:#111; padding: 8px 12px; border-radius: 10px; cursor:pointer;
}
.avatar { width:24px; height:24px; border-radius:50%; background:#2563eb; display:flex; align-items:center; justify-content:center; font-weight:800; color:#fff; }
.dropdown {
  position:absolute; right:0; top: 42px; min-width: 200px;
  background:#fff; border:1px solid #e5e7eb; border-radius:8px;
  box-shadow: 0 10px 20px rgba(0,0,0,0.08), 0 2px 6px rgba(0,0,0,0.08);
  overflow:hidden;
  z-index: 1000;
}
.dropdown-header{ padding:10px 12px; font-weight:800; background:#f8fafc; border-bottom:1px solid #e5e7eb; color:#111827; }
.dropdown-item{ display:block; width:100%; text-align:left; padding:10px 12px; background:#fff; border:none; color:#111827; cursor:pointer; text-decoration:none; }
.dropdown-item:hover{ background:#f3f4f6; }

.card{ background: var(--surface); border: 1px solid #e5e7eb; border-radius: 14px; box-shadow: 0 2px 6px rgba(16,24,40,.06), 0 8px 20px rgba(16,24,40,.06); padding: 24px; }
.records-head h2{ margin:0; font-weight:800; font-size: clamp(2rem, 2vw, 2.6rem); }
.records-head .muted{ margin-top: 6px; color: var(--muted); font-size: 1.05rem; }

.table-wrap{ overflow:auto; margin-top: 12px; }
.table{ width:100%; border-collapse: collapse; font-size: 1rem; }
.table th, .table td{ text-align:left; padding: 14px 12px; border-bottom: 1px solid #f0f2f5; }
.table th{ font-weight:800; color: var(--text); font-size: 1.05rem; }

.pill{ display:inline-flex; align-items:center; padding:8px 12px; border-radius: 999px; font-weight:800; font-size: 0.95rem; }
.pill-finalizado{ background:#d1fae5; color:#065f46; border: 1px solid rgba(6,95,70,.15); }
.pill-revision{ background:#fef3c7; color:#92400e; }
.pill-proceso{ background:#dbeafe; color:#1e40af; }

.pagination{ display:flex; gap:10px; justify-content:flex-end; padding-top: 16px; flex-wrap:wrap; }
.page-btn{ min-width: 40px; height: 40px; border-radius: 10px; border:1px solid #e5e7eb; background:#fff; cursor:pointer; font-size: 1rem; }
.page-btn:hover:not(:disabled):not(.active){ background:#f3f4f6; }
.page-btn.active{ background: var(--primary); color:#fff; border-color: var(--primary); }
.page-btn:disabled{ opacity:0.5; cursor:not-allowed; }

@media (max-width: 1024px){
  .entity-row{ gap:20px; }
  .entity-row > .entity-card{ flex: 0 0 calc((100% - 20px)/2); }
  .nav-btn.left{ left:-8px; }
  .nav-btn.right{ right:-8px; }
}
@media (max-width: 720px){
  .container{ padding-left:16px; padding-right:16px; }
  .entity-row{ gap:16px; }
  .entity-row > .entity-card{ flex: 1 0 100%; }
  .nav-btn{ top:auto; bottom:-22px; transform:none; }
  .nav-btn.left{ left:0; }
  .nav-btn.right{ right:0; }
}
</style>