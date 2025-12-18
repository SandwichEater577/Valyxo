package handlers

import (
	"net/http"
	"strconv"
	"time"

	"github.com/SandwichEater577/valyxo-backend/internal/db"
	"github.com/SandwichEater577/valyxo-backend/internal/middleware"
	"github.com/gin-gonic/gin"
)

// ProjectRequest represents project input
type ProjectRequest struct {
	Name        string `json:"name" binding:"required,min=1,max=100"`
	Description string `json:"description"`
}

// GetProjects returns all projects for current user
func GetProjects(c *gin.Context) {
	userID := middleware.GetUserID(c)

	projects, err := db.GetProjectsByUserID(userID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to fetch projects",
		})
		return
	}

	if projects == nil {
		projects = []db.Project{}
	}

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"data":    projects,
	})
}

// GetProject returns a single project
func GetProject(c *gin.Context) {
	userID := middleware.GetUserID(c)
	projectID, err := strconv.ParseInt(c.Param("projectId"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "Invalid project ID",
		})
		return
	}

	project, err := db.GetProjectByID(projectID, userID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to fetch project",
		})
		return
	}
	if project == nil {
		c.JSON(http.StatusNotFound, gin.H{
			"success": false,
			"error":   "Project not found",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"data":    project,
	})
}

// CreateProject creates a new project
func CreateProject(c *gin.Context) {
	userID := middleware.GetUserID(c)

	var req ProjectRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "Validation error: " + err.Error(),
		})
		return
	}

	projectID, err := db.CreateProject(userID, req.Name, req.Description)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to create project",
		})
		return
	}

	c.JSON(http.StatusCreated, gin.H{
		"success": true,
		"message": "Project created successfully",
		"data": gin.H{
			"id":          projectID,
			"name":        req.Name,
			"description": req.Description,
			"created_at":  time.Now().Format(time.RFC3339),
		},
	})
}

// UpdateProject updates an existing project
func UpdateProject(c *gin.Context) {
	userID := middleware.GetUserID(c)
	projectID, err := strconv.ParseInt(c.Param("projectId"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "Invalid project ID",
		})
		return
	}

	// Check ownership
	project, err := db.GetProjectByID(projectID, userID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to fetch project",
		})
		return
	}
	if project == nil {
		c.JSON(http.StatusNotFound, gin.H{
			"success": false,
			"error":   "Project not found",
		})
		return
	}

	var req ProjectRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "Validation error: " + err.Error(),
		})
		return
	}

	if err := db.UpdateProject(projectID, req.Name, req.Description); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to update project",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"message": "Project updated successfully",
		"data": gin.H{
			"id":          projectID,
			"name":        req.Name,
			"description": req.Description,
			"updated_at":  time.Now().Format(time.RFC3339),
		},
	})
}

// DeleteProject deletes a project
func DeleteProject(c *gin.Context) {
	userID := middleware.GetUserID(c)
	projectID, err := strconv.ParseInt(c.Param("projectId"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"error":   "Invalid project ID",
		})
		return
	}

	// Check ownership
	project, err := db.GetProjectByID(projectID, userID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to fetch project",
		})
		return
	}
	if project == nil {
		c.JSON(http.StatusNotFound, gin.H{
			"success": false,
			"error":   "Project not found",
		})
		return
	}

	if err := db.DeleteProject(projectID); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"error":   "Failed to delete project",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"message": "Project deleted successfully",
	})
}
