# Todo:
* delete https://pulse-hank-wawm2u-airflow.khinternal.net/home
* look at `add_descriptive_diagnosis_field()` in lynx

* s3://pulse.dev/configs/manual/
* aln alert yaml
  - alert 1: scripts/emr/livy/ALN_TTR/Alnylam_TTR_Tafamidis_continuous_therapy.yaml
    - aws s3 cp scripts/emr/livy/ALN_TTR/Alnylam_TTR_Amyloidosis_Continuous_Therapy.yaml    s3://pulse-scripts/airflow/ALN_TTR/
    - aws s3 cp scripts/emr/livy/ALN_TTR/Alnylam_TTR_Tafamidis_continuous_therapy.yaml      s3://pulse-scripts/airflow/ALN_TTR/
    - aws s3 cp scripts/emr/livy/ALN_TTR/Alnylam_TTR_continuous_therapy_combined_alert.yaml s3://pulse-scripts/airflow/ALN_TTR/
 s3://pulse-scripts/airflow/ALN_TTR/
  - alert 2: scripts/emr/livy/ALN_TTR/Alnylam_TTR_Amyloidosis_Continuous_Therapy.yaml

custom mapping field file?
what is era threshold? cutoff date? timegap---

# s3 delivery lambda
* update documentation
* more todos
  - maybe move each customer configs to their own config
  - have a default yaml, and a customer yaml overrides it
  - put SOURCE_BUCKET: "kh-pulse-sftp" in default config file 
  - document how the deployment script works, steps taken, and what gets overridden
  - add a version file

# questions about ucc yaml
* what does each claims_enrichment key do?
* many codes for enrichment is for what?
  - gets a list of the codes with OR logic
  - gets min date of all 8 of those codes, across all 8 of the codes
* what is source and target column name?
  - Source is dataframe col name, target is output csv column name
* claims_enrichment configs set what aggregations we run, and which code to use, on snowflake table of claims data


# Dag generator
* alert_dag_gen.py looks at the yaml files and top config values e.g.
  ```yaml
  # Aiflow configs
  auto_generate_dag: true
  airflow_schedule: "0 15 * * MON"  # 10AM ET / 7AM PT
  start_date: '20211101'
  use_subset_enrichment: true
  ```
* if need to generate a new dag, add to update_scr.sh bottom, `aws s3 sync scripts/emr/livy/{DAG_ID}/ s3://$CONFIG_BUCKET/configs/manual/{DAG_ID}/`   

CODE_TYPE_MAP = {
    'dx': 'icd',
    'px': 'procedure',
    'rx': 'ndc',
}