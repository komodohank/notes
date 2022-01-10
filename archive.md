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



