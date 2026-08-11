export interface User {
  id: number
  username: string
  role: string
}

export interface Dataset {
  id: number
  name: string
  type: 'text' | 'image'
  description?: string
  created_at?: string
}

export interface DataItem {
  id: number
  dataset_id: number
  content: string
  meta?: Record<string, unknown>
}

export interface Task {
  id: number
  dataset_id: number
  name: string
  type: 'text' | 'image'
  status: 'pending' | 'in_progress' | 'done'
  created_at?: string
}

export interface Annotation {
  id?: number
  task_id: number
  item_id: number
  type: 'text' | 'image'
  payload: Record<string, unknown>
  updated_at?: string
}

export interface PageResult<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}
