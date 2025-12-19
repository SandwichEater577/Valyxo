const request = require('supertest');
const app = require('../src/server');

describe('Valyxo API Integration Tests', () => {
  let token;
  let userId;
  let projectId;
  let scriptId;

  beforeAll(async () => {
    jest.setTimeout(10000);
  });

  describe('Authentication', () => {
    it('should register a new user', async () => {
      const res = await request(app)
        .post('/api/auth/register')
        .send({
          username: 'testuser' + Date.now(),
          email: 'test' + Date.now() + '@example.com',
          password: 'TestPass123'
        });

      expect(res.status).toBe(201);
      expect(res.body.success).toBe(true);
      expect(res.body.token).toBeDefined();
      expect(res.body.user.username).toBeDefined();

      token = res.body.token;
      userId = res.body.user.id;
    });

    it('should reject weak passwords', async () => {
      const res = await request(app)
        .post('/api/auth/register')
        .send({
          username: 'weakpass' + Date.now(),
          email: 'weak' + Date.now() + '@example.com',
          password: 'weak'
        });

      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
    });

    it('should login successfully', async () => {
      const username = 'logintest' + Date.now();
      
      await request(app)
        .post('/api/auth/register')
        .send({
          username,
          email: 'login' + Date.now() + '@example.com',
          password: 'LoginPass123'
        });

      const res = await request(app)
        .post('/api/auth/login')
        .send({
          username,
          password: 'LoginPass123'
        });

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.token).toBeDefined();
    });

    it('should get current user', async () => {
      const res = await request(app)
        .get('/api/auth/me')
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.user.id).toBe(userId);
    });
  });

  describe('Projects', () => {
    it('should create a project', async () => {
      const res = await request(app)
        .post('/api/projects')
        .set('Authorization', `Bearer ${token}`)
        .send({
          name: 'Test Project',
          description: 'A test project'
        });

      expect(res.status).toBe(201);
      expect(res.body.success).toBe(true);
      expect(res.body.data.name).toBe('Test Project');

      projectId = res.body.data.id;
    });

    it('should get all projects', async () => {
      const res = await request(app)
        .get('/api/projects')
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });

    it('should get project details', async () => {
      const res = await request(app)
        .get(`/api/projects/${projectId}`)
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data.id).toBe(projectId);
    });

    it('should update project', async () => {
      const res = await request(app)
        .put(`/api/projects/${projectId}`)
        .set('Authorization', `Bearer ${token}`)
        .send({
          name: 'Updated Project',
          description: 'Updated description'
        });

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data.name).toBe('Updated Project');
    });
  });

  describe('Scripts', () => {
    it('should create a script', async () => {
      const res = await request(app)
        .post(`/api/scripts/project/${projectId}`)
        .set('Authorization', `Bearer ${token}`)
        .send({
          name: 'Test Script',
          content: 'print "Hello"',
          language: 'valyxoscript'
        });

      expect(res.status).toBe(201);
      expect(res.body.success).toBe(true);
      expect(res.body.data.name).toBe('Test Script');

      scriptId = res.body.data.id;
    });

    it('should get project scripts', async () => {
      const res = await request(app)
        .get(`/api/scripts/project/${projectId}`)
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });

    it('should get script details', async () => {
      const res = await request(app)
        .get(`/api/scripts/${scriptId}`)
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data.id).toBe(scriptId);
    });

    it('should update script', async () => {
      const res = await request(app)
        .put(`/api/scripts/${scriptId}`)
        .set('Authorization', `Bearer ${token}`)
        .send({
          name: 'Updated Script',
          content: 'print "Updated"',
          language: 'valyxoscript'
        });

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data.name).toBe('Updated Script');
    });

    it('should execute script', async () => {
      const res = await request(app)
        .post(`/api/scripts/${scriptId}/execute`)
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data.status).toBeDefined();
      expect(res.body.data.execution_time_ms).toBeDefined();
    });

    it('should get execution history', async () => {
      const res = await request(app)
        .get(`/api/scripts/${scriptId}/executions`)
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });
  });

  describe('Users', () => {
    it('should get user profile', async () => {
      const res = await request(app)
        .get('/api/users/profile')
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.user.id).toBe(userId);
    });

    it('should get user statistics', async () => {
      const res = await request(app)
        .get('/api/users/stats')
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.stats.projects).toBeDefined();
      expect(res.body.stats.scripts).toBeDefined();
    });
  });

  describe('Cleanup', () => {
    it('should delete script', async () => {
      const res = await request(app)
        .delete(`/api/scripts/${scriptId}`)
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
    });

    it('should delete project', async () => {
      const res = await request(app)
        .delete(`/api/projects/${projectId}`)
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
    });
  });

  describe('Error Handling', () => {
    it('should require authentication', async () => {
      const res = await request(app)
        .get('/api/projects');

      expect(res.status).toBe(401);
      expect(res.body.success).toBe(false);
    });

    it('should return 404 for non-existent resource', async () => {
      const res = await request(app)
        .get('/api/projects/99999')
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(404);
      expect(res.body.success).toBe(false);
    });

    it('should return 404 for non-existent endpoint', async () => {
      const res = await request(app)
        .get('/api/nonexistent');

      expect(res.status).toBe(404);
      expect(res.body.success).toBe(false);
    });
  });
});
