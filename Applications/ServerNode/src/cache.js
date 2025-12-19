const NodeCache = require('node-cache');
const logger = require('./logger');

const cache = new NodeCache({ stdTTL: 300, checkperiod: 60 });

const cacheMiddleware = (duration = 300) => {
  return (req, res, next) => {
    if (req.method !== 'GET') {
      return next();
    }

    const key = `${req.userId || 'anon'}:${req.originalUrl}`;
    const cached = cache.get(key);

    if (cached) {
      logger.debug(`Cache hit for: ${req.path}`);
      return res.json(cached);
    }

    const originalJson = res.json.bind(res);

    res.json = (body) => {
      cache.set(key, body, duration);
      return originalJson(body);
    };

    next();
  };
};

const invalidateUserCache = (userId) => {
  const keys = cache.keys();
  const userKeys = keys.filter(k => k.startsWith(`${userId}:`));
  cache.del(userKeys);
  logger.debug(`Invalidated cache for user: ${userId} (${userKeys.length} keys)`);
};

const invalidateCache = (pattern) => {
  const keys = cache.keys();
  const matching = keys.filter(k => k.includes(pattern));
  cache.del(matching);
  logger.debug(`Invalidated cache matching pattern: ${pattern} (${matching.length} keys)`);
};

const getCacheStats = () => {
  const keys = cache.keys();
  return {
    keys: keys.length,
    stats: cache.getStats()
  };
};

module.exports = {
  cache,
  cacheMiddleware,
  invalidateUserCache,
  invalidateCache,
  getCacheStats
};
