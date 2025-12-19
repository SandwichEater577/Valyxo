const { body, validationResult } = require('express-validator');

const validateRequest = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      success: false,
      error: 'Validation error',
      details: errors.array()
    });
  }
  next();
};

const validateRegister = [
  body('username')
    .isLength({ min: 3, max: 32 })
    .withMessage('Username must be between 3 and 32 characters')
    .matches(/^[a-zA-Z0-9_-]+$/)
    .withMessage('Username can only contain letters, numbers, underscores, and hyphens'),
  body('email')
    .isEmail()
    .withMessage('Invalid email address'),
  body('password')
    .isLength({ min: 8 })
    .withMessage('Password must be at least 8 characters long')
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
    .withMessage('Password must contain uppercase, lowercase, and number'),
  validateRequest
];

const validateLogin = [
  body('username')
    .notEmpty()
    .withMessage('Username is required'),
  body('password')
    .notEmpty()
    .withMessage('Password is required'),
  validateRequest
];

const validateProject = [
  body('name')
    .trim()
    .isLength({ min: 1, max: 100 })
    .withMessage('Project name must be between 1 and 100 characters'),
  body('description')
    .optional()
    .trim()
    .isLength({ max: 500 })
    .withMessage('Description must not exceed 500 characters'),
  validateRequest
];

const validateScript = [
  body('name')
    .trim()
    .isLength({ min: 1, max: 100 })
    .withMessage('Script name must be between 1 and 100 characters'),
  body('content')
    .notEmpty()
    .withMessage('Script content is required'),
  body('language')
    .optional()
    .isIn(['valyxoscript', 'javascript', 'python'])
    .withMessage('Invalid language'),
  validateRequest
];

module.exports = {
  validateRequest,
  validateRegister,
  validateLogin,
  validateProject,
  validateScript
};
