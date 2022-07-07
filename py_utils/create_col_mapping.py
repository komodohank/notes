import yaml 

# add enrichment colmuns here. only put the name of the column, not the yaml
enrich_cols = [
  "AHN Flag",
  "First SM Diagnosis Date",
  "SM Flag",
  "AML Flag",
  "Last AHN Diagnosis Code",
  "Last AHN Diagnosis Date",
  "Treatment",
  "Treating Ayvakit"
]
enrich_col_map = []
for c in enrich_cols:
	col_name_map = {'source_column_name': c, 'target_column_name': c}
	enrich_col_map.append(col_name_map)

yaml_map = yaml.dump(enrich_col_map)
print(yaml_map)

# put old colum mapping here. Example below
old_mapping_yaml = '''
output_columns_map:
  - PatientID: patient_id_hash
  - SentinelPatientID: patient_id
  - NPI: NPI
  - FirstName: FirstName
  - MiddleName: MiddleName
  - LastName: LastName
  - Specialty1: Specialty 1
  - Specialty2: Specialty 2
  - HCOName: hco_orgname
  - HCOBillingNPI: hco_billing_npi
  - Address1: Address1
  - Address2: Address2
  - City: City
  - State: State
  - Zip: Zip
  - Email: Email
  - Phone: Phone
  - Year: year
  - Week: week
  - Date of Service: service_date
  - PatientAge: age_group
  - PatientGender: patient_gender
  - PayerName: payer_name
  - PayerType: payer_type
  - Treatment: regimen
'''

old_mapping_obj = yaml.safe_load(old_mapping_yaml)

print(old_mapping_obj)
new_col_map = []
for m in old_mapping_obj['output_columns_map']:
	col_name_map = {'source_column_name': list(m.values())[0], 'target_column_name': list(m.keys())[0]}
	new_col_map.append(col_name_map)
new_col_map = new_col_map + enrich_col_map
# prints new output_column_mapping
print(yaml.dump(new_col_map))
