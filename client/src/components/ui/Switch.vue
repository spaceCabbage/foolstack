<template>
  <label
    :class="[
      'inline-flex items-center gap-2 cursor-pointer select-none',
      disabled && 'cursor-not-allowed opacity-50',
    ]"
  >
    <button
      ref="buttonRef"
      type="button"
      role="switch"
      :aria-checked="model"
      :disabled="disabled"
      @click="toggle"
      :class="[
        'relative inline-flex shrink-0 rounded-full border-2 border-transparent transition-colors duration-150 ease-out',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        trackSize,
        model ? `bg-${color}-500` : 'bg-secondary-300 dark:bg-secondary-700',
      ]"
    >
      <span
        :class="[
          'pointer-events-none inline-block rounded-full bg-white shadow-sm ring-0 transition-transform duration-150 ease-out',
          thumbSize,
          model ? translateClass : 'translate-x-0',
        ]"
      />
    </button>
    <span v-if="$slots.default" :class="labelSizeClass">
      <slot />
    </span>
  </label>
</template>

<script setup>
import { ref, computed } from 'vue'

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
const buttonRef = ref(null)

const trackSize = computed(() => {
  const sizes = {
    sm: 'h-5 w-9',
    md: 'h-6 w-11',
    lg: 'h-7 w-14',
  }
  return sizes[props.size]
})

const thumbSize = computed(() => {
  const sizes = {
    sm: 'h-4 w-4',
    md: 'h-5 w-5',
    lg: 'h-6 w-6',
  }
  return sizes[props.size]
})

const translateClass = computed(() => {
  const sizes = {
    sm: 'translate-x-4',
    md: 'translate-x-5',
    lg: 'translate-x-7',
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

function toggle() {
  if (!props.disabled) {
    model.value = !model.value
  }
}

defineExpose({
  buttonRef,
  focus: () => buttonRef.value?.focus(),
})
</script>
