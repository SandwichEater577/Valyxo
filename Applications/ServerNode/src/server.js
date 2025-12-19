require("dotenv").config();

const path = require("path");
const fs = require("fs");
const express = require("express");
const cors = require("cors");
const helmet = require("helmet");
const morgan = require("morgan");
const compression = require("compression");
const swaggerUi = require("swagger-ui-express");

const { initializeDatabase } = require("./db");
const errorHandler = require("./middleware/errorHandler");
const {
  generalLimiter,
  authLimiter,
  sanitizeInput,
  requestLogger,
} = require("./middleware/security");
const { cacheMiddleware, invalidateUserCache } = require("./cache");
const {
  trackRequest,
  getHealthStatus,
  getMetrics,
  resetMetrics,
} = require("./monitoring");
const swaggerSpec = require("./swagger");
const logger = require("./logger");

const authRoutes = require("./routes/auth");
const projectRoutes = require("./routes/projects");
const scriptRoutes = require("./routes/scripts");
const userRoutes = require("./routes/users");

const app = express();
const PORT = process.env.PORT || 5000;

app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "'unsafe-inline'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", "data:"],
      },
    },
  })
);

app.use(compression());
app.use(
  morgan("combined", { stream: { write: (msg) => logger.info(msg.trim()) } })
);

app.use(
  cors({
    origin: (process.env.CORS_ORIGIN || "http://localhost:3000").split(","),
    credentials: true,
    methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allowedHeaders: ["Content-Type", "Authorization"],
  })
);

app.use(express.json({ limit: "10mb" }));
app.use(express.urlencoded({ extended: true, limit: "10mb" }));

app.use(sanitizeInput);
app.use(requestLogger);
app.use(trackRequest);
app.use(generalLimiter);

app.get("/health", async (req, res) => {
  try {
    const health = await getHealthStatus();
    res.json({
      success: true,
      ...health,
    });
  } catch (error) {
    logger.error("Health check error:", error);
    res.status(503).json({
      success: false,
      status: "unhealthy",
      error: error.message,
    });
  }
});

app.get("/metrics", async (req, res) => {
  try {
    const metrics = await getMetrics();
    res.json({
      success: true,
      metrics,
    });
  } catch (error) {
    logger.error("Metrics error:", error);
    res.status(500).json({
      success: false,
      error: "Failed to fetch metrics",
    });
  }
});

app.post("/metrics/reset", (req, res) => {
  try {
    const result = resetMetrics();
    logger.info("Metrics reset");
    res.json({
      success: true,
      ...result,
    });
  } catch (error) {
    logger.error("Metrics reset error:", error);
    res.status(500).json({
      success: false,
      error: "Failed to reset metrics",
    });
  }
});

app.use(
  "/api-docs",
  swaggerUi.serve,
  swaggerUi.setup(swaggerSpec, {
    swaggerOptions: {
      persistAuthorization: true,
    },
  })
);

app.get("/api", (req, res) => {
  res.json({
    success: true,
    api: "Valyxo Backend API",
    version: process.env.API_VERSION || "0.5.1",
    endpoints: {
      auth: "/api/auth",
      users: "/api/users",
      projects: "/api/projects",
      scripts: "/api/scripts",
    },
    docs: "/api-docs",
    health: "/health",
    metrics: "/metrics",
  });
});

app.use("/api/auth", authLimiter, authRoutes);
app.use("/api/users", cacheMiddleware(600), userRoutes);
app.use("/api/projects", cacheMiddleware(300), projectRoutes);
app.use("/api/scripts", scriptRoutes);

const websitePath = path.join(__dirname, "../../website");
if (fs.existsSync(websitePath)) {
  app.use(express.static(websitePath));

  app.get("/", (req, res) => {
    res.sendFile(path.join(websitePath, "index.html"));
  });

  app.get(/\.(html|css|js)$/, (req, res, next) => {
    res.sendFile(path.join(websitePath, req.path), { root: "/" }, (err) => {
      if (err) next();
    });
  });
}

app.use((req, res) => {
  logger.warn(`404 Not Found: ${req.method} ${req.path}`);
  res.status(404).json({
    success: false,
    error: "Endpoint not found",
  });
});

app.use(errorHandler);

const startServer = async () => {
  try {
    await initializeDatabase();
    logger.info("Database initialized successfully");

    app.listen(PORT, () => {
      logger.info(`Valyxo API server running on port ${PORT}`);
      logger.info(`Environment: ${process.env.NODE_ENV || "development"}`);
      logger.info(`Version: ${process.env.API_VERSION || "0.41"}`);
      logger.info(`API Docs available at http://localhost:${PORT}/api-docs`);
    });
  } catch (error) {
    logger.error("Failed to start server:", error);
    process.exit(1);
  }
};

if (require.main === module) {
  startServer();
}

module.exports = app;
