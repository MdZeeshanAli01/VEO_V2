# ==============================================================================
# Vision Error Observatory (VEO) - Container Image
# Lightweight Python runtime with native HTTP 206 Partial Content MP4 streaming
# ==============================================================================
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VEO_HOST=0.0.0.0

WORKDIR /app

# Copy the web application and server script
COPY web_app/ /app/web_app/

# The video and scene data are GitHub release assets; files already in the build context are reused
RUN python web_app/fetch_assets.py

# Expose server port (mapped to 80 via Docker/docker-compose)
EXPOSE 8000

# Start VEO server
CMD ["python", "web_app/serve.py"]
