import yaml 

codes = '''D460
D461
D4620
D4621
D4622
D46A
D46B
D46C
D464
D46Z
D469
D471
C9200
C9201
C9202
C9210
C9211
C9212
C9220
C9221
C9222
C9230
C9231
C9232
C9240
C9241
C9242
C9250
C9251
C9252
C9290
C9291
C9292
C92A0
C92A1
C92A2
C92Z0
C92Z1
C92Z2
C9260
C9261
C9262
C9300
C9301
C9302
C9310
C9311
C9312
C9330
C9331
C9332
C9390
C9391
C9392
C93Z0
C93Z1
C93Z2
C946
D45
D473
D474
D7581
C9622
C9629'''

code_list = codes.split('\n')
code_list = set(code_list)

cl_enrich_codes = []
for c in code_list:
	cl_enrich_codes.append({'code': c, 'code_type': 'icd'})

y_codes = yaml.dump(cl_enrich_codes)
print(y_codes)
print(len(cl_enrich_codes))