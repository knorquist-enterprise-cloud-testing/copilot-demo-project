interface RateLimitEntry {
  count: number
  resetAt: number
}

const store = new Map<string, RateLimitEntry>()

export function rateLimiter(maxRequests: number = 100, windowMs: number = 60_000) {
  return (req: any, res: any, next: any) => {
    const key = req.ip ?? 'unknown'
    const now = Date.now()
    const entry = store.get(key)

    if (!entry || now > entry.resetAt) {
      store.set(key, { count: 1, resetAt: now + windowMs })
      return next()
    }

    if (entry.count >= maxRequests) {
      res.status(429).json({ error: 'Too many requests' })
      return
    }

    entry.count++
    next()
  }
}
