FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose the app port
EXPOSE 8000

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
