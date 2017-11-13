FROM python:alpine3.6

ADD . /app/

WORKDIR /app/

RUN pip install -r requirements.txt

CMD ["python", "/app/download_source_code.py"]
