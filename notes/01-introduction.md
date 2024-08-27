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
  -v //c/Users/madan/OneDrive/Documents/GitHub/data-engg-zoomcamp/01-introduction/docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
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


