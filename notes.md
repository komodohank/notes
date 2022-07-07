# Todo:
* if code is enrichment flag, and a trigger, should i still include in the flag? if so, will have to add it to claims_enrichment 
* delete dev runs
* dentist appt
* run alert 2, with run dates 1 week apart 
  running the same alert in 2 consec day. claims that you're supposed to get will get deduped out. 
  day 1 in for rundate 0627: rundate 0627 has 100 new and unique claims and alert gets those new claims. these are not deduped out. but if future runs also see those 100 claims, they will be deduped out.
  day 2 in rundate 0627: you get 110 claims, 10 of which are new and unique. so you will end up with only 10 rows in day 2
  same thing will happen if rundates themselves are only 1 day apart.
* look a prod support to see what alerts need to have their GE updated
* look at logs to see if codes are NOT there. look at UCC logs
* add a column that lists list
* ask CX about blue earth alerts 1-4. early deliver this?
  
  hznp_cyst https://komodohealth.atlassian.net/browse/PT-5617
  gen cc https://komodohealth.atlassian.net/browse/PDP-162
  alxn hpp ge https://komodohealth.atlassian.net/browse/PDP-90
  Alnylam_TTR_Diflunisal_therapy_start_GE https://komodohealth.atlassian.net/browse/PDP-163
  Alnylam_TTR_Onpattro_therapy_start_GE https://komodohealth.atlassian.net/browse/PDP-163
  tak hae 1 https://komodohealth.atlassian.net/browse/PDP-164
  GE_Alexion_HPP_juvenile_low_alp_newly_tested (decreasing trend) https://komodohealth.atlassian.net/browse/PD-2151
  GE_Alexion_PNH_combined_alerts (need to update cols) https://komodohealth.atlassian.net/browse/PDP-137
  GE_rx_subset_ALXN_PNH https://komodohealth.atlassian.net/browse/PDP-138
  GE_Alexion_aHUS_continuous_therapy https://komodohealth.atlassian.net/browse/PDP-165
  GE Janssen PAH https://komodohealth.atlassian.net/browse/PDP-166  

* ask CX if we should add all the icd code flags in "Last AHN Diag Date". do we search for C9201 code in the Last AHN Date ClEnrich col?

# unioned encounters
* schema of patient data and claims data
* for ucc, get all encounters 
* entity summary table. UPK table
* entity summary patients: gets patient age, gender, zip3, payerID, etc. this is an output from UCC

run date - dev - prod
20220606 - 411 - 156
20220613 - 152 - 110
20220620 - 97  - 170
20220627 - 7   - 155


# bpmc dev counts
## alert 1 cohort id
0610 - 182682
0617 - 182765

0527 - 182873 - 1535  
0603 - 182952 - 142
0610 - 183027 - 118
<!--  -->
0617 - 186169  - 411
0624 - 186601  - 101
<!--  -->
0603 - 186955 - 494
0610 - 186701 - 507
0617 - 186776 - 186
0624 - 186853 - 68

pulse_g_claims gets only triggering claims
subset has all the that have all claims with triggering codes, all enrichment codes we look at, allow/deny list codes. 
subset can have more data because we look at subset data with the codes that we enrich on, and allow/deny on. can add codes that has the wrong type, but same code value during enrichment.
we will drop claims that dont have HCP data.
subset has TA level claims. in getclaims(), will filter with px-rx-dx codes. 

# findings
- subset csv contains alerts all throughout its qualifying window, will have data from rundate-qual window (13 weeks. Date of Service min and max shows this
- subset also missing alerts that happen within 1 week inclusive of run date 
- need to find if ucc file has the same data as subset. see if there's overlap. 
- see if we're properly adding the right alerts

When is the most recent claim for each source?
* 0617 - 0616
* 0624 - 0623
How many days have passed since then?
* 1 day
Which claims exist in the most recent ucc cohort but not the preceding ones.
136
```sql
SELECT COUNT(CLAIM_ID) FROM PULSE_GET_CLAIMS WHERE COHORT_ID = '186601' AND CLAIM_ID NOT IN (select CLAIM_ID from PULSE_GET_CLAIMS  where COHORT_ID = '186169');
```
How many claims have been deduped?
3301 - 101
Has the subset run in the correct environment if necessary?
yes
Did the alert take an unusually brief or long runtime?
no
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

## misc notes
- `find_earliest_or_latest_drug` shows 1st or last code a patient receieved. do not put in claims_enrichemnt
- bpmc sm-cont-ther smallest claim date is 2021-12-24 in PULSE_GET_CLAIMS



flag:
aggregation
codes
lookback window

## `claims_enrichment` item documentation
```yaml
- aggregation: # the aggregation type
  codes:
    - code: # code to run aggregation for
      code_type: # code type, like icd

  enrichment_column: # ???
  enrichment_level: # enrichment level, set in BRD
  event_name: # ??? usually same as fieldname
  fieldname: # column name of enrichment column, set in output_columns_map
  window_in_days: # code or flag lookback window  
```
## for python script alerts
* if you want columns with spaces (dont bother though)
  * set format column names like this in enrichment_configs
    ```
    'event_name': '"Congenital Heart Disease (CHD)"',
    'fieldname': '"Congenital Heart Disease (CHD)"
    ```
  * Output Columns Map: `{'Systemic connective tissue disorder (SCTD)': 'Systemic connective tissue disorder (SCTD)'}`. no extra "" 
* if there's DTS categorical columns, either: (must do this bc the caterogical column doesn't work for python-based alerts)
  * with custom code, add and fill the categorical colums between the execute and post exectute functions
  * in a preSupp step, add the categorical column, and run custom code _after_ the execute and post execute functions

codes to remove: D4709, C9620
# s3 paths
```bash
# alert 1
aws s3 cp /Users/hank/work/lynx/scripts/emr/livy/BEDX_PC/BEDX_PC_competitor_continuous_therapy.yaml   
aws s3 cp /Users/hank/work/lynx/scripts/configs/BEDX/PC-competitor-continuous-therapy/enrichment_config.yaml s3://pulse.dev/configs/BEDX/PC-competitor-continuous-therapy/enrichment_config.yaml

# alert 2
aws s3 cp /Users/hank/work/lynx/scripts/emr/livy/BEDX_PC/BEDX_PC_PSA_continuous_therapy.yaml s3://pulse.dev/airflow/BEDX_PC/BEDX_PC_PSA_continuous_therapy.yaml
aws s3 cp /Users/hank/work/lynx/scripts/configs/BEDX/PC-PSA-continuous-therapy/enrichment_config.yaml s3://pulse.dev/configs/BEDX/PC-PSA-continuous-therapy/enrichment_config.yaml

aws s3 cp /Users/hank/work/lynx/scripts/emr/livy/BEDX_PC/BEDX_PC_FDG_continuous_therapy.yaml s3://pulse.dev/airflow/BEDX_PC/BEDX_PC_FDG_continuous_therapy.yaml
aws s3 cp /Users/hank/work/lynx/scripts/configs/BEDX/PC-FDG-continuous-therapy/enrichment_config.yaml s3://pulse.dev/configs/BEDX/PC-FDG-continuous-therapy/enrichment_config.yaml

# alert 4
aws s3 cp /Users/hank/work/lynx/scripts/emr/livy/BEDX_PC/BEDX_PC_GA68_PSMA11_continuous_therapy.yaml s3://pulse.dev/airflow/BEDX_PC/BEDX_PC_GA68_PSMA11_continuous_therapy.yaml
aws s3 cp /Users/hank/work/lynx/scripts/configs/BEDX/PC-GA68-PSMA11-continuous-therapy/enrichment_config.yaml s3://pulse.dev/configs/BEDX/PC-GA68-PSMA11-continuous-therapy/enrichment_config.yaml

# bpmc alert 1 (sm cont. therapy)
aws s3 cp /Users/hank/work/lynx/scripts/emr/livy/BPMC_SM/BPMC_SM_continuous_therapy.yaml s3://pulse.dev/airflow/BPMC_SM/BPMC_SM_continuous_therapy.yaml
aws s3 cp /Users/hank/work/lynx/scripts/configs/BPMC/SM-continuous-therapy/enrichment_config.yaml s3://pulse.dev/configs/BPMC/SM-continuous-therapy/

aws s3 cp /Users/hank/work/lynx/scripts/emr/livy/BPMC_SM/BPMC_SM_continuous_therapy.yaml s3://pulse.dev/configs/manual/BPMC/SM-continuous-therapy/

#bpmc alert 2
aws s3 cp /Users/hank/work/lynx/scripts/emr/livy/BPMC_SM/BPMC_SM_start_therapy.yaml s3://pulse.dev/configs/manual/BPMC/SM-start-therapy/BPMC_SM_start_therapy.yaml
aws s3 cp /Users/hank/work/lynx/scripts/emr/livy/BPMC_SM/BPMC_SM_start_therapy.yaml s3://pulse.dev/airflow/BPMC_SM/BPMC_SM_start_therapy.yaml

aws s3 cp /Users/hank/work/lynx/scripts/configs/BPMC/SM-start-therapy/enrichment_config.yaml s3://pulse.dev/configs/manual/BPMC/SM-start-therapy/
aws s3 cp /Users/hank/work/lynx/scripts/configs/BPMC/SM-start-therapy/enrichment_config.yaml s3://pulse.dev/configs/BPMC/SM-start-therapy/

# bpmc alert 3
aws s3 cp /Users/hank/work/lynx/scripts/emr/livy/BPMC_SM/BPMC_SM_KitGeneticTest_continuous_therapy.yaml s3://pulse.dev/airflow/BPMC_SM/BPMC_SM_KitGeneticTest_continuous_therapy.yaml
aws s3 cp /Users/hank/work/lynx/scripts/configs/BPMC/SM-KitGeneticTest-continuous-therapy/enrichment_config.yaml s3://pulse.dev/configs/BPMC/SM-KitGeneticTest-continuous-therapy/

# bpmc alert 4
aws s3 cp /Users/hank/work/lynx/scripts/emr/livy/BPMC_SM/BPMC_SM_specialty_visit_continuous_therapy.yaml s3://pulse.dev/airflow/BPMC_SM/BPMC_SM_specialty_visit_continuous_therapy.yaml
aws s3 cp /Users/hank/work/lynx/scripts/configs/BPMC/SM-specialty-visit-continuous-therapy/enrichment_config.yaml s3://pulse.dev/configs/BPMC/SM-specialty-visit-continuous-therapy/

### alexion pnh
aws s3 cp /Users/hank/work/lynx/scripts/emr/livy/ALXN/Alexion_PNH_flow_test_lab_alert_prognos.py s3://pulse.dev/airflow/ALXN/Alexion_PNH_flow_test_lab_alert_prognos.py
```



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
