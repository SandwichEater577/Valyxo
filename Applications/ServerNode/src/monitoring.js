const logger = require('./logger');
const { getCacheStats } = require('./cache');
const { getAsync } = require('./db');

let startTime = Date.now();
let requestCount = 0;
let errorCount = 0;

const trackRequest = (req, res, next) => {
  requestCount++;
  
  res.on('finish', () => {
    if (res.statusCode >= 400) {
      errorCount++;
    }
  });
  
  next();
};

const getHealthStatus = async () => {
  try {
    const uptime = Math.floor((Date.now() - startTime) / 1000);
    const memoryUsage = process.memoryUsage();
    
    const userCount = await getAsync('SELECT COUNT(*) as count FROM users');
    const projectCount = await getAsync('SELECT COUNT(*) as count FROM projects');
    const scriptCount = await getAsync('SELECT COUNT(*) as count FROM scripts');
    const executionCount = await getAsync('SELECT COUNT(*) as count FROM script_executions');

    const cacheStats = getCacheStats();

    return {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime_seconds: uptime,
      version: process.env.API_VERSION || '0.41',
      environment: process.env.NODE_ENV || 'development',
      metrics: {
        requests: requestCount,
        errors: errorCount,
        error_rate: requestCount > 0 ? ((errorCount / requestCount) * 100).toFixed(2) + '%' : '0%'
      },
      database: {
        users: userCount.count,
        projects: projectCount.count,
        scripts: scriptCount.count,
        executions: executionCount.count
      },
      cache: cacheStats,
      memory: {
        rss_mb: Math.round(memoryUsage.rss / 1024 / 1024),
        heap_used_mb: Math.round(memoryUsage.heapUsed / 1024 / 1024),
        heap_total_mb: Math.round(memoryUsage.heapTotal / 1024 / 1024),
        external_mb: Math.round(memoryUsage.external / 1024 / 1024)
      },
      node_version: process.version
    };
  } catch (error) {
    logger.error('Health check error:', error);
    return {
      status: 'unhealthy',
      error: error.message
    };
  }
};

const getMetrics = async () => {
  return {
    timestamp: new Date().toISOString(),
    uptime_seconds: Math.floor((Date.now() - startTime) / 1000),
    requests_total: requestCount,
    errors_total: errorCount,
    error_rate: requestCount > 0 ? ((errorCount / requestCount) * 100).toFixed(2) : '0',
    memory_mb: Math.round(process.memoryUsage().heapUsed / 1024 / 1024),
    cache: getCacheStats()
  };
};

const resetMetrics = () => {
  startTime = Date.now();
  requestCount = 0;
  errorCount = 0;
  return { message: 'Metrics reset' };
};

module.exports = {
  trackRequest,
  getHealthStatus,
  getMetrics,
  resetMetrics
};
