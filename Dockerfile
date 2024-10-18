# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables for security
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create a working directory and set permissions
WORKDIR /home/appuser
RUN chown -R appuser:appuser /home/appuser

# Switch to the non-root user
USER appuser

# Copy the requirements file and install dependencies
COPY --chown=appuser:appuser requirements.txt /home/appuser/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY --chown=appuser:appuser webservice /home/appuser/webservice

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["python", "-m", "webservice"]