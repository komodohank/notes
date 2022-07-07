s = '''
codes:
      - code: D460
        code_type: icd
      - code: D4709
        code_type: icd
      - code: D461
        code_type: icd
      - code: D4620
        code_type: icd
      - code: D4621
        code_type: icd
      - code: D4622
        code_type: icd
      - code: D46A
        code_type: icd
      - code: D46B
        code_type: icd
      - code: D46C
        code_type: icd
      - code: D464
        code_type: icd
      - code: D46Z
        code_type: icd
      - code: D469
        code_type: icd
      - code: D471
        code_type: icd
      - code: C9200
        code_type: icd
      - code: C9201
        code_type: icd
      - code: C9202
        code_type: icd
      - code: C9210
        code_type: icd
      - code: C9211
        code_type: icd
      - code: C9212
        code_type: icd
      - code: C9220
        code_type: icd
      - code: C9221
        code_type: icd
      - code: C9222
        code_type: icd
      - code: C9230
        code_type: icd
      - code: C9231
        code_type: icd
      - code: C9232
        code_type: icd
      - code: C9240
        code_type: icd
      - code: C9241
        code_type: icd
      - code: C9242
        code_type: icd
      - code: C9250
        code_type: icd
      - code: C9251
        code_type: icd
      - code: C9252
        code_type: icd
      - code: C9290
        code_type: icd
      - code: C9291
        code_type: icd
      - code: C9292
        code_type: icd
      - code: C92A0
        code_type: icd
      - code: C92A1
        code_type: icd
      - code: C92A2
        code_type: icd
      - code: C92Z0
        code_type: icd
      - code: C92Z1
        code_type: icd
      - code: C92Z2
        code_type: icd
      - code: C9260
        code_type: icd
      - code: C9261
        code_type: icd
      - code: C9262
        code_type: icd
      - code: C9300
        code_type: icd
      - code: C9301
        code_type: icd
      - code: C9302
        code_type: icd
      - code: C9310
        code_type: icd
      - code: C9311
        code_type: icd
      - code: C9312
        code_type: icd
      - code: C9330
        code_type: icd
      - code: C9331
        code_type: icd
      - code: C9332
        code_type: icd
      - code: C9390
        code_type: icd
      - code: C9391
        code_type: icd
      - code: C9392
        code_type: icd
      - code: C93Z0
        code_type: icd
      - code: C93Z1
        code_type: icd
      - code: C93Z2
        code_type: icd
      - code: C946
        code_type: icd
      - code: D45
        code_type: icd
      - code: D473
        code_type: icd
      - code: D474
        code_type: icd
      - code: D7581
        code_type: icd
      - code: C9620
        code_type: icd
      - code: C9622
        code_type: icd
      - code: C9629
        code_type: icd
      - code: C9330
        code_type: icd
      - code: C9331
        code_type: icd
      - code: C9332
        code_type: icd
      - code: C9390
        code_type: icd
      - code: C9391
        code_type: icd
      - code: C9392
        code_type: icd
      - code: C93Z0
        code_type: icd
      - code: C93Z1
        code_type: icd
      - code: C93Z2
        code_type: icd
      - code: C946
        code_type: icd
      - code: D45
        code_type: icd
      - code: D473
        code_type: icd
      - code: D474
        code_type: icd
      - code: D7581
        code_type: icd
      - code: C9622
        code_type: icd
      - code: C9629
        code_type: icd
'''
import yaml
y_codes = yaml.safe_load(s)
seen = set()
dup = []
codes = y_codes['codes']
for i in codes:
	c = i['code']
	if c not in seen:
		seen.add(c)
	else:
		dup.append(c)

print(dup)
new_y = []
for c in seen:
	temp = {'code': c, 'code_type': 'icd'}
	new_y.append(temp)
print(yaml.dump(new_y))
print(len(new_y))
'''code_str =

codes = code_str.split('\n')
unique = set(codes)
code_list = list(unique)
code_list.sort()
d = {'rx_codes': code_list}
print(code_list)
import yaml
print(yaml.dump(d))'''