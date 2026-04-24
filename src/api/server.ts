import express from 'express'
import { metricsRouter } from './routes/metrics.js'
import { healthRouter } from './routes/health.js'

const app = express()
const PORT = process.env.PORT ?? 3000

app.use(express.json())
app.use('/api/metrics', metricsRouter)
app.use('/api/health', healthRouter)

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})

export { app }
