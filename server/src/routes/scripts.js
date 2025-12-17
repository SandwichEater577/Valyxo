const express = require('express');
const { authMiddleware } = require('../middleware/auth');
const { validateScript } = require('../middleware/validators');
const { runAsync, getAsync, allAsync } = require('../db');

const router = express.Router();

router.use(authMiddleware);

const verifyProjectOwnership = async (projectId, userId) => {
  const project = await getAsync(
    'SELECT id FROM projects WHERE id = ? AND user_id = ?',
    [projectId, userId]
  );
  return !!project;
};

router.get('/project/:projectId', async (req, res) => {
  try {
    const { projectId } = req.params;

    const isOwner = await verifyProjectOwnership(projectId, req.userId);
    if (!isOwner) {
      return res.status(403).json({
        success: false,
        error: 'Access denied'
      });
    }

    const scripts = await allAsync(
      'SELECT id, project_id, name, language, created_at, updated_at FROM scripts WHERE project_id = ? ORDER BY updated_at DESC',
      [projectId]
    );

    res.json({
      success: true,
      data: scripts
    });
  } catch (error) {
    console.error('Get scripts error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch scripts'
    });
  }
});

router.post('/project/:projectId', validateScript, async (req, res) => {
  try {
    const { projectId } = req.params;
    const { name, content, language } = req.body;

    const isOwner = await verifyProjectOwnership(projectId, req.userId);
    if (!isOwner) {
      return res.status(403).json({
        success: false,
        error: 'Access denied'
      });
    }

    const result = await runAsync(
      'INSERT INTO scripts (project_id, name, content, language) VALUES (?, ?, ?, ?)',
      [projectId, name, content, language || 'valyxoscript']
    );

    res.status(201).json({
      success: true,
      message: 'Script created successfully',
      data: {
        id: result.id,
        project_id: projectId,
        name,
        language: language || 'valyxoscript',
        created_at: new Date().toISOString()
      }
    });
  } catch (error) {
    console.error('Create script error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to create script'
    });
  }
});

router.get('/:scriptId', async (req, res) => {
  try {
    const { scriptId } = req.params;

    const script = await getAsync(
      `SELECT s.id, s.project_id, s.name, s.content, s.language, s.created_at, s.updated_at
       FROM scripts s
       JOIN projects p ON s.project_id = p.id
       WHERE s.id = ? AND p.user_id = ?`,
      [scriptId, req.userId]
    );

    if (!script) {
      return res.status(404).json({
        success: false,
        error: 'Script not found'
      });
    }

    res.json({
      success: true,
      data: script
    });
  } catch (error) {
    console.error('Get script error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch script'
    });
  }
});

router.put('/:scriptId', validateScript, async (req, res) => {
  try {
    const { scriptId } = req.params;
    const { name, content, language } = req.body;

    const script = await getAsync(
      `SELECT s.id, s.project_id
       FROM scripts s
       JOIN projects p ON s.project_id = p.id
       WHERE s.id = ? AND p.user_id = ?`,
      [scriptId, req.userId]
    );

    if (!script) {
      return res.status(404).json({
        success: false,
        error: 'Script not found'
      });
    }

    await runAsync(
      'UPDATE scripts SET name = ?, content = ?, language = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
      [name, content, language || 'valyxoscript', scriptId]
    );

    res.json({
      success: true,
      message: 'Script updated successfully',
      data: {
        id: scriptId,
        name,
        language: language || 'valyxoscript',
        updated_at: new Date().toISOString()
      }
    });
  } catch (error) {
    console.error('Update script error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to update script'
    });
  }
});

router.delete('/:scriptId', async (req, res) => {
  try {
    const { scriptId } = req.params;

    const script = await getAsync(
      `SELECT s.id FROM scripts s
       JOIN projects p ON s.project_id = p.id
       WHERE s.id = ? AND p.user_id = ?`,
      [scriptId, req.userId]
    );

    if (!script) {
      return res.status(404).json({
        success: false,
        error: 'Script not found'
      });
    }

    await runAsync(
      'DELETE FROM scripts WHERE id = ?',
      [scriptId]
    );

    res.json({
      success: true,
      message: 'Script deleted successfully'
    });
  } catch (error) {
    console.error('Delete script error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to delete script'
    });
  }
});

router.post('/:scriptId/execute', async (req, res) => {
  try {
    const { scriptId } = req.params;

    const script = await getAsync(
      `SELECT s.id, s.content, s.language FROM scripts s
       JOIN projects p ON s.project_id = p.id
       WHERE s.id = ? AND p.user_id = ?`,
      [scriptId, req.userId]
    );

    if (!script) {
      return res.status(404).json({
        success: false,
        error: 'Script not found'
      });
    }

    const startTime = Date.now();
    let output = '';
    let errorMessage = null;
    let status = 'success';

    try {
      if (script.language === 'valyxoscript') {
        const { ValyxoScriptRuntime } = require('../../src/valyxo/script.js');
        const runtime = new ValyxoScriptRuntime();
        const lines = script.content.split('\n');
        
        for (const line of lines) {
          runtime.run_line(line);
        }
        output = JSON.stringify(runtime.vars);
      } else {
        output = 'Language not supported in execution';
        status = 'unsupported';
      }
    } catch (execError) {
      errorMessage = execError.message;
      status = 'error';
    }

    const executionTime = Date.now() - startTime;

    const result = await runAsync(
      `INSERT INTO script_executions (script_id, status, output, error_message, execution_time_ms)
       VALUES (?, ?, ?, ?, ?)`,
      [scriptId, status, output, errorMessage, executionTime]
    );

    res.status(status === 'success' ? 200 : 400).json({
      success: status === 'success',
      data: {
        id: result.id,
        status,
        output,
        error: errorMessage,
        execution_time_ms: executionTime
      }
    });
  } catch (error) {
    console.error('Execute script error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to execute script'
    });
  }
});

router.get('/:scriptId/executions', async (req, res) => {
  try {
    const { scriptId } = req.params;

    const script = await getAsync(
      `SELECT s.id FROM scripts s
       JOIN projects p ON s.project_id = p.id
       WHERE s.id = ? AND p.user_id = ?`,
      [scriptId, req.userId]
    );

    if (!script) {
      return res.status(404).json({
        success: false,
        error: 'Script not found'
      });
    }

    const executions = await allAsync(
      'SELECT id, status, execution_time_ms, executed_at FROM script_executions WHERE script_id = ? ORDER BY executed_at DESC LIMIT 50',
      [scriptId]
    );

    res.json({
      success: true,
      data: executions
    });
  } catch (error) {
    console.error('Get executions error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch executions'
    });
  }
});

module.exports = router;
