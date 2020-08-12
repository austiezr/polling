FROM python:3.8

MAINTAINER Austin Robinson "austinziech@gmail.com"

COPY ./requirements.txt /app/requirements.txt

COPY ./templates /app/templates

COPY application/app.py /app/app.py

WORKDIR /app

RUN pip3 install -r ./requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python3", "app.py" ]