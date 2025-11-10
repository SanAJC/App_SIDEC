import axios from 'axios'

const instance = axios.create({
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true
})

let isRefreshing = false
let pendingRequests = []

function onRefreshed() {
  pendingRequests.forEach(cb => cb())
  pendingRequests = []
}

function clearAuthAndRedirect() {
  // Limpiar cualquier estado de autenticación
  localStorage.removeItem('user')
  sessionStorage.clear()
  
  // Redirigir al login solo si no estamos ya en páginas públicas
  const currentPath = window.location.pathname
  const publicPaths = ['/login', '/register', '/']
  
  if (!publicPaths.includes(currentPath)) {
    window.location.href = '/login?session=expired'
  }
}

instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config || {}

    if (!error.response) return Promise.reject(error)

    const status = error.response.status
    const url = (originalRequest.url || '')

    const isAuthEndpoint = (
      url.includes('/auth/users/login') ||
      url.includes('/auth/users/register') ||
      url.includes('/auth/users/refresh_token')
    )

    // Si es un endpoint de auth que falla, no intentar refrescar
    if (status === 401 && isAuthEndpoint) {
      // Si el refresh token falló, limpiar sesión
      if (url.includes('/auth/users/refresh_token')) {
        clearAuthAndRedirect()
      }
      return Promise.reject(error)
    }

    // Para otros endpoints con 401, intentar refrescar el token
    if (status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      // Si ya estamos refrescando, agregar a la cola
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          pendingRequests.push(() => {
            instance(originalRequest)
              .then(resolve)
              .catch(reject)
          })
        })
      }

      try {
        isRefreshing = true
        await instance.post('/auth/users/refresh_token/')
        isRefreshing = false
        onRefreshed()
        return instance(originalRequest)
      } catch (refreshError) {
        isRefreshing = false
        pendingRequests = []
        
        // Si el refresh falló, limpiar sesión y redirigir
        clearAuthAndRedirect()
        
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default instance