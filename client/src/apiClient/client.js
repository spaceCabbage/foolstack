import axios from 'axios'

const domain = import.meta.env.VITE_DOMAIN || 'localhost'
const baseURL = `https://${domain}/api`

const client = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export { client }
