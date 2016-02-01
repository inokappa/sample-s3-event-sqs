FROM python:2
MAINTAINER inokappa
WORKDIR /app
RUN mkdir /app/images
ADD requirements.txt /app
ADD app.sh /app
ADD _credentials.sh /app
ADD _function.sh /app
ADD supervisord.conf /app
RUN chmod 755 /app/app.sh
RUN wget https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 -O /usr/local/bin/jq && chmod +x /usr/local/bin/jq
RUN pip install -r /app/requirements.txt
RUN touch /tmp/supervisor.sock
CMD [ "/usr/local/bin/supervisord", "-c", "/app/supervisord.conf" ]
