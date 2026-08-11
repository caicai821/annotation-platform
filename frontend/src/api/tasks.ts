import http from './http'
import type { Task, PageResult } from '../types'

export function listTasks(params?: { page?: number; page_size?: number }) {
  return http.get<PageResult<Task>>('/tasks', { params })
}

export function createTask(data: { dataset_id: number; name: string; type: 'text' | 'image' }) {
  return http.post<Task>('/tasks', data)
}

export function getTask(id: number) {
  return http.get<Task>(`/tasks/${id}`)
}
