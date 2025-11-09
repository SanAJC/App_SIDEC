/* eslint-disable vue/multi-word-component-names */
<template>
  <header class="header">
    <div class="container">
      <div class="brand">
        <img src="@/assets/images/logo_blanco.png" alt="sidec logo" class="logo"/>
      </div>
      <div class="actions">
        <router-link to="/" class="btn btn-light">Inicio</router-link>
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
        <template v-else>
          <router-link to="/login" class="btn btn-light">Inicia Sesión</router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount, ref } from 'vue'
import { useRouter } from 'vue-router'
import auth from '@/stores/auth'

const router = useRouter()

const menuOpen = ref(false)
const initials = computed(() => {
  const name = auth.state.user?.username || ''
  return name.slice(0,1).toUpperCase()
})

function toggleMenu() { menuOpen.value = !menuOpen.value }
function closeMenu() { menuOpen.value = false }

async function handleLogout() {
  await auth.logout()
  closeMenu()
  router.push('/login')
}

// click outside directive (simple)
function onDocClick(e){
  const menu = document.querySelector('.user-menu')
  if (!menu) return
  if (!menu.contains(e.target)) closeMenu()
}
onMounted(()=> document.addEventListener('click', onDocClick))
onBeforeUnmount(()=> document.removeEventListener('click', onDocClick))
</script>

<style scoped>
.header {
  position: absolute;
  top: 16px;
  left: 0;
  right: 0;
  z-index: 30;
}
.container {
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding-left: 30px;   /* espacio lateral coherente */
  padding-right: 30px;  /* 30px desde el borde derecho para el botón */
}
@media (max-width: 768px){
  .container { padding-left:16px; padding-right:16px; }
}
.brand {
  display:flex;
  align-items:center;
  gap: 0;
}
.logo { width: 100%; height: 30px; display:block; object-fit: cover; }
.actions { display:flex; align-items:center; gap: 8px; }
.btn {
  padding: 10px 18px;
  border-radius: 10px;
  text-decoration: none; 
  font-weight:700;
  font-size: 1rem;
}
.btn-light {
  background: rgba(255,255,255,0.5);
  color: #ffffff;
  padding: 0.70rem 2rem;
  border-radius: 5px;
}
.user-menu { position: relative; }
.user-trigger {
  display:flex; align-items:center; gap:10px;
  background: rgba(255,255,255,0.18);
  border: 1px solid rgba(255,255,255,0.35);
  backdrop-filter: blur(6px);
  color:#fff; padding: 8px 12px; border-radius: 10px; cursor:pointer;
}
.avatar { width:24px; height:24px; border-radius:50%; background:#2563eb; display:flex; align-items:center; justify-content:center; font-weight:800; }
.username { font-weight:700; text-transform: lowercase; }
.hamburger { opacity: 0.9; }
.dropdown {
  position:absolute; right:0; top: 42px; min-width: 200px;
  background:#fff; border:1px solid #e5e7eb; border-radius:8px;
  box-shadow: 0 10px 20px rgba(0,0,0,0.08), 0 2px 6px rgba(0,0,0,0.08);
  overflow:hidden;
}
.dropdown-header{ padding:10px 12px; font-weight:800; background:#f8fafc; border-bottom:1px solid #e5e7eb; color:#111827; }
.dropdown-item{ display:block; width:100%; text-align:left; padding:10px 12px; background:#fff; border:none; color:#111827; cursor:pointer; text-decoration:none; }
.dropdown-item:hover{ background:#f3f4f6; }
</style>
