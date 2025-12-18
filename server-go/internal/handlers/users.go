package handlers

import (
	"net/http"
	"regexp"

	"github.com/SandwichEater577/valyxo-backend/internal/db"
	"github.com/SandwichEater577/valyxo-backend/internal/middleware"
	"github.com/gin-gonic/gin"
	"golang.org/x/crypto/bcrypt"
)

// email regex for validation
var emailPattern = regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)

// ProfileUpdateRequest represents profile update input
type ProfileUpdateRequest struct {
	Email    *string `json:"email"`
	Username *string `json:"username"`
}

// PasswordUpdateRequest represents password update input
type PasswordUpdateRequest struct {
	CurrentPassword string `json:"currentPassword" binding:"required"`
	NewPassword     string `json:"newPassword" binding:"required,min=8"`
}

// GetProfile returns current user's profile with stats
func GetProfile(c *gin.Context) {
	userID := middleware.GetUserID(c)

	user, err := db.GetUserByID(userID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to fetch profile",
		})
		return
	}
	if user == nil {
		c.JSON(http.StatusNotFound, gin.H{
			"success": false,
			"error":   "User not found",
		})
		return
	}

	projectCount, scriptCount, err := db.GetUserProjectAndScriptCount(userID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to fetch profile",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"user": gin.H{
			"id":           user.ID,
			"username":     user.Username,
			"email":        user.Email,
			"created_at":   user.CreatedAt,
			"updated_at":   user.UpdatedAt,
			"projectCount": projectCount,
			"scriptCount":  scriptCount,
		},
	})
}

// UpdateProfile updates user's profile
func UpdateProfile(c *gin.Context) {
	userID := middleware.GetUserID(c)

	var req ProfileUpdateRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "Validation error: " + err.Error(),
		})
		return
	}

	// Validate email format
	if req.Email != nil {
		if !emailPattern.MatchString(*req.Email) {
			c.JSON(http.StatusBadRequest, gin.H{
				"success": false,
				"error":   "Invalid email address",
			})
			return
		}

		// Check if email is already in use
		exists, err := db.CheckEmailExists(*req.Email, userID)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{
				"success": false,
				"error":   "Failed to update profile",
			})
			return
		}
		if exists {
			c.JSON(http.StatusBadRequest, gin.H{
				"success": false,
				"error":   "Email already in use",
			})
			return
		}
	}

	// Validate username
	if req.Username != nil {
		if len(*req.Username) < 3 || len(*req.Username) > 32 {
			c.JSON(http.StatusBadRequest, gin.H{
				"success": false,
				"error":   "Username must be between 3 and 32 characters",
			})
			return
		}

		// Check if username is already in use
		exists, err := db.CheckUsernameExists(*req.Username, userID)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{
				"success": false,
				"error":   "Failed to update profile",
			})
			return
		}
		if exists {
			c.JSON(http.StatusBadRequest, gin.H{
				"success": false,
				"error":   "Username already in use",
			})
			return
		}
	}

	if req.Email == nil && req.Username == nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "No valid fields to update",
		})
		return
	}

	if err := db.UpdateUserProfile(userID, req.Email, req.Username); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to update profile",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"message": "Profile updated successfully",
	})
}

// UpdatePassword updates user's password
func UpdatePassword(c *gin.Context) {
	userID := middleware.GetUserID(c)

	var req PasswordUpdateRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "Validation error: " + err.Error(),
		})
		return
	}

	// Check password strength
	if !validatePassword(req.NewPassword) {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "Password must contain uppercase, lowercase, and number",
		})
		return
	}

	// Get current user
	user, err := db.GetUserByID(userID)
	if err != nil || user == nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to update password",
		})
		return
	}

	// Verify current password
	if err := bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(req.CurrentPassword)); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "Current password is incorrect",
		})
		return
	}

	// Hash new password
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(req.NewPassword), bcrypt.DefaultCost)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to update password",
		})
		return
	}

	if err := db.UpdateUserPassword(userID, string(hashedPassword)); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to update password",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"message": "Password updated successfully",
	})
}
