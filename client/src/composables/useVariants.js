import { computed } from 'vue'

/**
 * @typedef {'sm' | 'md' | 'lg'} Size
 * @typedef {'primary' | 'secondary' | 'accent' | 'success' | 'warning' | 'error' | 'info'} Color
 * @typedef {'solid' | 'outline' | 'ghost' | 'soft'} Variant
 */

/**
 * Creates computed classes from variant props
 * @param {Object} props - Component props
 * @param {Object} config - Variant configuration
 * @returns {import('vue').ComputedRef<string>}
 */
export function useVariants(props, config) {
  return computed(() => {
    const classes = [config.base]

    // Size classes
    const size = props.size ?? 'md'
    if (config.sizes?.[size]) {
      classes.push(config.sizes[size])
    }

    // Color + variant combination
    const color = props.color ?? 'primary'
    const variant = props.variant ?? 'solid'
    if (config.colors?.[color]?.[variant]) {
      classes.push(config.colors[color][variant])
    }

    // State classes
    if (props.disabled) {
      classes.push(config.disabled ?? 'opacity-50 cursor-not-allowed')
    }
    if (props.loading) {
      classes.push(config.loading ?? 'cursor-wait')
    }

    return classes.filter(Boolean).join(' ')
  })
}

/**
 * Button variant configuration
 */
export const buttonVariants = {
  base: 'inline-flex items-center justify-center font-medium transition-colors duration-150 ease-out focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none select-none',
  sizes: {
    sm: 'h-8 px-3 text-sm rounded-md gap-1.5',
    md: 'h-10 px-4 text-sm rounded-lg gap-2',
    lg: 'h-12 px-6 text-base rounded-lg gap-2.5',
  },
  colors: {
    primary: {
      solid: 'bg-primary-500 text-white hover:bg-primary-600 active:bg-primary-700',
      outline: 'border-2 border-primary-500 text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-950 dark:text-primary-400',
      ghost: 'text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-950 dark:text-primary-400',
      soft: 'bg-primary-100 text-primary-700 hover:bg-primary-200 dark:bg-primary-950 dark:text-primary-300 dark:hover:bg-primary-900',
    },
    secondary: {
      solid: 'bg-secondary-500 text-white hover:bg-secondary-600 active:bg-secondary-700',
      outline: 'border-2 border-secondary-400 text-secondary-600 hover:bg-secondary-50 dark:hover:bg-secondary-950 dark:text-secondary-400',
      ghost: 'text-secondary-600 hover:bg-secondary-100 dark:hover:bg-secondary-900 dark:text-secondary-400',
      soft: 'bg-secondary-100 text-secondary-700 hover:bg-secondary-200 dark:bg-secondary-900 dark:text-secondary-300 dark:hover:bg-secondary-800',
    },
    accent: {
      solid: 'bg-accent-500 text-white hover:bg-accent-600 active:bg-accent-700',
      outline: 'border-2 border-accent-500 text-accent-600 hover:bg-accent-50 dark:hover:bg-accent-950 dark:text-accent-400',
      ghost: 'text-accent-600 hover:bg-accent-50 dark:hover:bg-accent-950 dark:text-accent-400',
      soft: 'bg-accent-100 text-accent-700 hover:bg-accent-200 dark:bg-accent-950 dark:text-accent-300 dark:hover:bg-accent-900',
    },
    success: {
      solid: 'bg-success-500 text-white hover:bg-success-600 active:bg-success-700',
      outline: 'border-2 border-success-500 text-success-600 hover:bg-success-50 dark:hover:bg-success-950 dark:text-success-400',
      ghost: 'text-success-600 hover:bg-success-50 dark:hover:bg-success-950 dark:text-success-400',
      soft: 'bg-success-100 text-success-700 hover:bg-success-200 dark:bg-success-950 dark:text-success-300 dark:hover:bg-success-900',
    },
    warning: {
      solid: 'bg-warning-500 text-warning-950 hover:bg-warning-600 active:bg-warning-700',
      outline: 'border-2 border-warning-500 text-warning-600 hover:bg-warning-50 dark:hover:bg-warning-950 dark:text-warning-400',
      ghost: 'text-warning-600 hover:bg-warning-50 dark:hover:bg-warning-950 dark:text-warning-400',
      soft: 'bg-warning-100 text-warning-800 hover:bg-warning-200 dark:bg-warning-950 dark:text-warning-300 dark:hover:bg-warning-900',
    },
    error: {
      solid: 'bg-error-500 text-white hover:bg-error-600 active:bg-error-700',
      outline: 'border-2 border-error-500 text-error-600 hover:bg-error-50 dark:hover:bg-error-950 dark:text-error-400',
      ghost: 'text-error-600 hover:bg-error-50 dark:hover:bg-error-950 dark:text-error-400',
      soft: 'bg-error-100 text-error-700 hover:bg-error-200 dark:bg-error-950 dark:text-error-300 dark:hover:bg-error-900',
    },
    info: {
      solid: 'bg-info-500 text-white hover:bg-info-600 active:bg-info-700',
      outline: 'border-2 border-info-500 text-info-600 hover:bg-info-50 dark:hover:bg-info-950 dark:text-info-400',
      ghost: 'text-info-600 hover:bg-info-50 dark:hover:bg-info-950 dark:text-info-400',
      soft: 'bg-info-100 text-info-700 hover:bg-info-200 dark:bg-info-950 dark:text-info-300 dark:hover:bg-info-900',
    },
  },
  disabled: 'opacity-50 cursor-not-allowed',
  loading: 'cursor-wait',
}

/**
 * Input variant configuration
 */
export const inputVariants = {
  base: 'w-full border bg-background text-foreground transition-colors duration-150 ease-out placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50',
  sizes: {
    sm: 'h-8 px-2.5 text-sm rounded-md',
    md: 'h-10 px-3 text-sm rounded-lg',
    lg: 'h-12 px-4 text-base rounded-lg',
  },
  colors: {
    primary: {
      solid: 'border-input focus:border-primary-500',
      outline: 'border-input focus:border-primary-500',
      ghost: 'border-transparent bg-muted focus:border-primary-500 focus:bg-background',
      soft: 'border-transparent bg-primary-50 focus:bg-background focus:border-primary-500 dark:bg-primary-950',
    },
    secondary: {
      solid: 'border-input focus:border-secondary-500',
      outline: 'border-input focus:border-secondary-500',
      ghost: 'border-transparent bg-muted focus:border-secondary-500 focus:bg-background',
      soft: 'border-transparent bg-secondary-50 focus:bg-background focus:border-secondary-500 dark:bg-secondary-950',
    },
    accent: {
      solid: 'border-input focus:border-accent-500',
      outline: 'border-input focus:border-accent-500',
      ghost: 'border-transparent bg-muted focus:border-accent-500 focus:bg-background',
      soft: 'border-transparent bg-accent-50 focus:bg-background focus:border-accent-500 dark:bg-accent-950',
    },
    success: {
      solid: 'border-success-500',
      outline: 'border-success-500',
      ghost: 'border-transparent bg-success-50 dark:bg-success-950',
      soft: 'border-transparent bg-success-50 dark:bg-success-950',
    },
    warning: {
      solid: 'border-warning-500',
      outline: 'border-warning-500',
      ghost: 'border-transparent bg-warning-50 dark:bg-warning-950',
      soft: 'border-transparent bg-warning-50 dark:bg-warning-950',
    },
    error: {
      solid: 'border-error-500 focus:ring-error-500',
      outline: 'border-error-500 focus:ring-error-500',
      ghost: 'border-transparent bg-error-50 focus:border-error-500 dark:bg-error-950',
      soft: 'border-transparent bg-error-50 focus:border-error-500 dark:bg-error-950',
    },
    info: {
      solid: 'border-input focus:border-info-500',
      outline: 'border-input focus:border-info-500',
      ghost: 'border-transparent bg-muted focus:border-info-500 focus:bg-background',
      soft: 'border-transparent bg-info-50 focus:bg-background focus:border-info-500 dark:bg-info-950',
    },
  },
  disabled: 'opacity-50 cursor-not-allowed bg-muted',
  loading: '',
}

/**
 * Badge variant configuration
 */
export const badgeVariants = {
  base: 'inline-flex items-center font-medium',
  sizes: {
    sm: 'px-1.5 py-0.5 text-xs rounded',
    md: 'px-2 py-0.5 text-xs rounded-md',
    lg: 'px-2.5 py-1 text-sm rounded-md',
  },
  colors: {
    primary: {
      solid: 'bg-primary-500 text-white',
      outline: 'border border-primary-500 text-primary-600 dark:text-primary-400',
      ghost: 'text-primary-600 dark:text-primary-400',
      soft: 'bg-primary-100 text-primary-700 dark:bg-primary-950 dark:text-primary-300',
    },
    secondary: {
      solid: 'bg-secondary-500 text-white',
      outline: 'border border-secondary-400 text-secondary-600 dark:text-secondary-400',
      ghost: 'text-secondary-600 dark:text-secondary-400',
      soft: 'bg-secondary-100 text-secondary-700 dark:bg-secondary-900 dark:text-secondary-300',
    },
    accent: {
      solid: 'bg-accent-500 text-white',
      outline: 'border border-accent-500 text-accent-600 dark:text-accent-400',
      ghost: 'text-accent-600 dark:text-accent-400',
      soft: 'bg-accent-100 text-accent-700 dark:bg-accent-950 dark:text-accent-300',
    },
    success: {
      solid: 'bg-success-500 text-white',
      outline: 'border border-success-500 text-success-600 dark:text-success-400',
      ghost: 'text-success-600 dark:text-success-400',
      soft: 'bg-success-100 text-success-700 dark:bg-success-950 dark:text-success-300',
    },
    warning: {
      solid: 'bg-warning-500 text-warning-950',
      outline: 'border border-warning-500 text-warning-600 dark:text-warning-400',
      ghost: 'text-warning-600 dark:text-warning-400',
      soft: 'bg-warning-100 text-warning-800 dark:bg-warning-950 dark:text-warning-300',
    },
    error: {
      solid: 'bg-error-500 text-white',
      outline: 'border border-error-500 text-error-600 dark:text-error-400',
      ghost: 'text-error-600 dark:text-error-400',
      soft: 'bg-error-100 text-error-700 dark:bg-error-950 dark:text-error-300',
    },
    info: {
      solid: 'bg-info-500 text-white',
      outline: 'border border-info-500 text-info-600 dark:text-info-400',
      ghost: 'text-info-600 dark:text-info-400',
      soft: 'bg-info-100 text-info-700 dark:bg-info-950 dark:text-info-300',
    },
  },
  disabled: '',
  loading: '',
}

/**
 * Alert variant configuration
 */
export const alertVariants = {
  base: 'relative flex gap-3 rounded-lg p-4',
  sizes: {
    sm: 'p-3 text-sm',
    md: 'p-4 text-sm',
    lg: 'p-5 text-base',
  },
  colors: {
    primary: {
      solid: 'bg-primary-500 text-white',
      outline: 'border-2 border-primary-500 text-primary-700 dark:text-primary-300',
      ghost: 'text-primary-700 dark:text-primary-300',
      soft: 'bg-primary-50 text-primary-700 dark:bg-primary-950 dark:text-primary-300',
    },
    secondary: {
      solid: 'bg-secondary-500 text-white',
      outline: 'border-2 border-secondary-400 text-secondary-700 dark:text-secondary-300',
      ghost: 'text-secondary-700 dark:text-secondary-300',
      soft: 'bg-secondary-100 text-secondary-700 dark:bg-secondary-900 dark:text-secondary-300',
    },
    accent: {
      solid: 'bg-accent-500 text-white',
      outline: 'border-2 border-accent-500 text-accent-700 dark:text-accent-300',
      ghost: 'text-accent-700 dark:text-accent-300',
      soft: 'bg-accent-50 text-accent-700 dark:bg-accent-950 dark:text-accent-300',
    },
    success: {
      solid: 'bg-success-500 text-white',
      outline: 'border-2 border-success-500 text-success-700 dark:text-success-300',
      ghost: 'text-success-700 dark:text-success-300',
      soft: 'bg-success-50 text-success-700 dark:bg-success-950 dark:text-success-300',
    },
    warning: {
      solid: 'bg-warning-500 text-warning-950',
      outline: 'border-2 border-warning-500 text-warning-700 dark:text-warning-300',
      ghost: 'text-warning-700 dark:text-warning-300',
      soft: 'bg-warning-50 text-warning-800 dark:bg-warning-950 dark:text-warning-300',
    },
    error: {
      solid: 'bg-error-500 text-white',
      outline: 'border-2 border-error-500 text-error-700 dark:text-error-300',
      ghost: 'text-error-700 dark:text-error-300',
      soft: 'bg-error-50 text-error-700 dark:bg-error-950 dark:text-error-300',
    },
    info: {
      solid: 'bg-info-500 text-white',
      outline: 'border-2 border-info-500 text-info-700 dark:text-info-300',
      ghost: 'text-info-700 dark:text-info-300',
      soft: 'bg-info-50 text-info-700 dark:bg-info-950 dark:text-info-300',
    },
  },
  disabled: '',
  loading: '',
}
