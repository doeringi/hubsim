FROM python:3.9.18

# Install required system packages (including cmake)
RUN apt-get update && \
    apt-get install -y \
    cmake \
    build-essential

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install requirements from docker-requirements.txt
RUN pip install -r docker-requirements.txt

CMD ["python", "main.py"]

