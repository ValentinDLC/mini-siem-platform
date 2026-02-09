import axios from 'axios'

const API = axios.create({
  baseURL: '/api/v1'
})

export const getStats = () => API.get('/stats/')
export const getLogs = (params = {}) => API.get('/logs/', { params })
export const getAlerts = (params = {}) => API.get('/alerts/', { params })
export const searchLogs = (q) => API.get(`/logs/search/?q=${q}`)
export const acknowledgeAlert = (id) => API.put(`/alerts/${id}/acknowledge`)
