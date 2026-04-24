import { Router } from 'express'

const healthRouter = Router()

healthRouter.get('/', (_req, res) => {
  res.json({
    status: 'healthy',
    uptime: process.uptime(),
    timestamp: new Date().toISOString(),
  })
})

export { healthRouter }
