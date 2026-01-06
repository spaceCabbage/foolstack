<template>
  <span
    :class="[variantClasses, $attrs.class]"
    v-bind="{ ...$attrs, class: undefined }"
  >
    <slot name="leading" />
    <slot />
    <slot name="trailing" />
  </span>
</template>

<script setup>
import { useVariants, badgeVariants } from '@/composables/useVariants'

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
    default: 'soft',
    validator: (v) => ['solid', 'outline', 'ghost', 'soft'].includes(v),
  },
})

defineOptions({
  inheritAttrs: false,
})

const variantClasses = useVariants(props, badgeVariants)
</script>
