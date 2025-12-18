package main

import (
	"fmt"
	"log"
	"os"
	"runtime"
	"time"

	"github.com/SandwichEater577/valyxo-backend/internal/config"
	"github.com/SandwichEater577/valyxo-backend/internal/db"
	"github.com/SandwichEater577/valyxo-backend/internal/handlers"
	"github.com/SandwichEater577/valyxo-backend/internal/middleware"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
)

var (
	startTime    = time.Now()
	requestCount int64
)

func main() {
	// Load .env file if it exists
	_ = godotenv.Load()

	// Load configuration
	cfg := config.Load()

	// Initialize JWT
	middleware.InitJWT(cfg.JWTSecret, cfg.JWTExpire)

	// Initialize database
	if err := db.Initialize(cfg.DBPath); err != nil {
		log.Fatalf("Failed to initialize database: %v", err)
	}
	defer db.Close()
	log.Println("Database initialized successfully")

	// Set Gin mode
	if cfg.Environment == "production" {
		gin.SetMode(gin.ReleaseMode)
	}

	// Create router
	r := gin.New()

	// Apply global middleware
	r.Use(gin.Recovery())
	r.Use(middleware.SecurityHeaders())
	r.Use(middleware.CORS(cfg.CORSOrigin))

	// Create rate limiters
	generalLimiter := middleware.NewRateLimiter(cfg.RateLimitGeneral, 15*time.Minute)
	authLimiter := middleware.NewRateLimiter(cfg.RateLimitAuth, 15*time.Minute)

	// Apply general rate limiting to all routes
	r.Use(middleware.RateLimitMiddleware(generalLimiter, "Too many requests, please try again later"))

	// Health check endpoint
	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"success":    true,
			"status":     "healthy",
			"uptime":     time.Since(startTime).String(),
			"version":    cfg.APIVersion,
			"go_version": runtime.Version(),
		})
	})

	// Metrics endpoint
	r.GET("/metrics", func(c *gin.Context) {
		var m runtime.MemStats
		runtime.ReadMemStats(&m)

		c.JSON(200, gin.H{
			"success": true,
			"metrics": gin.H{
				"uptime_seconds":   time.Since(startTime).Seconds(),
				"goroutines":       runtime.NumGoroutine(),
				"memory_alloc_mb":  float64(m.Alloc) / 1024 / 1024,
				"memory_sys_mb":    float64(m.Sys) / 1024 / 1024,
				"gc_cycles":        m.NumGC,
				"go_version":       runtime.Version(),
				"num_cpu":          runtime.NumCPU(),
			},
		})
	})

	// API info endpoint
	r.GET("/api", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"success": true,
			"api":     "Valyxo Backend API (Go)",
			"version": cfg.APIVersion,
			"endpoints": gin.H{
				"auth":     "/api/auth",
				"users":    "/api/users",
				"projects": "/api/projects",
				"scripts":  "/api/scripts",
			},
			"health":  "/health",
			"metrics": "/metrics",
		})
	})

	// API routes
	api := r.Group("/api")

	// Auth routes (with stricter rate limiting)
	auth := api.Group("/auth")
	auth.Use(middleware.RateLimitMiddleware(authLimiter, "Too many login attempts. Please try again later."))
	{
		auth.POST("/register", handlers.Register)
		auth.POST("/login", handlers.Login)
		auth.POST("/logout", middleware.AuthMiddleware(), handlers.Logout)
		auth.GET("/me", middleware.AuthMiddleware(), handlers.GetMe)
	}

	// User routes (protected)
	users := api.Group("/users")
	users.Use(middleware.AuthMiddleware())
	{
		users.GET("/profile", handlers.GetProfile)
		users.PUT("/profile", handlers.UpdateProfile)
		users.PUT("/password", handlers.UpdatePassword)
	}

	// Project routes (protected)
	projects := api.Group("/projects")
	projects.Use(middleware.AuthMiddleware())
	{
		projects.GET("", handlers.GetProjects)
		projects.POST("", handlers.CreateProject)
		projects.GET("/:projectId", handlers.GetProject)
		projects.PUT("/:projectId", handlers.UpdateProject)
		projects.DELETE("/:projectId", handlers.DeleteProject)
	}

	// Script routes (protected)
	scripts := api.Group("/scripts")
	scripts.Use(middleware.AuthMiddleware())
	{
		scripts.GET("/project/:projectId", handlers.GetScriptsByProject)
		scripts.POST("/project/:projectId", handlers.CreateScript)
		scripts.GET("/:scriptId", handlers.GetScript)
		scripts.PUT("/:scriptId", handlers.UpdateScript)
		scripts.DELETE("/:scriptId", handlers.DeleteScript)
	}

	// Serve static files from website directory
	websitePath := "../website"
	if _, err := os.Stat(websitePath); err == nil {
		r.Static("/css", websitePath+"/css")
		r.Static("/js", websitePath+"/js")
		r.Static("/HTML", websitePath+"/HTML")
		r.Static("/Assets", websitePath+"/Assets")
		r.StaticFile("/", websitePath+"/index.html")
	}

	// 404 handler
	r.NoRoute(func(c *gin.Context) {
		c.JSON(404, gin.H{
			"success": false,
			"error":   "Endpoint not found",
		})
	})

	// Start server
	addr := fmt.Sprintf(":%s", cfg.Port)
	log.Printf("Valyxo API server (Go) running on port %s", cfg.Port)
	log.Printf("Environment: %s", cfg.Environment)
	log.Printf("Version: %s", cfg.APIVersion)

	if err := r.Run(addr); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
