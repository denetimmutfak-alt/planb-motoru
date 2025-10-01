# PlanB Motoru v2.0 - Hephaistos & Hermes Entegrasyonlu Finansal Analiz Sistemi
# Multi-stage build for optimized production image

# Stage 1: Build stage
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    FLASK_APP=main.py \
    FLASK_ENV=production

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN groupadd -r planb && useradd -r -g planb planb

# Create app directory
WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/static /app/templates \
    && chown -R planb:planb /app

# Switch to non-root user
USER planb

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Default command
CMD ["python", "main.py", "dashboard", "--host", "0.0.0.0", "--port", "5000"]

# Labels for metadata
LABEL maintainer="PlanB Motoru Team" \
      version="2.0" \
      description="Hephaistos & Hermes Entegrasyonlu Finansal Analiz Sistemi" \
      org.opencontainers.image.title="PlanB Motoru" \
      org.opencontainers.image.description="Multi-market financial analysis system with astrology integration" \
      org.opencontainers.image.version="2.0" \
      org.opencontainers.image.authors="PlanB Motoru Team"


