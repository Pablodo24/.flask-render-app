# Use a slim Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 8080

# Start the Gunicorn server
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
