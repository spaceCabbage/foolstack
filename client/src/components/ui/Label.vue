<template>
  <label
    :class="[
      'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
      $attrs.class,
    ]"
    v-bind="{ ...$attrs, class: undefined }"
  >
    <slot />
    <span v-if="required" class="text-error-500 ml-0.5">*</span>
  </label>
</template>

<script setup>
defineProps({
  required: {
    type: Boolean,
    default: false,
  },
})

defineOptions({
  inheritAttrs: false,
})
</script>
