# open search query
application_id: application_1642788023961_0646 and driver: true and file_name:stdout 

# migrating to ucc
* set these:
  ```yaml
  use_ucc: true
  use_subset_enrichment: false
  use_sql: true
  ```
* add in rx, px, dx codes. these are separate, top level items. UCC uses them to filter codes, determined by the filter setting
  * if there are existing code list keys in all caps, keep them. e.g. keep `DX_CODES` item
  * for each code item, there needs to be a upper case code item too. the converse is true too.
* add product or regimen or subtype mapping
  * if there's a separate mapping yaml file, keep it
* add `claims_enrichment` elements
  * if you're using codes from BRD, make sure you dedupe them first.
  * look at the aggregation types in enrichment yaml. in `function_column_mapping`
  * add quotes to all codes that have leading zeros. e.g. 0041234023 > '0041234023'
  * be careful when migrating codes. they can be overlap with trigger codes
* change `output_columns_map` to new format
  * add enrichment code columns to columns map
* remove claims path s3 URIs
* remove PreSupplement step;
* remove `codes:` in enrichment_config, as they're not used in UCC
  * instead, set it to `default: []`
* before running DAG, check the dag code to see if reads the right script path
  * if the dag only looks at pulse-scripts, then update dag to use env vars
* make these changes in the dag
  * remove enrichment task in dag.
  * remove `--disable_enrichment` args in the alert task
  * reduce amount of max executors to 5
* update python or yaml files in s3
  * this is for dev only
  * its a reminder to update your yaml or python files after making changes
* ask CX if there are extra columns in the BRD that should not be in the alert.
  * sometimes they add cols that should be deleted
  * also check that BRD has most recent codes
* delete mx and rx subset tasks in subset dag

# DAG Note
* airflow pulls github for DAG changes
* `depends_on_pastc` in dag config: current dag run depends on successful past dag runs. mark dags as successful if you want to run current dag with current run date
* depending on past ensures dags run sequentially, and not in parallel. useful for creating alerts for only that week's file, avoid creating alert with 2 weeks of data, or multiple alerts for one week
* look at all claims in subset for past qualifying window (8 weeks) that has DX_CODES = ... (in alert yaml)
* qual window is 8 weeks because data comes in late, like 5 weeks late.
* make sure that all claims in past 8 weeks are unique.
* can get empty file errors if running alert with only 2-4 weeks worth of claims data, esp if they are all ord.
	means that pulse already saw those old claims, and no new claims came in, so file might be empty
* if dag doesn't work, try these things:
	* reapply a3s
	* make sure its reading from right branch
	* check yaml file in s3 AND the file path in airflow are right
	* check zip file is correct
	* check any hardcoded paths in the DAG code
	

# airflow docs
`pip3 install a3scli  -i https://nexus3.khinternal.net/repository/pypi-all/simple --upgrade`
use this to get the name of your scheduler pod `kubectl get pods -n airflow-pulse-dev --context=dev-eks1`
then run this to see if there's any weird messages `kubectl logs -f {scheduler_pod_name} -n airflow-pulse-dev --context=dev-eks1 example name pulse-jason-vg0wu8-airflow-scheduler-5889f778d6-q22bt`

# When to run `a3s apply`
1. Changing your `py_file_path` source in `value.yaml`.
	1. The python files that back the yaml files are here.
	1. Any changes under the `variables` yaml variable, Can also update this variable on airflow UI
2. changing git branch that airflow should pull dags from, like when you start working on a feature branch. Note that `branch` is not under `airflow` in `values.yaml`
3. changes to your airflow `host`, or if you have multiple AF instances and are switching between AF dev versions. 
	1. You might have multiple instances if you're testing DAG in diff configurations.
4. Starting up a new, or restarting, your airflow instance
5. or any a3s config file change

# when to run `update_scripts.sh`
1. changes to these YAML files:
	1. enrichment yaml
	2. GE validation yaml files
	3. standard and non-standard alert filters
	4. subset config file filters
	5. any changes to `lynx/scripts/*` files (not really all, see update_scripts.sh)
	6. old python scripts that do the filtering
2. for lab alerts, can make changes, manually upload to s3 or run this script
3. If your airflow already points to your github branch, airflow will automatically pull that change into your instance. Airflow polls github for changes to a branch.

# when to create a new lynx zip and push to `kh-pulse-dev`?
1. Changes to DAG code, like adding a node to a graph.
	1. updates to `lynx/lynx/`, req.txt, will need an updated zip. can put to new bucket, and then point airflow to that s3 path
2. adding new dag and there's changes to `lynx/lynx`.
	1. eg changes to slack message posting from dag execution, dag calls the function to psot message, but that code is stored in lynx, thus, the zip file
4. changes to executable (entrypoint script) e.g. alert_runner.py, need to create a new lynx zip file 

# S3 dates 
* s3://pulse.dev/output/JANSSEN/CD-start-therapy/20211216/KH_Janssen_RD_CD_Pulse_Deliverable_20211221.csv
	- 20211216 is the day the alert runs and generates the file
	- 20211221 is the day the alert should be delivered.

# flores
* tracks delivery date of alerts
* shows next alert delivery date
* alert file created in s3
* s3 event with alert info gets sent to sqs
* flores api reads from sqs, runs celery task with the message
* if its time to deliver, flores will 

# DTS
ciao reads from alerts address fields, queries google api to get lat and long
pulse takes NPI from the alert, queries MAP_PROVIDER.PUBLIC.BASE_HCP, find  HCP's lat and long, adds to alert df, cross join with site_df
	site_df: all the SITE lat and long, given a client id and project id
calculate distance between 2 coordinates via google api, calculatie travel distance
pick the closest site
add that to the alert df

# CD-start-therapy
```sql
insert into PULSE_DEV.DISTANCE_TO_SITE.CLIENT_SITE
select
	'JANSSEN' as client_id, 
	'CTEPH' as project_id, 
	ci_id as project_site_id, 
	site_name as site_name, 
	'Active' as site_status,
	site_lat as latitude, 
	site_long as longitude, 
	site_address as site_address, 
	NULL as site_pi_npi, 
	site_pi as site_pi_name
from CIAO_REQUESTS.PULSE_GEO_CUSTOMER_INPUTS.JANSSEN_CTEPH_PAH_SITES;
```

# Janssen notes
- if rerun at the enrichment step only:
	- delete csv without the `_original` 
	- remove `_original` from the other csv file
- rerun at therapy_start:
	- delete both csvs
- `JANSSEN_CD_therapy_start` creates file WITHOUT `_original`. will only have standard fields. no enrichment.
- `Janssen_CD_therapy_start_enrichment` reads the created csv file, will rename that file to X_original, add enrichmend fields, saves it without _ file name

# sftp hostnames
* Old SFTP: sftp-pulse.komodohealth.net
* AWS Transfer SFTP: pulse-sftp.komodohealth.net

# onboarding topics:
1. set up local lynx and run unit tests
2. set up dev airflow
3. understand flores
4. GE:
	GE validation config YAML
	GE in Jupyter
	GE in Airflow
5. UCC API
6. review ATA2P DAG in airflow. its a simple dag
7. `execute()` function in `alert_emr_runner.py`
8. how yaml config files are used to filter and select columns, and the underlying python files that back the yaml configs
9. BRD - document that pulse uses to understand requirements

# subset enrichment
* triggering on a claim or code, means we add it to our alert
* subset enrichment means you enrich the original df with subset data
* mx subsets undergoes preprocess step
* create mx and rx subsets from DI data drop

# open search query
id: application_1642788023961_0646 and driver: true and file_name:stdout 

sparkContext is the entrypoint for sqlcontext and hivecontext. provides the connection and apis to use those thing
sparkSession combines all 3, and abstracts them away. dont need to manually cal sql or hive context to create those contexts