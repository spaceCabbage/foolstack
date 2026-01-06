<template>
  <div
    role="radiogroup"
    :aria-label="label"
    :class="[
      orientation === 'horizontal' ? 'flex flex-wrap gap-4' : 'flex flex-col gap-2',
      $attrs.class,
    ]"
    v-bind="{ ...$attrs, class: undefined }"
  >
    <slot />
  </div>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    default: '',
  },
  orientation: {
    type: String,
    default: 'vertical',
    validator: (v) => ['horizontal', 'vertical'].includes(v),
  },
})

defineOptions({
  inheritAttrs: false,
})
</script>
