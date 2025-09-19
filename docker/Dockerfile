# Build stage
FROM golang:1.21-alpine AS builder

# Install build dependencies
RUN apk add --no-cache git make

# Set working directory
WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build the binary
RUN make build

# Runtime stage
FROM alpine:3.18

# Install runtime dependencies
RUN apk add --no-cache ca-certificates tzdata

# Create non-root user
RUN addgroup -g 1001 -S traceloop && \
    adduser -u 1001 -S traceloop -G traceloop

# Create directories
RUN mkdir -p /app/data /app/web && \
    chown -R traceloop:traceloop /app

# Copy binary from builder stage
COPY --from=builder /app/build/traceloop /app/traceloop

# Copy web assets (when available)
# COPY --from=builder /app/web/dashboard/build /app/web/dashboard/build

# Set user
USER traceloop

# Set working directory
WORKDIR /app

# Expose ports
EXPOSE 8080 8081

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

# Set entrypoint
ENTRYPOINT ["./traceloop"]
CMD ["server", "--host", "0.0.0.0", "--port", "8080"]
