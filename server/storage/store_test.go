package storage

import (
	"context"
	"os"
	"testing"
)

func TestBadgerStore_GetTraces(t *testing.T) {
	// Clean up any existing test data
	os.RemoveAll("/tmp/traceloop-test")

	// Create a temporary store
	store, err := NewBadgerStore("/tmp/traceloop-test")
	if err != nil {
		t.Fatalf("Failed to create store: %v", err)
	}
	defer func() {
		store.Close()
		os.RemoveAll("/tmp/traceloop-test")
	}()

	// Test getting traces from empty store
	traces, err := store.GetTraces(context.Background(), 10)
	if err != nil {
		t.Fatalf("Failed to get traces: %v", err)
	}

	// Should return empty list
	if len(traces) != 0 {
		t.Errorf("Expected empty traces, got %d", len(traces))
	}
}

func TestBadgerStore_GetStats(t *testing.T) {
	// Clean up any existing test data
	os.RemoveAll("/tmp/traceloop-test")

	// Create a temporary store
	store, err := NewBadgerStore("/tmp/traceloop-test")
	if err != nil {
		t.Fatalf("Failed to create store: %v", err)
	}
	defer func() {
		store.Close()
		os.RemoveAll("/tmp/traceloop-test")
	}()

	// Test getting stats from empty store
	stats, err := store.GetStats(context.Background())
	if err != nil {
		t.Fatalf("Failed to get stats: %v", err)
	}

	// Should return zero stats
	if stats["total_traces"] != 0 {
		t.Errorf("Expected 0 total traces, got %v", stats["total_traces"])
	}
}

func TestBadgerStore_StoreTrace(t *testing.T) {
	// Clean up any existing test data
	os.RemoveAll("/tmp/traceloop-test")

	// Create a temporary store
	store, err := NewBadgerStore("/tmp/traceloop-test")
	if err != nil {
		t.Fatalf("Failed to create store: %v", err)
	}
	defer func() {
		store.Close()
		os.RemoveAll("/tmp/traceloop-test")
	}()

	// Test storing a trace
	trace := map[string]interface{}{
		"trace_id":   "test-trace-1",
		"name":       "test-trace",
		"start_time": "2024-09-20T10:00:00Z",
		"status":     "ok",
		"spans":      []map[string]interface{}{},
	}

	err = store.StoreTrace(context.Background(), trace)
	if err != nil {
		t.Fatalf("Failed to store trace: %v", err)
	}

	// Test retrieving the stored trace
	retrievedTrace, err := store.GetTrace(context.Background(), "test-trace-1")
	if err != nil {
		t.Fatalf("Failed to get trace: %v", err)
	}

	if retrievedTrace["trace_id"] != "test-trace-1" {
		t.Errorf("Expected trace_id 'test-trace-1', got %v", retrievedTrace["trace_id"])
	}
}
