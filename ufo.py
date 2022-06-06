import pandas as pd
import csv 
import matplotlib.pyplot as plt

#read ufo csv
dfufo  = pd.read_csv('csv/ufo_data_nuforc.csv')
#read sat score csv total
dfsat = pd.read_csv('csv/sat.csv', usecols = ['Total']).reset_index(drop=True)
dfsat = dfsat[dfsat.iloc[:,0] != 950].reset_index(drop=True)
#read us states csv 
dfstates = pd.read_csv('csv/usstates.csv', usecols = ['State'])
dfstates = dfstates[dfstates['State'] != 'District of Columbia'].reset_index(drop=True)

#total ufo sightings by state
dfbystate = dfufo.groupby(['state']).size().to_frame().reset_index(drop=True)

dfbystate.to_csv(f'csv/ufosightingsbystate.csv', index= False)

#ufo sightings by state 
ufostate = pd.merge(dfstates, dfbystate, left_index=True, right_index=True)
#ufo sightings by state with sat scores
ufo_state_sat = pd.merge(ufostate, dfsat, left_index=True, right_index=True)
ufo_state_sat = ufo_state_sat.rename(columns={0: 'Sightings', "Total": "SAT Score"})

def conditions(s):
    if (s['SAT Score'] < 1050):
        return 'Low'
    elif (s['SAT Score'] < 1100 and s['SAT Score'] >= 1050):
        return 'Medium'
    elif (s['SAT Score'] >= 1150) :
        return 'High'

#apply above method
ufo_state_sat['SAT Criteria'] = ufo_state_sat.apply(conditions, axis=1)

ufo_state_sat = ufo_state_sat.groupby(['SAT Criteria'])['Sightings'].sum()
ufo_state_sat.plot(kind='bar',x='SAT Criteria',y='Sightings')
#plt.show()

#print(ufo_state_sat)



