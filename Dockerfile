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

# Command to run the application
# We use "python -m app.main" so it executes the logic inside "if __name__ == '__main__':"
# This allows it to read the PORT env var or default to 8000
CMD ["python", "-m", "app.main"]
