<template>
  <div
    :class="[variantClasses, $attrs.class]"
    role="alert"
    v-bind="{ ...$attrs, class: undefined }"
  >
    <slot name="icon">
      <component
        v-if="icon"
        :is="iconComponent"
        :class="iconSize"
        weight="fill"
      />
    </slot>
    <div class="flex-1 min-w-0">
      <h5 v-if="title" class="font-medium mb-1">{{ title }}</h5>
      <div :class="[title ? 'text-sm opacity-90' : '']">
        <slot />
      </div>
    </div>
    <button
      v-if="dismissible"
      @click="$emit('dismiss')"
      class="shrink-0 p-0.5 rounded opacity-70 hover:opacity-100 transition-opacity"
      aria-label="Dismiss alert"
    >
      <PhX class="w-4 h-4" />
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useVariants, alertVariants } from '@/composables/useVariants'
import {
  PhCheckCircle,
  PhWarning,
  PhXCircle,
  PhInfo,
  PhX,
} from '@phosphor-icons/vue'

const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v),
  },
  color: {
    type: String,
    default: 'info',
    validator: (v) =>
      ['primary', 'secondary', 'accent', 'success', 'warning', 'error', 'info'].includes(v),
  },
  variant: {
    type: String,
    default: 'soft',
    validator: (v) => ['solid', 'outline', 'ghost', 'soft'].includes(v),
  },
  title: {
    type: String,
    default: '',
  },
  icon: {
    type: Boolean,
    default: true,
  },
  dismissible: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['dismiss'])

defineOptions({
  inheritAttrs: false,
})

const variantClasses = useVariants(props, alertVariants)

const iconComponent = computed(() => {
  const icons = {
    success: PhCheckCircle,
    warning: PhWarning,
    error: PhXCircle,
    info: PhInfo,
    primary: PhInfo,
    secondary: PhInfo,
    accent: PhInfo,
  }
  return icons[props.color]
})

const iconSize = computed(() => {
  const sizes = {
    sm: 'w-4 h-4 shrink-0 mt-0.5',
    md: 'w-5 h-5 shrink-0 mt-0.5',
    lg: 'w-6 h-6 shrink-0',
  }
  return sizes[props.size]
})
</script>
