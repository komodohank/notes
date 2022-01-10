# Todo:
* ask tom about what CR topics are relevant to Anand
* talk about tom for on-call expectations, and ask to be roped into any issue
* add UCC api to onboarding slide show
* ask Scott about the "when to do X" stuff

# S3 dates 
* s3://pulse.dev/output/JANSSEN/CD-start-therapy/20211216/KH_Janssen_RD_CD_Pulse_Deliverable_20211221.csv
	- 20211216 is the day the alert runs and generates the file
	- 20211221 is the day the alert should be delivered.

# Janssen notes
- if rerun at the enrichment step only:
	- delete csv without the `_original` 
	- remove `_original` from the other csv file
- rerun at therapy_start:
	- delete both csvs
- `JANSSEN_CD_therapy_start` creates file WITHOUT `_original`. will only have standard fields. no enrichment.
- `Janssen_CD_therapy_start_enrichment` reads the created csv file, will rename that file to X_original, add enrichmend fields, saves it without _ file name


# testing Lynx code changes to airflow
1. make code changes
2. to test in airflow, upload to s3 with `update_scripts.sh ENV hank`
3. update airflow variable `py_file_path` to point to dev bucket
4. `py_file_path` contains arguments that are passed into the DAG nodes
5. sometimes you will need to set `py_file_path` to prod if you're only testing config changes
6. `s3://pulse-scripts/airflow-dev/` contains regular and subset filter yaml files in DEV. 
    1. If you make changes to filter yaml files, you will need to upload them to this s3 path
    2. and make sure airflow is reading from this scripts path

# update dev airflow to reflect core code changes
1. update `py_file_path` to new s3 path in `values.yaml`
2. deploy other configs first
3. zip new lynx changes
4. copy zip to s3
```bash 
zip -r9 ../lynx.zip lynx -x "*.pyc" __init__.py version requirements.txt MANIFEST.in Makefile README.md setup.py setup.cfg
aws s3 cp ../lynx.zip s3://kh-pulse-dev/lib/hank-lynx.zip
```	
5. run `a3s apply`

# update dev airflow to reflect config changes
1. this includes things like GE yaml updates, enrichment config changes, etc
2. update config file in s3. manually, or use `update_scripts.sh`

# When to run `a3s apply`
1. Changing your `py_file_path` source 
2. changing git branch that airflow should pull dags from
3. changes to your airflow `host`
4. starting up a new, or restarting, your airflow instance
5. or any a3s config file

# when to run `update_scripts.sh`
1. changes to these YAML files:
	1. enrichment yaml
	2. GE validation
	3. standard and non-standard alert filters
	4. subset filters
	5. any changes to `lynx/scripts/*` files 

# when to create a new create new lynx zip and push to `kh-pulse-dev` zip file?
1. "core code changes".
2. DAGs
3. code that runs the yaml files
5. or code that defines or "backs" the filtering logic in the yaml files

# subset
internal filtering process that looks for claims data based on certain codes. filter by diagnosis, medical, and pharmacy codes. its 

# updating GE yaml, generate GE suite
update alert ge yaml,
save to s3
update paths in test suite gen script
run the ge validation python script in 

# running nodes in dag 
1. enter correct base date
2. turn on dag
3. mark upstream nodes as successful
4. clear node you want to start.
base date: run date for the file you want to run the dag with. If you want to run dag for file on 2021-11-01, make sure base date is the same value
start_date:

## dag notes
* `depends_on_past` in dag config: current dag run depends on successful past dag runs. mark dags as successful if you want to run current dag with current run date
* depending on past ensures dags run sequentially, and not in parallel. useful for creating alerts for only that week's file, avoid creating alert with 2 weeks of data, or multiple alerts for one week

# sftp hostnames
* Old SFTP: sftp-pulse.komodohealth.net
* AWS Transfer SFTP: pulse-sftp.komodohealth.net

okr, lives the values, impact to company

Review timeline of incident from post mortem document
Identify root causes of incident. one-off or systematic problem?
	- unit tests that query to 
List potential solutions to fix root issues
	- short run: use medium WH
	- long run: redesign unit tests to properly mock up returned data from snowflake 
		- 
Create action items/tickets to prevent issue like this in the future.
	- make tickets - fix unit tests 	PR to use medium ticket, all ready for grooming
	- make PR to use medium WH, wait for tom to get back to you.

}fqt89WQgmn>V
rcgo$$o90812()()

https://clips.twitch.tv/BlazingGoodOrangeTF2John-z98DZ2pSp7Y2l-0Z



On netbenefits.com, if you plan offers chat you access it the same way you did on Fidelity.com. You can also contact out 401k department by phone! You can contact the Fidelity 401(k) group by calling:

800-835-5095
8:30 a.m. to 8:30 p.m.,* Eastern time
Monday through Friday