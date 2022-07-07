import yaml

CODE_TYPE_MAP = {
    'dx': 'icd',
    'px': 'procedure',
    'rx': 'ndc',
}

# the aggregation type for each function, found in the function_columns_mapping
# note that this aggregation will apply to ALL of the claims enrichment values
# You should convert each aggregation type at a time, so you don't accidentally 
# add a max aggregation with codes that should be min-ed 
aggregation = 'max'
window = '1830'
# paste in the yaml that have the column and codes mapping. 
subset_enrich_codes = '''
  
'''

subset_enrich_codes = yaml.safe_load(subset_enrich_codes)
# function_mapping = yaml.safe_load(function_mapping_yaml) will be used at a later update

warns = []
claims_enrichment = []
for code_group, code_list in subset_enrich_codes.items():
  codes_for_group = []
  ucc_enrich_agg_setting = {
    'aggregation': aggregation,
    'codes': [
      {'code': 'R972', 'code_type': 'icd'} # this is just an example entry. it will be overriden
    ],
    'enrichment_column': 'CLAIM_DATE', 
    'enrichment_level': 'Patient_ID', 
    'event_name': 'Prior Therapy (Y/N)', 
    'fieldname': 'Prior Therapy (Y/N)',
    'window_in_days': window
  }
  
  for c in code_list:
    # checking if a code is ICD, NPC, or procedure
    if len(c) >= 6:
      code_record = {'code': f'{c}', 'code_type': 'ndc'}
    elif c[0] == 'R' or c[0] == 'C' or c[0] == 'D' or c[0] == 'Z':
      code_record = {'code': f'{c}', 'code_type': 'icd'}
    elif c[0] == 'A' or c[0] == 'J':
      code_record = {'code': f'{c}', 'code_type': 'procedure'}
    else:
      warns.append(c)
      code_record = {'code': f'{c}', 'code_type': 'warning'}
    codes_for_group.append(code_record)
  ucc_enrich_agg_setting['codes'] = codes_for_group
  ucc_enrich_agg_setting['event_name'] = str(code_group)
  ucc_enrich_agg_setting['fieldname'] = str(code_group)
  # print('***',ucc_enrich_agg_setting)
  claims_enrichment.append(ucc_enrich_agg_setting)

# print(claims_enrichment)
yaml_claims_enrich = yaml.dump(claims_enrichment)
# print new claims_enrichment yaml blob
print(yaml_claims_enrich)
# prints keys that do not match our if statements. The script is unsure what code types these are
print(warns)

# subset_enrich_codes = ["D460", "D4709", "D461", "D4620", "D4621", "D4622", "D46A", "D46B", "D46C", "D464",
#                                   "D46Z", "D469", "D471", "C9200", "C9201", "C9202", "C9210", "C9211", "C9212", "C9220",
#                                   "C9221", "C9222", "C9230", "C9231", "C9232", "C9240", "C9241", "C9242", "C9250",
#                                   "C9251", "C9252", "C9290", "C9291", "C9292", "C92A0", "C92A1", "C92A2", "C92Z0",
#                                   "C92Z1", "C92Z2", "C9260", "C9261", "C9262", "C9300", "C9301", "C9302", "C9310",
#                                   "C9311", "C9312", "C9330", "C9331", "C9332", "C9390", "C9391", "C9392", "C93Z0",
#                                   "C93Z1", "C93Z2", "C946", "D45", "D473", "D474", "D7581", "C9620", "C9622", "C9629"]
# for c in code_list:
#   # checking if a code is ICD, NPC, or procedure
#   if len(c) >= 6:
#     code_record = {'code': f'{c}', 'code_type': 'ndc'}
#   elif c[0] == 'R' or c[0] == 'C' or c[0] == 'D' or c[0] == 'Z':
#     code_record = {'code': f'{c}', 'code_type': 'icd'}
#   elif c[0] == 'A' or c[0] == 'J':
#     code_record = {'code': f'{c}', 'code_type': 'procedure'}
#   else:
#     warns.append(c)
#     code_record = {'code': f'{c}', 'code_type': 'warning'}
#   codes_for_group.append(code_record)
# ucc_enrich_agg_setting['codes'] = codes_for_group
# ucc_enrich_agg_setting['event_name'] = str(code_group)
# ucc_enrich_agg_setting['fieldname'] = str(code_group)
# # print('***',ucc_enrich_agg_setting)
# claims_enrichment.append(ucc_enrich_agg_setting)
