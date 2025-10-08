import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export const api = axios.create({ baseURL })

export async function uploadFile(file) {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function fetchSummary(id) {
  const { data } = await api.get(`/summary/${id}`)
  return data
}

export async function fetchHistory() {
  const { data } = await api.get('/history')
  return data.items
}
