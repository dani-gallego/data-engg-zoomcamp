> [Back to index](README.md)

> Next lesson: [Data Ingestion]()

### Table of Contents
- [Introduction to Data Engineering]()



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

### Advantages of Docker
Docker provides the following advantages:
- Reproducibility: Docker images can be shared and run in various environments, ensuring that the application behaves the same way everywhere it is deployed.
- Isolation: Containers ensure that applications and their dependencies are isolated, minimizing conflicts between different software versions on a host machine.
- Local Testing/Experimentation: Docker aids in setting up local experiments and integration tests, allowing data engineers to validate their data pipelines effectively before deployment.
- Inegration Tests (CI.CD)
- Running pipelines on the cloud platform (AWS, Google Cloud, Azure)
- Spark
- Serverless (AWS Lambda, Google functions)