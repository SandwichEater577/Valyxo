package config

import (
	"os"
	"strconv"
	"time"
)

type Config struct {
	Port           string
	JWTSecret      string
	JWTExpire      time.Duration
	DBPath         string
	CORSOrigin     string
	APIVersion     string
	Environment    string
	RateLimitGeneral int
	RateLimitAuth    int
}

func Load() *Config {
	return &Config{
		Port:             getEnv("PORT", "5000"),
		JWTSecret:        getEnv("JWT_SECRET", "valyxo-super-secret-key-change-in-production"),
		JWTExpire:        parseDuration(getEnv("JWT_EXPIRE", "168h")), // 7 days
		DBPath:           getEnv("DB_PATH", "./data/valyxo.db"),
		CORSOrigin:       getEnv("CORS_ORIGIN", "http://localhost:3000"),
		APIVersion:       getEnv("API_VERSION", "0.5.1"),
		Environment:      getEnv("NODE_ENV", "development"),
		RateLimitGeneral: getEnvInt("RATE_LIMIT_GENERAL", 100),
		RateLimitAuth:    getEnvInt("RATE_LIMIT_AUTH", 5),
	}
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		if intVal, err := strconv.Atoi(value); err == nil {
			return intVal
		}
	}
	return defaultValue
}

func parseDuration(s string) time.Duration {
	d, err := time.ParseDuration(s)
	if err != nil {
		return 168 * time.Hour // 7 days default
	}
	return d
}
