<template>
  <div class="space-y-1.5">
    <Label v-if="label" :for="fieldId" :required="required">
      {{ label }}
    </Label>
    <slot :id="fieldId" :has-error="!!error" :aria-describedby="ariaDescribedBy" />
    <p v-if="hint && !error" :id="`${fieldId}-hint`" class="text-sm text-muted-foreground">
      {{ hint }}
    </p>
    <p v-if="error" :id="`${fieldId}-error`" class="text-sm text-error-500" role="alert">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import { computed, useId } from 'vue'
import Label from './Label.vue'

const props = defineProps({
  label: {
    type: String,
    default: '',
  },
  hint: {
    type: String,
    default: '',
  },
  error: {
    type: String,
    default: '',
  },
  required: {
    type: Boolean,
    default: false,
  },
})

const fieldId = useId()

const ariaDescribedBy = computed(() => {
  const ids = []
  if (props.hint && !props.error) ids.push(`${fieldId}-hint`)
  if (props.error) ids.push(`${fieldId}-error`)
  return ids.length ? ids.join(' ') : undefined
})
</script>
