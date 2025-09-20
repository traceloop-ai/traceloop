package storage

import (
	"context"
	"encoding/json"
	"fmt"
	"path/filepath"

	"github.com/dgraph-io/badger/v4"
)

// Store interface defines the storage operations
type Store interface {
	GetTraces(ctx context.Context, limit int) ([]map[string]interface{}, error)
	GetTrace(ctx context.Context, id string) (map[string]interface{}, error)
	GetStats(ctx context.Context) (map[string]interface{}, error)
	StoreTrace(ctx context.Context, trace map[string]interface{}) error
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
		opts.Prefix = []byte("trace:")
		it := txn.NewIterator(opts)
		defer it.Close()

		count := 0
		for it.Rewind(); it.Valid() && count < limit; it.Next() {
			item := it.Item()
			key := item.Key()

			// Only process trace keys
			if string(key[:6]) == "trace:" {
				err := item.Value(func(val []byte) error {
					// Parse the stored trace data
					var trace map[string]interface{}
					if err := json.Unmarshal(val, &trace); err != nil {
						return fmt.Errorf("failed to unmarshal trace: %w", err)
					}
					traces = append(traces, trace)
					count++
					return nil
				})
				if err != nil {
					return err
				}
			}
		}

		return nil
	})

	if err != nil {
		return nil, fmt.Errorf("failed to get traces: %w", err)
	}

	return traces, nil
}

// GetTrace retrieves a specific trace by ID
func (s *BadgerStore) GetTrace(ctx context.Context, id string) (map[string]interface{}, error) {
	var trace map[string]interface{}

	err := s.db.View(func(txn *badger.Txn) error {
		key := []byte("trace:" + id)
		item, err := txn.Get(key)
		if err != nil {
			if err == badger.ErrKeyNotFound {
				return fmt.Errorf("trace not found")
			}
			return err
		}

		return item.Value(func(val []byte) error {
			return json.Unmarshal(val, &trace)
		})
	})

	if err != nil {
		return nil, err
	}

	return trace, nil
}

// StoreTrace stores a trace in the database
func (s *BadgerStore) StoreTrace(ctx context.Context, trace map[string]interface{}) error {
	// Extract trace ID
	traceID, ok := trace["trace_id"].(string)
	if !ok {
		return fmt.Errorf("trace_id is required")
	}

	// Serialize trace to JSON
	data, err := json.Marshal(trace)
	if err != nil {
		return fmt.Errorf("failed to marshal trace: %w", err)
	}

	// Store in BadgerDB
	key := []byte("trace:" + traceID)
	return s.db.Update(func(txn *badger.Txn) error {
		return txn.Set(key, data)
	})
}

// GetStats retrieves storage statistics
func (s *BadgerStore) GetStats(ctx context.Context) (map[string]interface{}, error) {
	var totalTraces, totalSpans int
	var storageSize int64

	err := s.db.View(func(txn *badger.Txn) error {
		opts := badger.DefaultIteratorOptions
		opts.Prefix = []byte("trace:")
		it := txn.NewIterator(opts)
		defer it.Close()

		for it.Rewind(); it.Valid(); it.Next() {
			item := it.Item()
			key := item.Key()

			if string(key[:6]) == "trace:" {
				totalTraces++

				// Count spans in this trace
				err := item.Value(func(val []byte) error {
					var trace map[string]interface{}
					if err := json.Unmarshal(val, &trace); err != nil {
						return err
					}

					if spans, ok := trace["spans"].([]interface{}); ok {
						totalSpans += len(spans)
					}

					storageSize += int64(len(val))
					return nil
				})
				if err != nil {
					return err
				}
			}
		}

		return nil
	})

	if err != nil {
		return nil, fmt.Errorf("failed to get stats: %w", err)
	}

	// Convert storage size to human readable format
	storageSizeMB := float64(storageSize) / (1024 * 1024)
	storageSizeStr := fmt.Sprintf("%.2f MB", storageSizeMB)

	return map[string]interface{}{
		"total_traces": totalTraces,
		"total_spans":  totalSpans,
		"storage_size": storageSizeStr,
	}, nil
}
