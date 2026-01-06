<template>
  <div
    :class="['relative overflow-hidden rounded-full bg-secondary-200 dark:bg-secondary-800', heightClass]"
    role="progressbar"
    :aria-valuenow="value"
    :aria-valuemin="0"
    :aria-valuemax="max"
  >
    <div
      :class="[
        'h-full rounded-full transition-all duration-300 ease-out',
        `bg-${color}-500`,
        indeterminate && 'animate-indeterminate',
      ]"
      :style="indeterminate ? {} : { width: `${percentage}%` }"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: {
    type: Number,
    default: 0,
  },
  max: {
    type: Number,
    default: 100,
  },
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
  indeterminate: {
    type: Boolean,
    default: false,
  },
})

const percentage = computed(() => {
  return Math.min(100, Math.max(0, (props.value / props.max) * 100))
})

const heightClass = computed(() => {
  const sizes = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3',
  }
  return sizes[props.size]
})
</script>

<style scoped>
@keyframes indeterminate {
  0% {
    width: 30%;
    transform: translateX(-100%);
  }
  50% {
    width: 30%;
  }
  100% {
    width: 30%;
    transform: translateX(400%);
  }
}

.animate-indeterminate {
  animation: indeterminate 1.5s ease-in-out infinite;
}
</style>
