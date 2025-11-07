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
    const data = await getProfile()
    state.user = data
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
  const data = await apiUpdateProfile(payload)
  state.user = data
  return data
}

export default {
  state,
  loadSession,
  logout,
  updateProfile,
}
