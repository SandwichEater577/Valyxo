const express = require('express');
const { authMiddleware } = require('../middleware/auth');
const { validateProject } = require('../middleware/validators');
const { runAsync, getAsync, allAsync } = require('../db');
const { invalidateUserCache, invalidateCache } = require('../cache');
const logger = require('../logger');

const router = express.Router();

router.use(authMiddleware);

router.get('/', async (req, res) => {
  try {
    const projects = await allAsync(
      'SELECT id, name, description, created_at, updated_at FROM projects WHERE user_id = ? ORDER BY updated_at DESC',
      [req.userId]
    );

    res.json({
      success: true,
      data: projects
    });
  } catch (error) {
    console.error('Get projects error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch projects'
    });
  }
});

router.post('/', validateProject, async (req, res) => {
  try {
    const { name, description } = req.body;

    const result = await runAsync(
      'INSERT INTO projects (user_id, name, description) VALUES (?, ?, ?)',
      [req.userId, name, description || '']
    );

    invalidateUserCache(req.userId);
    logger.info(`Project created: ${name} (user: ${req.userId})`);

    res.status(201).json({
      success: true,
      message: 'Project created successfully',
      data: {
        id: result.id,
        name,
        description: description || '',
        created_at: new Date().toISOString()
      }
    });
  } catch (error) {
    logger.error('Create project error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to create project'
    });
  }
});

router.get('/:projectId', async (req, res) => {
  try {
    const { projectId } = req.params;

    const project = await getAsync(
      'SELECT id, name, description, created_at, updated_at FROM projects WHERE id = ? AND user_id = ?',
      [projectId, req.userId]
    );

    if (!project) {
      return res.status(404).json({
        success: false,
        error: 'Project not found'
      });
    }

    res.json({
      success: true,
      data: project
    });
  } catch (error) {
    console.error('Get project error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch project'
    });
  }
});

router.put('/:projectId', validateProject, async (req, res) => {
  try {
    const { projectId } = req.params;
    const { name, description } = req.body;

    const project = await getAsync(
      'SELECT id FROM projects WHERE id = ? AND user_id = ?',
      [projectId, req.userId]
    );

    if (!project) {
      return res.status(404).json({
        success: false,
        error: 'Project not found'
      });
    }

    await runAsync(
      'UPDATE projects SET name = ?, description = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
      [name, description || '', projectId]
    );

    res.json({
      success: true,
      message: 'Project updated successfully',
      data: {
        id: projectId,
        name,
        description: description || '',
        updated_at: new Date().toISOString()
      }
    });
  } catch (error) {
    console.error('Update project error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to update project'
    });
  }
});

router.delete('/:projectId', async (req, res) => {
  try {
    const { projectId } = req.params;

    const project = await getAsync(
      'SELECT id FROM projects WHERE id = ? AND user_id = ?',
      [projectId, req.userId]
    );

    if (!project) {
      return res.status(404).json({
        success: false,
        error: 'Project not found'
      });
    }

    await runAsync(
      'DELETE FROM projects WHERE id = ?',
      [projectId]
    );

    res.json({
      success: true,
      message: 'Project deleted successfully'
    });
  } catch (error) {
    console.error('Delete project error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to delete project'
    });
  }
});

module.exports = router;
