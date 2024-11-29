# Start from the official Python base image.
FROM python:3.11

# Set the current working directory to 'ml-service'
# This is where we'll put the requirements.txt file and the app directory.
WORKDIR /app-server

# copy requirements
COPY ./requirements.txt /app-server/requirements.txt

# --no-cache-dir option tells pip to not save the downloaded packages locally in the cache
# because cache using is necessary when pip run again to install the same packages
# this is not about working with the containers
RUN pip install --no-cache-dir --upgrade -r /app-server/requirements.txt

# copy sources
COPY ./database /app-server/database
COPY ./models /app-server/models
COPY ./requests_tools /app-server/requests_tools
COPY ./services /app-server/services
COPY ./settings /app-server/settings
COPY main.py /app-server/

# start app command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]