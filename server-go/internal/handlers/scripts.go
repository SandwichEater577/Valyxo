package handlers

import (
	"net/http"
	"strconv"
	"time"

	"github.com/SandwichEater577/valyxo-backend/internal/db"
	"github.com/SandwichEater577/valyxo-backend/internal/middleware"
	"github.com/gin-gonic/gin"
)

// ScriptRequest represents script input
type ScriptRequest struct {
	Name     string `json:"name" binding:"required,min=1,max=100"`
	Content  string `json:"content"`
	Language string `json:"language"`
}

// GetScriptsByProject returns all scripts for a project
func GetScriptsByProject(c *gin.Context) {
	userID := middleware.GetUserID(c)
	projectID, err := strconv.ParseInt(c.Param("projectId"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "Invalid project ID",
		})
		return
	}

	// Check project ownership
	isOwner, err := db.CheckProjectOwnership(projectID, userID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to verify access",
		})
		return
	}
	if !isOwner {
		c.JSON(http.StatusForbidden, gin.H{
			"success": false,
			"error":   "Access denied",
		})
		return
	}

	scripts, err := db.GetScriptsByProjectID(projectID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to fetch scripts",
		})
		return
	}

	if scripts == nil {
		scripts = []db.Script{}
	}

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"data":    scripts,
	})
}

// CreateScript creates a new script in a project
func CreateScript(c *gin.Context) {
	userID := middleware.GetUserID(c)
	projectID, err := strconv.ParseInt(c.Param("projectId"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "Invalid project ID",
		})
		return
	}

	// Check project ownership
	isOwner, err := db.CheckProjectOwnership(projectID, userID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to verify access",
		})
		return
	}
	if !isOwner {
		c.JSON(http.StatusForbidden, gin.H{
			"success": false,
			"error":   "Access denied",
		})
		return
	}

	var req ScriptRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "Validation error: " + err.Error(),
		})
		return
	}

	language := req.Language
	if language == "" {
		language = "valyxoscript"
	}

	scriptID, err := db.CreateScript(projectID, req.Name, req.Content, language)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to create script",
		})
		return
	}

	c.JSON(http.StatusCreated, gin.H{
		"success": true,
		"message": "Script created successfully",
		"data": gin.H{
			"id":         scriptID,
			"project_id": projectID,
			"name":       req.Name,
			"language":   language,
			"created_at": time.Now().Format(time.RFC3339),
		},
	})
}

// GetScript returns a single script
func GetScript(c *gin.Context) {
	userID := middleware.GetUserID(c)
	scriptID, err := strconv.ParseInt(c.Param("scriptId"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "Invalid script ID",
		})
		return
	}

	script, err := db.GetScriptByID(scriptID, userID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to fetch script",
		})
		return
	}
	if script == nil {
		c.JSON(http.StatusNotFound, gin.H{
			"success": false,
			"error":   "Script not found",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"data":    script,
	})
}

// UpdateScript updates an existing script
func UpdateScript(c *gin.Context) {
	userID := middleware.GetUserID(c)
	scriptID, err := strconv.ParseInt(c.Param("scriptId"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "Invalid script ID",
		})
		return
	}

	// Check ownership
	script, err := db.CheckScriptOwnership(scriptID, userID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to verify access",
		})
		return
	}
	if script == nil {
		c.JSON(http.StatusNotFound, gin.H{
			"success": false,
			"error":   "Script not found",
		})
		return
	}

	var req ScriptRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "Validation error: " + err.Error(),
		})
		return
	}

	language := req.Language
	if language == "" {
		language = "valyxoscript"
	}

	if err := db.UpdateScript(scriptID, req.Name, req.Content, language); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to update script",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"message": "Script updated successfully",
		"data": gin.H{
			"id":         scriptID,
			"name":       req.Name,
			"language":   language,
			"updated_at": time.Now().Format(time.RFC3339),
		},
	})
}

// DeleteScript deletes a script
func DeleteScript(c *gin.Context) {
	userID := middleware.GetUserID(c)
	scriptID, err := strconv.ParseInt(c.Param("scriptId"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "Invalid script ID",
		})
		return
	}

	// Check ownership
	script, err := db.CheckScriptOwnership(scriptID, userID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to verify access",
		})
		return
	}
	if script == nil {
		c.JSON(http.StatusNotFound, gin.H{
			"success": false,
			"error":   "Script not found",
		})
		return
	}

	if err := db.DeleteScript(scriptID); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to delete script",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"message": "Script deleted successfully",
	})
}
