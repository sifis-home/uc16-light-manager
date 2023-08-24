# syntax=docker/dockerfile:1
FROM python:3.8

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

ADD main.py /

ADD run_manager.sh /
ADD launch_light_manager.sh /

ENTRYPOINT ["/bin/bash", "/run_manager.sh"]


