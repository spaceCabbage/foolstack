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
        type="radio"
        :value="value"
        v-model="model"
        :disabled="disabled"
        :name="name"
        class="peer sr-only"
        v-bind="$attrs"
      />
      <div
        :class="[
          'flex items-center justify-center border-2 rounded-full transition-colors duration-150',
          sizeClasses,
          isSelected
            ? `border-${color}-500`
            : 'border-input',
          'peer-focus-visible:ring-2 peer-focus-visible:ring-ring peer-focus-visible:ring-offset-2',
        ]"
      >
        <div
          v-if="isSelected"
          :class="[
            'rounded-full',
            `bg-${color}-500`,
            dotSize,
          ]"
        />
      </div>
    </div>
    <span v-if="$slots.default" :class="labelSizeClass">
      <slot />
    </span>
  </label>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  value: {
    type: [String, Number, Boolean],
    required: true,
  },
  name: {
    type: String,
    default: '',
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
  disabled: {
    type: Boolean,
    default: false,
  },
})

const model = defineModel()
const inputRef = ref(null)

const isSelected = computed(() => model.value === props.value)

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
  }
  return sizes[props.size]
})

const dotSize = computed(() => {
  const sizes = {
    sm: 'w-2 h-2',
    md: 'w-2.5 h-2.5',
    lg: 'w-3 h-3',
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
