# start jupyter notebook
screen -SUL jupyter -dm jupyter-lab --ip 0.0.0.0 --port 8888 --LabApp.token=''
```python 
sc 
###
sc.addPyFile('s3://kh-pulse-prod/lib/lynx.zip')
###
import datetime
import argparse
from types import SimpleNamespace

from lynx.lib import yaml_parser
from lynx.lib.spark_sql_utils import create_spark_hive_session
from lynx.lib.yaml_parser_utils import get_pulse_alert
from lynx.lib import yaml_parser as yaml
from lynx.lib.post_execute_utils import post_execute_transformation
from lynx.lib.alert_pipeline_utils import end_of_pipeline_snowflake_ops, start_of_pipeline_snowflake_ops
args = SimpleNamespace(
                        output_bucket_name= 'pulse.dev',
                        bucket_name = 'pulse.dev',
                        env = 'dev',
                        config = 's3://pulse-scripts/airflow/test/smoke_test.yaml', # this is the yaml file that defines an alert.
                        run_date = datetime.datetime.strptime('20211126', '%Y%m%d').date(),
                        disable_enrichment = True,
                        snowflake_persist = False,
                        disable_snowflake_persist = True
                      )
# from alert_runner_emr.py
print("Starting Pulse Alert Runner\n" + '-' * 75 + '\n')
print("Grabbing YAML config parameters...\n")
args_dict = {
    "config": args.config,
    "run_date": args.run_date,
    "output_bucket_name": args.output_bucket_name,
    "bucket_name": args.bucket_name,
    "pulse_env": args.env,
    "snowflake_persist": args.snowflake_persist,
    "disable_snowflake_persist": args.disable_snowflake_persist,
}
args_dict = yaml.make_and_parse_arguments(args_dict)
print("Generating Spark Session: {client_id}_{project_id}\n".format(**args_dict) + '-' * 75 + '\n')
spark = create_spark_hive_session("{client_id}_{project_id} ".format(**args_dict))
print("Creating Pulse Alert Class object...")
alert_therapy = get_pulse_alert(spark, args_dict)
print("Running Alert execute method...")
if args.disable_enrichment:
    print("Skipping enrichment")
    results = alert_therapy.execute()
else:
    results = alert_therapy.execute().transform(post_execute_transformation(spark, alert_therapy.config))
print("Saving Results to S3")
alert_therapy.save_output(results, delimiter=args_dict["output_csv_delimiter"])

print("Alert Runner Successful!" + '-' * 75 + '\n')
```

# stop jupyter notebook with screen
screen -ls
screen -X -S [session # you want to kill] quit

# stop jupyter notebook with jupyter cli
jupyter server list
jupyter notebook stop [port number]

# updating GE yaml, generate GE suite
update alert ge yaml,
save to s3
update paths in test suite gen script
run the ge validation python script in jupyter

`git show --pretty="" --name-only`

# creating ge suite
```python
sc
####
sc.addPyFile('s3://kh-pulse-prod/lib/lynx.zip')
alert_yaml = 's3://pulse.dev/hankcorner/Alexion_aHUS_Ultomiris_continuous_therapy_combined_alert.yaml'

# Generate suite
from lynx.lib.test.great_expectations.ge_generator import generate_ge_suite

generate_ge_suite(
    spark_session=spark,
    create_suite_in_env='dev',
    yaml_config=alert_yaml,
    replace_existing=True,
    build_data_docs=False,
    sample_data_from_env='dev'
)
```

# creating zip files
```bash 
zip -r9 ../lynx.zip lynx -x "*.pyc" __init__.py version requirements.txt MANIFEST.in Makefile README.md setup.py setup.cfg
aws s3 cp ../lynx.zip s3://kh-pulse-dev/lib/hank-lynx.zip
```     

# update enrichment scripts (one script)
```bash
aws s3 cp scripts/configs/ALN/TTR-2-Continuous-Therapy/enrichment_config.yaml s3://pulse.dev/configs/ALN/TTR-2-Continuous-Therapy/enrichment_config.yaml
aws s3 cp scripts/emr/livy/ALN_TTR/Alnylam_TTR_Amyloidosis_Continuous_Therapy.yaml s3://pulse.dev/configs/manual/ALN_TTR/
```

# check airflow inst and scheduler
```bash
kubectl get pods -n airflow-pulse-dev --context=dev-eks1
kubectl logs -f -n airflow-pulse-dev --context=dev-eks1
```