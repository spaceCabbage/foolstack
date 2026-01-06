<template>
  <div class="relative">
    <select
      ref="selectRef"
      v-model="model"
      :class="[
        variantClasses,
        'appearance-none pr-10 cursor-pointer',
        hasError && 'border-error-500 focus:ring-error-500',
        $attrs.class,
      ]"
      :disabled="disabled"
      :aria-invalid="hasError || undefined"
      v-bind="{ ...$attrs, class: undefined }"
    >
      <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
      <slot />
    </select>
    <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-muted-foreground">
      <PhCaretDown class="w-4 h-4" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useVariants, inputVariants } from '@/composables/useVariants'
import { PhCaretDown } from '@phosphor-icons/vue'

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
  placeholder: {
    type: String,
    default: '',
  },
})

defineOptions({
  inheritAttrs: false,
})

const model = defineModel()
const selectRef = ref(null)

const variantClasses = useVariants(props, inputVariants)

defineExpose({
  selectRef,
  focus: () => selectRef.value?.focus(),
})
</script>
