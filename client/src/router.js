import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/pages/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
]

// Dev-only routes
if (import.meta.env.DEV) {
  routes.push({
    path: '/dev/showcase',
    name: 'showcase',
    component: () => import('@/pages/ShowcasePage.vue'),
  })
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
