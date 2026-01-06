<template>
  <div
    :class="[
      'relative inline-flex items-center justify-center overflow-hidden rounded-full bg-muted text-muted-foreground font-medium',
      sizeClasses,
      $attrs.class,
    ]"
    v-bind="{ ...$attrs, class: undefined }"
  >
    <img
      v-if="src && !imgError"
      :src="src"
      :alt="alt"
      class="w-full h-full object-cover"
      @error="imgError = true"
    />
    <span v-else-if="initials">{{ initials }}</span>
    <slot v-else>
      <PhUser :class="iconSize" />
    </slot>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { PhUser } from '@phosphor-icons/vue'

const props = defineProps({
  src: {
    type: String,
    default: '',
  },
  alt: {
    type: String,
    default: '',
  },
  initials: {
    type: String,
    default: '',
  },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg', 'xl'].includes(v),
  },
})

defineOptions({
  inheritAttrs: false,
})

const imgError = ref(false)

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'w-8 h-8 text-xs',
    md: 'w-10 h-10 text-sm',
    lg: 'w-12 h-12 text-base',
    xl: 'w-16 h-16 text-lg',
  }
  return sizes[props.size]
})

const iconSize = computed(() => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
    xl: 'w-8 h-8',
  }
  return sizes[props.size]
})
</script>
