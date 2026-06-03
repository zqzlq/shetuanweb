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

export async function submitContact(payload) {
  return request('/contact', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

// ─── User Auth API ───

const USER_TOKEN_KEY = 'xingyu_user_token'

async function userRequest(url, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...options.headers }
  const token = localStorage.getItem(USER_TOKEN_KEY)
  if (token) headers['Authorization'] = `Bearer ${token}`

  try {
    const res = await fetch(`${API_BASE}${url}`, { ...options, headers })
    if (res.status === 401 || res.status === 422) {
      localStorage.removeItem(USER_TOKEN_KEY)
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

export async function userRegister(payload) {
  return request('/auth/register', { method: 'POST', body: JSON.stringify(payload) })
}

export async function userLogin(username, password) {
  const data = await request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
  if (data.token) localStorage.setItem(USER_TOKEN_KEY, data.token)
  return data
}

export function userLogout() {
  localStorage.removeItem(USER_TOKEN_KEY)
}

export function isUserLoggedIn() {
  return !!localStorage.getItem(USER_TOKEN_KEY)
}

export function getUserToken() {
  return localStorage.getItem(USER_TOKEN_KEY)
}

export async function getCurrentMemberUser() {
  return userRequest('/auth/me')
}

export async function changePassword(old_password, new_password) {
  return userRequest('/auth/password', { method: 'PATCH', body: JSON.stringify({ old_password, new_password }) })
}

export async function updateUserProfile(payload) {
  return userRequest('/auth/profile', { method: 'PATCH', body: JSON.stringify(payload) })
}

export async function submitUserSubmission(payload) {
  return userRequest('/auth/submission', { method: 'POST', body: JSON.stringify(payload) })
}

export async function getUserSubmissions() {
  return userRequest('/auth/submissions')
}

export async function deleteUserSubmission(id) {
  return userRequest(`/auth/submission/${id}`, { method: 'DELETE' })
}

// ─── Admin: Users & Submissions ───

export async function getUsers(status = 'all') {
  return request(`/admin/users?status=${status}`)
}

export async function updateUser(id, payload) {
  return request(`/admin/users/${id}`, { method: 'PATCH', body: JSON.stringify(payload) })
}

export async function getSubmissions(status = 'all') {
  return request(`/admin/submissions?status=${status}`)
}

export async function updateSubmission(id, payload) {
  return request(`/admin/submissions/${id}`, { method: 'PATCH', body: JSON.stringify(payload) })
}

export async function deleteUser(id) {
  return request(`/admin/users/${id}`, { method: 'DELETE' })
}

export async function batchUpdateUsers(payload) {
  return request('/admin/users/batch', { method: 'POST', body: JSON.stringify(payload) })
}

export async function syncUserToMember(id) {
  return request(`/admin/users/${id}/sync-member`, { method: 'POST' })
}

export async function syncSubmissionToPage(id) {
  return request(`/admin/submissions/${id}/sync`, { method: 'POST' })
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

export async function getApplications(status = 'all', session = '') {
  const params = new URLSearchParams()
  params.set('status', status)
  if (session) params.set('session', session)
  return request(`/admin/applications?${params.toString()}`)
}

export async function updateApplication(id, payload) {
  return request(`/admin/applications/${id}`, { method: 'PATCH', body: JSON.stringify(payload) })
}

export async function batchUpdateApplications(payload) {
  return request('/admin/applications/batch', { method: 'POST', body: JSON.stringify(payload) })
}

export async function deleteApplication(id) {
  return request(`/admin/applications/${id}`, { method: 'DELETE' })
}

export async function getContactMessages(status = 'all') {
  return request(`/admin/contact-messages?status=${status}`)
}

export async function updateContactMessage(id, payload) {
  return request(`/admin/contact-messages/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}

export async function deleteContactMessage(id) {
  return request(`/admin/contact-messages/${id}`, { method: 'DELETE' })
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
  // 优先用 admin token，没有则用 user token
  const token = localStorage.getItem(TOKEN_KEY) || localStorage.getItem(USER_TOKEN_KEY)
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
  const token = localStorage.getItem(TOKEN_KEY) || localStorage.getItem(USER_TOKEN_KEY)
  const headers = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(`${API_BASE}/admin/delete-image`, {
    method: 'POST', headers, body: JSON.stringify({ url }),
  })
  const data = await res.json()
  if (!res.ok) throw { status: res.status, message: data.message || '删除失败' }
  return data
}

// ─── Resources API (user) ───

export async function getResourceTree() {
  return userRequest('/resources/tree')
}

export async function getResourceStats(parentId) {
  const params = parentId ? `?parent_id=${parentId}` : ''
  return userRequest(`/resources/stats${params}`)
}

export async function getResourceTags() {
  return userRequest('/resources/tags')
}

export async function getResources(params = {}) {
  const searchParams = new URLSearchParams()
  if (params.parent_id) searchParams.set('parent_id', params.parent_id)
  if (params.page) searchParams.set('page', params.page)
  if (params.per_page) searchParams.set('per_page', params.per_page)
  if (params.search) searchParams.set('search', params.search)
  if (params.category) searchParams.set('category', params.category)
  if (params.tag) searchParams.set('tag', params.tag)
  return userRequest(`/resources?${searchParams.toString()}`)
}

export async function getResource(id) {
  return userRequest(`/resources/${id}`)
}

export async function uploadResource(formData) {
  const token = localStorage.getItem(USER_TOKEN_KEY)
  const res = await fetch(`${API_BASE}/resources/upload`, {
    method: 'POST',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    body: formData,
  })
  const data = await res.json()
  if (!res.ok) throw { status: res.status, message: data.message || '上传失败' }
  return data
}

export async function createFolder(payload) {
  return userRequest('/resources/folder', { method: 'POST', body: JSON.stringify(payload) })
}

export async function downloadResource(id) {
  return userRequest(`/resources/${id}/download`)
}

export async function batchDownloadResources(fileIds, folderIds) {
  const API_BASE = import.meta.env.VITE_API_BASE || '/api'
  const token = localStorage.getItem(USER_TOKEN_KEY)
  const res = await fetch(`${API_BASE}/resources/batch-download`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify({ file_ids: fileIds || [], folder_ids: folderIds || [] }),
  })
  if (!res.ok) {
    const data = await res.json().catch(() => ({}))
    throw { status: res.status, message: data.message || '下载失败' }
  }
  const blob = await res.blob()
  const disposition = res.headers.get('Content-Disposition') || ''
  const match = disposition.match(/filename\*=UTF-8''(.+)/i)
  const filename = match ? decodeURIComponent(match[1]) : 'resources.zip'
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

export async function previewResource(id) {
  return userRequest(`/resources/${id}/preview`)
}

export async function getResourceVersions(id) {
  return userRequest(`/resources/${id}/versions`)
}

export async function restoreVersion(resourceId, versionId) {
  return userRequest(`/resources/${resourceId}/versions/${versionId}/restore`, { method: 'POST' })
}

export async function createShareLink(id) {
  return userRequest(`/resources/${id}/share`, { method: 'POST' })
}

export async function removeShareLink(id) {
  return userRequest(`/resources/${id}/unshare`, { method: 'POST' })
}

export async function getComments(resourceId) {
  return userRequest(`/resources/${resourceId}/comments`)
}

export async function addComment(resourceId, content) {
  return userRequest(`/resources/${resourceId}/comments`, { method: 'POST', body: JSON.stringify({ content }) })
}

// ─── Resources API (admin) ───

export async function getAdminResources(params = {}) {
  const searchParams = new URLSearchParams()
  if (params.parent_id) searchParams.set('parent_id', params.parent_id)
  if (params.page) searchParams.set('page', params.page)
  if (params.per_page) searchParams.set('per_page', params.per_page)
  if (params.search) searchParams.set('search', params.search)
  if (params.status) searchParams.set('status', params.status)
  if (params.category) searchParams.set('category', params.category)
  if (params.is_folder !== undefined) searchParams.set('is_folder', params.is_folder)
  return request(`/admin/resources?${searchParams.toString()}`)
}

export async function updateResource(id, payload) {
  return userRequest(`/resources/${id}`, { method: 'PATCH', body: JSON.stringify(payload) })
}

export async function deleteResource(id) {
  return request(`/admin/resources/${id}`, { method: 'DELETE' })
}

export async function moveResource(id, newParentId) {
  return request(`/admin/resources/${id}/move`, { method: 'POST', body: JSON.stringify({ new_parent_id: newParentId }) })
}

export async function updateResourceStatus(id, status) {
  return request(`/admin/resources/${id}/status`, { method: 'PATCH', body: JSON.stringify({ status }) })
}

export async function batchResources(payload) {
  return request('/admin/resources/batch', { method: 'POST', body: JSON.stringify(payload) })
}

export async function getAdminFolders() {
  return request('/admin/resources/folders')
}

export async function getFolders() {
  return userRequest('/resources/folders')
}

export async function getTrash(params = {}) {
  const searchParams = new URLSearchParams()
  if (params.page) searchParams.set('page', params.page)
  if (params.per_page) searchParams.set('per_page', params.per_page)
  return request(`/admin/resources/trash?${searchParams.toString()}`)
}

export async function restoreResource(id) {
  return request(`/admin/resources/${id}/restore`, { method: 'POST' })
}

export async function permanentDeleteResource(id) {
  return request(`/admin/resources/${id}/permanent`, { method: 'DELETE' })
}

export async function getResourceLogs(params = {}) {
  const searchParams = new URLSearchParams()
  if (params.page) searchParams.set('page', params.page)
  if (params.per_page) searchParams.set('per_page', params.per_page)
  return request(`/admin/resources/logs?${searchParams.toString()}`)
}
