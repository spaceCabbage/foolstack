<template>
  <button
    :class="[
      'flex w-full items-center gap-2 px-3 py-2 text-sm text-left transition-colors',
      'hover:bg-muted focus:bg-muted focus:outline-none',
      disabled && 'opacity-50 pointer-events-none',
      destructive && 'text-error-500 hover:bg-error-50 dark:hover:bg-error-950',
    ]"
    :disabled="disabled"
    v-bind="$attrs"
  >
    <slot name="leading" />
    <span class="flex-1">
      <slot />
    </span>
    <slot name="trailing" />
  </button>
</template>

<script setup>
defineProps({
  disabled: {
    type: Boolean,
    default: false,
  },
  destructive: {
    type: Boolean,
    default: false,
  },
})
</script>
