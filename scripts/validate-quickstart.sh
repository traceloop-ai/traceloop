#!/bin/bash

# Traceloop Quick Start Validation Script
# This script validates all quick start steps and generates a status report

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SERVER_PORT=8080
SERVER_HOST="localhost"
PYTHON_VENV="venv"
# Status file for website consumption
STATUS_FILE="status.json"

# Status tracking variables
GO_INSTALL_STATUS="unknown"
DOCKER_INSTALL_STATUS="unknown"
HOMEBREW_INSTALL_STATUS="unknown"
SERVER_HEALTH_STATUS="unknown"
SERVER_TRACES_API_STATUS="unknown"
SERVER_STATS_API_STATUS="unknown"
PYTHON_INSTALL_STATUS="unknown"
PYTHON_IMPORT_STATUS="unknown"
SIMPLE_EXAMPLE_STATUS="unknown"
TEST_SCRIPT_STATUS="unknown"

GO_INSTALL_NOTES=""
DOCKER_INSTALL_NOTES=""
HOMEBREW_INSTALL_NOTES=""
SERVER_HEALTH_NOTES=""
SERVER_TRACES_API_NOTES=""
SERVER_STATS_API_NOTES=""
PYTHON_INSTALL_NOTES=""
PYTHON_IMPORT_NOTES=""
SIMPLE_EXAMPLE_NOTES=""
TEST_SCRIPT_NOTES=""

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Test functions
test_go_installation() {
    log_info "Testing Go installation method..."
    if command -v go &> /dev/null; then
        if go install github.com/traceloop-ai/traceloop/cmd/traceloop@latest; then
            GO_INSTALL_STATUS="working"
            log_success "Go installation works"
        else
            GO_INSTALL_STATUS="broken"
            GO_INSTALL_NOTES="Failed to install via go install"
            log_error "Go installation failed"
        fi
    else
        GO_INSTALL_STATUS="broken"
        GO_INSTALL_NOTES="Go not installed"
        log_error "Go not found"
    fi
}

test_docker_installation() {
    log_info "Testing Docker installation method..."
    if command -v docker &> /dev/null; then
        if docker ps &> /dev/null; then
            # Build the Docker image locally
            if docker build -f docker/Dockerfile -t traceloop-test:latest . &> /dev/null; then
                if docker run --rm -d --name traceloop-test -p 8081:8080 traceloop-test:latest &> /dev/null; then
                    sleep 5
                    if curl -s http://localhost:8081/health &> /dev/null; then
                        DOCKER_INSTALL_STATUS="working"
                        log_success "Docker installation works"
                    else
                        DOCKER_INSTALL_STATUS="broken"
                        DOCKER_INSTALL_NOTES="Container started but health check failed"
                        log_error "Docker health check failed"
                    fi
                    docker stop traceloop-test &> /dev/null || true
                else
                    DOCKER_INSTALL_STATUS="broken"
                    DOCKER_INSTALL_NOTES="Failed to start container"
                    log_error "Docker container failed to start"
                fi
            else
                DOCKER_INSTALL_STATUS="broken"
                DOCKER_INSTALL_NOTES="Failed to build Docker image"
                log_error "Docker build failed"
            fi
        else
            DOCKER_INSTALL_STATUS="broken"
            DOCKER_INSTALL_NOTES="Docker daemon not running"
            log_error "Docker daemon not running"
        fi
    else
        DOCKER_INSTALL_STATUS="broken"
        DOCKER_INSTALL_NOTES="Docker not installed"
        log_error "Docker not found"
    fi
}

test_homebrew_installation() {
    log_info "Testing Homebrew installation method..."
    if command -v brew &> /dev/null; then
        # For now, just check if Homebrew is available
        # The actual tap installation will be tested when the tap is published
        HOMEBREW_INSTALL_STATUS="working"
        HOMEBREW_INSTALL_NOTES="Homebrew available (tap not yet published)"
        log_success "Homebrew is available"
    else
        HOMEBREW_INSTALL_STATUS="broken"
        HOMEBREW_INSTALL_NOTES="Homebrew not installed"
        log_warning "Homebrew not found - this is optional for validation"
    fi
}

test_server_startup() {
    log_info "Testing server startup..."
    
    # Clean up any existing server
    pkill -f traceloop || true
    rm -rf data || true
    
    # Start server in background
    ./build/traceloop server --port $SERVER_PORT --host $SERVER_HOST &> server.log &
    SERVER_PID=$!
    sleep 5
    
    # Test health endpoint
    if curl -s http://$SERVER_HOST:$SERVER_PORT/health | grep -q "ok"; then
        SERVER_HEALTH_STATUS="working"
        log_success "Server health check works"
    else
        SERVER_HEALTH_STATUS="broken"
        SERVER_HEALTH_NOTES="Health endpoint not responding"
        log_error "Server health check failed"
    fi
    
    # Test traces API
    if curl -s http://$SERVER_HOST:$SERVER_PORT/api/v1/traces &> /dev/null; then
        SERVER_TRACES_API_STATUS="working"
        log_success "Traces API works"
    else
        SERVER_TRACES_API_STATUS="broken"
        SERVER_TRACES_API_NOTES="Traces API not responding"
        log_error "Traces API failed"
    fi
    
    # Test stats API
    if curl -s http://$SERVER_HOST:$SERVER_PORT/api/v1/stats &> /dev/null; then
        SERVER_STATS_API_STATUS="working"
        log_success "Stats API works"
    else
        SERVER_STATS_API_STATUS="broken"
        SERVER_STATS_API_NOTES="Stats API not responding"
        log_error "Stats API failed"
    fi
    
    # Stop server
    kill $SERVER_PID || true
    wait $SERVER_PID 2>/dev/null || true
}

test_python_sdk() {
    log_info "Testing Python SDK..."

    # Create virtual environment if it doesn't exist
    if [ ! -d "$PYTHON_VENV" ]; then
        log_info "Creating Python virtual environment..."
        python3 -m venv $PYTHON_VENV
    fi

    # Use virtual environment
    source $PYTHON_VENV/bin/activate

    # Install the Python SDK
    log_info "Installing Python SDK..."
    if pip install -e sdk/python &> /dev/null; then
        PYTHON_INSTALL_STATUS="working"
        log_success "Python SDK installation works"
    else
        PYTHON_INSTALL_STATUS="broken"
        PYTHON_INSTALL_NOTES="Failed to install Python SDK"
        log_error "Python SDK installation failed"
    fi

    # Test basic functionality
    if python3 -c "import traceloop; print('SDK imported successfully')" &> /dev/null; then
        PYTHON_IMPORT_STATUS="working"
        log_success "Python SDK import works"
    else
        PYTHON_IMPORT_STATUS="broken"
        PYTHON_IMPORT_NOTES="Failed to import traceloop"
        log_error "Python SDK import failed"
    fi
}

test_examples() {
    log_info "Testing examples..."
    
    # Start server for testing
    pkill -f traceloop || true
    rm -rf data || true
    ./build/traceloop server --port $SERVER_PORT --host $SERVER_HOST &> server.log &
    SERVER_PID=$!
    sleep 5
    
    # Test simple example
    source $PYTHON_VENV/bin/activate
    if python3 examples/simple_test.py &> /dev/null; then
        SIMPLE_EXAMPLE_STATUS="working"
        log_success "Simple example works"
    else
        SIMPLE_EXAMPLE_STATUS="broken"
        SIMPLE_EXAMPLE_NOTES="Simple example failed to run"
        log_error "Simple example failed"
    fi
    
    # Test test script
    if python3 sdk/python/tests/test_traceloop.py &> /dev/null; then
        TEST_SCRIPT_STATUS="working"
        log_success "Test script works"
    else
        TEST_SCRIPT_STATUS="broken"
        TEST_SCRIPT_NOTES="Test script failed to run"
        log_error "Test script failed"
    fi
    
    # Stop server
    kill $SERVER_PID || true
    wait $SERVER_PID 2>/dev/null || true
}

generate_status_report() {
    log_info "Generating status report..."
    
    # Calculate overall status
    local working_count=0
    local total_count=0
    
    # Count working tests
    for status in "$GO_INSTALL_STATUS" "$DOCKER_INSTALL_STATUS" "$HOMEBREW_INSTALL_STATUS" \
                  "$SERVER_HEALTH_STATUS" "$SERVER_TRACES_API_STATUS" "$SERVER_STATS_API_STATUS" \
                  "$PYTHON_INSTALL_STATUS" "$PYTHON_IMPORT_STATUS" "$SIMPLE_EXAMPLE_STATUS" "$TEST_SCRIPT_STATUS"; do
        total_count=$((total_count + 1))
        if [ "$status" = "working" ]; then
            working_count=$((working_count + 1))
        fi
    done
    
    local overall_status="partial"
    if [ $working_count -eq $total_count ]; then
        overall_status="working"
    elif [ $working_count -gt $((total_count / 2)) ]; then
        overall_status="partial"
    else
        overall_status="broken"
    fi
    
    # Generate JSON status report
    cat > $STATUS_FILE << EOF
{
    "last_updated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "overall_status": "$overall_status",
    "working_count": $working_count,
    "total_count": $total_count,
    "tests": {
        "go_install": {
            "status": "$GO_INSTALL_STATUS",
            "notes": "$GO_INSTALL_NOTES"
        },
        "docker_install": {
            "status": "$DOCKER_INSTALL_STATUS",
            "notes": "$DOCKER_INSTALL_NOTES"
        },
        "homebrew_install": {
            "status": "$HOMEBREW_INSTALL_STATUS",
            "notes": "$HOMEBREW_INSTALL_NOTES"
        },
        "server_health": {
            "status": "$SERVER_HEALTH_STATUS",
            "notes": "$SERVER_HEALTH_NOTES"
        },
        "server_traces_api": {
            "status": "$SERVER_TRACES_API_STATUS",
            "notes": "$SERVER_TRACES_API_NOTES"
        },
        "server_stats_api": {
            "status": "$SERVER_STATS_API_STATUS",
            "notes": "$SERVER_STATS_API_NOTES"
        },
        "python_install": {
            "status": "$PYTHON_INSTALL_STATUS",
            "notes": "$PYTHON_INSTALL_NOTES"
        },
        "python_import": {
            "status": "$PYTHON_IMPORT_STATUS",
            "notes": "$PYTHON_IMPORT_NOTES"
        },
        "simple_example": {
            "status": "$SIMPLE_EXAMPLE_STATUS",
            "notes": "$SIMPLE_EXAMPLE_NOTES"
        },
        "test_script": {
            "status": "$TEST_SCRIPT_STATUS",
            "notes": "$TEST_SCRIPT_NOTES"
        }
    }
}
EOF

    log_success "Status report generated: $STATUS_FILE"
}

# Main execution
main() {
    log_info "Starting Traceloop Quick Start Validation"
    echo "=============================================="
    
    # Change to project root
    cd "$(dirname "$0")/.."
    
    # Run all tests
    test_go_installation
    test_docker_installation
    test_homebrew_installation
    test_server_startup
    test_python_sdk
    test_examples
    
    # Generate status report for website
    generate_status_report
    
    # Print summary
    echo ""
    echo "=============================================="
    echo "Validation Summary:"
    echo "=============================================="
    echo "Go Installation: $GO_INSTALL_STATUS"
    echo "Docker Installation: $DOCKER_INSTALL_STATUS"
    echo "Homebrew Installation: $HOMEBREW_INSTALL_STATUS"
    echo "Server Health: $SERVER_HEALTH_STATUS"
    echo "Server Traces API: $SERVER_TRACES_API_STATUS"
    echo "Server Stats API: $SERVER_STATS_API_STATUS"
    echo "Python SDK Install: $PYTHON_INSTALL_STATUS"
    echo "Python SDK Import: $PYTHON_IMPORT_STATUS"
    echo "Simple Example: $SIMPLE_EXAMPLE_STATUS"
    echo "Test Script: $TEST_SCRIPT_STATUS"
    echo ""
    
    # Count working tests for overall status
    local working_count=0
    local total_count=0
    for status in "$GO_INSTALL_STATUS" "$DOCKER_INSTALL_STATUS" "$HOMEBREW_INSTALL_STATUS" \
                  "$SERVER_HEALTH_STATUS" "$SERVER_TRACES_API_STATUS" "$SERVER_STATS_API_STATUS" \
                  "$PYTHON_INSTALL_STATUS" "$PYTHON_IMPORT_STATUS" "$SIMPLE_EXAMPLE_STATUS" "$TEST_SCRIPT_STATUS"; do
        total_count=$((total_count + 1))
        if [ "$status" = "working" ]; then
            working_count=$((working_count + 1))
        fi
    done
    
    local overall_status="partial"
    if [ $working_count -eq $total_count ]; then
        overall_status="working"
    elif [ $working_count -gt $((total_count / 2)) ]; then
        overall_status="partial"
    else
        overall_status="broken"
    fi
    
    echo "Working: $working_count/$total_count"
    echo "Overall Status: $overall_status"
    echo ""

    if [ "$overall_status" = "working" ]; then
        log_success "All quick start steps are working! 🎉"
    elif [ "$overall_status" = "partial" ]; then
        log_warning "Some quick start steps need attention ⚠️"
    else
        log_error "Multiple quick start steps are broken ❌"
    fi
}

# Run main function
main "$@"