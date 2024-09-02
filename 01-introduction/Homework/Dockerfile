FROM python:3.12

# We need to install wget to download the csv file
RUN apt-get install wget
# psycopg2 is a postgres db adapter for python: sqlalchemy needs it
RUN pip install pandas sqlalchemy psycopg2
# RUN requests libary
RUN pip install requests


WORKDIR /app
COPY ingest_data_homework.py ingest_data_homework.py


ENTRYPOINT [ "python", "ingest_data_homework.py" ]