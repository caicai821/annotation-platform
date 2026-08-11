import http from './http'
import type { User } from '../types'

export interface LoginResult {
  token: string
  user: User
}

export function login(username: string, password: string) {
  return http.post<LoginResult>('/auth/login', { username, password })
}

export function register(username: string, password: string) {
  return http.post<User>('/auth/register', { username, password })
}

export function getProfile() {
  return http.get<User>('/auth/me')
}
