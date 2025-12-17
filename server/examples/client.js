const API_URL = 'http://localhost:5000/api';

class ValyxoClient {
  constructor(baseUrl = API_URL) {
    this.baseUrl = baseUrl;
    this.token = null;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || `HTTP ${response.status}`);
    }

    return data;
  }

  async register(username, email, password) {
    const data = await this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password })
    });

    this.token = data.token;
    return data;
  }

  async login(username, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });

    this.token = data.token;
    return data;
  }

  async logout() {
    return await this.request('/auth/logout', {
      method: 'POST'
    });
  }

  async getCurrentUser() {
    return await this.request('/auth/me');
  }

  async getUserProfile() {
    return await this.request('/users/profile');
  }

  async updateProfile(username, email) {
    return await this.request('/users/profile', {
      method: 'PUT',
      body: JSON.stringify({ username, email })
    });
  }

  async changePassword(currentPassword, newPassword) {
    return await this.request('/users/password', {
      method: 'PUT',
      body: JSON.stringify({ currentPassword, newPassword })
    });
  }

  async getUserStats() {
    return await this.request('/users/stats');
  }

  async getProjects() {
    return await this.request('/projects');
  }

  async createProject(name, description = '') {
    return await this.request('/projects', {
      method: 'POST',
      body: JSON.stringify({ name, description })
    });
  }

  async getProject(projectId) {
    return await this.request(`/projects/${projectId}`);
  }

  async updateProject(projectId, name, description) {
    return await this.request(`/projects/${projectId}`, {
      method: 'PUT',
      body: JSON.stringify({ name, description })
    });
  }

  async deleteProject(projectId) {
    return await this.request(`/projects/${projectId}`, {
      method: 'DELETE'
    });
  }

  async getProjectScripts(projectId) {
    return await this.request(`/scripts/project/${projectId}`);
  }

  async createScript(projectId, name, content, language = 'valyxoscript') {
    return await this.request(`/scripts/project/${projectId}`, {
      method: 'POST',
      body: JSON.stringify({ name, content, language })
    });
  }

  async getScript(scriptId) {
    return await this.request(`/scripts/${scriptId}`);
  }

  async updateScript(scriptId, name, content, language = 'valyxoscript') {
    return await this.request(`/scripts/${scriptId}`, {
      method: 'PUT',
      body: JSON.stringify({ name, content, language })
    });
  }

  async deleteScript(scriptId) {
    return await this.request(`/scripts/${scriptId}`, {
      method: 'DELETE'
    });
  }

  async executeScript(scriptId) {
    return await this.request(`/scripts/${scriptId}/execute`, {
      method: 'POST'
    });
  }

  async getScriptExecutions(scriptId) {
    return await this.request(`/scripts/${scriptId}/executions`);
  }
}

module.exports = ValyxoClient;

if (typeof window !== 'undefined') {
  window.ValyxoClient = ValyxoClient;
}
