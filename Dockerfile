# Optimized Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy only necessary files first (for caching efficiency)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose necessary ports (if needed)
EXPOSE 5000

# Define the entry point
CMD ["python", "app.py"]
