FROM python:3.11.4-slim-bullseye
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update

# Copy requirements first to leverage Docker caching
COPY ./requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

ENTRYPOINT ["gunicorn", "WaterBillingSystem.wsgi", "-b", "0.0.0.0:8000"]
