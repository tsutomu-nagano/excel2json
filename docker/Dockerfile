FROM python:3.9-slim

WORKDIR /code

RUN apt -y update && apt -y install locales
RUN echo "ja_JP UTF-8" > /etc/locale.gen
RUN locale-gen

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./excel2json /code/app
COPY ./sample /code/sample

ENV PYTHONPATH /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
