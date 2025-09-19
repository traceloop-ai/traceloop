package storage

import (
	"context"
	"fmt"
	"path/filepath"
	"time"

	"github.com/dgraph-io/badger/v4"
)

// Store interface defines the storage operations
type Store interface {
	GetTraces(ctx context.Context, limit int) ([]map[string]interface{}, error)
	GetTrace(ctx context.Context, id string) (map[string]interface{}, error)
	GetStats(ctx context.Context) (map[string]interface{}, error)
	Close() error
}

// BadgerStore implements the Store interface using BadgerDB
type BadgerStore struct {
	db *badger.DB
}

// NewBadgerStore creates a new BadgerDB-based store
func NewBadgerStore(dataDir string) (*BadgerStore, error) {
	opts := badger.DefaultOptions(filepath.Join(dataDir, "traceloop"))
	opts.Logger = nil // Disable BadgerDB logging for now

	db, err := badger.Open(opts)
	if err != nil {
		return nil, fmt.Errorf("failed to open BadgerDB: %w", err)
	}

	return &BadgerStore{db: db}, nil
}

// Close closes the store
func (s *BadgerStore) Close() error {
	if s.db != nil {
		return s.db.Close()
	}
	return nil
}

// GetTraces retrieves traces from storage
func (s *BadgerStore) GetTraces(ctx context.Context, limit int) ([]map[string]interface{}, error) {
	var traces []map[string]interface{}

	err := s.db.View(func(txn *badger.Txn) error {
		opts := badger.DefaultIteratorOptions
		opts.PrefetchSize = 10
		it := txn.NewIterator(opts)
		defer it.Close()

		count := 0
		for it.Rewind(); it.Valid() && count < limit; it.Next() {
			item := it.Item()
			key := item.Key()

			// For now, return mock data
			if string(key) == "trace:" {
				trace := map[string]interface{}{
					"id":         fmt.Sprintf("trace-%d", count),
					"name":       "test-trace",
					"start_time": time.Now().Add(-time.Hour).Format(time.RFC3339),
					"status":     "ok",
					"spans":      []map[string]interface{}{},
				}
				traces = append(traces, trace)
				count++
			}
		}

		return nil
	})

	if err != nil {
		return nil, fmt.Errorf("failed to get traces: %w", err)
	}

	// If no traces found, return empty list
	if len(traces) == 0 {
		return []map[string]interface{}{}, nil
	}

	return traces, nil
}

// GetTrace retrieves a specific trace by ID
func (s *BadgerStore) GetTrace(ctx context.Context, id string) (map[string]interface{}, error) {
	// For now, return mock data
	return map[string]interface{}{
		"id":         id,
		"name":       "test-trace",
		"start_time": time.Now().Add(-time.Hour).Format(time.RFC3339),
		"status":     "ok",
		"spans":      []map[string]interface{}{},
	}, nil
}

// GetStats retrieves storage statistics
func (s *BadgerStore) GetStats(ctx context.Context) (map[string]interface{}, error) {
	// For now, return mock stats
	return map[string]interface{}{
		"total_traces": 0,
		"total_spans":  0,
		"storage_size": "0 MB",
	}, nil
}
