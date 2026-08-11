import http from './http'
import type { Dataset, DataItem, PageResult } from '../types'

export function listDatasets(params?: { page?: number; page_size?: number }) {
  return http.get<PageResult<Dataset>>('/datasets', { params })
}

export function createDataset(data: { name: string; type: 'text' | 'image'; description?: string }) {
  return http.post<Dataset>('/datasets', data)
}

export function listItems(datasetId: number, params?: { page?: number; page_size?: number }) {
  return http.get<PageResult<DataItem>>(`/datasets/${datasetId}/items`, { params })
}

export function createItem(datasetId: number, data: { content: string; meta?: Record<string, unknown> }) {
  return http.post<DataItem>(`/datasets/${datasetId}/items`, data)
}
