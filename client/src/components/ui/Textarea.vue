<template>
  <textarea
    ref="textareaRef"
    v-model="model"
    :class="[
      variantClasses,
      'min-h-[80px] resize-y py-2',
      hasError && 'border-error-500 focus:ring-error-500',
      $attrs.class,
    ]"
    :disabled="disabled"
    :aria-invalid="hasError || undefined"
    v-bind="{ ...$attrs, class: undefined }"
  />
</template>

<script setup>
import { ref } from 'vue'
import { useVariants, inputVariants } from '@/composables/useVariants'

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
  variant: {
    type: String,
    default: 'outline',
    validator: (v) => ['solid', 'outline', 'ghost', 'soft'].includes(v),
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  hasError: {
    type: Boolean,
    default: false,
  },
})

defineOptions({
  inheritAttrs: false,
})

const model = defineModel()
const textareaRef = ref(null)

// Override height from inputVariants since textarea doesn't use fixed height
const variantClasses = useVariants({ ...props, size: undefined }, {
  ...inputVariants,
  sizes: {
    sm: 'px-2.5 text-sm rounded-md',
    md: 'px-3 text-sm rounded-lg',
    lg: 'px-4 text-base rounded-lg',
  },
})

defineExpose({
  textareaRef,
  focus: () => textareaRef.value?.focus(),
  blur: () => textareaRef.value?.blur(),
})
</script>
