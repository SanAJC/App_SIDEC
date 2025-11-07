<template>
  <div class="page">
    <div class="container">
      <h1>Mi perfil</h1>

      <div class="card">
        <h2>Datos de la cuenta</h2>
        <form @submit.prevent="onUpdateProfile" class="form">
          <label>Email</label>
          <input v-model="profile.email" type="email" required />

          <label>Nombre de usuario</label>
          <input v-model="profile.username" type="text" required />

          <button class="btn-primary" :disabled="savingProfile">{{ savingProfile ? 'Guardando...' : 'Guardar cambios' }}</button>
        </form>
      </div>

      <div class="card">
        <h2>Cambiar contraseña</h2>
        <form @submit.prevent="onChangePassword" class="form">
          <label>Contraseña actual</label>
          <input v-model="pwd.current" type="password" required />

          <label>Nueva contraseña</label>
          <input v-model="pwd.new1" type="password" required />

          <label>Confirmar nueva contraseña</label>
          <input v-model="pwd.new2" type="password" required />

          <button class="btn-primary" :disabled="changingPwd">{{ changingPwd ? 'Actualizando...' : 'Cambiar contraseña' }}</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted, ref } from 'vue'
import auth from '@/stores/auth'
import { changePassword } from '@/api/auth'

const profile = reactive({ email: '', username: '' })
const savingProfile = ref(false)
const changingPwd = ref(false)
const pwd = reactive({ current: '', new1: '', new2: '' })

onMounted(() => {
  if (auth.state.user) {
    profile.email = auth.state.user.email
    profile.username = auth.state.user.username
  }
})

async function onUpdateProfile() {
  try {
    savingProfile.value = true
    await auth.updateProfile({ email: profile.email, username: profile.username })
    alert('Perfil actualizado')
  } catch (e) {
    const msg = e?.response?.data?.error || 'No se pudo actualizar el perfil'
    alert(msg)
  } finally {
    savingProfile.value = false
  }
}

async function onChangePassword() {
  if (pwd.new1 !== pwd.new2) {
    alert('Las nuevas contraseñas no coinciden')
    return
  }
  try {
    changingPwd.value = true
    await changePassword({ current_password: pwd.current, new_password: pwd.new1 })
    pwd.current = ''
    pwd.new1 = ''
    pwd.new2 = ''
    alert('Contraseña actualizada')
  } catch (e) {
    const msg = e?.response?.data?.error || 'No se pudo cambiar la contraseña'
    alert(msg)
  } finally {
    changingPwd.value = false
  }
}
</script>

<style scoped>
.page{ min-height:100vh; background:#f6f7f9; padding:48px 16px; }
.container{ max-width:720px; margin:0 auto; display:flex; flex-direction:column; gap:16px; }
h1{ font-size:1.6rem; font-weight:800; margin-bottom:8px; }
.card{ background:#fff; border:1px solid #e5e7eb; border-radius:10px; padding:16px; }
.form{ display:flex; flex-direction:column; gap:10px; }
label{ font-weight:700; }
input{ height:44px; border:1.5px solid #cfd4dc; border-radius:8px; padding:0 12px; }
.btn-primary{ height:44px; border-radius:8px; background:#2563eb; color:#fff; font-weight:800; border:none; cursor:pointer; }
</style>
