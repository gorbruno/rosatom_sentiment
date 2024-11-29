# Start from the official Python base image.
FROM python:3.11
# set main dir
WORKDIR /ml-service
# copy requirements
COPY ./requirements.txt /ml-service/requirements.txt

# install requirements
RUN pip install --no-cache-dir --upgrade -r /ml-service/requirements.txt

# copy sources and model
COPY ./entity_models /ml-service/entity_models
COPY ./services /ml-service/services
COPY ./ml_models /ml-service/ml_models
COPY ./main.py /ml-service/

# start app command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]