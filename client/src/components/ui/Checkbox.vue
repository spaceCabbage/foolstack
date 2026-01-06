<template>
  <label
    :class="[
      'inline-flex items-center gap-2 cursor-pointer select-none',
      disabled && 'cursor-not-allowed opacity-50',
    ]"
  >
    <div class="relative">
      <input
        ref="inputRef"
        type="checkbox"
        v-model="model"
        :disabled="disabled"
        :class="[
          'peer sr-only',
        ]"
        v-bind="$attrs"
      />
      <div
        :class="[
          'flex items-center justify-center border-2 rounded transition-colors duration-150',
          sizeClasses,
          model
            ? `bg-${color}-500 border-${color}-500 text-white`
            : 'bg-background border-input',
          'peer-focus-visible:ring-2 peer-focus-visible:ring-ring peer-focus-visible:ring-offset-2',
        ]"
      >
        <PhCheck v-if="model" :class="iconSize" weight="bold" />
      </div>
    </div>
    <span v-if="$slots.default" :class="labelSizeClass">
      <slot />
    </span>
  </label>
</template>

<script setup>
import { ref, computed } from 'vue'
import { PhCheck } from '@phosphor-icons/vue'

const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v),
  },
  color: {
    type: String,
    default: 'primary',
    validator: (v) =>
      ['primary', 'secondary', 'accent', 'success', 'warning', 'error', 'info'].includes(v),
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})

const model = defineModel({ type: Boolean, default: false })
const inputRef = ref(null)

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
  }
  return sizes[props.size]
})

const iconSize = computed(() => {
  const sizes = {
    sm: 'w-3 h-3',
    md: 'w-3.5 h-3.5',
    lg: 'w-4 h-4',
  }
  return sizes[props.size]
})

const labelSizeClass = computed(() => {
  const sizes = {
    sm: 'text-sm',
    md: 'text-sm',
    lg: 'text-base',
  }
  return sizes[props.size]
})

defineExpose({
  inputRef,
  focus: () => inputRef.value?.focus(),
})
</script>
