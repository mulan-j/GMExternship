from sklearn.cluster import OPTICS, cluster_optics_dbscan
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import csv
import gmplot

#opening chicago crime data
with open('chicago_crimes.csv') as file:
    csv_reader = csv.reader(file, delimiter=',')
    count = 0
    latitude = []
    longitude = []
    for row in csv_reader:
        if count == 0:
            count += 1
        else:
            #if "VEHICLE" in row[4] or "VEHICLE" in row[5]:
            if "TO VEHICLE" in row[5] or 'VEHICULAR' in row[5]:
                if row[14] == '' or row[15] == '':
                    count += 1
                else:
                    latitude.append(float(row[14]))
                    longitude.append(float(row[15]))

coordinates = []
for i in range(0, len(latitude)):
    #latitude[i] = latitude[i] - 48.88
    #longitude[i] = longitude[i] + 87.63
    coordinates = [latitude[i],longitude[i]]
print(len(latitude))

#overlaying an image
img = plt.imread("chicago.png")
fig, ax = plt.subplots()
#ax.imshow(img, extent = [-7.5, -5.9, -.5, .5])
#ax.plot(latitude[:len], longitude[:len], '.')
#plt.show()

with open("car_crime_filtered.csv", 'w', newline = '') as csvfile:
    fieldnames = ['latitude', 'longitude']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    for i in range(0, len(latitude)):
        writer.writerow([str(latitude[i]), str(longitude[i])])

'''#okay time to try the google maps
apikey = 'AIzaSyDzpharH9YLTJyBuM3mZRW9ZV48QdIOc7U'
gmap  = gmplot.GoogleMapPlotter(41.88, 87.63, 40, apikey = apikey)

len = len(latitude)
print(len)
gmap.scatter(latitude[:5], longitude[:5], color = '#3B0B39', size=40, marker=False)
gmap.draw('map.html')'''

'''gmap = gmplot.GoogleMapPlotter(37.766956, -122.448481, 14, apikey=apikey)

# Highlight some attractions:
attractions_lats, attractions_lngs = zip(*[
    (37.769901, -122.498331),
    (37.768645, -122.475328),
    (37.771478, -122.468677),
    (37.769867, -122.466102),
    (37.767187, -122.467496),
    (37.770104, -122.470436)
])
gmap.scatter(attractions_lats, attractions_lngs, color='#3B0B39', size=40, marker=False)

# Mark a hidden gem:
gmap.marker(37.770776, -122.461689, color='cornflowerblue')

# Draw the map:
gmap.draw('map.html')'''
