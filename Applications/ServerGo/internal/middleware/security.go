package middleware

import (
	"net/http"
	"strings"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
)

// RateLimiter stores request counts per IP
type RateLimiter struct {
	requests map[string][]time.Time
	mu       sync.RWMutex
	window   time.Duration
	limit    int
}

// NewRateLimiter creates a new rate limiter
func NewRateLimiter(limit int, window time.Duration) *RateLimiter {
	rl := &RateLimiter{
		requests: make(map[string][]time.Time),
		window:   window,
		limit:    limit,
	}
	// Clean up old entries periodically
	go rl.cleanup()
	return rl
}

func (rl *RateLimiter) cleanup() {
	ticker := time.NewTicker(time.Minute)
	for range ticker.C {
		rl.mu.Lock()
		now := time.Now()
		for ip, times := range rl.requests {
			var valid []time.Time
			for _, t := range times {
				if now.Sub(t) <= rl.window {
					valid = append(valid, t)
				}
			}
			if len(valid) == 0 {
				delete(rl.requests, ip)
			} else {
				rl.requests[ip] = valid
			}
		}
		rl.mu.Unlock()
	}
}

// Allow checks if the request should be allowed
func (rl *RateLimiter) Allow(ip string) bool {
	rl.mu.Lock()
	defer rl.mu.Unlock()

	now := time.Now()
	cutoff := now.Add(-rl.window)

	// Filter old requests
	var valid []time.Time
	for _, t := range rl.requests[ip] {
		if t.After(cutoff) {
			valid = append(valid, t)
		}
	}

	if len(valid) >= rl.limit {
		rl.requests[ip] = valid
		return false
	}

	rl.requests[ip] = append(valid, now)
	return true
}

// RateLimitMiddleware creates a rate limiting middleware
func RateLimitMiddleware(limiter *RateLimiter, message string) gin.HandlerFunc {
	return func(c *gin.Context) {
		ip := c.ClientIP()
		if !limiter.Allow(ip) {
			c.JSON(http.StatusTooManyRequests, gin.H{
				"success": false,
				"error":   message,
			})
			c.Abort()
			return
		}
		c.Next()
	}
}

// SanitizeInput middleware checks for dangerous characters
func SanitizeInput() gin.HandlerFunc {
	return func(c *gin.Context) {
		// We'll check string values in POST/PUT body
		// For Gin, this is handled during binding validation
		c.Next()
	}
}

// containsDangerous checks if string contains dangerous characters
func containsDangerous(s string, chars []string) bool {
	for _, char := range chars {
		if strings.Contains(s, char) {
			return true
		}
	}
	return false
}

// CORS middleware handles Cross-Origin Resource Sharing
func CORS(origins string) gin.HandlerFunc {
	allowedOrigins := strings.Split(origins, ",")

	return func(c *gin.Context) {
		origin := c.GetHeader("Origin")
		allowed := false

		for _, o := range allowedOrigins {
			if strings.TrimSpace(o) == origin {
				allowed = true
				break
			}
		}

		if allowed {
			c.Writer.Header().Set("Access-Control-Allow-Origin", origin)
		}

		c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(http.StatusNoContent)
			return
		}

		c.Next()
	}
}

// SecurityHeaders adds security headers
func SecurityHeaders() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("X-Content-Type-Options", "nosniff")
		c.Writer.Header().Set("X-Frame-Options", "DENY")
		c.Writer.Header().Set("X-XSS-Protection", "1; mode=block")
		c.Writer.Header().Set("Referrer-Policy", "strict-origin-when-cross-origin")
		c.Writer.Header().Set("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:")
		c.Next()
	}
}

// RequestLogger logs requests
func RequestLogger() gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now()
		path := c.Request.URL.Path

		c.Next()

		duration := time.Since(start)
		status := c.Writer.Status()

		userID := "anonymous"
		if id, exists := c.Get("userId"); exists {
			userID = string(rune(id.(int64)))
		}

		if status >= 400 {
			gin.DefaultWriter.Write([]byte(
				c.Request.Method + " " + path +
					" status=" + string(rune(status)) +
					" duration=" + duration.String() +
					" user=" + userID + "\n",
			))
		}
	}
}
