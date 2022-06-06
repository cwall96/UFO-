import pandas as pd
import csv 
import matplotlib.pyplot as plt

#read bigfoot csv
dfbigfoot = pd.read_csv('csv/bfro_reports_geocoded.csv')

#total bigfoot sightings by state
dfbystate = dfbigfoot.groupby(['state']).size().to_frame()
dfbystate.columns = ['Sightings']
dfbystate = dfbystate['Sightings'].replace(1,0).reset_index(drop=True)

dfbystate.to_csv(r'csv/bfsightingsbystate.csv', index=False)

#read sat score csv total
dfsat = pd.read_csv('csv/sat.csv', usecols = ['Total']).reset_index(drop=True)
dfsat = dfsat.rename(columns={ "Total": "SAT Score"})

#print(dfsat)

def conditions(s):
    if (s['SAT Score'] < 1050):
        return 'Low'
    elif (s['SAT Score'] < 1100 and s['SAT Score'] >= 1050):
        return 'Medium'
    elif (s['SAT Score'] >= 1150) :
        return 'High'

bigfoot_sat = pd.merge(dfbystate, dfsat, left_index=True, right_index=True)

#apply above method
bigfoot_sat['SAT Criteria'] = bigfoot_sat.apply(conditions, axis=1)

#print(bigfoot_sat)

bigfoot_sat = bigfoot_sat.groupby(['SAT Criteria'])['Sightings'].sum()
bigfoot_sat.plot(kind='bar',x='SAT Criteria',y='Sightings')
#plt.show()


