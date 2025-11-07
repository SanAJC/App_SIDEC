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

    if (status === 401 && !originalRequest._retry && !isAuthEndpoint) {
      originalRequest._retry = true

      if (isRefreshing) {
        return new Promise((resolve) => {
          pendingRequests.push(() => resolve(instance(originalRequest)))
        })
      }

      try {
        isRefreshing = true
        await instance.post('/auth/users/refresh_token/')
        isRefreshing = false
        onRefreshed()
        return instance(originalRequest)
      } catch (e) {
        isRefreshing = false
        pendingRequests = []
        return Promise.reject(e)
      }
    }

    return Promise.reject(error)
  }
)

export default instance