package grpc

import (
	"fmt"
	"log"
	"net"

	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

// Server represents the gRPC server
type Server struct {
	grpcServer *grpc.Server
	store      Store
}

// Store interface for data storage
type Store interface {
	// Add methods that the gRPC server needs
	Close() error
}

// NewServer creates a new gRPC server
func NewServer(store Store) (*Server, error) {
	grpcServer := grpc.NewServer()

	// Register services here when we implement them
	// For now, just enable reflection for testing
	reflection.Register(grpcServer)

	return &Server{
		grpcServer: grpcServer,
		store:      store,
	}, nil
}

// Start starts the gRPC server
func (s *Server) Start(port int) error {
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", port))
	if err != nil {
		return fmt.Errorf("failed to listen on port %d: %w", port, err)
	}

	log.Printf("gRPC server listening on port %d", port)

	if err := s.grpcServer.Serve(lis); err != nil {
		return fmt.Errorf("failed to serve gRPC: %w", err)
	}

	return nil
}

// Stop stops the gRPC server
func (s *Server) Stop() {
	if s.grpcServer != nil {
		s.grpcServer.GracefulStop()
	}
}
