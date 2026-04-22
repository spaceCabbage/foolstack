import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { client } from '@/apiClient/client'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))
  const initialized = ref(false)

  const isAuthenticated = computed(() => !!accessToken.value)

  function setTokens(tokens) {
    accessToken.value = tokens.access
    refreshToken.value = tokens.refresh
    localStorage.setItem('access_token', tokens.access)
    localStorage.setItem('refresh_token', tokens.refresh)
  }

  function clearTokens() {
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  async function fetchUser() {
    if (!accessToken.value) {
      initialized.value = true
      return
    }
    try {
      const response = await client.get('/auth/profile/')
      user.value = response.data
    } catch (error) {
      // If profile fetch fails, tokens might be invalid
      if (error.response?.status === 401) {
        // Interceptor might handle this, but being safe
        // clearTokens()
      }
    } finally {
      initialized.value = true
    }
  }

  async function login(credentials) {
    const response = await client.post('/auth/login/', credentials)
    setTokens({
      access: response.data.access,
      refresh: response.data.refresh,
    })
    user.value = response.data.user
    return response.data
  }

  async function register(userData) {
    const response = await client.post('/auth/register/', userData)
    setTokens({
      access: response.data.access,
      refresh: response.data.refresh,
    })
    user.value = response.data.user
    return response.data
  }

  async function logout() {
    // Note: SimpleJWT doesn't have a default logout endpoint unless using blacklist
    // For now, we just clear local state
    clearTokens()
  }

  return {
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    initialized,
    fetchUser,
    login,
    register,
    logout,
    setTokens,
    clearTokens,
  }
})
