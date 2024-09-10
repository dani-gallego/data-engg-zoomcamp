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

[!NOTE]
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

Step 1: Add Transformer Block and then add **Python** > ***Generic (no template)***

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

