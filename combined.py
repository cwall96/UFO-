import pandas as pd
import csv 
import matplotlib.pyplot as plt
from scipy.stats import pearsonr,spearmanr
import numpy as np

#read main csvs
dfbigfootsightings = pd.read_csv('csv/bfsightingsbystate.csv').reset_index(drop=True)
dfufosightings = pd.read_csv('csv/ufosightingsbystate.csv').reset_index(drop = True)
dfhaunted = pd.read_csv('csv/hauntedplacesbystate.csv').reset_index(drop=True)

#read us states csv 
dfstates = pd.read_csv('csv/usstates.csv', usecols = ['State'])
dfstates = dfstates[dfstates['State'] != 'District of Columbia'].reset_index(drop=True)

#read population csv
dfpopulation = pd.read_csv('csv/population.csv', usecols =['STATE', 'POPESTIMATE2019'])
dfpopulation = dfpopulation[dfpopulation['STATE'] != 'District of Columbia'].reset_index(drop=True)
dfpopulation = dfpopulation.drop('STATE', axis=1)

#gdp csv
dfgdp = pd.read_csv('csv/gdp.csv', usecols=['Area', '2017'])
dfgdp = dfgdp[dfgdp['Area'] != 'District of Columbia'].reset_index(drop=True)
dfgdp = dfgdp[dfgdp['Area'] != 'United States'].reset_index(drop=True)
dfgdp = dfgdp[: 50]

#read sat score csv total
dfsat = pd.read_csv('csv/sat.csv', usecols = ['Total']).reset_index(drop=True)
dfsat = dfsat.rename(columns={ "Total": "SAT Score"})

#read forest csv
dfforest = pd.read_csv('csv/forestedstates.csv').sort_values(by=['State']).reset_index(drop=True)
dfforest = dfforest.drop('State', axis=1)

#read us govenors csv
dfparty = pd.read_csv('csv/us-governors.csv', usecols=['party']).reset_index(drop=True)
dfparty['party'] = dfparty['party'].map({'republican': 1, 'democrat': 0})

dfethnicity = pd.read_csv('csv/ethnicity.csv', usecols=['State', 'WhiteTotalPerc'])
dfethnicity = dfethnicity[dfethnicity['State'] != 'District of Columbia'].reset_index(drop=True)
dfethnicity = dfethnicity.drop('State', axis=1)

dftemp = pd.read_csv('csv/temperature.csv', usecols=['State', 'Avg °C']).reset_index(drop=True)
dftemp = dftemp.drop('State', axis=1)

dfcombined = pd.merge(dfbigfootsightings, dfufosightings, left_index=True, right_index=True)
dfcombined = pd.merge(dfstates, dfcombined, left_index=True, right_index=True)
dfcombined = pd.merge(dfcombined, dfpopulation, left_index=True,right_index=True)
dfcombined = pd.merge(dfcombined, dfgdp, left_index=True, right_index=True)
dfcombined = pd.merge(dfcombined, dfsat, left_index=True, right_index=True)
dfcombined = pd.merge(dfcombined, dfhaunted, left_index=True, right_index=True)
dfcombined = pd.merge(dfcombined, dfforest,left_index=True, right_index=True)
dfcombined = pd.merge(dfcombined, dfparty, left_index=True, right_index=True)
dfcombined = pd.merge(dfcombined, dfethnicity, left_index=True, right_index=True)
dfcombined = pd.merge(dfcombined, dftemp, left_index=True, right_index=True)

#combine state comparison and sat comparison
dfcombined = dfcombined.rename(columns={'Sightings': 'Bigfoot', '0_x': "UFO", '0_y' : 'Haunted Locations', 'POPESTIMATE2019': 'Population', '2017':'GDP Per Capita', 'forestArea':'Forest', 'WhiteTotalPerc':'WhitePop', 'Avg °C':'AverageTemp'})

#percapita calculations
dfcombined['Bigfoot Per Capita'] = dfcombined['Bigfoot'] / dfcombined['Population'] * 1000000
dfcombined['UFO Per Capita'] = dfcombined['UFO'] / dfcombined['Population'] * 1000000
dfcombined['Haunted Per Capita'] = dfcombined['Haunted Locations'] / dfcombined['Population'] * 1000000
#rank by ufo and bigfoot sightings
dfcombined["Bigfoot Rank"] = dfcombined["Bigfoot Per Capita"].rank(ascending = False)
dfcombined["UFO Rank"] = dfcombined["UFO Per Capita"].rank(ascending = False)
dfcombined["SAT Rank"] = dfcombined['SAT Score'].rank(ascending= False)
dfcombined['Haunted Rank'] = dfcombined['Haunted Per Capita'].rank(ascending=False)
dfcombined['GDP Rank'] = dfcombined['GDP Per Capita'].rank(ascending=False)
dfcombined['Total'] = dfcombined['Bigfoot Rank'] + dfcombined['UFO Rank'] + dfcombined['Haunted Rank']
dfcombined['Total Rank'] = dfcombined['Total'].rank(ascending=False)
dfcombined['Forest Rank'] = dfcombined['Forest'].rank(ascending=False)
dfcombined['WhitePop Rank'] = dfcombined['WhitePop'].rank(ascending=False)
dfcombined['Temp Rank'] = dfcombined['AverageTemp'].rank(ascending=True)
#plot combined df
dfcombined.plot(x="State", y=["Bigfoot Rank", "UFO Rank"], kind="barh")
#plt.show()
print('--------------------------------------')
print('Bigfoot and UFO Correlation')
corr1, _ = pearsonr(dfcombined['Bigfoot Rank'], dfcombined['UFO Rank'])
print('Pearsons correlation: %.3f' % corr1)
print(_)
dfrankonly = dfcombined[['Bigfoot Rank', 'UFO Rank']]
print(dfrankonly.corr(method ='kendall'))

print('--------------------------------------')
print('SAT and Bigfoot Correlation')
corr2, _ = pearsonr(dfcombined['SAT Rank'], dfcombined['Bigfoot Rank'])
print('Pearsons correlation: %.3f' % corr2)
print(_)
satandbf = dfcombined[['SAT Rank', 'Bigfoot Rank']]
print(satandbf.corr(method ='kendall'))

print('--------------------------------------')
print('SAT and UFO Correlation')
corr3, _ = pearsonr(dfcombined['SAT Rank'], dfcombined['UFO Rank'])
print('Pearsons correlation: %.3f' % corr3)
print(_)
satandufo = dfcombined[['SAT Rank', 'Bigfoot Rank']]
print(satandufo.corr(method ='kendall'))

print('--------------------------------------')
print('UFO and Haunted Correlation')
corr4, _ = pearsonr(dfcombined['UFO Rank'], dfcombined['Haunted Rank'])
print('Pearsons correlation: %.3f' % corr4)
print(_)
ufonandhaunt = dfcombined[['UFO Rank', 'Haunted Rank']]
print(ufonandhaunt.corr(method ='kendall'))

print('--------------------------------------')
print('Bigfoot and Haunted Correlation')
corr5, _ = pearsonr(dfcombined['Bigfoot Rank'], dfcombined['Haunted Rank'])
print('Pearsons correlation: %.3f' % corr5)
print(_)
bigandhaunt = dfcombined[['Bigfoot Rank', 'Haunted Rank']]
print(bigandhaunt.corr(method ='kendall'))

print('--------------------------------------')
print('SAT and Haunted Correlation')
corr6, _ = pearsonr(dfcombined['SAT Rank'], dfcombined['Haunted Rank'])
print('Pearsons correlation: %.3f' % corr6)
print(_)
satandhaunt = dfcombined[['SAT Rank', 'Haunted Rank']]
print(satandhaunt.corr(method ='kendall'))

print('--------------------------------------')
print('GDP and Haunted Correlation')
corr7, _ = pearsonr(dfcombined['GDP Rank'], dfcombined['Haunted Rank'])
print('Pearsons correlation: %.3f' % corr7)
print(_)
gdpandhaunt = dfcombined[['GDP Rank', 'Haunted Rank']]
print(gdpandhaunt.corr(method ='kendall'))

print('--------------------------------------')
print('GDP and Bigfoot Correlation')
corr8, _ = pearsonr(dfcombined['GDP Rank'], dfcombined['Bigfoot Rank'])
print('Pearsons correlation: %.3f' % corr8)
print(_)
gdpandbig = dfcombined[['GDP Rank', 'Bigfoot Rank']]
print(gdpandbig.corr(method ='kendall'))

print('--------------------------------------')
print('Forest and Bigfoot Correlation')
corr9, _ = pearsonr(dfcombined['Forest Rank'], dfcombined['Bigfoot Rank'])
print('Pearsons correlation: %.3f' % corr9)
print(_)
forestandbig = dfcombined[['Forest Rank', 'Bigfoot Rank']]
print(forestandbig.corr(method ='kendall'))

print('--------------------------------------')
print('Party and Bigfoot Correlation')
corr10, _ = pearsonr(dfcombined['party'], dfcombined['Bigfoot'])
print('Pearsons correlation: %.3f' % corr10)
print(_)
partyandbig = dfcombined[['party', 'Bigfoot']]
print(partyandbig.corr(method ='kendall'))

print('--------------------------------------')
print('WhitePop and Bigfoot Correlation')
corr11, _ = pearsonr(dfcombined['WhitePop Rank'], dfcombined['Bigfoot Rank'])
print('Pearsons correlation: %.3f' % corr11)
print(_)
whiteandbig = dfcombined[['WhitePop Rank', 'Bigfoot Rank']]
print(whiteandbig.corr(method ='kendall'))

print('--------------------------------------')
print('Average Temperature and Bigfoot Correlation')
corr12, _ = pearsonr(dfcombined['Temp Rank'], dfcombined['Bigfoot Rank'])
print('Pearsons correlation: %.3f' % corr12)
print(_)
tempandbig = dfcombined[['Temp Rank', 'Bigfoot Rank']]
print(tempandbig.corr(method ='kendall'))


finalcombined = dfcombined[['State', 'Bigfoot Rank', 'UFO Rank', 'Haunted Rank', 'Forest Rank', 'WhitePop Rank','Total Rank',]]
print(finalcombined)
#dfcombined.plot(x="party", y=["Bigfoot Rank"], kind="barh")


import numpy as np
from sklearn.linear_model import LinearRegression

model = LinearRegression()

dfbigfootnp= dfcombined['Bigfoot Rank'].to_numpy().reshape(-1,1)
dfforestnp = dfcombined['Forest Rank'].to_numpy()

model.fit(dfbigfootnp, dfforestnp)

r_sq = model.score(dfbigfootnp, dfforestnp)
print('coefficient of determination:', r_sq)


from sklearn.feature_selection import f_regression

freg=f_regression(dfbigfootnp, dfforestnp)

p=freg[1]

print(p)

print('git test')
