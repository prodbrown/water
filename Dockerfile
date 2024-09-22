FROM python:3.11.4-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create a non-root user
RUN useradd -m myuser
USER myuser

# Set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker caching
COPY --chown=myuser:myuser ./requirements.txt /app/
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application
COPY --chown=myuser:myuser . /app

# Health check to ensure the app is running
HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1

# Start the application
ENTRYPOINT ["gunicorn", "WaterBillingSystem.wsgi", "-b", "0.0.0.0:8000"]
