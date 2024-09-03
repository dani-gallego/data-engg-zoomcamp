# Week 2: Workflow Orchestration

### Table of Contents



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

## What is Mage?
- [Mage](https://docs.mage.ai/introduction/overview) is an open-source tool designed for workflow orchestration, particularly in data engineering and data science workflows. It's used to build, run, and monitor data pipelines, making it easier to manage complex workflows that involve data extraction, transformation, and loading (ETL).

#### Architecture using Mage
For the week 2: Workflow Orchestration, we will be re-creating the following architecture:

![Mage Architecture](https://github.com/dani-gallego/data-engg-zoomcamp/blob/main/notes/images/mage%20-%20architecture.png)

#### ETL (Extact, Transform, Load)
- ETL stands for Extract, Transform, Load. It's a process used in data integration, data warehousing, and data engineering to move data from various sources into a centralized data storage system, such as a data warehouse or data lake.

In this week, we will be doing the following tasks:

- **Extract** - Pulling data from a source (API - <u> NYC Taxi Dataset</u>)

- **Transform** - Data cleaning, transformation, and partitioning.

- **Load** - API to Mage, Mage to Postgres, GCS, BigQuery.

