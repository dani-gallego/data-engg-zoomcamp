# Module 1 Homework

>Link: [Week 1: Homework](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/01-docker-terraform/homework.md)

# Docker and SQL
## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits* 

- `--delete`
- `--rc`
- `--rmc`
- `--rm`

> Answer:
```
--rm 
```

## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 

What is version of the package *wheel* ?

- 0.42.0
- 1.0.0
- 23.0.1
- 58.1.0

> Answer: 
```
0.42.0
```
> [!NOTE]
> This version is outdated. But in my `pip list`, the wheel version is `0.44.0`.

# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi_homework" \
  -v //c/Users/.../Homework/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database-homework\
  postgres:13
```

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-homework \
  dpage/pgadmin4
```

```bash
docker build -t taxi_ingest:homework .
```

```bash
URL1="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"
URL2="https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

docker run -it \
    --network=pg-network \
    taxi_ingest:homework \
    --user=root \
    --password=root \
    --host=pg-database-homework \
    --port=5432 \
    --db=ny_taxi_homework \
    --table_name_1=green_taxi_trips \
    --table_name_2=zones \
    --url1="${URL1}" \
    --url2="${URL2}" 
```
```bash
docker-compose up
```
## Question 3. Count records 

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 15767
- 15612
- 15859
- 89009

> Command:
```SQL
SELECT
	COUNT(*) AS total_taxi_trips
FROM
	green_taxi_trips g
WHERE
	CAST(lpep_pickup_datetime AS DATE) = '2019-09-18' AND
	CAST(lpep_dropoff_datetime AS DATE) = '2019-09-18';
```
> Output:
```
15612
```

## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance?
Use the pick up time for your calculations.

Tip: For every trip on a single day, we only care about the trip with the longest distance. 

- 2019-09-18
- 2019-09-16
- 2019-09-26
- 2019-09-21

> Command:
```SQL
WITH daily_max_distance AS (
  SELECT
    CAST(lpep_pickup_datetime AS DATE) AS pickup_date,
    MAX(trip_distance) AS max_distance
  FROM green_taxi_trips g
  GROUP BY pickup_date
)

SELECT pickup_date, max_distance
FROM daily_max_distance
ORDER BY max_distance DESC
LIMIT 1;
```
> Output:

|pickup_date  | max_distance |
|--------------|-------------|
|2019-09-26   |  341.64      |

> Answer:
The longest trip for each day was on **2019-09-26** with a distance of 341.64.

## Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
 
- "Brooklyn" "Manhattan" "Queens"
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens" 
- "Brooklyn" "Queens" "Staten Island"

> Command:
```SQL
SELECT 
    zpd."Borough",
    TRUNC(CAST(SUM(total_amount) AS NUMERIC), 2) AS total_sum
FROM 
    green_taxi_trips g JOIN zones zpd
	ON g."PULocationID" = zpd."LocationID"
WHERE 
    DATE(lpep_pickup_datetime) = '2019-09-18'
    AND zpd."Borough" != 'Unknown'
GROUP BY 
    zpd."Borough"
HAVING 
    SUM(total_amount) > 50000
ORDER BY 
    total_sum DESC
LIMIT 3;
```

> Output:

| Borough | total_sum|
|----------|---------|
| Brooklyn |  96333.23|
| Manhattan |  92271.29|
| Queens   |  78671.70|

> Answer:
The three pick up Boroughs that had a sum of total_amount superior to 50000 were **Brooklyn**, **Manhattan**, and **Queens**.


## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- JFK Airport
- Long Island City/Queens Plaza

> Command:

```SQL
SELECT 
    zdo."Zone" AS dropoff_zone,
    MAX(g.tip_amount) AS max_tip
FROM 
    green_taxi_trips g
JOIN 
    zones zpu ON g."PULocationID" = zpu."LocationID"
JOIN 
    zones zdo ON g."DOLocationID" = zdo."LocationID"
WHERE 
    zpu."Zone" = 'Astoria'
    AND EXTRACT(MONTH FROM g.lpep_pickup_datetime) = 9
    AND EXTRACT(YEAR FROM g.lpep_pickup_datetime) = 2019
GROUP BY 
    zdo."Zone"
ORDER BY 
    max_tip DESC
LIMIT 1;
```

> Output:

| dropoff_zone | max_tip |
|--------------|---------|
| JFK Airport  |  62.31  |

> Answer:
The largest tip was in the zone **JFK Airport**.

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```


Paste the output of this command into the homework submission form.

```
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "trips_data_all"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = {
          + "goog-terraform-provisioned" = "true"
        }
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "europe-west6"
      + max_time_travel_hours      = (known after apply)
      + project                    = "<omitted>"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = {
          + "goog-terraform-provisioned" = "true"
        }

      + access (known after apply)
    }

  # google_bigquery_table.table will be created
  + resource "google_bigquery_table" "table" {
      + creation_time       = (known after apply)
      + dataset_id          = "trips_data_all"
      + deletion_protection = false
      + effective_labels    = {
          + "goog-terraform-provisioned" = "true"
        }
      + etag                = (known after apply)
      + expiration_time     = (known after apply)
      + id                  = (known after apply)
      + last_modified_time  = (known after apply)
      + location            = (known after apply)
      + num_bytes           = (known after apply)
      + num_long_term_bytes = (known after apply)
      + num_rows            = (known after apply)
      + project             = "<omitted>"
      + schema              = (known after apply)
      + self_link           = (known after apply)
      + table_id            = "ny_trips"
      + terraform_labels    = {
          + "goog-terraform-provisioned" = "true"
        }
      + type                = (known after apply)
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + effective_labels            = {
          + "goog-terraform-provisioned" = "true"
        }
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "EUROPE-WEST6"
      + name                        = "dtc_data_lake_<omitted>"
      + project                     = (known after apply)
      + project_number              = (known after apply)
      + public_access_prevention    = (known after apply)
      + rpo                         = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = {
          + "goog-terraform-provisioned" = "true"
        }
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type          = "Delete"
                # (1 unchanged attribute hidden)
            }
          + condition {
              + age                    = 30
              + matches_prefix         = []
              + matches_storage_class  = []
              + matches_suffix         = []
              + with_state             = (known after apply)
                # (3 unchanged attributes hidden)
            }
        }

      + soft_delete_policy (known after apply)

      + versioning {
          + enabled = true
        }

      + website (known after apply)
    }
```