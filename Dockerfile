FROM python:3.9

WORKDIR /json

COPY . /json

RUN pip install pandas

CMD ["python", "./docker_json.py"]