# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /calculator

# Copy the current directory contents into the container
COPY . /calculator

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the outside world
EXPOSE 5000

# Define the command to run the application
CMD ["python", "app.py"]