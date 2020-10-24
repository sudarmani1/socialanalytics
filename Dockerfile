FROM ubuntu:18.04
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.7 python3.7-dev libmysqlclient-dev apache2 python3-pip mysql-client
COPY . /socialanalytics/
RUN cd /socialanalytics/ && python3.7 -m pip install -r requirements.txt
RUN cd /socialanalytics/ python3.7 manage.py collectstatic --noinput
RUN cd /socialanalytics/ CMD ["python3.7", "manage.py", "makemigrations"]
RUN cd /socialanalytics/ CMD ["python3.7", "manage.py", "migrate"]
RUN cd /socialanalytics/ CMD ["python3.7", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
