import pandas as pd

pulseDir = '~/Documents/KH_Janssen_RD_CD_Pulse_Deliverable_20211228.csv'
ciaoDir = '~/Documents/ciaoJJ.csv'

pulse = pd.read_csv(pulseDir)
ciao = pd.read_csv(ciaoDir)

coreCols = ['NPI', 'HCOName', 'GALAXI Site', 'Distance from GALAXI']
ciaoCols = ['NPI', 'HCOName', 'GALAXI_Site', 'GALAXI_Distance']

pulsedf = pulse[coreCols]
ciaodf = ciao[ciaoCols]

joined = pd.merge(pulsedf, ciaodf, how='inner', on='NPI')

joined.to_csv('~/Documents/joinedJJ.csv')

