# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Copy the requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script and any other necessary files
COPY script.py .
COPY generate_qrcode.py .

# Expose the port your script is listening on (if applicable)
EXPOSE 80

# Define the command to run your script
CMD ["python", "script.py"]
