<template>
  <main class="h-screen w-screen flex items-center justify-center">
    <div>
      <h1 class="text-9xl font-bold">GELT</h1>
      <div class="text-center">
        <span v-if="isLoading">loading</span>
        <span v-else-if="isError">{{ error }}</span>
        <span v-else>{{ data.status }}</span>
      </div>
    </div>
  </main>
</template>

<script setup>
import { useQuery } from '@tanstack/vue-query'
import { getHealth } from '@/apiClient/queries'

const { data, isLoading, isError, error } = useQuery({
  queryFn: getHealth,
  queryKey: ['health'],
})
</script>
