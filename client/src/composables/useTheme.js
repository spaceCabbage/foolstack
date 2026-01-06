import { ref, watch, onMounted } from 'vue'

/**
 * @typedef {'light' | 'dark' | 'system'} Theme
 */

const STORAGE_KEY = 'foolstack-theme'

/** @type {import('vue').Ref<Theme>} */
const theme = ref('system')
const isDark = ref(false)

let initialized = false

function getSystemTheme() {
  if (typeof window === 'undefined') return false
  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

function applyTheme(dark) {
  isDark.value = dark
  if (typeof document !== 'undefined') {
    if (dark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }
}

function updateTheme() {
  if (theme.value === 'system') {
    applyTheme(getSystemTheme())
  } else {
    applyTheme(theme.value === 'dark')
  }
}

function initTheme() {
  if (initialized || typeof window === 'undefined') return
  initialized = true

  // Load saved preference
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved && ['light', 'dark', 'system'].includes(saved)) {
    theme.value = saved
  }
  updateTheme()

  // Listen for system theme changes
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  mediaQuery.addEventListener('change', () => {
    if (theme.value === 'system') {
      applyTheme(getSystemTheme())
    }
  })
}

// Watch for theme changes
watch(theme, (newTheme) => {
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem(STORAGE_KEY, newTheme)
  }
  updateTheme()
})

/**
 * Theme management composable
 * @returns {{
 *   theme: import('vue').Ref<Theme>,
 *   isDark: import('vue').Ref<boolean>,
 *   setTheme: (theme: Theme) => void,
 *   toggleTheme: () => void,
 *   cycleTheme: () => void
 * }}
 */
export function useTheme() {
  onMounted(() => {
    initTheme()
  })

  /**
   * Set the theme directly
   * @param {Theme} newTheme
   */
  function setTheme(newTheme) {
    theme.value = newTheme
  }

  /**
   * Toggle between light and dark (ignores system)
   */
  function toggleTheme() {
    theme.value = isDark.value ? 'light' : 'dark'
  }

  /**
   * Cycle through light -> dark -> system
   */
  function cycleTheme() {
    if (theme.value === 'light') {
      theme.value = 'dark'
    } else if (theme.value === 'dark') {
      theme.value = 'system'
    } else {
      theme.value = 'light'
    }
  }

  return {
    theme,
    isDark,
    setTheme,
    toggleTheme,
    cycleTheme,
  }
}
