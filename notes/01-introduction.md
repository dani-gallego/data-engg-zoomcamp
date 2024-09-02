# Week 1: Introduction

### Table of Contents
- [Introduction to Data Engineering](#introduction-to-data-engineering)
  - [Architecture](#architecture)
  - [Data Pipelines](#data-pipelines)
- [Docker and Postgres](#docker-and-postgres)
  - [Docker Image](#docker-image)
  - [Creating a Dockerfile and custom pipeline with the Docker](#creating-a-docker-file-and-custom-pipeline-with-the-docker)
  - [Running Postgres in Docker](#running-postgres-in-docker)
    - [What is Airflow?](#what-is-airflow)
    - [For Windows](#for-windows)
    - [For Linux and MacOS](#for-linux-and-macos)
  - [Ingesting Data to Postgres with Python](#ingesting-data-to-postgres-with-python)
  - [Connecting pgAdmin and Postgres](#connecting-pgadmin-and-postgres)
    - [pgAdmin](#pgadmin)
    - [Linking pgAdmin container and Postgres container](#linking-pgadmin-container-and-postgres-container)
    - [Creating a server in pgAdmin](#creating-a-server-in-pgadmin)
  - [Using Ingestion Script with Docker](#using-ingestion-script-with-docker)
  - [Dockering Ingestion Script](#dockerizing-ingestion-script)
  - [Running Postgres and pgAdmin with Docker Compose](#running-postgres-and-pgadmin-with-docker-compose)
  - [SQL Refresher](#sql-refresher)
    - [SQL Command Types](#sql-command-types)
    - [SQL Queries](#sql-queries)
  - [Terraform and Google Cloud Platform ](#terraform-and-google-cloud-platform)
    - [GCP Initial Setup](#gcp-initial-setup)
    - [GCP Setup for Access](#gcp-setup-for-access)
    - [Terraform Basic](#terraform-basics)
    - [Creating GCP Infrastructure with Terraform](#creating-gcp-infrastructure-with-terraform)
    



# Introduction to Data Engineering
Data engineering involves designing, building, and maintaining systems that collect, store, and analyze large volumes of data.

## Architecture
In this course, we will be re-creating the following architecture:
![Architecture Diagram](https://github.com/DataTalksClub/data-engineering-zoomcamp/raw/main/images/architecture/arch_v3_workshops.jpg)

Throughout the course, we will be using the NYC Taxi Record Dataset: [NYC TLC Data](https://github.com/DataTalksClub/nyc-tlc-data)

## Data Pipelines
A data pipeline is a series of processes that move data from one or more sources to a destination, where it can be stored, analyzed, or used in applications. 

The pipeline typically involves steps like data extraction (from databases, APIs, or files), data transformation (cleaning, filtering, or aggregating the data), and data loading (storing the data in a database, data warehouse, or data lake). 

Data pipelines can handle batch processing, where data is processed in chunks at scheduled times, or stream processing, where data is processed in real-time as it arrives.

![Data Pipelines](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/data-pipelines.PNG)


# Docker and Postgres
Docker is a platform that allows developers to package applications and their dependencies into containers. These containers are lightweight, portable, and can run consistently across different environments, ensuring that the application behaves the same way on any system. 

## Docker Image
A Docker image is a lightweight, standalone, and executable package that includes everything needed to run a piece of software: the code, runtime, libraries, environment variables, and configuration files. Essentially, its a blueprint for creating Docker containers. When you start a container, it runs from a Docker image, ensuring consistency across different environments.

**Advantages of Docker**

Docker provides the following advantages:
- Reproducibility: Docker images can be shared and run in various environments, ensuring that the application behaves the same way everywhere it is deployed.
- Isolation: Containers ensure that applications and their dependencies are isolated, minimizing conflicts between different software versions on a host machine.
- Local Testing/Experimentation: Docker aids in setting up local experiments and integration tests, allowing data engineers to validate their data pipelines effectively before deployment.
- Inegration Tests (CI.CD)
- Running pipelines on the cloud platform (AWS, Google Cloud, Azure)
- Spark
- Serverless (AWS Lambda, Google functions)

## Creating a docker file and custom pipeline with the Docker
> Video Source: [DE Zoomcamp - Introduction to Docker](https://www.youtube.com/watch?v=EYNwNlOrpr0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=5)

Note: By doing this custom pipeline, you must change the directory where you want to create a pipeline using git bash.

To create a custom pipeline, we will create a 'pipeline.py'. It's a python script that receives an argument and then prints it.

```python
# We will import and use pandas library as well as sys module
import sys
import pandas as pd

# Print the arguments
print(sys.argv)

# The first element; sys.argv[0] is the name of the script
# Subsequent elements; sys.argv[1] and etc., are the arguments passed to the script
day = sys.argv[1]

# You can add some code stuff with pandas here

# Print a sentence with the argument
print(f'Job finished successfully for day = {day}.')
```

Now, let's create a simple 'Dockerfile' that we can specify all the intructions of what we want to run in order to create a new image in the docker.

```dockerfile
# For an example, we want to use base image from python environment
FROM python:3.12

# Run command to install pandas
RUN pip install pandas

# Setting up the working directory inside the container
WORKDIR /app

# Below is to copy the scipt to the container
# 1st name will be the source file
# 2nd name will be the destination
COPY pipeline.py pipeline.py

# To define what to do first when the container runs
# In this simple custom dockerfile, we will run the script
ENTRYPOINT [ "python", "pipeline.py" ]
```

Let's build the image in Docker

```ssh
docker build -t test:pandas .
```

* The image will be named as `test` and its tag will be `pandas`.

After we build the container, we can now run it. For an example, we will run it for specific day.
```ssh
docker run -it test:pandas 2024-08-19
```

Expected output:
```
['pipeline.py', '2024-08-19']
Job finished successfully for day 2024-08-19.
``` 
You should be able to get the same output when you ran the pipeline script.

>Note: As mentioned above, these custom simple script must be in the same directory; Dockerfile and pipeline.py

## Running Postgres in Docker
> Video Source: [DE Zoomcamp - Ingesting NY Taxi Data to Postgres](https://www.youtube.com/watch?v=2JM-ziJt0WI&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=5)

### What is Airflow?
Airflow is a platform to programmatically schedule and monitor workflows. It uses Postgres internally hence for simpler tests we can use PostgreSQL directly. 

In this section, we will be using Airflow. And we can run a containerized version of PostgreSQL using Docker without needing to install PostgreSQL directly on our system.

We will create a folder `ny_taxi_postgres_data`, below are the code syntax in order to run the container.

### For Windows
```bash
winpty docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v //c/Users/.../docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

### For Linux and MacOS
```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

Below are the explanation of what are the syntax inside the base script command above:
- `docker run -it` is the command to run the container in interactive mode.
- `-e POSTGRES_USER="root"`: This is setting the username for the Postgres.
- `-e POSTGRES_PASSWORD="root"`: This is setting the password for the Postgres.
- `-e POSTGRES_DB="ny_taxi"`: This is setting the database name for the database.
- `-v` points to the volume directory.
- `-p 5432:5432` maps the port 5432 on the host machine.
- `postgres:13` is the image name and version of the Postgres image.

> **Troubleshooting**: If the ny_taxi_postgres_data is empty, you may qoute the absolute path in the -v parameter. It will solve the issue and all the files will be visible in the VSCode ny_taxi folder.

```bash
"C:\Users\...\docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data"
```

Afterwards, the container should be running. We can access the database with [pgcli](https://www.pgcli.com/) by the following command using git bash.

> Before executing the command below, you must install the pgcli `pip install pgcli`

```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

* `-h` is the host name, since we are running locally we have used `localhost`.
* `-p` is the port number, we have used `5432`. Which indicated when we created the container.
* `-u` is the username, we have used `root`.
* `-d` is the database name, we have used `ny_taxi`.

This will open a command line interface to interact with the Postgres database. You can execute SQL queries.

> **Troubleshooting**: In case when running the command above and you are stuck on password prompt for postgress. Use winpty:
```bash
winpty pgcli -h localhost -p 5432 -u root -d ny_taxi
```

## Ingesting data to Postgres with Python

In this section, we will now create a Jupyter Notebook named as `upload-data.ipynb` file which we will use to read the dataset and export it to Postgres.

We will use the data from what we have mentioned in [Architecture](#architecture). Specifically, we will use the [yellow_tripdata_2021-01](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz). [Here](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf) is the dictionary to understand each field.

You may check the completed `upload-data.ipynb` by clicking this [link](docker_sql\upload-data.ipynb). This should be in the same directory with CSV file and the `ny_taxi_postgres_data` subdirectory.

## Connecting pgAdmin and Postgres
> Video Source: [DE - Connecting pgAdmin and Postgres](https://www.youtube.com/watch?v=hCAIVe9N0ow&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=8)

### pgAdmin
Although, both **pgAdmin** and **pgcli** are tools for interacting with PostgreSQL databases, but they serve different puposes and cater to different user preferences. Here is the few comparison between the two:
- **pgAdmin** is a graphical user interface (GUI) tool that allows you to visually manage your PostgreSQL databases.
- **pgcli** is a command-line interface (CLI) tool with focus on simplicity and provides command-line environment where you can execute SQL queries directly.

It's not convenient to use **pgcli** for data exploration and querying hence we will use **pgAdmin** that makes more convenient to access and manage the database. 

We can install the **pgAdmin** but since we already have docker we actually don't need to, what we can do is to pull a command for a docker image that has **pgAdmin** [container](https://hub.docker.com/r/dpage/pgadmin4/). However, it doesn't shows the environment variable that are needed so please follow the bash command below that we need to execute to run pgAdmin container in Docker.

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```

After it was successfully executed, you can open your browser and navigate to `localhost:8080`. Now, we have pgAdmin created through Docker. Please use the credentials above to login to the pgAdmin.

### Linking pgAdmin container and Postgres container
pgAdmin and Postgres are in different container, in this case, both containers must be in the same virtual network in order to connect them we will be using `network`.

Let's create a virtual Docker network called [`pg-network`](https://docs.docker.com/reference/cli/docker/network/create/).

```bash
docker network create pg-network
```

Now, we will be re-running the Postgres container with container network name.

```bash
winpty docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v //c/Users/madan/OneDrive/Documents/GitHub/data-engg-zoomcamp/01-introduction/docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13
```

Afterwards, we will also re-run the pgAdmin container and to specify the network and container name.

```bash
winpty docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```
**Important key notes:**
- The container needs 2 credentials: login email and password - we indicated the login email and password `admin@admin.com` and `root`.
- pgAdmin is a web tool application which by default port is 80; Support mapping so we map a port on our host maching port as 8080.
- We have to specify the network and container name just like what we did in Postgres container.
- The actual image name is `dpage/pgadmin4`.

We've done linking the pgAdmin container and POstgres container, we should be able to re-load pgAdmin on a web browser to `localhost:8080` as mentioned above. Please use the login email and password to login to the pgAdmin.

### Creating a server in pgAdmin
After successfully logged in to the `localhost:8080`, let's now create a server.

Right click on *Servers* on the left sidebar, select *Register* and then **Server...**.

![Creating pgAdmin Server](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/creating-pgadmin-server.PNG)

It will show server configuration. Under *General* section, promptly input a server name. For an example, `Docker Localhost`.

![General section - server configuration](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/pgadmin-server-configuration-01.PNG)

Furthermore, under *Connection* section add the same host name that is indicated when the container was created. Since we have used the name as `pg-database`, we will use that. As for the username and password would be ***root*** as an example.

![Connection section - server configuration](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/pgadmin-server-configuration-02.PNG)

Click the *Save* button. We are now connected to the database.

## Using ingestion script with Docker
> Video Source: [DE Zoomcamp - Dockerizing the Ingestion Script](https://www.youtube.com/watch?v=B1WwATwf-vY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=8)

>[!NOTE]
>
> There are a few parts that have been modified to ensure proper execution, as I encountered some problems. This is optional if you face the same issues. Otherwise, you can follow the instructions and code provided in the [video source](https://www.youtube.com/watch?v=B1WwATwf-vY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=8).

For this section, we will now turn the Jupyter Notebook that we created into regular Python script and use Docker to run it.

We can actually export the `ipynb` file to `py` in bash terminal.
```bash
jupyter nbconvert --to=script upload-data.ipynb
```

We have to clean the script and remove the unnecessary command. The converted file will be named as `ingest-data.py` and add a few configurations.

We will be using [argparse](https://docs.python.org/3/library/argparse.html) to execute the following command line arguments:
- Username
- Password
- Hostname
- Database name
- Table name
- Port number
- URL for CSV file

We have also need to edit the `engine` that we created for connecting to Postgres environment so we can pass the parameters mentioned above. Instead of using the previous one:
```python
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')'
```
The engine command should look like this:
```python
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
```
You can check the complete script from [ingest-data.py](ingest_data.py).

> [!NOTE]
>
> I have encounter a problem when getting the url using the python script provided from [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/2_docker_sql/ingest_data.py), so there's an alternative method that I have used to get the URL and download it locally using the [request library](https://pypi.org/project/requests).
>
> If you don't encounter any problem using [this](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/2_docker_sql/ingest_data.py) script, you can ignore my modified script.

To test the script, we'll need to drop the table we created earlier. In pgAdmin, go to the sidebar and navigate through Servers > Docker localhost > Databases > ny_taxi > Schemas > public > Tables > yellow_taxi_data. Right-click on the yellow_taxi_data table and choose Query Tool. Then, enter the following command:

```SQL
DROP TABLE yellow_taxi_data;
```

Refresh the **Tables** and it should be empty since we have drop the table. Now, let's test the python script using the command below and enter this to the bash terminal:
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```
Please note that the `host = localhost` is not connected to the Postgres environment. We will have to change `host` later so we are able to connect it to the same network as Postgres and pgAdmin container. And we also changed the table name from `yellow_taxi_data` to `yellow_taxi_trips`.

When the python script is executed successfully, refresh the *Tables* in pgAdmin and we will find that we have new table name `yellow_taxi_trips`. You may also check and run SQL query using the SQL statment below:
```SQL
SELECT
  COUNT(1)
FROM
  yellow_taxi_trips;
```
**Expected Output:** 1,369,765 rows.

## Dockerizing Ingestion Script
Now that we have our ingestion script working, let's create a Docker image for it.

Go to your `Dockerfile`, we will have to modify it in order to include `ingest_data.py`.

```dockerfile
FROM python:3.12

# We need to install wget to download the csv file
RUN apt-get install wget
# psycopg2 is a postgres db adapter for python: sqlalchemy needs it
RUN pip install pandas sqlalchemy psycopg2
# [Optional] Installing requests library due to modified script in ingest_data.py
RUN pip install requests

WORKDIR /app
COPY ingest_data.py ingest_data.py 

ENTRYPOINT [ "python", "ingest_data.py" ]
```

We have to build the image using the bash command below:
```bash
docker build -t taxi_ingest:v001 .
```

Instead of using python, we will use the `docker run` to run it. As I have mentioned earlier, we will have to change the `host` and connect it to the same network as Postgres and pgAdmin container.

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```
- You can drop the table in `pgAdmin` browser beforehand in order to see if the script will be automatically replace the pre-existing table since we have run the bash command above.

## Running Postgres and pgAdmin with Docker-compose
> Video Source: [DE Zoomcamp - Running Postgres and pgAdmin with Docker-Compose](https://www.youtube.com/watch?v=hKI6PkPhpa0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=9)

## What is Docker Compose?
[Docker Compose](https://docs.docker.com/compose/) allows you to define and manage multi-container Docker applications using a YAML file. It streamlines the setup and orchestration of services, networks, and volumes, enabling you to start and manage your application with a few straightforward commands.

By using this we don't need to execute `docker run` commands separately as we have used previously. Here's the `docker-compose.yaml` file for running the Postgres and pgAdmin container.

Before running the yaml command, please stop the container with postgres and pgAdmin. To check if there are no containers running in Docker, use the command below.

```bash
docker ps
```

Now, let's create the `docker-compose.yaml` file.

```yaml
services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    volumes:
      - "./ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    volumes:
      - "./pgadmin:/var/lib/pgadmin/"
    ports:
      - "8080:80"
```
- As you may notice, we don't need to actually specify a network name as we did previously because `docker-compose` allows every single container (`services`) to run within the same network.
- We've included a volume for pgAdmin to save its settings, so you won't need to repeatedly recreate the connection to Postgres each time you restart the container. Be sure to create a 'pgadmin' directory in your working folder where you run 'docker-compose'.

We can run Docker compose by running the following command in the same directory where `docker-compose.yaml` located. 

```bash
docker-compose up
```

It will create all of the environment variables for both postgres database and pgAdmin. Once it was executed successfully, you have to reload the pgAdmin browser `localhost:8080` and re-create the server from this [instruction](#creating-a-server-in-pgadmin).

Furthermore, you can use `Ctrl + C` to shutdown the containers. But the proper way to do this is using this command.

```bash
docker-compose down
```

And if you want to run the container again, we can use the [detached mode](https://docs.docker.com/language/golang/run-containers/#:~:text=Run%20in%20detached%20mode,-This%20is%20great&text=Docker%20can%20run%20your%20container,you%20to%20the%20terminal%20prompt.) using this command:

```bash
docker-compose up -d
```

[<u> [Go to Top]</u>](#table-of-contents)


## SQL Refresher
> Video Source: [SQL Refresher](https://www.youtube.com/watch?v=QEcps_iskgg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=11)

We will have to work on 2 tables; `yellow_data_trips` and `zones` in this section. Before we proceed to the SQL query examples. We have to establish a new table called `zones` and added to the Postgres and pgAdmin container.

Please check the [upload-data.ipnyb](01-introduction/docker_sql/upload-data.ipynb) to continue to work on table `zones`.

I've created a new dockerfile named `Dockerfile-2` and `ingest_data_2.py` in order to connect the `taxi_zone_lookup.csv` to the same network as Postgres and pgAdmin container. 

```dockerfile
FROM python:3.12

# We need to install wget to download the csv file
RUN apt-get install wget
# psycopg2 is a postgres db adapter for python: sqlalchemy needs it
RUN pip install pandas sqlalchemy psycopg2
# [Optional] Installing requests library due to modified script in ingest_data.py
RUN pip install requests

WORKDIR /app
COPY ingest_data_2.py ingest_data_2.py 

ENTRYPOINT [ "python", "ingest_data_2.py" ]
```

We need to build a new version of taxi_ingest container.
```bash
docker build -t taxi_ingest:v002 -f Dockerfile-2 .
```

Before doing this there must be no container running, use `docker ps` to check. Then we can run the new container using the following command.

```bash
URL1="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
URL2=https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv

docker run -it \
    --network=pg-network \
    taxi_ingest:v002 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name_1=yellow_taxi_trips \
    --table_name_2=zones \
    --url1=${URL1} \
    --url2=${URL2}
```

We will be using the same `docker-compose.yaml`. Hence, we can use this [instruction](#running-postgres-and-pgadmin-with-docker-compose) like we did before.

Before proceeding with SQL queries, we will briefly tackle the SQL Command Types. However you can skip this if you have knowledge about SQL Command Types by clicking [this](#basic-retrieval-of-taxi-trips). 

### SQL Command Types
#### Data Definition Language (DDL)
DDL commands are used to define and manage database structure. They affect the database schema.

  - CREATE: Creates a new table, database, index, or other database objects.
   - Example: CREATE TABLE students (id INT, name VARCHAR(100));
  - ALTER: Modifies an existing database object like a table.
    - Example: ALTER TABLE students ADD COLUMN age INT;
  - DROP: Deletes an existing database object like a table or database.
    - Example: DROP TABLE students;
  - TRUNCATE: Removes all records from a table, but the table - structure remains.
    - Example: TRUNCATE TABLE students;

#### Data Manipulation Language (DML)
DML commands are used for managing data within database tables.

  - SELECT: Retrieves data from the database.
    - Example: SELECT * FROM students;
  - INSERT: Adds new data into a table.
    - Example: INSERT INTO students (id, name, age) VALUES (1, 'John Doe', 20);
  - UPDATE: Modifies existing data within a table.
    - Example: UPDATE students SET age = 21 WHERE id = 1;
  - DELETE: Removes data from a table.
    - Example: DELETE FROM students WHERE id = 1;

#### Data Control Language (DCL)
DCL commands manage permissions and access to the database.

  - GRANT: Provides specific user permissions.
    - Example: GRANT SELECT ON students TO user_name;
  - REVOKE: Removes specific user permissions.
    - Example: REVOKE SELECT ON students FROM user_name;

#### Transaction Control Language (TCL)
TCL commands manage transactions within the database, ensuring data integrity.

  - COMMIT: Saves all changes made in the current transaction
    - Example: COMMIT;
  - ROLLBACK: Reverts changes made in the current transaction.
    - Example: ROLLBACK;
  - SAVEPOINT: Sets a savepoint within a transaction to which you can rollback.
    - Example: SAVEPOINT savepoint_name;
  - RELEASE SAVEPOINT: Removes a savepoint, making it no longer available for rollback.
    - Example: RELEASE SAVEPOINT savepoint_name;
  - SET TRANSACTION: Defines the transaction properties such as isolation level.
    - Example: SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

#### Data Query Language (DQL)
DQL primarily consists of the SELECT command, used to query data from the database.

  - SELECT: Used to query data from a table or view.
    - Example: SELECT name, age FROM students WHERE age > 20;

### SQL Queries
These SQL queries below is to execute retrieval and analyze data from the `taxi_yellow_trips` table and `zone` table.

#### Basic Retrieval of Taxi Trips
```SQL
SELECT 
  *
FROM
  yellow_taxi_trips
LIMIT 100;
```
- This query retrieves the first 100 rows of all columns from the yellow_taxi_trips table.

#### Joining Trips with Pickup and Dropoff Zones
```SQL
SELECT
  *
FROM
  yellow_taxi_trips t,
  zones zpu,
  zones zdo
WHERE
  t."PULocationID" = zpu."LocationID" AND
  t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```
- This query retrieves all columns from the yellow_taxi_trips table and joins it with the zones table twice: once for the pickup location (zpu) and once for the dropoff location (zdo). The first 100 matching rows are returned.
- We gave aliases (temporary name) to the `yellow_taxi_trips` and `zones` to make it easier to reference.
- In Postgres, we have to use the double qoutes (`""`) if the column names composed of capital letter.

#### [Implicit Joins] Retrieving Specific Columns with Concatenated Zone Information
```SQL
SELECT 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zpu."Borough", ' / ', zpu."Zone") AS pickup_loc,
	CONCAT(zdo."Borough", ' / ', zdo."Zone") AS dropoff_loc
FROM 
	yellow_taxi_trips t,
	zones zpu,
	zones zdo
WHERE
	t."PULocationID" = zpu."LocationID" AND
	t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```
- This query selects specific columns, including pickup and dropoff times, the total fare amount, and concatenated location details for both pickup and dropoff zones. The first 100 matching rows are returned.
- We used the `CONCAT` function to combine the borough and zone names into a single string.
  - We used the `AS` keyword to give an alias to the concatenated string.
- We specifically used `implicit joins` which is the old-style of join syntax. This approach involves listing multiple tables in the `FROM` clause and using `WHERE` clause to specify the join conditions.
  - Advantages: 
    1. Simple for very basic queries
  - Disadvantages: 
    1. Less readable and more error-prone for complex queries.
    2. No explicit indication of join types which can lead to confusion.

#### [Explicit Joins] Refined Query Using JOIN Syntax
```SQL
SELECT 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zpu."Borough", ' / ', zpu."Zone") AS pickup_loc,
	CONCAT(zdo."Borough", ' / ', zdo."Zone") AS dropoff_loc
FROM 
	yellow_taxi_trips t 
	JOIN zones zpu 
		ON t."PULocationID" = zpu."LocationID" 
	JOIN zones zdo 
		ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```
- Similar to the previous query, this one uses explicit JOIN syntax to combine the yellow_taxi_trips table with the zones table for both pickup and dropoff locations, returning the first 100 rows. This syntax is more modern and clear in expressing the relationships between table.
- We have different type of JOINS, but in this one, we used INNER JOIN to return records with matching values in both values.
- Besides implicit joins, we have used explicit joins for the SQL statement above. Explicit Joins approach is more modern and preferred for it's clarity and readability.
  - Advantages:
    1. Clear and explicit definition of the join type.
    2. Improved readability and maintainability of queries
    3. Better suited for complex queries and multiple joins
  - Disadvantages:
    1. Slightly more verbose than implicit joins.

For further understanding about JOIN, learn more from [here](https://www.atlassian.com/data/sql/sql-join-types-explained-visually).

These SQL queries below used to analyzed and manipulate data in the `yellow_taxi_trips` and `zones` table.

#### Find Records with Null Pickup Location
```SQL
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    "PULocationID",
    "DOLocationID"
FROM
    yellow_taxi_trips t
WHERE
    "PULocationID" is NULL
LIMIT 100;
```

#### Find Records with Null Dropoff Location
```SQL
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    "PULocationID",
    "DOLocationID"
FROM
    yellow_taxi_trips t
WHERE
    "DOLocationID" NOT IN (
        SELECT "LocationID" FROM zones
    )
LIMIT 100;
```
- This queries retrieves the first 100 records where the PULocationID (Pickup Location ID) is NULL as wells as the DOLocationID.
- It must be return to an empty list if you have not modified the original tables.


#### Delete Specific Zone
```SQL
DELETE FROM zones WHERE "LocationID" = 142;
```
- This query deletes all the rows in the `zones` table with `LocationID` = 142.
- Be careful when running this query as it will permanently delete the data.
- In order to test the NULL syntax that we have used previously, the result must return list of rows with `PULocationID` of 142.

#### JOIN `yellow_data_trips` with `zones` for Pickup and Dropoff Location
```SQL
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", '/', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", '/', zdo."Zone") AS "dropoff_loc"
FROM
    yellow_taxi_trips t LEFT JOIN zones zpu
        ON t."PULocationID" = zpu."LocationID"
    LEFT JOIN zones zdo
        ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```
- This query retrieves `yellow_taxi_trips` data, along with the concatenated borough and `zone` names for both pickup and dropoff locations, using left joins with the zones table. The first 100 rows are returned.
- Performs a LEFT JOIN between the `yellow_taxi_trips` table (t) and the `zones` table (zpu), where t."PULocationID" matches zpu."LocationID". Performs another LEFT JOIN, this time between the `yellow_taxi_trips` table (t) and the `zones` table (zdo), where t."DOLocationID" matches zdo."LocationID".
  - Left Table: The table listed before the LEFT JOIN keyword, in this case, `yellow_taxi_trips`.
  - Right Table: The table listed after the LEFT JOIN keyword, in this case, `zones`.
- If a row in the `yellow_taxi_trips table` has no corresponding match in the `zones` table for either the pickup or dropoff location, the query will still include that row from `yellow_taxi_trips`, but with NULL values for the concatenated location fields (pickup_loc and dropoff_loc).

#### Query to Truncate Date to Day
```SQL
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    DATE_TRUNC('DAY', tpep_pickup_datetime),
    total_amount
FROM
    yellow_taxi_trips t
LIMIT 100;
```
- This query selects the pickup and dropoff datetime, truncates the pickup datetime to the start of the day, and includes the total amount.
  - `DATE_TRUNC('DAY', tpep_pickup_datetime)`: Truncates the tpep_pickup_datetime to the day level, effectively removing the time part.
  - `LIMIT 100`: Limits the results to the first 100 rows.

#### Query to Cast Date to Day
```SQL
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    CAST(tpep_pickup_datetime AS DATE) as "day",
    total_amount
FROM
    yellow_taxi_trips t
LIMIT 100;
```
- This query selects the pickup and dropoff datetime, casts the pickup datetime to just the date (removing the time part), and includes the total amount.
  - `CAST(tpep_pickup_datetime AS DATE) as "day"`: Converts tpep_pickup_datetime to a date-only format and labels it as "day".

#### Query to Aggregate by Day
```SQL
SELECT
    CAST(tpep_pickup_datetime AS DATE) as "day",
    COUNT(1) as "count",
    MAX(total_amount),
    MAX(passenger_count)
FROM
    yellow_taxi_trips t
GROUP BY
    CAST(tpep_pickup_datetime AS DATE)
ORDER BY "count" DESC;
```
- This query groups the data by day, counts the number of `yellow_taxi_trips` for each day, and retrieves the maximum total amount and maximum passenger count for each day.
  - `COUNT(1) as "count"`: Counts the number of records for each day.
  - `MAX(total_amount)`: Finds the maximum total amount for each day.
  - `MAX(passenger_count)`: Finds the maximum passenger count for each day.
  - `GROUP BY CAST(tpep_pickup_datetime AS DATE)`: Groups the results by the date.
  - `ORDER BY "count" DESC`: Orders the results by the count of `yellow_taxi_trips` in descending order.

#### Query to Aggregate by Day and Dropoff Location ID
```SQL
SELECT
    CAST(tpep_pickup_datetime AS DATE) as "day",
    "DOLocationID",
    COUNT(1) as "count",
    MAX(total_amount),
    MAX(passenger_count)
FROM
    yellow_taxi_trips t
GROUP BY
    1, 2
ORDER BY "count" DESC;
```
- This query groups the data by day and dropoff location ID, counts the number of `yellow_taxi_trips` for each combination, and retrieves the maximum total amount and passenger count for each combination.
  - `GROUP BY 1, 2`: Groups by the first and second columns in the SELECT clause, which are the day and DOLocationID.

#### Query to Aggregate by Day and Dropoff Location ID with Sorted Output
```SQL
SELECT
    CAST(tpep_pickup_datetime AS DATE) as "day",
    "DOLocationID",
    COUNT(1) as "count",
    MAX(total_amount),
    MAX(passenger_count)
FROM
    yellow_taxi_trips t
GROUP BY
    1, 2
ORDER BY
    "day" ASC,
    "DOLocationID" ASC;
```
- This query is similar to the previous one but sorts the results first by day in ascending order and then by dropoff location ID in ascending order.
  - `ORDER BY "day" ASC, "DOLocationID" ASC`: Orders the results first by the day in ascending order, and then by DOLocationID in ascending order.

[<u> [Go to Top]</u>](#table-of-contents)

# Terraform and Google Cloud Platform
> Video Source: [DE Zoomcamp - Terraform Primer](https://www.youtube.com/watch?v=s2bOYDCKl_M&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=12)

[Terraform](https://www.terraform.io/), by HashiCorp, is an Infrastructure as Code tool that simplifies cloud and on-prem resources management.

#### Key Insights

1. `Conceptual Foundation`: Terraform draws inspiration from the idea of terraforming, transforming inhospitable environments into livable spaces, paralleling how it modifies cloud infrastructure. This analogy emphasizes Terraform’s role in creating functional digital environments.

2. `Infrastructure as Code`: By using human-readable configuration files, Terraform allows users to define, version, and share infrastructure setups easily, making it accessible for collaboration and management. This shifts infrastructure management towards software development practices.

3. `Collaboration Benefits`: The ability to push Terraform files to repositories like GitHub fosters teamwork, enabling multiple contributors to review and enhance configurations, thus improving overall project quality.

4. `Reproducibility and Flexibility`: Terraform’s design allows users to replicate infrastructure setups in different environments (Dev, Prod), making it easier to test changes without affecting live systems, enhancing operational efficiency.

5. `Cost Awareness`: Users must be cautious when deploying resources, as costs can escalate quickly. Understanding the implications of infrastructure deployment is crucial in cloud environments.

6. `Limited Scope`: Terraform is not a software deployment tool or resource manager for external configurations, which helps clarify its purpose and avoid misuse in broader DevOps practices.

7. `Essential Commands`: Mastering key Terraform commands like init, plan, apply, and destroy is vital for effective infrastructure management and automation, streamlining workflows in cloud environments.

Throughout the course, we will use [Google Cloud Platform](https://cloud.google.com/?_gl=1*672i6v*_up*MQ..&gclid=Cj0KCQjw_sq2BhCUARIsAIVqmQs00W3mRbsHIk5IM1Pc6c6rEvupW-HyoXPAsnIKuKTtqGE2RdzSR6gaAhFlEALw_wcB&gclsrc=aw.ds&hl=en) as cloud service provider.

## GCP Initial Setup
> Video Source: [DE Zoomcamp - Introduction to Terraform Concepts and GCP Pre-requisites](https://www.youtube.com/watch?v=Hajwnmj0xfQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=8)

- To use `Terraform`, you need the Terraform client and a `GCP` account, with the free account with a certain amount of credits depending on the region.

- A service account in `GCP` is created for services to interact with **cloud resources**, with restricted permissions for security.

- Service accounts are used to grant specific permissions to interact with GCP resources like `Cloud Storage` and `BigQuery`.

- The `Google Cloud SDK (gcloud)` is necessary for local interaction with GCP services, and it can be authenticated using `OAuth`.

- For the tutorial, permissions are kept simple with admin roles, but in production, custom roles with specific permissions are recommended.

- APIs need to be enabled in GCP for services like `IAM` and `BigQuery` to interact with the cloud resources through the local environment.

You can [skip] this part of GCP initial setup, if you already know how to do it.

The following are the steps for GCP account:
1. Create an account on [GCP](https://cloud.google.com/?_gl=1*672i6v*_up*MQ..&gclid=Cj0KCQjw_sq2BhCUARIsAIVqmQs00W3mRbsHIk5IM1Pc6c6rEvupW-HyoXPAsnIKuKTtqGE2RdzSR6gaAhFlEALw_wcB&gclsrc=aw.ds&hl=en). If you are signing up for the first time, you should be able to receive a credit based on your region.
1. Create a new project in the GCP console. Please remember your Project ID.
    1. You will be directed to GCP dashboard, in order to create a new project you have to click the drop down option next to the *Google Cloud Platform*. It will show the project list and click on *New Project*.
    1. Enter the project name, we will use `dtc-de` in this exmaple. Edit the `Project ID` using auto-generated so the ID will be unique for all of GCP. We will leave the orgation as *No organization*. You can now click on *Create*. You will be directed to the project dashboard, however, you have to make sure that `dtc-de` is selected as your project on the drop down option that I've mentioned earlier.
1. Setting up a service account for our project and download the JSON authentication key files.
    1. Go to the *Navigation menu* (three horizontal lines) and if you can't find the IAM & Admin service, click on *View All Products*. Then click the *search button* (it looks like manifying glass) on the top right to search the `IAM and Admin`. Once you've done that, you can click the pin button in order to see it in the *Navigation menu* so it won't be hassle to search it manually.
    1. Go to the *IAM & Admin* > *Service accounts* and click on *Create Service Account*.
    1. Enter the service account name, we will use `dtc-de-user` in this case it doesn't need to be globally unique since it will have the combination to the email project ID. Let's leave all the other configuration as it is. Then we can now click on *CREATE AND CONTINUE*.
    1. Grant the Viewer role (*Basic > Viewer*) to the service account and click on *Continue*.
    1. Click on *Done* to finish the creation of the service account. This step is not something we need for now but this is would be useful if you're setting up production environment and have a multiple users associated to a certain service account.
    1. Once the service account was created, you will see that there is no key ID generated. Click on three dots below *Actions* and navigate until you see the *Manage Keys*.
    1. *Add key* > *Create new key*. Select `JSON` and click *Create*. The file will be downloaded to your computer. Save them to a folder and copy the path location.
1. Download the [GCP SDK](https://cloud.google.com/sdk/docs/downloads-interactive) on Windows for local setup. Follow the instructions to install and connect to your GCP account and project
1. Set the environment variable to point to the auth keys.
    1. Our environment variable name is set as `GOOGLE_APPLICATION_CREDENTIALS`.
    1. The path to json authentication file is the one you've downloaded previously.
    1. You can set it using the following command in your terminal: ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="<path/to.authkeys>.json"
    ```
    1. Refresh the token and verify the authentication with the GCP SDK:
    ```bash
    gcloud auth application-default login
    ```

The GCP initial setup is completed. We will now be ready to work using GCP service provider.

## GCP setup for access
> Video Source: [DE Zoomcamp - Introduction to Terraform Concepts and GCP Pre-requisites](https://www.youtube.com/watch?v=Hajwnmj0xfQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=8)

In this section, we will have to setup a *Data Lake* on Google Cloud Storage and a *Data Warehouse* in BigQuery. We will discuss the concepts as we progress through the course but for now this is the general idea:

#### Data Lake
A data lake is a centralized repository that allows you to store all your structured and unstructured data at any scale. You can store your data as-is, without needing to first structure it, and run different types of analytics—from dashboards and visualizations to big data processing, real-time analytics, and machine learning.

#### Data Warehouse
A data warehouse is a central repository of integrated data from one or more disparate sources, used primarily for reporting and data analysis. It stores current and historical data in a structured format and is optimized for fast query performance.

It means that the *Data Lake* is to stores vast amounts of raw data, flexible, suitable for big data and machine learnings. On the other hand, *Data Warehouse* is to stores structured, processed data, optimized for fast querying and reporting.

In this case, we will need to setup access by assigning `Storage Admin`, `Storage Object Admin`, `BigQuery Admin`, and `Viewer IAM` roles to our service account. And then we will have to enable the `iam` and `iamcredentials` APIs to the project.

> [!WARNING]
> Please be aware that the following steps are for educational purposes only. You should not assign these roles in production environment.
Please follow the instructions to assign the accesses for mentioned roles.
1. On the GCP Project Dashboard, go to `IAM & Admin` (since we pinned that earlier we will be able to see it right away in navigation menu). Go to the *IAM*.
1. Select the service account that we created previously, and edit the permission by clicking the pencil icon on the right side of your screen.
1. Add the following roles and then click *Save*.
    1. `Storage Admin`: Grants full control over Cloud Storage, including creating, deleting, and managing buckets and their settings.
    1. `Storage Object Admin`: Provides full control over objects in Cloud Storage, allowing for uploading, downloading, deleting, and modifying objects.
    1. `BigQuery Admin`: Offers full control over all BigQuery resources, including datasets, tables, and jobs, as well as setting access controls.
    1. `Viewer`: Allows read-only access to view resources across GCP, without the ability to modify or manage them.
1. Now we have setup accesses for roles, we will need to enable the APIs for the project. Below are needed to enable for Terraform (local environment) able to interact with GCP (cloud environment):
    - [Identity and Access Management (IAM) API](https://console.cloud.google.com/apis/library/iam.googleapis.com)
    - [IAM Service Account Credentials API](https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com)

## Terraform Basics

In **Terraform** there are three main blocks; `terraform`, `provider` and `resource`. 

### `terraform` Block
The `terraform` block is the root block of the configuration file. It configures settings that apply to the entire *Terraform* projects, such as the backend configuration for storing state files and setting the required Terraform version. 

### `provider` Block
The `provider` block is used to specifies the cloud service provider (e.g., AWS, GCP, Azure) including *project ID*, *region*, and *credentials*. Providers are essential for **Terraform** to interact with various cloud platforms and services.


### `resource` Block
The `resource` block is used to create, update, or delete resources in the cloud. It defines specific infrastructure components you want to create, such as *virtual machines*, *storage*, or *networks*. Each `resource` block specifies the type of resource and it's configuration.

These blocks are essential for managing your cloud provider, for an example - Google Cloud infrastructure with Terraform, allowing you to automate and control your cloud environment efficiently.

With your configuration ready, you can now start building your infrastructure. Here's a sequence of commands you should follow:

- `terraform init`: Sets up your working directory by downloading the necessary providers and plugins.
- `terraform fmt (optional)`: Ensures your configuration files are formatted consistently.
- `terraform validate (optional)`: Checks your configuration for errors and confirms it's valid.
- `terraform plan`: Generates a preview of the changes that will be made, letting you review them before execution.
- `terraform apply`: Executes the planned changes and updates your infrastructure.
- `terraform destroy`: Removes the infrastructure you've created.

## Creating GCP Infrastructure with Terraform
> Video Source: [DE Zoomcamp - Creating GCP Infrastructure with Terraform](https://www.youtube.com/watch?v=dNkEgO-CExg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=11)

In this section we will create a `main.tf` file as well as the auxiliary `variable.tf` file with all the blocks that we have mentioned earlier.

In `main.tf`, we will set a configuration for the `terraform` block:
```terraform
terraform {
  required_version = ">= 1.0"
  backend "local" {}
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}
```
- `required_version` is to specifies the minimum version of Terraform that is required to run this configuration. It means that any Terraform version 1.0 or higher is acceptable.
- `backend "local" {}` defines the backend where Terraform will store it's state file. The *local backend* is suitable for simple projects or local development but is not recommended for collaborative work. Also, keep in mind that you can edit the `local` to your desired cloud provider.
- `required_providers` is the configuration for providers that Terraform needs in order to manage the infrastructure which is specified. It lists the providers and specifies their sources and versions.

> [!IMPORTANT]
> 
> The method of choosing between credential configuration (like using a credentials file directly in your Terraform configuration) and setting the `GOOGLE_APPLICATION_CREDENTIALS` environment variable can impact both security and ease of use. 

In this section, the method that we used is the `GOOGLE_APPLICATION_CREDENTIALS` environment variable for manageing credentials for Google Cloud since we already created the env-var previously. 

As for the `variable.tf`, we will be storing variables that may change depending on your desired needs and location. Please advised to change the following:
- `region` choosing the right region can help minimize costs due to regional pricing differences.
- `BQ_DATASET` has the name of the table for BigQuery. You may update it to suit your needs.
- `project` should contain your GCP Project ID. In our case, every time we run it, it will ask for *Your GCP Project ID* since we have different unique ID.

You can access the mentioned files in the [terraform folder](). Check them out to get detailed look at how everything is set up. Next, it's recommended to copy these files into a new folder within your work directory so that the folder only contains Terraform configuration files. Afterwards, we will run the following commands below:

This command will initialize Terraform and download the necessary providers and plugins.
```bash
terraform init
```

This command to plan the infrastructure in Terraform.
```bash
terraform plan
```
- Since we've mentioned that we used env-var to store our project ID. It will ask for your Project ID.

This command to apply the infrastructure in Terraform.
```bash
terraform apply
```
- It will ask for confirmation to apply the specified configuration within our `main.tf`, prompty input ***yes*** to confirm. This will create all of the necessary components in the infrastructure and return a `terraform.tfstate` along with the current state of the infrastructure.

After we've successfully executed all of the commands above. This command below is to destroy the infrastructure that we apply so it doesn't consume our free credits.
```bash
terraform destroy
```
- It will ask for confirmation to destroy the specified configuration within our `main.tf`, prompty input ***yes*** to confirm. This will remove the components from the cloud. 

> [!WARNING]
>
> Before you run `terraform destroy`, just a quick reminder that this command will permanently delete all the resources you've set up with Terraform. Double-check what you're about to remove to make sure you don’t accidentally wipe out something important. Once it's gone, it can't be brought back, so use this command carefully!

[<u> [Go to Top]</u>](#table-of-contents)


# Homework 1: Pre-Requisites (Docker, Terraform, SQL)
In this homework we'll prepare the environment and practice with Docker and SQL. Please refer to this [link]() to check out the homework for week 1.

