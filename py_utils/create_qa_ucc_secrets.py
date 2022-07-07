import boto3
import json

c = boto3.client('secretsmanager')

# secret_name = 'qa_dev/pulse/ucc_token'
# secret_name = 'qa_staging/pulse/ucc_token'
secret_name = 'qa_regression/pulse/ucc_token'
# secret_name = 'qa_automation/pulse/ucc_token'

secrets = {
	'GUCCI_TOKEN':'pulse-test-profile-9ad49d7d-d30e-42c7-a50f-7deb8e861ab1',
	'GUCCI_TOKEN_SOW15':'pulse-sow-15-c8a51009-b835-4d90-91f4-c6036d962728',
	'STATUS_REFRESH_TOKEN':'TEMPTOKEN_TILL_AUG2021_msklso',
	'GUCCI_TOKEN_SOW0':'pulse-sow-0-677a0410-7772-4f01-897d-18d39f1d6773',
	'GUCCI_TOKEN_SOW900':'pulse-sow-900-fa9031c5-59b4-4543-94a3-94708b04b5c0',
	'GUCCI_TOKEN_SOW901':'pulse-sow-901-4bab985e-8262-40d7-9c1b-cf9f8ad3ff52',
	'GUCCI_TOKEN_SOW900-0':'pulse-sow-900-0-ec87af8e-9fbf-42b0-9b02-402a850162bd'
}
tags = [
	{
		'Key': 'nest',
		'Value': 'pulse'
	},
	{
		'Key': 'Env',
		'Value': 'dev'
	},
	{
		'Key': 'Nest',
		'Value': 'pulse'
	},
	{
		'Key': 'LAST_GOV_RULE_APPLIED',
		'Value': 'Secrets_Tagging@2022-03-18 02:12:28'
	}
]

args = {
	'Name': secret_name,
	'Description': 'QA token for UCC',
	'SecretString': json.dumps(secrets),
	'Tags': tags
}

res = c.create_secret(**args)
print(res)


