# Week 2: Workflow Orchestration

### Table of Contents
- [Introduction to Work Orchestration](#introduction-to-workflow-orchestration)
    - [Architecture using Mage](#architecture-using-mage)
- [Workflow Orchestration using Mage](#workflow-orchestration-using-mage)
    - [What is Mage?](#what-is-mage)
    - [Setting up Mage](#setting-up-mage)
    - [Build and run Mage container](#build-and-run-mage-container)
    - [Accessing Mage](#accessing-mage)
    - [Simple Pipeline using Mage](#simple-pipeline-using-mage)
- [ETL: From API to Postgres](#etl-from-api-to-postgres)
    - [Configuring Postgres](#configuring-postgres)
    - [Creating Custom Connection Profile](#creating-custom-connection-profile)
    - [From API to Postgres](#from-api-to-postgres)
- [ETL: From API to GCS](#etl-from-api-to-gcs)
    - [Configure Google Cloud Platform](#configure-google-cloud-platform)
        - [Creating Google Cloud Bucket](#creating-google-cloud-bucket)
        - [Add a Mage Service Account](#add-a-mage-service-account)
        - [Authentiacate using JSON Credentials](#authenticate-using-json-credentials)
        - [Testing Pipeline for Google Cloud Storage and BigQuery](#testing-pipeline-for-google-cloud-storage-and-bigquery)
    - [ETL: API to GCS ](#etl-api-to-gcs)
        - [Load Data to GCS](#load-data-to-gcs)
        - [Partitioning the Data](#partitioning-the-data)
- [ETL: GCS to BigQuery](#etl-gcs-to-bigquery)
    - [Loading the Data from GCS](#loading-the-data-from-gcs)
    - [Transform the Data for BigQuery](#transform-the-data-for-bigquery)
    - [Exporting the Data to BigQuery](#exporting-the-data-to-bigquery)
    - [Trigger Events: Scheduling](#triggering-events-scheduling)

# Introduction to Workflow Orchestration
> Video Source: [DE Zoomcamp - What is Orchestration?](https://www.youtube.com/watch?v=Li8-MWHhTbo&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=18)


## What is Orchestration?
- Workflow orchestration is the process of managing and automating the execution of complex workflows or sequences of tasks, particularly in data engineering, software development, or cloud operations. It involves coordinating the order, timing, and dependencies of tasks to ensure they run efficiently, reliably, and in the correct sequence.
- **Orchestration** is a process of dependency management, facilitated through ***automation***.
- The *data orchestration* manages scheduling, triggering, monitoring and even resource allocation.

A good orchestrator handles the following:
- Workflow management
- Automation
- Error handling
- Recovery
- Monitoring and alerting
- Resource optimization
- Observability
- Debugging
- Compliance/Auditing
A good orchestrator prioritizes:
    - Flow State
    - Feedback Loops
    - Cognitive Load


## Architecture using Mage
For the week 2: Workflow Orchestration, we will be re-creating the following architecture:

![Mage Architecture](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/mage%20-%20architecture.png)

# Workflow Orchestration using Mage
## What is Mage?
- [Mage](https://docs.mage.ai/introduction/overview) is an open-source tool designed for workflow orchestration, particularly in data engineering and data science workflows. It's used to build, run, and monitor data pipelines, making it easier to manage complex workflows that involve data extraction, transformation, and loading (ETL).

#### ETL (Extact, Transform, Load)
- ETL stands for Extract, Transform, Load. It's a process used in data integration, data warehousing, and data engineering to move data from various sources into a centralized data storage system, such as a data warehouse or data lake.

In this week, we will be doing the following tasks:

- **Extract** - Pulling data from a source (API - <u> NYC Taxi Dataset</u>)

- **Transform** - Data cleaning, transformation, and partitioning.

- **Load** - API to Mage, Mage to Postgres, GCS, BigQuery.

## Setting Up Mage
> Video Source: [DE Zoomcamp - Configure Mage](https://www.youtube.com/watch?v=tNiV7Wp08XE&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=20)

We will clone this repository locally: [Mage zoomcamp](https://github.com/mage-ai/mage-zoomcamp)

Choose your directory first then clone the repo. What i did is to clone the repo to the same directory for week 1. You can do whatever suits you.

```bash
git clone https://github.com/mage-ai/mage-zoomcamp.git mage-zoomcamp
```

We will also must rename the `dev.env` to `.env` in the mage repo since this file containes environmental variable that we needed for this section, it contains sensitive data. The `.gitignore` file already includes `.env` - changing the file name ensures that we won't accidentally commit to GitHub about our sensitive credentials.

```bash
mv dev.env .env
```

### Build and run Mage container
You might want to quick glance the file `docker-compose.yaml` which has services `Mage` and `Postgres`. We will build a container using this.

```bash
docker-compose build
```

In order to run the docker container, we will use:

```bash
docker-compose up
```

In case you encounter a problem when running the `docker-compose up`, try to update the mage. Afterwards run the command above again.

```bash
pull mageai/mageai:latest
```

### Accessing Mage
Once the docker container is running, Mage can be accessed through our browser at the port specified in the `docker-compose.yaml` file.

```
localhost:6789
```

### Simple Pipeline using Mage
> Video Source: [DE Zoomcamp - A Simple Pipeline](https://www.youtube.com/watch?v=stI-gg4QBnI&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=21)

In this section we will learn how to configure a simple pipeline.

In Mage Dashboard, go to **Pipeline** you will find an `example_pipeline` and then open the file. As you notice, there are blocks in the pipeline. Let's briefly discuss the following blocks:

`Data Loader` Block
-------------------
This block is responsible for loading or ingesting data from various sources. It can fetch data from APIs, Databases, files (e.g., CSV, JSON) or cloud storage.

`Transformer` Block
-------------------
This block processes and transforms the data according to the logic defined. This can include data cleaning, filtering, aggregation or any custom configuration using Python, SQL or other tools.

`Data Exporter` Block
-------------------
After transformation, this block is essential to export or stores the processed data to its destination. This could be database, data warehouse or cloud storage

By putting this together, it is basically ETL (Extract, Transform, Load). This workflow closely mirrors a traditional ETL pipeline but with modular component that allows to build and manage the process more flexibly. 

You can also navigate to the right side of the screen to see the Pipeline Tree. This `Pipeline Tree` in Mage is a visual representation of the steps in data pipeline. It shows the flow of data and the dependencies between different tasks. Here's the overview of `Pipeline Tree` with `Data loader` Block

![Pipeline Tree](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/mage%20-%20overview%20of%20example_pipeline.PNG)

Going back to the `example_pipeline`, in this data pipeline, we will execute the blocks. Since the pipeline is composed of a Data Loader, Transformer, and Data Exporter blocks, instead of running them one by one, we will go to the last block, find the three dots (...), and click **Execute with all upstream blocks**. This way, all the blocks will be executed sequentially.

[Go to Top](#week-2-workflow-orchestration)

## ETL: From API to Postgres
### Configuring Postgres
> Video Source: [DE Zoomcamp - Configuring Postgres](https://www.youtube.com/watch?v=pmhI-ezd3BE&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=22)

In this section, we will learn to configure Postgres client in order to connect to local Postgres database in the Docker container.

As I have mentioned, the `docker-compose.yaml` file contains environmental variables which defined in the `.env` file.

```yaml
  # PostgreSQL Service defined in docker-compose 
  postgres:
    image: postgres:14
    restart: on-failure
    container_name: ${PROJECT_NAME}-postgres
    env_file:
      - .env
    environment:
      POSTGRES_DB: ${POSTGRES_DBNAME}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "${POSTGRES_PORT}:5432"
```

In the mage repo, under the folder named magic-zoomcamp we have `io_config.yaml`. You can access the file from VSCode or any tool that you've been using or using Mage. 

If using Mage, go to the **Files**

![Mage - Files](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/mage%20-%20files.PNG)

Then you can locate the io_config.yaml

![Mage - io_config.yaml](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/mage%20-%20io_config.PNG)

This contains the default connection parameters under the `default:` profile. You can locate the Postgres service from there.

```yaml
  # PostgresSQL
  POSTGRES_CONNECT_TIMEOUT: 10
  POSTGRES_DBNAME: postgres
  POSTGRES_SCHEMA: public # Optional
  POSTGRES_USER: username
  POSTGRES_PASSWORD: password
  POSTGRES_HOST: hostname
  POSTGRES_PORT: 5432
```

#### Creating Custom Connection Profile
You can specify a custom connection profile in io_config.yaml. It can be useful to define a Postgres connection for the development environment, for an example.

In order to create a custom profile, go to the last line create `dev:` then copy the Postgres service under `dev:` profile. So this profile, we will pass the environmental variable from `.env` file using [Jingja Templating](https://realpython.com/primer-on-jinja-templating/). The custom dev profile with Postgres connection should look like this in io_config.yaml.

```yaml
dev:
  POSTGRES_CONNECT_TIMEOUT: 10
  POSTGRES_DBNAME: "{{ env_var('POSTGRES_DBNAME') }}"
  POSTGRES_SCHEMA: "{{ env_var('POSTGRES_SCHEMA') }}" # Optional
  POSTGRES_USER: "{{ env_var('POSTGRES_USER') }}"
  POSTGRES_PASSWORD: "{{ env_var('POSTGRES_PASSWORD') }}"
  POSTGRES_HOST: "{{ env_var('POSTGRES_HOST') }}"
  POSTGRES_PORT: "{{ env_var('POSTGRES_PORT') }}"
```

Now, we have established a dev profile. We will now test it by creating a new pipeline.

Step 1: Add create a new pipeline and then select ***Standard (batch)***.
![New Pipeline](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/mage%20-%20create%20new%20pipeline.PNG)

![Pipeline Config](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/mage%20-%20pipeline%20config_standard.PNG)

Step 2: Rename it to `test_config`

Step 3: Add a `Data load` block - SQL. The connection should be Postgres and profile connection should be dev. Check the *Use raw SQL*.

![Data Loader SQL](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/mage%20-%20sql_dataloader.PNG)

Step 4: Run the block with the SQL query below. This way it will initialized connection to the Postgres.

```SQL
SELECT (1);
```

![test_config](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/mage%20-%20test_config.PNG)

> [!NOTE]
> You can delete the block by clicking the three dots (...), from there you will find **Delete block**

### From API to Postgres
> Video Source: [DE Zoomcamp - ETL: API to Postgres](https://www.youtube.com/watch?v=Maidfe7oKLs&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=23)

In this section, we will learn to import the NY taxi dataset, transform the data and load it to Postgres.

`Data loader` Block
-------------------

Step 1: Add a new pipeline as ***Standard (batch)*** and then rename it as `api_to_postgres`.

Step 2: We have to add a new **Data loader** block, set the connection to **Python** > ***API***

Step 3: We will modify the template:
-  URL - we will add URL for the NY Taxi Dataset - [yellow_taxi_data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz)
- Requests - we don't actually need the requests library. Since we are using mage, it don't need to  make requests for loading CSV file with Pandas
- Data Types - declare or map the data types is recommended but not required
    - Declaring **data types** in pandas is important for several reasons, particularly for optimizing performance, ensuring data accuracy, and improving memory efficiency in data processing tasks.
    - **Implicit assertions** refer to the checks or validations that occur automatically based on data type declarations or constraints. When you declare a data type, pandas will implicitly enforce that the data conforms to the specified type. If the data does not match the declared type, pandas will raise errors or exceptions.
- Date Columns - we will create a list of datetime columns to be parsed by read_csv as dates
- Return the data

```python
@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'
    
    # map/declare data types
    taxi_dtypes = {
                    'VendorID' : pd.Int64Dtype(),
                    'passenger_count' : pd.Int64Dtype(),
                    'trip_distance' : float,
                    'RatecodeID' : pd.Int64Dtype(),
                    'store_and_fwd_flag' : str,
                    'PULocationID' : pd.Int64Dtype(),
                    'DOLocationID' : pd.Int64Dtype(),
                    'payment_type' : pd.Int64Dtype(),
                    'fare_amount' : float,
                    'extra' : float,
                    'mta_tax' : float,
                    'tip_amount' : float,
                    'tolls_amount' : float,
                    'improvement_surcharge' : float,
                    'total_amount' : float,
                    'congestion_surcharge' : float
                }
    parse_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']

    return pd.read_csv(url, sep=",", compression="gzip", dtype=taxi_dtypes, parse_dates=parse_dates)
```

>[!TIP]
>
> You can use a Jupyter Notebook to inspect data types before declaring.

`Transformer` Block
----------------
In this block, we will data clean the import data from data loader block. As you notice in the data loader block, there are records of passenger_count is equal to 0. We will assume that it represent a bad data and in order to clean the data, we will have to remove these rows.

Step 1: Add Transformer Block and then add **Python** > ***Generic (no template)***. Rename it as `transform_taxi_data` or whatever you want.

Step 2: Modify the decorator `@transformer`:
- Add a pre-processing steps that prints the number of rows with passenger_count = 0
- Return the data frame filtered for passenger_count > 0

```python
@transformer
def transform(data, *args, **kwargs):
    print(f'[Pre-processing] Rows with zero passengers:', {data['passenger_count'].isin([0]).sum()})

    return data[data['passenger_count'] > 0]
```

Step 3: Add decorator `@test`
- Add decorator `@test` in order to check that there are no records with passenger_count = 0
    - If there are any rides with passenger_count equal to 0, the assertion will fail, and the error message 'There are rides with zero passengers' will be displayed.

```python
@test
def test_output(output, *args):
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'
```

`Data exporter` Block
-----------------
In this block, we will export the cleaned data to a CSV file.

Step 1: Add Data exporter block, choose Python > Postgres and then rename it as data_to_postgres

Step 2: Modify the decorator `@data_exporter`
- schema_name = 'ny_taxi'
- table_name = 'yellow_taxi_data'
- config_profile = 'dev'

```python
@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    schema_name = 'ny_taxi'  # Specify the name of the schema to export data to
    table_name = 'yellow_taxi_data'  # Specify the name of the table to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,  # Specifies whether to include index in exported table
            if_exists='replace',  # Specify resolution policy if table name already exists
        )
```

This is optional but you can actually check the exported data by adding another data loader block at the end.

Step 1: Add a new Data loader block, choose SQL connection, dev as profile connection, and checked the Use raw SQL.

Step 2: Add SQL query

```SQL
SELECT * FROM ny_taxi.yellow_taxi_data;
```

## ETL: From API to GCS
### Configure Google Cloud Platform
> Video Source: [DE Zoomcamp - Configure GCP](https://www.youtube.com/watch?v=00LP360iYvE&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=24)

In this section we will learn on how to set up google cloud to allow Mage to read and write data for Google Cloud Storage and Google BigQuery.

#### Creating Google Cloud Bucket
Step 1: Go to your **Google Cloud Console** > **Cloud Storage** > ***Bucket***. Create a new bucket.

Step 2: Configuring the bucket
- Pick a globally unique name
- Location: choose your region. But for now, we will leave it as US to avoid any conflict in Mage container.
- Storage Class: We will keep it as default `standard`
- Access Control: Leave it as it is but make sure that **Enforce public access prevention** is checked.

#### Add a Mage Service Account
Step 1: Go to your **Google Cloud Console** > **IAM & Admin** > ***Service accounts***. Create a new service account for Mage in order to connect to GCP Project.

Step 2: Configuration of service account
- Service account name: You can choose whatever you want. 
- Role: Set the role to **Basic** > ***Owner***. Please advise that this is only for educational purposes. In production environment, you must set role to more restrictive manner.
- Click *Continue* and *Done*. You have successfully created a service account for Mage.

Step 3: Create a Key
- Go to your **Google Cloud Console** > **IAM & Admin** > ***Service accounts***. Select the service account that we just created.
- Go to the ***Keys*** section > ***Add key*** > ***Create new key***
- Select JSON and click *Create*. This file will be downloaded locally.

Step 4: Move the JSON file to your local Mage directory. This way the JSON file will be available to accessed and can be used by Mage to authenticate. 

#### Authenticate using JSON credentials
Now that we successfully implemented a Mage service account and created a key for credentials. We will now learn how to authenticate these credentials using Mage.

Step 1: Go back to the Mage Dashboard > Files > io_config.yaml

Step 2: Configuring and setting up the Google Service in Mage
- We will use the `GOOGLE_SERVICE_ACC_KEY_PATH` which is a preferred way to authenticate. 
- Find the Google service under default profile connection
- Delete the lines before the `GOOGLE_SERVICE_ACC_KEY_PATH`. Below should be look as the same as yours. 

```yaml
  # Google
  GOOGLE_SERVICE_ACC_KEY_FILEPATH: "/home/src/key_file_name.json"
  GOOGLE_LOCATION: US # Optional
```

>[!TIP]
>
> If you're not sure what is the name of your json file, go to the Mage Terminal use `ls -la` to see the files inside the Mage directory. And if you do not know the directory path, use `pwd` to print your working directory.

Once the Google Credentials is specified, Mage will know where to look adn access the credentials. Mage will use that service acccount key.

#### Testing Pipeline for Google Cloud Storage and BigQuery
Now, we will test a data pipeline if we will able to connect to GCS and BigQuery after setting up the connection.

Step 1: Test Big Query
- Go back to **Mage Pipeline**, select the `test_config`.
- We will change the **Data Loader** Block connection to ***BigQuery*** and set the profile connection to `default`. Since the Google service credential is under the `default` profile and not `dev` profile.
- After running the query below, this will initialized a connection to Google BigQuery.

![test_config - bigquery](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/mage%20-%20test_config_bigquery.PNG)

Step 2: Test GCS
- Go to the example_pipeline in Mage
- Execute the pipeline using the **Execute with all upstream blocks** from the last block. This will download `titanic_clean.csv` to your local Mage directory
- Go to the **Google Bucket** that we created for Mage.
- Upload the file `titanic_clean.csv`.
- Go back to the `test_config` pipeline and delete the **data loader** block.
- We will have to add a new **data loader** block. Add it as **Python** > ***Google Cloud Storage***. Rename it as `test_gcs`.
- Configure the following:
    - bucket_name = 'your-bucket-name'
    - object_key = 'titanic_clean.csv'
- Let's run the block. It will loading the data frame from the Google Bucket.

### ETL: API to GCS
> Video Source: [DE Zoomcamp - ETL: API to GCS](https://www.youtube.com/watch?v=w0XmcASRUnc&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=25)

In this section, we will learn how to write data to GCS. Previously, we write data to Postgres, an OLTP database. Now, we are going to write data to Google Cloud Storage which is a file system in the cloud. Often the data is written to cloud storage as it's destination because it is relatively inexpensive and can also accept semi structured data better than a relational database.

The workflow typically include staging, cleaning, transforming and writing to an analytical source or data lake solution.

#### Load Data to GCS
We are going to create a new pipeline where we will be re-using the blocks that we created in the earlier videos. As it is bad to write a duplicate of code but the good thing about Mage is that everything is exist as code, we can reuse the block.

Step 1: Create a new Standard (batch) pipeline. 

Step 2: You can actually drag the `load_api_data` to the new standard pipeline. We will going to have exactly what we wrote before. Now, we are pulling the same API data again.

Step 3: We will also reuse the transformer block which clean the taxi data - `transform_taxi_data`. 

> If you notice the Pipeline Tree, there is no connection. You must ensure that these block are attached; attaching block can be done by dragging.
> ![Pipeline Tree - Attached](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/mage%20-%20pipeline%20tree%20connection.PNG)

Now that we successfully set up the import and transform the data. We will now need to write it to GCS

Step 4: Add **Data exporter** Block > ***Python*** > ***Google Cloud Storage***. Rename it as `taxi_to_gcs_parquet`

Step 5: Modification of variables
- bucket_name = 'your_bucket_name'
- object_key = 'nyc_taxi_data.parquet'

Step 6: Click the **Execute with all upstream blocks**. 

After executing all the upstream blocks, refresh the Google Cloud Storage page, we should be able to see that there is a new bucket that has been uploaded.

![GCS NYC Taxi Parquet](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/gcs%20-%20nyc_taxi-parquet.PNG)

#### Partitioning the Data
Partitioning is a method used to divide data into smaller, more manageable chunks. This is particularly helpful when dealing with large datasets that can't be stored in a single file. In these situations, it's necessary to split the dataset into multiple files, often based on specific rows or characteristics. Partitioning by date is an effective approach for the taxi dataset as it evenly distributes the rides and offers a convenient way to query the data based on date.

Step 1: We will have to add another data exporter block > Python > Generic (no template). Rename it to taxi_to_gcs_partitioned_parquet.

Step 2: See the Pipeline Tree, the connection of blocks is not what we want. We want to execute the block parallel to the taxi_to_gcs_parquet.

> This is the automatically connection when we add another block.
>
> ![GCS Parquet Pipeline Tree](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/mage%20-%20test_gcs_partitioned_parquet%20block.PNG)

- To correct the connection, click the connection line that connected to taxi_to_gcs_parquet and taxi_to_gcs_partitioned_parquet then remove the connection. Then add the connection directly from the transformer block to the taxi_to_gcs_partitioned_parquet block. Now, we established connection and can be executed parallel instead of series. Here's what it should look like:

>![GCS Parquet Parallel Tree](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/mage%20-%20test_gcs_partitioned_parquet%20parallel.PNG)

Step 3: We will manually add credentials and use [pyarrow](https://arrow.apache.org/docs/python/filesystems.html) library to partition the dataset. 

> PyArrow is a Python library designed to handle large datasets efficiently, particularly for working with data in memory. It is part of the Apache Arrow project, which provides a standard for representing columnar data in memory to enable fast analytics and interoperability across different systems.
> PyArrow can help handle the chunking logic needed to partition data, especially when working with large datasets and file formats like Parquet. While PyArrow itself doesn't automatically partition data during writes, you can easily combine it with logic in Python to split the data into chunks and write each chunk to a separate file or partition.

```python
import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# Set the environment variable to the locationn
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/your-google-credentials.json"

# Define your bucket_name, project_id and table_name
bucket_name = 'mage-zoomcamp-week-2-090924'
project_id = 'project-id'

table_name = "nyc_taxi_data"

# This root_path represent the location of a dataset within a cloud storage bucket
root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data(data, *args, **kwargs):
    # Define the column to partition on
    # This line changes the tpep_pickup_datetime column from a datetime to just a date (removes time information), which will be used later for partitioning the data by day.
    data['tpep_pickup_datetime'] = data['tpep_pickup_datetime'].dt.date

    # Converts the Pandas DataFrame to a PyArrow Table to work with Arrow-compatible tools and formats, like Parquet.
    table = pa.Table.from_pandas(data)

    # Creates a connection to Google Cloud Storage using PyArrow’s file system interface for GCS.
    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['tpep_pickup_datetime'],
        filesystem=gcs
    )

```

Here's the code breakdown for `pq.write_to_dataset`:
- **table**: The data is written in the Parquet format.
- **root_path=root_path**: The root_path is where the partitioned data will be stored in GCS.
- **partition_cols**=['tpep_pickup_datetime']: The data will be partitioned by the tpep_pickup_datetime column, so the dataset will be split into directories based on this date.
- **filesystem**=gcs: This writes the data to Google Cloud Storage.

After executing the last block, it will upload a folder named ny_taxi_data/ in the GCS bucket.
> ![NYC Taxi Data Folder](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/gcs%20-%20nyc_taxi_data_folder.PNG)

### ETL: GCS to BigQuery
> Video Source: [DE Zoomcamp - ETL: GCS to BigQuery](https://www.youtube.com/watch?v=JKp_uzM-XsM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=26)

In this section, we will learn to load the data that we have in GCS bucket and write it to BigQiery, an OLAP database. 

Before we get into it, please make sure that the location of your bucket and BigQuery are the same. As well as the GOOGLE_LOCATION in io_config.yaml to avoid any issues. Another thing is to create a dataset in BigQuery - this is very simple to create. Go to your Google Console > BigQuery > Create dataset. You can name it as nyc_taxi_data or whatever you want.

#### Loading the Data from GCS
Step 1: Create a new pipeline > Standard (batch). Rename it as gcs_to_bigquery.

Step 2: Add a data loader block > Python > Google Cloud Storage. Rename it as load_taxi_gcs

Step 3: We will use the unpartitioned paquet file that we have in our GCS bucket for this section. But if you want to use the partitioned files, you need to use pyarrow just what we did last time.

Step 4: Modify the necessary information:
- bucket_name: 'your_bucket_name'
- object_key: 'ny_taxi_data.parquet'

Step 5: Delete the @test assertion. 

```python
@data_loader
def load_from_google_cloud_storage(*args, **kwargs):

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'your_bucket_name'
    object_key = 'nyc_taxi_data.parquet'

    return GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    )
```

#### Transform the Data for BigQuery
We have successfully import the dataset, we will now transform the data.

Step 1: Add Transformer block > Python > Generic (no template). Rename it as transformed_staged_data.

Step 2: We will standardized the column names to lower case with no spaces.

```python
@transformer
def transform(data, *args, **kwargs):
    data.columns = (data.columns
                    .str.replace(' ', '_')
                    .str.lower()
    )

    return data
```

Step 3: We will also delete the assertion below the decorator @transformer.

Step 4: Run the transformer block.

#### Exporting the Data to BigQuery
We have successfully transformed the data, we will now export the data to BigQuery.

Step 1: Add a new Data exporter block > SQL. Rename it as write_taxi_to_bigquery.

Step 2: Modify the necessary credentials.
- Connection: BigQuery
- Profile: Default
- Schema: nyc_taxi_data (Note: I've mentioned that we need to manualy create a database in Google Bigquery- whatever you named it you must input the same name here)
- Table: yellow_taxi_data (Note: You can also set any name- depends on you)

Step 3: The transform block will return a dataframe. What’s great about Mage is that you can directly select from that dataframe.

> ![Write Data to BigQuery](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/mage%20-%20write_taxi_to_bigquery.PNG)

#### Triggering Events: Scheduling
We have successfully exported the data to BigQuery, we will now trigger events to schedule the data to execute. 

- In Mage, "trigger scheduling" allows you to set up automated execution of your workflows or tasks based on a defined schedule. This means you can specify when and how frequently a particular workflow should run without manual intervention.

- For example, you might schedule a workflow to run daily at a specific time, weekly, or at any other interval you choose. This helps in automating repetitive tasks and ensuring that data processing or other workflows happen consistently according to your requirements.

> ![Scheduling](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/mage%20-%20scheduling.PNG)