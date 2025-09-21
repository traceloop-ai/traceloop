# Traceloop Makefile
# Production observability for AI agents

.PHONY: help init build test clean install deps fmt lint docker docs

# Default target
help: ## Show this help message
	@echo "Traceloop - Production observability for AI agents"
	@echo ""
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Project configuration
PROJECT_NAME := traceloop
GO_MODULE := github.com/traceloop-ai/traceloop
BINARY_NAME := traceloop
BUILD_DIR := ./build
DOCKER_IMAGE := ghcr.io/traceloop-ai/traceloop

# Go configuration
GO_VERSION := 1.24
GOFLAGS := -mod=readonly
LDFLAGS := -s -w -X main.version=$(shell git describe --tags --always --dirty) -X main.commit=$(shell git rev-parse HEAD)

# Python configuration  
PYTHON := python3
PIP := pip3
VENV_DIR := venv

# Colors for output
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RESET := \033[0m

init: ## Initialize the project dependencies
	@echo "$(BLUE)Initializing project dependencies...$(RESET)"
	@go mod download
	@go mod tidy
	@$(PYTHON) -m venv $(VENV_DIR) && \
		source $(VENV_DIR)/bin/activate && \
		$(PIP) install -e "sdk/python[dev]"
	@echo "$(GREEN)✓ Dependencies initialized$(RESET)"

deps: ## Install/update dependencies
	@echo "$(BLUE)Installing dependencies...$(RESET)"
	@go mod download
	@go mod tidy
	@source $(VENV_DIR)/bin/activate && $(PIP) install -e "sdk/python[dev]"
	@echo "$(GREEN)✓ Dependencies updated$(RESET)"

build: ## Build the Go binary
	@echo "$(BLUE)Building $(BINARY_NAME)...$(RESET)"
	@mkdir -p $(BUILD_DIR)
	@go build $(GOFLAGS) -ldflags "$(LDFLAGS)" -o $(BUILD_DIR)/$(BINARY_NAME) ./cmd/traceloop
	@echo "$(GREEN)✓ Built $(BUILD_DIR)/$(BINARY_NAME)$(RESET)"

build-all: ## Build binaries for multiple platforms
	@echo "$(BLUE)Building for multiple platforms...$(RESET)"
	@mkdir -p $(BUILD_DIR)
	@GOOS=linux GOARCH=amd64 go build $(GOFLAGS) -ldflags "$(LDFLAGS)" -o $(BUILD_DIR)/$(BINARY_NAME)-linux-amd64 ./cmd/traceloop
	@GOOS=darwin GOARCH=amd64 go build $(GOFLAGS) -ldflags "$(LDFLAGS)" -o $(BUILD_DIR)/$(BINARY_NAME)-darwin-amd64 ./cmd/traceloop
	@GOOS=darwin GOARCH=arm64 go build $(GOFLAGS) -ldflags "$(LDFLAGS)" -o $(BUILD_DIR)/$(BINARY_NAME)-darwin-arm64 ./cmd/traceloop
	@GOOS=windows GOARCH=amd64 go build $(GOFLAGS) -ldflags "$(LDFLAGS)" -o $(BUILD_DIR)/$(BINARY_NAME)-windows-amd64.exe ./cmd/traceloop
	@echo "$(GREEN)✓ Built binaries for multiple platforms$(RESET)"

install: build ## Install the binary to GOPATH/bin
	@echo "$(BLUE)Installing $(BINARY_NAME)...$(RESET)"
	@go install $(GOFLAGS) -ldflags "$(LDFLAGS)" ./cmd/traceloop
	@echo "$(GREEN)✓ Installed $(BINARY_NAME)$(RESET)"

test-go: ## Run Go tests
	@echo "$(BLUE)Running Go tests...$(RESET)"
	@go test -v -race -coverprofile=coverage.out ./...
	@go tool cover -html=coverage.out -o coverage.html
	@echo "$(GREEN)✓ Go tests completed$(RESET)"

test-python: ## Run Python tests
	@echo "$(BLUE)Running Python tests...$(RESET)"
	@source $(VENV_DIR)/bin/activate && \
		cd sdk/python && \
		pytest -v --cov=traceloop --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Python tests completed$(RESET)"

test: test-go test-python ## Run all tests

benchmark: ## Run Go benchmarks
	@echo "$(BLUE)Running benchmarks...$(RESET)"
	@go test -bench=. -benchmem ./...
	@echo "$(GREEN)✓ Benchmarks completed$(RESET)"

fmt: ## Format code
	@echo "$(BLUE)Formatting code...$(RESET)"
	@go fmt ./...
	@cd sdk/python && \
		source $(VENV_DIR)/bin/activate && \
		black . && \
		isort .
	@echo "$(GREEN)✓ Code formatted$(RESET)"

lint: ## Lint code
	@echo "$(BLUE)Linting code...$(RESET)"
	@golangci-lint run ./...
	@source $(VENV_DIR)/bin/activate && \
		cd sdk/python && \
		black --check . && \
		isort --check-only . && \
		flake8 . && \
		mypy traceloop
	@echo "$(GREEN)✓ Linting completed$(RESET)"

clean: ## Clean build artifacts
	@echo "$(BLUE)Cleaning build artifacts...$(RESET)"
	@rm -rf $(BUILD_DIR)
	@rm -f coverage.out coverage.html
	@cd sdk/python && rm -rf build/ dist/ *.egg-info/ .coverage htmlcov/ .pytest_cache/
	@go clean -cache -testcache
	@echo "$(GREEN)✓ Cleaned build artifacts$(RESET)"

docker: ## Build Docker image
	@echo "$(BLUE)Building Docker image...$(RESET)"
	@docker build -t $(DOCKER_IMAGE):latest .
	@docker build -t $(DOCKER_IMAGE):$(shell git describe --tags --always) .
	@echo "$(GREEN)✓ Docker image built$(RESET)"

docker-push: docker ## Build and push Docker image
	@echo "$(BLUE)Pushing Docker image...$(RESET)"
	@docker push $(DOCKER_IMAGE):latest
	@docker push $(DOCKER_IMAGE):$(shell git describe --tags --always)
	@echo "$(GREEN)✓ Docker image pushed$(RESET)"

run: build ## Build and run the server locally
	@echo "$(BLUE)Starting traceloop server...$(RESET)"
	@$(BUILD_DIR)/$(BINARY_NAME) server --port 8080

dev: ## Run in development mode with hot reload
	@echo "$(BLUE)Starting development server...$(RESET)"
	@go run ./cmd/traceloop server --port 8080

proto: ## Generate protobuf files
	@echo "$(BLUE)Generating protobuf files...$(RESET)"
	@protoc --go_out=. --go-grpc_out=. sdk/proto/*.proto
	@cd sdk/python && python -m grpc_tools.protoc -I../proto --python_out=traceloop --grpc_python_out=traceloop ../proto/*.proto
	@echo "$(GREEN)✓ Protobuf files generated$(RESET)"

docs: ## Generate documentation
	@echo "$(BLUE)Generating documentation...$(RESET)"
	@go doc -all > docs/go-api.md
	@cd sdk/python && \
		source $(VENV_DIR)/bin/activate && \
		sphinx-build -b html docs docs/_build/html
	@echo "$(GREEN)✓ Documentation generated$(RESET)"

release: ## Create a release (requires VERSION environment variable)
	@if [ -z "$(VERSION)" ]; then \
		echo "$(RED)ERROR: VERSION environment variable is required$(RESET)"; \
		exit 1; \
	fi
	@echo "$(BLUE)Creating release $(VERSION)...$(RESET)"
	@git tag -a v$(VERSION) -m "Release v$(VERSION)"
	@git push origin v$(VERSION)
	@$(MAKE) build-all
	@echo "$(GREEN)✓ Release v$(VERSION) created$(RESET)"

# Development helpers
watch: ## Watch for file changes and rebuild
	@echo "$(BLUE)Watching for changes...$(RESET)"
	@command -v air >/dev/null 2>&1 || go install github.com/cosmtrek/air@latest
	@air

setup-hooks: ## Set up git hooks
	@echo "$(BLUE)Setting up git hooks...$(RESET)"
	@cp scripts/pre-commit .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@echo "$(GREEN)✓ Git hooks installed$(RESET)"

check: fmt lint test ## Run all checks (format, lint, test)

ci: deps check build ## Run CI pipeline locally

# Database and migration helpers (for future use)
migrate-up: ## Run database migrations up
	@echo "$(BLUE)Running migrations up...$(RESET)"
	@# TODO: Add migration command when database layer is implemented

migrate-down: ## Run database migrations down
	@echo "$(BLUE)Running migrations down...$(RESET)"
	@# TODO: Add migration command when database layer is implemented

# Quick development tasks
quick-test: ## Run quick tests (no race detection)
	@go test ./...
	@cd sdk/python && $(PYTHON) -m pytest --tb=short

quick-build: ## Quick build without optimizations
	@go build -o $(BUILD_DIR)/$(BINARY_NAME) ./cmd/traceloop
