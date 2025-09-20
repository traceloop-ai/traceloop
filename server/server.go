package server

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/traceloop-ai/traceloop/server/grpc"
	"github.com/traceloop-ai/traceloop/server/storage"
)

// Config holds the server configuration
type Config struct {
	Host string
	Port int
}

// Server represents the main traceloop server
type Server struct {
	config  Config
	storage storage.Store
	grpc    *grpc.Server
	http    *http.Server
}

// Start initializes and starts the traceloop server
func Start(config Config) error {
	// Initialize storage
	store, err := storage.NewBadgerStore("./data")
	if err != nil {
		return fmt.Errorf("failed to initialize storage: %w", err)
	}

	server := &Server{
		config:  config,
		storage: store,
	}

	// Start gRPC server for SDK communication
	grpcServer, err := grpc.NewServer(store)
	if err != nil {
		return fmt.Errorf("failed to create gRPC server: %w", err)
	}
	server.grpc = grpcServer

	// Start HTTP server for REST API and web UI
	router := gin.Default()
	server.setupRoutes(router)

	httpServer := &http.Server{
		Addr:    fmt.Sprintf("%s:%d", config.Host, config.Port),
		Handler: router,
	}
	server.http = httpServer

	// Start servers in goroutines
	go func() {
		log.Printf("Starting gRPC server on port %d", config.Port+1)
		if err := server.grpc.Start(config.Port + 1); err != nil {
			log.Printf("gRPC server error: %v", err)
		}
	}()

	go func() {
		log.Printf("Starting HTTP server on %s", httpServer.Addr)
		if err := httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Printf("HTTP server error: %v", err)
		}
	}()

	// Wait for interrupt signal to gracefully shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Println("Shutting down server...")

	// Create a deadline for shutdown
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	// Shutdown HTTP server
	if err := server.http.Shutdown(ctx); err != nil {
		log.Printf("HTTP server forced to shutdown: %v", err)
	}

	// Shutdown gRPC server
	server.grpc.Stop()

	// Close storage
	if err := server.storage.Close(); err != nil {
		log.Printf("Error closing storage: %v", err)
	}

	log.Println("Server exited")
	return nil
}

// setupRoutes configures the HTTP routes
func (s *Server) setupRoutes(router *gin.Engine) {
	// Health check
	router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	// API routes
	api := router.Group("/api/v1")
	{
		api.GET("/traces", s.handleGetTraces)
		api.POST("/traces", s.handleStoreTrace)
		api.GET("/traces/:id", s.handleGetTrace)
		api.GET("/stats", s.handleGetStats)
	}

	// Serve static files for dashboard
	router.Static("/static", "./web/dashboard/build/static")
	router.StaticFile("/", "./web/dashboard/build/index.html")
	router.NoRoute(func(c *gin.Context) {
		c.File("./web/dashboard/build/index.html")
	})
}

// HTTP handlers
func (s *Server) handleGetTraces(c *gin.Context) {
	traces, err := s.storage.GetTraces(context.Background(), 100)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, traces)
}

func (s *Server) handleStoreTrace(c *gin.Context) {
	var trace map[string]interface{}
	if err := c.ShouldBindJSON(&trace); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if err := s.storage.StoreTrace(context.Background(), trace); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"status": "stored"})
}

func (s *Server) handleGetTrace(c *gin.Context) {
	id := c.Param("id")
	trace, err := s.storage.GetTrace(context.Background(), id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "trace not found"})
		return
	}
	c.JSON(http.StatusOK, trace)
}

func (s *Server) handleGetStats(c *gin.Context) {
	stats, err := s.storage.GetStats(context.Background())
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, stats)
}
