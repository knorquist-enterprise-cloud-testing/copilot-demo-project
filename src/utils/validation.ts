import { z } from 'zod'

export const DateRangeSchema = z.object({
  from: z.string().datetime(),
  to: z.string().datetime(),
}).refine(
  (data) => new Date(data.from) < new Date(data.to),
  { message: 'Start date must be before end date' }
)

export const PaginationSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
})

export const MetricQuerySchema = z.object({
  name: z.string().optional(),
  tags: z.record(z.string()).optional(),
  dateRange: DateRangeSchema.optional(),
  pagination: PaginationSchema.optional(),
})

export type MetricQuery = z.infer<typeof MetricQuerySchema>
export type DateRange = z.infer<typeof DateRangeSchema>
export type Pagination = z.infer<typeof PaginationSchema>
