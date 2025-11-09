import api from './axios'

export function getEntidades() {
  return api.get('/api/entidades/')
}

export function getEntidad(id) {
  return api.get(`/api/entidades/${id}/`)
}

export function getDenuncias() {
  return api.get('/api/denuncias/')
}

export function getDenuncia(id) {
  return api.get(`/api/denuncias/${id}/`)
}

export function createDenuncia(payload) {
  // Usar FormData si hay archivos, sino enviar JSON
  const isFormData = payload instanceof FormData
  const config = isFormData ? {
    headers: { 'Content-Type': 'multipart/form-data' }
  } : {}
  
  return api.post('/api/denuncias/', payload, config)
}

export function updateDenuncia(id, payload) {
  return api.patch(`/api/denuncias/${id}/`, payload)
}

export function deleteDenuncia(id) {
  return api.delete(`/api/denuncias/${id}/`)
}