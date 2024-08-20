> [Back to index](README.md)

> Next lesson: [Data Ingestion]()

### Table of Contents
- [Introduction to Data Engineering](#introduction-to-data-engineering)
  - [Architecture](#architecture)
  - [Data Pipelines](#data-pipelines)
- [Docker](#docker)
  - [Docker Image](#docker-image)
  - [Creating a dockerfile and custom pipeline with the Docker](#creating-a-docker-file-and-custome-pipeline-with-the-docker)



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

![Data Pipelines](notes/images/data-pipelines.PNG)


# Docker
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
FROM python:3.9.1

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
