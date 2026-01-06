<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        @keydown.escape="closeOnEscape && close()"
      >
        <!-- Backdrop -->
        <div
          class="absolute inset-0 bg-black/50 backdrop-blur-sm"
          @click="closeOnBackdrop && close()"
          aria-hidden="true"
        />

        <!-- Modal panel -->
        <div
          ref="panelRef"
          role="dialog"
          aria-modal="true"
          :aria-labelledby="title ? titleId : undefined"
          :class="[
            'relative z-10 w-full bg-card text-card-foreground rounded-xl shadow-xl',
            'max-h-[90vh] overflow-hidden flex flex-col',
            sizeClasses,
          ]"
        >
          <!-- Header -->
          <div
            v-if="$slots.header || title"
            class="flex items-center justify-between px-6 py-4 border-b border-border"
          >
            <slot name="header">
              <h2 :id="titleId" class="text-lg font-semibold">{{ title }}</h2>
            </slot>
            <button
              v-if="closable"
              @click="close"
              class="p-1.5 rounded-md text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
              aria-label="Close modal"
            >
              <PhX class="w-5 h-5" />
            </button>
          </div>

          <!-- Body -->
          <div class="flex-1 overflow-y-auto px-6 py-4">
            <slot />
          </div>

          <!-- Footer -->
          <div
            v-if="$slots.footer"
            class="flex items-center justify-end gap-3 px-6 py-4 border-t border-border bg-muted/30"
          >
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, onUnmounted, useId } from 'vue'
import { PhX } from '@phosphor-icons/vue'

const props = defineProps({
  title: {
    type: String,
    default: '',
  },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg', 'xl', 'full'].includes(v),
  },
  closable: {
    type: Boolean,
    default: true,
  },
  closeOnBackdrop: {
    type: Boolean,
    default: true,
  },
  closeOnEscape: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['close'])

const modelValue = defineModel({ type: Boolean, default: false })

const panelRef = ref(null)
const titleId = useId()

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    full: 'max-w-4xl',
  }
  return sizes[props.size]
})

function close() {
  modelValue.value = false
  emit('close')
}

// Lock body scroll when open
watch(modelValue, (open) => {
  if (open) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

onUnmounted(() => {
  document.body.style.overflow = ''
})

defineExpose({
  close,
})
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 200ms ease;
}
.modal-enter-active > div:last-child,
.modal-leave-active > div:last-child {
  transition: transform 200ms ease, opacity 200ms ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from > div:last-child,
.modal-leave-to > div:last-child {
  transform: scale(0.95);
  opacity: 0;
}
</style>
