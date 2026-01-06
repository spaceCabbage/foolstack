<template>
  <button
    :class="[variantClasses, $attrs.class]"
    :disabled="disabled || loading"
    :aria-disabled="disabled || loading"
    :aria-busy="loading"
    v-bind="{ ...$attrs, class: undefined }"
  >
    <Spinner v-if="loading" :size="spinnerSize" class="shrink-0" />
    <slot v-else name="leading" />
    <span v-if="$slots.default" :class="{ 'opacity-0': loading && !$slots.leading }">
      <slot />
    </span>
    <slot name="trailing" />
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { useVariants, buttonVariants } from '@/composables/useVariants'
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
    default: 'solid',
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
})

defineOptions({
  inheritAttrs: false,
})

const variantClasses = useVariants(props, buttonVariants)

const spinnerSize = computed(() => {
  return props.size === 'lg' ? 'md' : 'sm'
})
</script>
