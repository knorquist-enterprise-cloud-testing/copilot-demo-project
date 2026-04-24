type LogLevel = 'debug' | 'info' | 'warn' | 'error'

interface LogEntry {
  level: LogLevel
  message: string
  timestamp: string
  context?: Record<string, unknown>
}

const LOG_LEVELS: Record<LogLevel, number> = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
}

class Logger {
  private minLevel: LogLevel

  constructor(minLevel: LogLevel = 'info') {
    this.minLevel = minLevel
  }

  private log(level: LogLevel, message: string, context?: Record<string, unknown>) {
    if (LOG_LEVELS[level] < LOG_LEVELS[this.minLevel]) return

    const entry: LogEntry = {
      level,
      message,
      timestamp: new Date().toISOString(),
      context,
    }

    const output = JSON.stringify(entry)
    if (level === 'error') {
      console.error(output)
    } else {
      console.log(output)
    }
  }

  debug(msg: string, ctx?: Record<string, unknown>) { this.log('debug', msg, ctx) }
  info(msg: string, ctx?: Record<string, unknown>) { this.log('info', msg, ctx) }
  warn(msg: string, ctx?: Record<string, unknown>) { this.log('warn', msg, ctx) }
  error(msg: string, ctx?: Record<string, unknown>) { this.log('error', msg, ctx) }
}

export const logger = new Logger(process.env.LOG_LEVEL as LogLevel ?? 'info')
export { Logger, type LogLevel, type LogEntry }
