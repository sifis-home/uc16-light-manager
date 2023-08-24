# syntax=docker/dockerfile:1
FROM python:3.8

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

ADD main.py /

ENTRYPOINT ["/usr/local/bin/python3", "/main.py"]


