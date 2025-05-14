# -------- Stage 1: Build --------
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# -------- Stage 2: Runtime --------
FROM python:3.11-slim

# Create non-root user
RUN useradd -m flaskuser

# Set workdir
WORKDIR /app

# Copy only necessary files
COPY --from=builder /root/.local /root/.local
COPY . .

# Ensure permissions
RUN chown -R flaskuser:flaskuser /app

# Use non-root user
USER flaskuser

# Use user's local Python bin
ENV PATH=/root/.local/bin:$PATH

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s CMD curl -f http://localhost:5000/ || exit 1

# Start app
CMD ["python", "app.py"]
