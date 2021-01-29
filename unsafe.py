import csv
import gmplot
import matplotlib.pyplot as plt

#chicago 2020 Jan 23 -2021 Jan 16? (I think it updates to a year ago to now)
chicago_list = [1,2,4,5,14,15,16]
chicago_dict = {'DATE  OF OCCURRENCE':0, 'BLOCK':1, ' PRIMARY DESCRIPTION':2, ' SECONDARY DESCRIPTION':3, 'LATITUDE':4, 'LONGITUDE':5, 'LOCATION': 6}
chicago_crimes = [4,5]
chicago_streetnames = 'BLOCK'
loc_to_info = {'chicago':[chicago_list,chicago_dict,'chicago_crimes.csv',chicago_crimes, chicago_streetnames],}



def fielder(loc):
    field_to_col_num =  loc_to_info[loc][1]
    field_list = loc_to_info[loc][0]
    source = loc_to_info[loc][2]
    field_names = []
    with open(source) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            column_count = 0
            if line_count == 0:
                for column in row:
                    if column_count in field_list:
                        field_names.append(column)
                    column_count += 1
            line_count += 1
    return field_names

#print(fielder('chicago'))

"""finds all crime related to that category"""
#use 'VEHICLE' for chicago
def crime_source_finder(loc,category):
    field_list = loc_to_info[loc][0]
    source = loc_to_info[loc][2]
    category_colnums = loc_to_info[loc][3]
    categorical_crimes = []
    with open(source) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        found = False
        for row in csv_reader:
            column_count = 0
            row_info = []
            for colnum in category_colnums:
                if category in row[colnum]:
                    found = True
            if found == True:
                for colnum in category_colnums:
                    if 'VIN' in row[colnum] or 'REGISTRATION' in row[colnum] or 'MOTOR' in row[colnum] or 'TITLE' in row[colnum]:
                        found = False
            if found == True:
                for column in row:
                    if column_count in field_list:
                        row_info.append(column)
                    column_count += 1
                categorical_crimes.append(row_info)
            found = False            
        line_count += 1
    return categorical_crimes

chicago_vehicle_crimes = crime_source_finder('chicago','VEHICLE')

def list_coordinates(crash_table):
    coorlist = []
    for row in crash_table:
        coor_num_list = []
        coorstring = row[6]
        coorstripped = coorstring[1:-1]
        coor_str_list = coorstripped.split(', ')
        for coor in coor_str_list:
            if not coor:
                break
            else:
                coor_num_list.append(float(coor))
        try:
            coorlist.append((coor_num_list[0],coor_num_list[1]))
        except:
            pass
    return coorlist

chicago_vehicle_coors = list_coordinates(chicago_vehicle_crimes)

def allcrimes(loc):
    field_list = loc_to_info[loc][0]
    source = loc_to_info[loc][2]
    allcrimes = []
    with open(source) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            column_count = 0
            row_info = []
            for column in row:
                if column_count in field_list:
                    row_info.append(column)
                column_count += 1
            allcrimes.append(row_info)          
        line_count += 1
    return allcrimes

#chicago_crimes = allcrimes('chicago')

"""given crash table, talleys field name"""
def counter(loc,crash_table,field_name):
    field_to_col_num =  loc_to_info[loc][1]
    seen = set()
    counts = {}
    col_num = field_to_col_num[field_name]
    row_num = 0
    for row in crash_table:
        if row_num == 0:
            pass
        else:
            if field_name == 'DATE  OF OCCURRENCE':
                field = int(row[col_num][11:13])
                am_pm = row[col_num][20:22]
                if am_pm == 'PM':
                    field = field + 12
                field = str(field)
            elif field_name == 'BLOCK':
                field = row[col_num][6:]
            else:
                field = row[col_num]
            if field not in seen:
                seen.add(field)
                counts[field] = 1
            else:
                counts[field] = counts[field] + 1     
        row_num += 1
    return counts

#crimesperhour = counter('chicago',chicago_vehicle_crimes,'DATE  OF OCCURRENCE')
#print(counter('chicago',chicago_vehicle_crimes,' SECONDARY DESCRIPTION'))
#print(counter('chicago', chicago_vehicle_crimes, 'BLOCK'))

def freqgrapher(freq_table):
    yvals = []
    xvals = []
    try:
        int(freq_table.keys().pop())
        for field in freq_table.keys():
            xvals.append(int(field))
        xvals.sort()
        for field in xvals:
            yvals.append(freq_table[str(field)])
        plt.plot(xvals,yvals)
        plt.show()
        return
    except:
        for field in freq_table.keys():
            yvals.append(field)
            xvals.append(freq_table[str(field)])
        plt.plot(xvals,yvals)
        plt.show()
        return

#freqgrapher(crimesperhour)

def high_freq(loc,crash_table,freqval,category):
    freqcounts = counter(loc,crash_table,category)
    highfreqs = {}
    for cat in freqcounts.keys():
        if freqcounts[cat] > freqval:
            highfreqs[cat] = freqcounts[cat]
    return highfreqs


#print(high_freq('chicago',chicago_vehicle_crimes,50,'BLOCK'))
#print(high_freq('chicago',chicago_vehicle_crimes,700,'DATE  OF OCCURRENCE'))
#print(high_freq('chicago', chicago_crimes,500,'BLOCK'))
#freqgrapher(high_freq('chicago',chicago_vehicle_crimes,50,'BLOCK'))
#not coordinates tho
def print_all_fieldcounts(loc,crash_table):
    field_to_col_num =  loc_to_info[loc][1]
    source = loc_to_info[loc][2]
    for field_name in field_to_col_num.keys():
        if field_name == 'DATE OF OCCURENCE':
            hour_count = counter(loc,crash_table,field_name)
            print('hour')
            print(hour_count)
        elif field_name.upper()!='LATITUDE' and field_name.upper()!='LONGITUDE' and field_name.lower()!='coordinates' and field_name.lower()!='location':
            print(field_name)
            print(counter(loc,crash_table,field_name))
    return

#print_all_fieldcounts('chicago',chicago_vehicle_crimes)
#print_all_fieldcounts('chicago',chicago_crimes)



def mapify(loc):
    apikey = 'AIzaSyCwavs9SsjAqCXhWXBRhl2vVB6RM3egItM'
    gmap = gmplot.GoogleMapPlotter(41.8, -87.7, 14, apikey=apikey)
    zip(*chicago_vehicle_coors)
    gmap.scatter(*zip(*chicago_vehicle_coors), color='#3B0B39', size=40, marker=False)
    gmap.draw( "C:\\Users\\user\\Desktop\\newmap.html" ) 
    return


mapify('chicago')


"""
with open("car_crime.csv", 'w', newline = '') as csvfile:
    fieldnames = ['latitude', 'longitude']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
"""