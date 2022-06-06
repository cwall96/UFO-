import pandas as pd
import csv 
import matplotlib.pyplot as plt

#read ghost csv
dfghost  = pd.read_csv('csv/haunted_places.csv')

#total bigfoot sightings by state
dfbystate = dfghost.groupby(['state']).size().to_frame()

dfbystate.to_csv(f'csv/hauntedplacesbystate.csv', index = False )