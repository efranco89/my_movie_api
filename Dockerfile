FROM python:3.10

WORKDIR /my_movie_api
COPY requirements.txt /my_movie_api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /my_movie_api/requirements.txt

COPY . /my_movie_api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload", "--port", "80"]