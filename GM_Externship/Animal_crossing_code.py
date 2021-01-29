# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:13:30 2021

@author: jawad yousef
"""

#Classifying "unsafe" traffic conditions and systematic isolation of said conditions

#Going to use police data and Community Crime Map Data

import gmplot
import gmaps
import gmaps.datasets
from pandas import DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns; sns.set()
import csv
#
##To Break up chicago crash data


counter = 0
pandas_list = []
with open('Traffic_Crashes_-_Crashes.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if counter == 0:
            pandas_list.append(row)
            counter += 1
            
        elif row[9] == 'ANIMAL' :
            pandas_list.append(row)
            
        elif row[22] == 'EVASIVE ACTION DUE TO ANIMAL, OBJECT, NONMOTORIST':
            pandas_list.append(row)
            
        elif row[23] == 'EVASIVE ACTION DUE TO ANIMAL, OBJECT, NONMOTORIST':
            pandas_list.append(row)


column_names = pandas_list.pop(0)
data = pd.DataFrame(pandas_list, columns=column_names) 

#Removing Un-needed colomns
not_needed = ['CRASH_RECORD_ID','RD_NO','CRASH_DATE_EST_I','TRAFFIC_CONTROL_DEVICE','DEVICE_CONDITION','LANE_CNT','ALIGNMENT','ROAD_DEFECT','REPORT_TYPE',
              'INTERSECTION_RELATED_I','NOT_RIGHT_OF_WAY_I','HIT_AND_RUN_I','PHOTOS_TAKEN_I','STATEMENTS_TAKEN_I','DOORING_I','WORK_ZONE_I','WORK_ZONE_I',
              'WORKERS_PRESENT_I','NUM_UNITS','MOST_SEVERE_INJURY','INJURIES_REPORTED_NOT_EVIDENT','INJURIES_NO_INDICATION','LOCATION']


data.drop(not_needed, inplace=True, axis=1, errors='ignore')

#Debugging
#data.to_csv(r'Visual_data.csv', index = False)


new_data = [data['LATITUDE'][12:], data['LONGITUDE'][12:]]
#
headers = ['LATITUDE','LONGITUDE']
df3 = pd.concat(new_data, axis=1, keys=headers)
df3['LATITUDE'] = df3['LATITUDE'].astype(float)
df3['LONGITUDE'] = df3['LONGITUDE'].astype(float)
#
##debugging

#df3.to_csv(r'longlatnew.csv', index = False)
#
#
##KMeans Clustering
##Elbow Curve
K_clusters = range(1,20)
kmeans = [KMeans(n_clusters=i) for i in K_clusters]
X_axis = df3[['LATITUDE']]
Y_axis = df3[['LONGITUDE']]
score = [kmeans[i].fit(X_axis).score(X_axis) for i in range(len(kmeans))]
plt.plot(K_clusters, score)
plt.xlabel('Number of Clusters')
plt.ylabel('Score')
plt.title('Elbow Curve')
plt.show()
#
##The Actual Clustering
kmeans = KMeans(n_clusters=3).fit(df3)
centroids = kmeans.cluster_centers_
print(centroids)
up_top= kmeans.labels_.astype(float)
plt.scatter(df3['LONGITUDE'],df3['LATITUDE'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.show()

#Attempt at DBSCAM
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df3)
# cluster the data into five clusters
dbscan = DBSCAN(eps=0.08, min_samples = 5)
clusters = dbscan.fit_predict(X_scaled)

# plot the cluster assignments
plt.scatter(df3['LONGITUDE'],df3['LATITUDE'], c=clusters, cmap="plasma")
plt.xlabel("Feature 0")
plt.ylabel("Feature 1")

#To deal with Washington State Data
#Very Detailed Such as Deer, Elk, Bear, Raccoon, etc.

def washington_break_down(filed):
    pandas_list = []
    header = None
    damage_counter = 0
    loc_dict = {}
    light_dict = {}
    city_dict = {}
    
    counter = 0
    with open(filed, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if counter == 0:
                header = row 
                counter += 1
            else:
                pandas_list.append(row)
                
    data = pd.DataFrame(pandas_list, columns=header) 
    for x in data['Primary Trafficway']:
        if x.strip() in loc_dict:
            loc_dict[x.strip()] += 1
        else:
            loc_dict[x.strip()] = 1
            
    for x in data['Secondary Trafficway']:
        if x.strip() in loc_dict:
            loc_dict[x.strip()] += 1
        else:
            loc_dict[x.strip()] = 1
            
    for x in data['Lighting Condition']:
        if x in light_dict:
            light_dict[x] += 1
        else:
            light_dict[x] = 1

    for x in data['Damage Threshold Met']:
        if x == 'Y':
            damage_counter += 1000
    for x in data['City']:
        if x in city_dict:
            city_dict[x] += 1
        else:
            city_dict[x] = 1
    
    return damage_counter

#Debugging
#print(washington_break_down('WA_Crash_Summary_deer.csv'))

         
#To Go through Vermont state data       
def vermont_deer(filed):
    pandas_list = []
    header = None
    counter = 0
    lat = []
    long = []
    
    with open(filed, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if counter == 0:
                header = row 
                counter += 1
            else:
                pandas_list.append(row)
    data = pd.DataFrame(pandas_list, columns=header) 
    for x in data['Coordinates']:
        if len(x) > 2:
            chunks = x.split(',')
            lat.append(chunks[0])
            long.append(chunks[1])
    diction = {'lat' : lat, 'long':long}
    newdf = pd.DataFrame(diction)

    K_clusters = range(1,20)
    kmeans = [KMeans(n_clusters=i) for i in K_clusters]
    Y_axis = newdf[['lat']]
    X_axis = newdf[['long']]
    score = [kmeans[i].fit(X_axis).score(Y_axis) for i in range(len(kmeans))]
    plt.plot(K_clusters, score)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Score')
    plt.title('Elbow Curve')
    plt.show()
    
    #The Actual Clustering
    kmeans = KMeans(n_clusters=2).fit(newdf)
    centroids = kmeans.cluster_centers_
    print(centroids)
    
    w= kmeans.labels_.astype(float)
    print(w)
    
    plt.scatter(Y_axis, X_axis,c= w, s=50, alpha=0.5)
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
    plt.show()

print(vermont_deer('vt_anim_crashes.csv'))

    
#Attempted code on working with Google Maps
#It very much didnt like my API key
#________________________________________________
#
#gmaps.configure(api_key = key)
#earth = gmaps.datasets.load_dataset_as_df('earthquakes')
#print(earth.head())
#
#locations = earth[['latitude','longitude']]
#weights = earth['magnitude']
#fig = gmaps.figure()
#fig.add_layer(gmaps.heatmap_layer(locations,weights=weights))
#fig

#gps = []
#zipped = zip(data['LATITUDE'], data['LONGITUDE'])
#print(list(zipped))

#gmap1 = gmplot.GoogleMapPlotter.from_geocode("Chicago, USA")
#gmap1.scatter( data['LATITUDE'], data['LONGITUDE'], '# FF0000', size = 40, marker = False) 
#gmap1.draw( "C:\\Users\\user\\Desktop\\map12.html" ) 


    
#print(data['LATITUDE'], data['LONGITUDE'])

#df = pd.read_csv('Traffic_Crashes_-_Crashes.csv')
#
#animal_related = 

