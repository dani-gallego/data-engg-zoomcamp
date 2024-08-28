#!/usr/bin/env python
# coding: utf-8

import requests
import os
import pandas as pd
import argparse

from sqlalchemy import create_engine
from time import time


# This function, download_file, is designed to download a file from a given URL and save it locally to your machine.
def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name_1 = params.table_name_1
    table_name_2 = params.table_name_2
    url1 = params.url1
    url2 = params.url2

    # Download the URL for yellow_taxi_data
    csv_name_1 = url1.split("/")[-1]
    download_file(url1, csv_name_1)

    # Download the URL for taxi_zone_lookup
    csv_name_2 = url2.split("/")[-1]
    download_file(url2, csv_name_2)

    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    print("Let's process the first file - yellow_taxi_data")
    df_iter = pd.read_csv(csv_name_1, iterator=True, chunksize=100000, engine='python')
    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name_1, con=engine, if_exists='replace')
    df.to_sql(name=table_name_1, con=engine, if_exists='append')

    while True: 
        try:
            t_start = time()
            df = next(df_iter)

            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table_name_1, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting trips into the postgres database")
            break

    print("We will also process the second file - taxi_zone_lookup")
    df = pd.read_csv(csv_name_2)
    df.to_sql(name=table_name_2, con=engine, if_exists='append')
    print("Finished inserting zones into postgres database")
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name_1', required=True, help='name of the first table where we will write the first CSV results')
    parser.add_argument('--table_name_2', required=True, help='name of the second table where we will write the second CSV results')
    parser.add_argument('--url1', required=True, help='URL of the first CSV file')
    parser.add_argument('--url2', required=True, help='URL of the second CSV file')

    args = parser.parse_args()

    main(args)
