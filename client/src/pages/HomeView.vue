<template>
  <MainLayout class="h-screen w-screen flex items-center justify-center">
    <div>
      <h1
        class="text-9xl font-bold text-shadow"
        :class="{
          'text-yellow-500': isLoading,
          'text-red-500': isError || (data && data.status !== 'healthy'),
          'text-green-500': !isLoading && !isError && data && data.status === 'healthy',
        }"
      >
        FOOLSTACK
      </h1>
    </div>
  </MainLayout>
</template>

<script setup>
import { useQuery } from '@tanstack/vue-query'
import { getHealth } from '@/apiClient/queries'
import MainLayout from '@/components/layouts/MainLayout.vue'

const { data, isLoading, isError } = useQuery({
  queryFn: getHealth,
  queryKey: ['health'],
})
</script>
