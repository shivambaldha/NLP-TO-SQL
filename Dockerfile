# Use the official Python 3.10.12 image as the base image
FROM python:3.10.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit runs on (default is 8501)
EXPOSE 8501

# Command to run your Streamlit application
CMD ["streamlit", "run", "main.py"]