FROM python:2
MAINTAINER inokappa
RUN mkdir /app
ADD requirements.txt /app
ADD app.py /app
ADD supervisord.conf /app
RUN pip install -r /app/requirements.txt
RUN touch /tmp/supervisor.sock
CMD [ "/usr/local/bin/supervisord", "-c", "/app/supervisord.conf" ]
