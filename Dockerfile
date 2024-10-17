# Use the official Python image as the base
FROM python:3.10.6

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files into the container
COPY . .

# Expose the port for the application
EXPOSE 8000

# Command to run the application using Django's development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
