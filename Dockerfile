FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies required for building Python packages
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml into the container
COPY pyproject.toml .

# Install project dependencies using pip or a dependency tool of your choice
# If your project uses pip, ensure the dependencies from pyproject.toml are installed,
# or adjust this section if you're using another tool like Poetry.
RUN python -m pip install --upgrade pip && \
    python -m pip install sqlalchemy mysql-connector-python

# Copy the rest of your project files into the container
COPY . .

# Define the command to run your application; adjust as necessary
CMD ["python", "mysqlconnector.py"]