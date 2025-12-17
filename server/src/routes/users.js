const express = require('express');
const bcrypt = require('bcryptjs');
const { authMiddleware } = require('../middleware/auth');
const { runAsync, getAsync, allAsync } = require('../db');
const { body, validationResult } = require('express-validator');

const router = express.Router();

router.use(authMiddleware);

router.get('/profile', async (req, res) => {
  try {
    const user = await getAsync(
      'SELECT id, username, email, created_at, updated_at FROM users WHERE id = ?',
      [req.userId]
    );

    if (!user) {
      return res.status(404).json({
        success: false,
        error: 'User not found'
      });
    }

    const projectCount = await getAsync(
      'SELECT COUNT(*) as count FROM projects WHERE user_id = ?',
      [req.userId]
    );

    const scriptCount = await getAsync(
      'SELECT COUNT(*) as count FROM scripts WHERE project_id IN (SELECT id FROM projects WHERE user_id = ?)',
      [req.userId]
    );

    res.json({
      success: true,
      user: {
        ...user,
        projectCount: projectCount.count,
        scriptCount: scriptCount.count
      }
    });
  } catch (error) {
    console.error('Get profile error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch profile'
    });
  }
});

router.put('/profile', [
  body('email')
    .optional()
    .isEmail()
    .withMessage('Invalid email address'),
  body('username')
    .optional()
    .isLength({ min: 3, max: 32 })
    .withMessage('Username must be between 3 and 32 characters')
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        error: 'Validation error',
        details: errors.array()
      });
    }

    const { email, username } = req.body;
    const updates = [];
    const values = [];

    if (email) {
      const existingEmail = await getAsync(
        'SELECT id FROM users WHERE email = ? AND id != ?',
        [email, req.userId]
      );
      if (existingEmail) {
        return res.status(400).json({
          success: false,
          error: 'Email already in use'
        });
      }
      updates.push('email = ?');
      values.push(email);
    }

    if (username) {
      const existingUsername = await getAsync(
        'SELECT id FROM users WHERE username = ? AND id != ?',
        [username, req.userId]
      );
      if (existingUsername) {
        return res.status(400).json({
          success: false,
          error: 'Username already in use'
        });
      }
      updates.push('username = ?');
      values.push(username);
    }

    if (updates.length === 0) {
      return res.status(400).json({
        success: false,
        error: 'No valid fields to update'
      });
    }

    updates.push('updated_at = CURRENT_TIMESTAMP');
    values.push(req.userId);

    await runAsync(
      `UPDATE users SET ${updates.join(', ')} WHERE id = ?`,
      values
    );

    res.json({
      success: true,
      message: 'Profile updated successfully'
    });
  } catch (error) {
    console.error('Update profile error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to update profile'
    });
  }
});

router.put('/password', [
  body('currentPassword')
    .notEmpty()
    .withMessage('Current password is required'),
  body('newPassword')
    .isLength({ min: 8 })
    .withMessage('New password must be at least 8 characters')
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
    .withMessage('Password must contain uppercase, lowercase, and number')
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        error: 'Validation error',
        details: errors.array()
      });
    }

    const { currentPassword, newPassword } = req.body;

    const user = await getAsync(
      'SELECT password_hash FROM users WHERE id = ?',
      [req.userId]
    );

    if (!user) {
      return res.status(404).json({
        success: false,
        error: 'User not found'
      });
    }

    const passwordMatch = await bcrypt.compare(currentPassword, user.password_hash);
    if (!passwordMatch) {
      return res.status(401).json({
        success: false,
        error: 'Current password is incorrect'
      });
    }

    const newPasswordHash = await bcrypt.hash(newPassword, 10);

    await runAsync(
      'UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
      [newPasswordHash, req.userId]
    );

    res.json({
      success: true,
      message: 'Password changed successfully'
    });
  } catch (error) {
    console.error('Change password error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to change password'
    });
  }
});

router.get('/stats', async (req, res) => {
  try {
    const projectCount = await getAsync(
      'SELECT COUNT(*) as count FROM projects WHERE user_id = ?',
      [req.userId]
    );

    const scriptCount = await getAsync(
      'SELECT COUNT(*) as count FROM scripts WHERE project_id IN (SELECT id FROM projects WHERE user_id = ?)',
      [req.userId]
    );

    const executionCount = await getAsync(
      `SELECT COUNT(*) as count FROM script_executions WHERE script_id IN
       (SELECT id FROM scripts WHERE project_id IN (SELECT id FROM projects WHERE user_id = ?))`,
      [req.userId]
    );

    const totalExecutionTime = await getAsync(
      `SELECT SUM(execution_time_ms) as total FROM script_executions WHERE script_id IN
       (SELECT id FROM scripts WHERE project_id IN (SELECT id FROM projects WHERE user_id = ?))`,
      [req.userId]
    );

    res.json({
      success: true,
      stats: {
        projects: projectCount.count,
        scripts: scriptCount.count,
        executions: executionCount.count,
        totalExecutionTimeMs: totalExecutionTime.total || 0
      }
    });
  } catch (error) {
    console.error('Get stats error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch statistics'
    });
  }
});

module.exports = router;
