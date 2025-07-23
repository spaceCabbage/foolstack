import { client } from '@/apiClient/client'

export async function getHealth() {
  const res = await client.get('/health/')
  return res.data
}
