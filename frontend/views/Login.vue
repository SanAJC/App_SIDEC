<template>
  <div class="auth-page">
    <div class="brand-top">
      <router-link to="/" class="brand">
        <img src="@/assets/images/logo_max.png" alt="SIDEC logo" class="logo" />
      </router-link>
      <router-link to="/" class="btn btn-light">Inicio</router-link>
    </div>

    <div class="tabs">
      <button :class="['tab', activeTab==='login' && 'active']" @click="activeTab='login'">Iniciar Sesión</button>
      <button :class="['tab', activeTab==='register' && 'active']" @click="activeTab='register'">Registrarse</button>
    </div>

    <div class="card">
      <h2 class="card-title">{{ activeTab==='login' ? 'Bienvenido' : 'Crea tu cuenta' }}</h2>
      <p class="card-sub">Ingresa tus credenciales para acceder.</p>

      <form class="form" @submit.prevent="onSubmit">
        <template v-if="activeTab==='register'">
          <label>Nombre de Usuario</label>
          <input v-model="form.username" type="text" placeholder="Tu nombre de usuario" required />
        </template>

        <label>Correo Electrónico</label>
        <input v-model="form.email" type="email" placeholder="tu@correo.com" required />

        <label>Contraseña</label>
        <input v-model="form.password" type="password" placeholder="********" required />

        <template v-if="activeTab==='register'">
          <label>Confirmar Contraseña</label>
          <input v-model="form.confirm" type="password" placeholder="********" required />
        </template>

        <div class="actions">
          <button type="submit" class="btn-primary" :disabled="submitting">{{ submitting ? 'Procesando...' : (activeTab==='login' ? 'Iniciar Sesión' : 'Crear cuenta') }}</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { login, register } from '@/api/auth'
import auth from '@/stores/auth'

const activeTab = ref('login')
const route = useRoute()
const router = useRouter()

const submitting = ref(false)
const form = ref({
  email: '',
  password: '',
  username: '',
  confirm: ''
})

onMounted(() => {
  if (route.query.register === '1') activeTab.value = 'register'
})

async function onSubmit() {
  try {
    submitting.value = true
    if (activeTab.value === 'login') {
      await login({ email: form.value.email, password: form.value.password })
      // actualizar estado de sesión y llevar al dashboard
      await auth.loadSession()
      await router.push('/dashboard')
    } else {
      if (form.value.password !== form.value.confirm) {
        alert('Las contraseñas no coinciden')
        return
      }
      await register({ email: form.value.email, password: form.value.password, username: form.value.username })
      // notificación y redirigir a la pestaña de iniciar sesión
      alert('Tu sesión se inició correctamente')
      activeTab.value = 'login'
      // limpiar query register si existe
      router.replace({ name: 'Login' })
      return
    }
  } catch (e) {
    const msg = e?.response?.data?.error || e?.response?.data?.detail || 'Error en la autenticación'
    alert(msg)
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.auth-page{
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 48px 16px;
  background: #f6f7f9;
}
.brand-top { margin-bottom: 12px; }
.brand-top { display:flex; align-items:center; justify-content: space-between; width:100%; max-width: 640px; }
.brand { display:flex; align-items:center; gap:10px; text-decoration:none; color: inherit; }
.logo{ width:100%; height:30px; display:block; object-fit: cover; }

.tabs{
  display:flex; gap:6px; margin: 8px 0 10px; background:#e5e7eb; padding:4px; border-radius: 8px;
}
.tab{ background: transparent; border:none; padding:8px 16px; border-radius: 6px; cursor:pointer; font-weight:700; color:#374151; }
.tab.active{ background:#fff; box-shadow: 0 1px 2px rgba(16,24,40,.06), 0 1px 3px rgba(16,24,40,.1); }

.card{
  width: 100%;
  max-width: 520px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  box-shadow: 0 1px 2px rgba(16,24,40,.04), 0 1px 3px rgba(16,24,40,.06);
  padding: 18px 18px 22px;
}
.card-title{ font-size: 1.4rem; font-weight: 800; margin:4px 0 4px; }
.card-sub{ color:#6b7280; margin:0 0 12px; }

.form{ display:flex; flex-direction:column; gap:10px; }
label{ font-weight:700; font-size:0.94rem; }
input{
  height: 44px;
  border: 1.5px solid #cfd4dc;
  border-radius: 8px;
  padding: 0 12px;
  background:#fff;
  outline: none;
}
input:focus{ border-color:#2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,.15); }
.actions{ margin-top: 6px; }
.btn-primary{ width: 100%; height: 44px; border-radius: 8px; background:#2563eb; color:#fff; font-weight:800; border:none; cursor:pointer; }
</style>