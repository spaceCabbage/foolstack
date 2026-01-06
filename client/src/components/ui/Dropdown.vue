<template>
  <div class="relative inline-block" ref="containerRef">
    <div @click="toggle">
      <slot name="trigger" :open="isOpen" />
    </div>

    <Teleport to="body">
      <Transition name="dropdown">
        <div
          v-if="isOpen"
          ref="menuRef"
          :class="[
            'fixed z-50 min-w-48 rounded-lg border bg-popover text-popover-foreground shadow-lg',
            'overflow-hidden py-1',
          ]"
          :style="menuStyle"
          @click="closeOnSelect && close()"
        >
          <slot />
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'

const props = defineProps({
  align: {
    type: String,
    default: 'start',
    validator: (v) => ['start', 'end', 'center'].includes(v),
  },
  side: {
    type: String,
    default: 'bottom',
    validator: (v) => ['top', 'bottom'].includes(v),
  },
  closeOnSelect: {
    type: Boolean,
    default: true,
  },
})

const isOpen = defineModel('open', { type: Boolean, default: false })

const containerRef = ref(null)
const menuRef = ref(null)
const menuStyle = ref({})

function toggle() {
  isOpen.value = !isOpen.value
}

function close() {
  isOpen.value = false
}

function updatePosition() {
  if (!containerRef.value || !isOpen.value) return

  const triggerRect = containerRef.value.getBoundingClientRect()
  const style = {}

  // Vertical position
  if (props.side === 'bottom') {
    style.top = `${triggerRect.bottom + 4}px`
  } else {
    style.bottom = `${window.innerHeight - triggerRect.top + 4}px`
  }

  // Horizontal position
  if (props.align === 'start') {
    style.left = `${triggerRect.left}px`
  } else if (props.align === 'end') {
    style.right = `${window.innerWidth - triggerRect.right}px`
  } else {
    style.left = `${triggerRect.left + triggerRect.width / 2}px`
    style.transform = 'translateX(-50%)'
  }

  menuStyle.value = style
}

// Update position when opening
watch(isOpen, async (open) => {
  if (open) {
    await nextTick()
    updatePosition()
  }
})

// Close on outside click
function handleClickOutside(event) {
  if (
    isOpen.value &&
    containerRef.value &&
    !containerRef.value.contains(event.target) &&
    menuRef.value &&
    !menuRef.value.contains(event.target)
  ) {
    close()
  }
}

// Close on escape
function handleEscape(event) {
  if (event.key === 'Escape' && isOpen.value) {
    close()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleEscape)
  window.addEventListener('resize', updatePosition)
  window.addEventListener('scroll', updatePosition, true)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleEscape)
  window.removeEventListener('resize', updatePosition)
  window.removeEventListener('scroll', updatePosition, true)
})

defineExpose({
  open: () => (isOpen.value = true),
  close,
  toggle,
})
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 150ms ease, transform 150ms ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
