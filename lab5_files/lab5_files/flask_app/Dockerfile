FROM python:3.9-slim

# Install PostgreSQL dependencies (libpq-dev and gcc for building Python packages)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy and install the Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Start the Flask application
CMD ["python", "app.py"]
