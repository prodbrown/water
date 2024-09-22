FROM python:3.11.4-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create a non-root user and set working directory
RUN useradd -m myuser
USER myuser
WORKDIR /app

# Switch back to root for installing system dependencies
USER root

# Install required system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY --chown=myuser:myuser ./requirements.txt /app/

# Switch to non-root user for installing Python dependencies
USER myuser

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY --chown=myuser:myuser . /app

# Switch back to root to clean up system dependencies and gcc
USER root

# Clean up unnecessary build tools to reduce the image size
RUN apt-get purge -y --auto-remove gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Set health check to ensure the app is running
HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1

# Switch back to non-root user for running the application
USER myuser

# Start the application
ENTRYPOINT ["gunicorn", "WaterBillingSystem.wsgi", "-b", "0.0.0.0:8000"]
