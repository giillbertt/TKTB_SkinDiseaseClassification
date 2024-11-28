# 1. Use a base image with Python (Python 3.12 in this case)
FROM python:3.12-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy the backend files to the container
COPY ./Backend /app/Backend

# 4. Copy the frontend files (optional, for static files)
COPY ./Frontend /app/Frontend

# 5. Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r /app/Backend/requirements.txt

# 6. Expose the port your app runs on (5000 for Flask, for example)
EXPOSE 5000

# 7. Command to run the backend app
CMD ["python", "/app/Backend/app.py"]
