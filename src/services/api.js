import { defaultSiteConfig } from '@/data/defaultConfig'
import { defaultPages } from '@/data/defaultPages'

const API_BASE = import.meta.env.VITE_API_BASE || '/api'
const TOKEN_KEY = 'xingyu_admin_token'

async function request(url, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...options.headers }
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) headers['Authorization'] = `Bearer ${token}`

  try {
    const res = await fetch(`${API_BASE}${url}`, { ...options, headers })
    if (res.status === 401 || res.status === 422) {
      localStorage.removeItem(TOKEN_KEY)
      throw { status: res.status, message: '认证失效，请重新登录' }
    }
    const data = await res.json()
    if (!res.ok) throw { status: res.status, message: data.message || '请求失败' }
    return data
  } catch (err) {
    if (err.status) throw err
    throw { status: 0, message: '网络错误，请检查后端服务是否启动' }
  }
}

// ─── Public API ───

let _configCache = null

export async function getSiteConfig() {
  if (_configCache) return _configCache
  try {
    const data = await request('/config')
    _configCache = data
    return data
  } catch {
    return null
  }
}

export async function getPage(slug) {
  try {
    const data = await request(`/pages/${slug}`)
    return data
  } catch {
    return null
  }
}

export async function getAllPages() {
  try {
    return await request('/pages')
  } catch {
    return []
  }
}

export async function submitApplication(payload) {
  return request('/applications', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

// ─── Admin API ───

export async function login(username, password) {
  const data = await request('/admin/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
  if (data.token) localStorage.setItem(TOKEN_KEY, data.token)
  return data
}

export function logout() {
  localStorage.removeItem(TOKEN_KEY)
}

export function isLoggedIn() {
  return !!localStorage.getItem(TOKEN_KEY)
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export async function getCurrentUser() {
  return request('/admin/me')
}

export async function getAdminConfig() {
  return request('/admin/config')
}

export async function updateConfig(config) {
  const result = await request('/admin/config', { method: 'PUT', body: JSON.stringify(config) })
  _configCache = null
  return result
}

export async function updateConfigSection(key, value) {
  return request(`/admin/config/${key}`, { method: 'PUT', body: JSON.stringify(value) })
}

export async function getAdminPages() {
  return request('/admin/pages')
}

export async function getAdminPage(slug) {
  return request(`/admin/pages/${slug}`)
}

export async function updatePage(slug, data) {
  return request(`/admin/pages/${slug}`, { method: 'PUT', body: JSON.stringify(data) })
}

export async function createPage(slug, data) {
  return request('/admin/pages', { method: 'POST', body: JSON.stringify({ slug, ...data }) })
}

export async function deletePage(slug) {
  return request(`/admin/pages/${slug}`, { method: 'DELETE' })
}

export async function resetPage(slug) {
  return request(`/admin/pages/${slug}/reset`, { method: 'POST' })
}

export async function getApplications(status = 'all') {
  return request(`/admin/applications?status=${status}`)
}

export async function updateApplication(id, payload) {
  return request(`/admin/applications/${id}`, { method: 'PATCH', body: JSON.stringify(payload) })
}

export async function deleteApplication(id) {
  return request(`/admin/applications/${id}`, { method: 'DELETE' })
}

export async function exportAll() {
  return request('/admin/export')
}

export async function importAll(data) {
  return request('/admin/import', { method: 'POST', body: JSON.stringify(data) })
}

export async function resetAllContent() {
  const result = await request('/admin/reset-all', { method: 'POST' })
  _configCache = null
  return result
}

export async function uploadImage(file) {
  const token = localStorage.getItem(TOKEN_KEY)
  const formData = new FormData()
  formData.append('file', file)

  const res = await fetch(`${API_BASE}/admin/upload-image`, {
    method: 'POST',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    body: formData,
  })

  const data = await res.json()
  if (!res.ok) throw { status: res.status, message: data.message || '上传失败' }
  return data
}

export function getDefaultConfig() {
  return JSON.parse(JSON.stringify(defaultSiteConfig))
}

export async function deleteImage(url) {
  return request('/admin/delete-image', {
    method: 'POST',
    body: JSON.stringify({ url }),
  })
}
