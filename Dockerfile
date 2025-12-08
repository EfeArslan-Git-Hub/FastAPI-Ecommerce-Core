# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Copy the file with the requirements to the container
COPY ./requirements.txt /code/requirements.txt

# Install the package dependencies in the requirements file
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application's code to the container
COPY ./app /code/app

# Command to run the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
