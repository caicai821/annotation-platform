import http from './http'
import type { Annotation } from '../types'

export function getAnnotation(taskId: number, itemId: number) {
  return http.get<Annotation | null>(`/tasks/${taskId}/items/${itemId}/annotation`)
}

export function saveAnnotation(
  taskId: number,
  itemId: number,
  data: { type: 'image'; payload: Record<string, unknown> },
) {
  return http.put<Annotation>(`/tasks/${taskId}/items/${itemId}/annotation`, data)
}
