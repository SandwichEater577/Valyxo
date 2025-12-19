const rateLimit = require('express-rate-limit');
const logger = require('../logger');

const generalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: 'Too many requests, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    logger.warn(`Rate limit exceeded for IP: ${req.ip}`);
    res.status(429).json({
      success: false,
      error: 'Too many requests, please try again later'
    });
  },
  skip: (req) => process.env.NODE_ENV === 'test'
});

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: 'Too many login attempts, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    logger.warn(`Auth rate limit exceeded for IP: ${req.ip}`);
    res.status(429).json({
      success: false,
      error: 'Too many login attempts. Please try again later.'
    });
  },
  skip: (req) => process.env.NODE_ENV === 'test'
});

const scriptExecutionLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 30,
  message: 'Too many script executions, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    logger.warn(`Script execution rate limit exceeded for user: ${req.userId}`);
    res.status(429).json({
      success: false,
      error: 'Too many script executions. Please try again later.'
    });
  },
  skip: (req) => process.env.NODE_ENV === 'test',
  keyGenerator: (req) => req.userId || req.ip
});

const sanitizeInput = (req, res, next) => {
  try {
    if (req.body && typeof req.body === 'object') {
      sanitizeObject(req.body);
    }
    if (req.query && typeof req.query === 'object') {
      sanitizeObject(req.query);
    }
    if (req.params && typeof req.params === 'object') {
      sanitizeObject(req.params);
    }
    next();
  } catch (error) {
    logger.error('Input sanitization error:', error);
    res.status(400).json({
      success: false,
      error: 'Invalid input'
    });
  }
};

function sanitizeObject(obj) {
  const dangerous = /[<>\"'`]/g;
  
  for (const key in obj) {
    if (typeof obj[key] === 'string') {
      if (dangerous.test(obj[key])) {
        throw new Error(`Potentially dangerous characters in field: ${key}`);
      }
      obj[key] = obj[key].trim();
    } else if (typeof obj[key] === 'object' && obj[key] !== null) {
      sanitizeObject(obj[key]);
    }
  }
}

const requestLogger = (req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    const level = res.statusCode >= 400 ? 'warn' : 'debug';
    
    logger[level](`${req.method} ${req.path}`, {
      status: res.statusCode,
      duration: `${duration}ms`,
      ip: req.ip,
      userId: req.userId || 'anonymous'
    });
  });
  
  next();
};

module.exports = {
  generalLimiter,
  authLimiter,
  scriptExecutionLimiter,
  sanitizeInput,
  requestLogger
};
