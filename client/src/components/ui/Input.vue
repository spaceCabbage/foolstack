<template>
  <div class="relative">
    <div
      v-if="$slots.leading"
      class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-muted-foreground"
    >
      <slot name="leading" />
    </div>
    <input
      ref="inputRef"
      v-model="model"
      :class="[
        variantClasses,
        $slots.leading && paddingLeft,
        ($slots.trailing || loading) && 'pr-10',
        hasError && 'border-error-500 focus:ring-error-500',
        $attrs.class,
      ]"
      :disabled="disabled || loading"
      :aria-invalid="hasError || undefined"
      :aria-describedby="hasError ? `${inputId}-error` : undefined"
      v-bind="{ ...$attrs, class: undefined }"
    />
    <div
      v-if="$slots.trailing || loading"
      class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-muted-foreground"
    >
      <Spinner v-if="loading" size="sm" />
      <slot v-else name="trailing" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, useId } from 'vue'
import { useVariants, inputVariants } from '@/composables/useVariants'
import Spinner from './Spinner.vue'

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
  loading: {
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
const inputRef = ref(null)
const inputId = useId()

const variantClasses = useVariants(props, inputVariants)

const paddingLeft = computed(() => {
  const sizes = {
    sm: 'pl-9',
    md: 'pl-10',
    lg: 'pl-11',
  }
  return sizes[props.size]
})

defineExpose({
  inputRef,
  focus: () => inputRef.value?.focus(),
  blur: () => inputRef.value?.blur(),
  select: () => inputRef.value?.select(),
})
</script>
