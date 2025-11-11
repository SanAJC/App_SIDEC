import { reactive } from 'vue'
import { getProfile, logout as apiLogout, updateProfile as apiUpdateProfile } from '@/api/auth'

const state = reactive({
  user: null,
  loading: false,
  error: null,
})

async function loadSession() {
  try {
    state.loading = true
    const response = await getProfile()
    console.log('loadSession response:', response)
    // Guardar todo el objeto del usuario, no solo el email
    state.user = response.data || null
    console.log('loadSession user:', state.user)
    state.error = null
  } catch (e) {
    state.user = null
    state.error = null
  } finally {
    state.loading = false
  }
}

async function logout() {
  try {
    await apiLogout()
  } finally {
    state.user = null
  }
}

async function updateProfile(payload) {
  const response = await apiUpdateProfile(payload)
  state.user = response.data || null
  return response.data
}

export default {
  state,
  loadSession,
  logout,
  updateProfile,
}
