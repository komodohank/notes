raw_codes = '''A9593
A9594
A9595
A9580
A9552
A9515
A9588
J9218
76394264203
71258002201
00469012599
00469072560
00469062599
62311070501
62559068030
54868450300
00310070510
00310070512
00310070530
00310070539
00310070595
54921070502
00074334603
00409362602
52125073601
54569452600
11532142101
11532142303
11532142602
11532142902
11532145000
11532145005
11532145101
11532145105
11532145201
11532145301
11532145401
11532333803
11532333808
11532366202
11532366206
00074969403
54868282500
00074105205
00074105210
00074105305
00074377903
54868327700
00074210803
00074228203
00074244003
00074347303
00074364103
00074364104
00074364107
00074364171
00074364203
00074366303
00074366304
00074368303
00300210801
00300228201
00300244001
00300361224
00300361228
00300364201
00300366301
00300368301
57894015012
57894015025
57894018412
57894019506
57894019515
59676060012
59676060056
59676060099'''

aggregation = 'max'
window = 1830
code_list = raw_codes.split('\n')
print(code_list)
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
claims_enrichment = []
codes_for_group, warns = [], []
for c in code_list:
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

