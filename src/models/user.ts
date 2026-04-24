import { z } from 'zod'

export const UserSchema = z.object({
  id: z.string().uuid(),
  login: z.string().min(1),
  email: z.string().email(),
  role: z.enum(['admin', 'member', 'viewer']),
  createdAt: z.string().datetime(),
  lastActiveAt: z.string().datetime().optional(),
})

export type User = z.infer<typeof UserSchema>

export function createUser(login: string, email: string, role: User['role'] = 'member'): User {
  return {
    id: crypto.randomUUID(),
    login,
    email,
    role,
    createdAt: new Date().toISOString(),
  }
}

export function isAdmin(user: User): boolean {
  return user.role === 'admin'
}
