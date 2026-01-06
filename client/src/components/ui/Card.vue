<template>
  <div
    :class="[
      'rounded-xl border bg-card text-card-foreground',
      shadow && 'shadow-md',
      $attrs.class,
    ]"
    v-bind="{ ...$attrs, class: undefined }"
  >
    <!-- Header slot -->
    <div v-if="$slots.header" class="flex flex-col space-y-1.5 p-6 pb-0">
      <slot name="header" />
    </div>

    <!-- Default content slot -->
    <div class="p-6">
      <slot />
    </div>

    <!-- Footer slot -->
    <div v-if="$slots.footer" class="flex items-center p-6 pt-0">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  shadow: {
    type: Boolean,
    default: false,
  },
})

defineOptions({
  inheritAttrs: false,
})
</script>
