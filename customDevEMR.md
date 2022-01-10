# How to spin up an emr cluster to test out updates
Can test EMR scripts, cluster requirements.txt changes, etc

1. Update the requirements.txt in S3 manually (https://s3.console.aws.amazon.com/s3/buckets/pulse-emr-automation?region=us-west-2&prefix=BootstrapActionFiles/&showversions=false)

2. spin up an emr cluster (`./scripts/emr_cluster/spin_up_pulse_emr_template.py` -c dev) https://komodohealth.atlassian.net/wiki/spaces/PT/pages/987365377/Leveraging+AWS+EMR+clusters+for+Pulse+Alerts#Spinning-up-pulse_emr_livy_dev

3.Run an alert on the emr cluster (You can update url in your `~/.sparkmagic/config.json` to point to the additional dev emr cluster)

4.Terminate cluster (can do using the UI or script noted in confluence page above)

5. revert requirements.txt in S3 because that file is used in by all emr cluster (including current dev and prod). Shouldn't cause issues because those clusters don't spin-up/terminate on any schedule