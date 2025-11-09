import api from './axios'

export function login(payload) {
  return api.post('/auth/users/login/', payload)
}

export function register(payload) {
  return api.post('/auth/users/register/', payload)
}

export function logout() {
  return api.post('/auth/users/logout/')
}

export function getProfile() {
  return api.get('/auth/users/profile/')
}

export function updateProfile(payload) {
  return api.patch('/auth/users/update-profile/', payload)
}

export function changePassword(payload) {
  return api.post('/auth/users/change-password/', payload)
}
