const express = require('express');
const bcrypt = require('bcryptjs');
const { generateToken, authMiddleware } = require('../middleware/auth');
const { validateRegister, validateLogin } = require('../middleware/validators');
const { runAsync, getAsync } = require('../db');
const { invalidateUserCache } = require('../cache');
const logger = require('../logger');

const router = express.Router();

router.post('/register', validateRegister, async (req, res) => {
  try {
    const { username, email, password } = req.body;

    const existingUser = await getAsync(
      'SELECT id FROM users WHERE username = ? OR email = ?',
      [username, email]
    );

    if (existingUser) {
      return res.status(400).json({
        success: false,
        error: 'Username or email already exists'
      });
    }

    const passwordHash = await bcrypt.hash(password, 10);

    const result = await runAsync(
      'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
      [username, email, passwordHash]
    );

    const token = generateToken(result.id, username);
    logger.info(`User registered: ${username}`);

    res.status(201).json({
      success: true,
      message: 'User registered successfully',
      user: {
        id: result.id,
        username,
        email
      },
      token
    });
  } catch (error) {
    logger.error('Registration error:', error);
    res.status(500).json({
      success: false,
      error: 'Registration failed'
    });
  }
});

router.post('/login', validateLogin, async (req, res) => {
  try {
    const { username, password } = req.body;

    const user = await getAsync(
      'SELECT id, username, email, password_hash FROM users WHERE username = ?',
      [username]
    );

    if (!user) {
      return res.status(401).json({
        success: false,
        error: 'Invalid username or password'
      });
    }

    const passwordMatch = await bcrypt.compare(password, user.password_hash);

    if (!passwordMatch) {
      return res.status(401).json({
        success: false,
        error: 'Invalid username or password'
      });
    }

    const token = generateToken(user.id, user.username);

    res.json({
      success: true,
      message: 'Login successful',
      user: {
        id: user.id,
        username: user.username,
        email: user.email
      },
      token
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({
      success: false,
      error: 'Login failed'
    });
  }
});

router.post('/logout', authMiddleware, (req, res) => {
  res.json({
    success: true,
    message: 'Logout successful'
  });
});

router.get('/me', authMiddleware, async (req, res) => {
  try {
    const user = await getAsync(
      'SELECT id, username, email, created_at FROM users WHERE id = ?',
      [req.userId]
    );

    if (!user) {
      return res.status(404).json({
        success: false,
        error: 'User not found'
      });
    }

    res.json({
      success: true,
      user
    });
  } catch (error) {
    console.error('Get user error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch user'
    });
  }
});

module.exports = router;
