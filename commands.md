# start jupyter notebook
screen -SUL jupyter -dm jupyter-lab --ip 0.0.0.0 --port 8888 --LabApp.token=''

# git commands
```bash 
# restore one file to a branch
git restore --source main scripts/emr/livy/JANSSEN/Janssen_PAH_continuous_therapy.py

#???
git show --pretty="" --name-only
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
kubectl -n airflow-pulse-prod --context=dev-eks1 get pods 
```

# ssh or sftp

```bash
sftp -i ~/.ssh/sftp.pem ubuntu@sftp-pulse.komodohealth.net
```