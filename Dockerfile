# Use the official Python image as the base
FROM python:3.9-slim

# Add metadata labels
LABEL version="1.2" \
      description="To-Do App Dashboard with Flask, Docker, and CRUD Operations" \
      maintainer="Ahmed Khalil" \
      release="v1.2"

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app/ /app/

# Expose port 5000 to access the app
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
