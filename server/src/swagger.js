const swaggerJsdoc = require('swagger-jsdoc');

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Valyxo Backend API',
      version: '0.41.0',
      description: 'Complete Backend API for Valyxo Developer Ecosystem',
      contact: {
        name: 'Valyxo Team',
        url: 'https://github.com/valyxo'
      },
      license: {
        name: 'MIT'
      }
    },
    servers: [
      {
        url: 'http://localhost:5000',
        description: 'Development Server'
      },
      {
        url: 'https://api.valyxo.dev',
        description: 'Production Server'
      }
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT'
        }
      },
      schemas: {
        User: {
          type: 'object',
          properties: {
            id: { type: 'integer' },
            username: { type: 'string' },
            email: { type: 'string', format: 'email' },
            created_at: { type: 'string', format: 'date-time' },
            updated_at: { type: 'string', format: 'date-time' }
          }
        },
        Project: {
          type: 'object',
          properties: {
            id: { type: 'integer' },
            user_id: { type: 'integer' },
            name: { type: 'string' },
            description: { type: 'string' },
            created_at: { type: 'string', format: 'date-time' },
            updated_at: { type: 'string', format: 'date-time' }
          }
        },
        Script: {
          type: 'object',
          properties: {
            id: { type: 'integer' },
            project_id: { type: 'integer' },
            name: { type: 'string' },
            content: { type: 'string' },
            language: { type: 'string', enum: ['valyxoscript', 'javascript', 'python'] },
            created_at: { type: 'string', format: 'date-time' },
            updated_at: { type: 'string', format: 'date-time' }
          }
        },
        ScriptExecution: {
          type: 'object',
          properties: {
            id: { type: 'integer' },
            script_id: { type: 'integer' },
            status: { type: 'string', enum: ['success', 'error', 'pending', 'unsupported'] },
            output: { type: 'string' },
            error_message: { type: 'string' },
            execution_time_ms: { type: 'integer' },
            executed_at: { type: 'string', format: 'date-time' }
          }
        },
        Error: {
          type: 'object',
          properties: {
            success: { type: 'boolean', example: false },
            error: { type: 'string' },
            details: { type: 'array' }
          }
        }
      }
    }
  },
  apis: ['./src/routes/*.js', './src/server.js']
};

const swaggerSpec = swaggerJsdoc(options);

module.exports = swaggerSpec;
