import { Router } from 'express'
import { z } from 'zod'

const metricsRouter = Router()

const MetricSchema = z.object({
  name: z.string(),
  value: z.number(),
  timestamp: z.string().datetime(),
  tags: z.record(z.string()).optional(),
})

type Metric = z.infer<typeof MetricSchema>

const metrics: Metric[] = []

metricsRouter.get('/', (_req, res) => {
  res.json({ metrics, count: metrics.length })
})

metricsRouter.post('/', (req, res) => {
  const result = MetricSchema.safeParse(req.body)
  if (!result.success) {
    res.status(400).json({ error: result.error.flatten() })
    return
  }
  metrics.push(result.data)
  res.status(201).json(result.data)
})

export { metricsRouter }
