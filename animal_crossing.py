import csv
import matplotlib.pyplot as plt
import random

#chicago from 2013-now, vt 2015-2020, nyc 2015-2020
chicago_list = [7,8,9,10,13,22,23,26,45,46,47]
chicago_dict = {'WEATHER_CONDITION':0, 'LIGHTING_CONDITION':1, 'FIRST_CRASH_TYPE':2, 'TRAFFICWAY_TYPE':3, 'ROADWAY_SURFACE_COND':4, 'PRIM_CONTRIBUTORY_CAUSE':5, 'SEC_CONTRIBUTORY_CAUSE':6, 'STREET_NAME':7, 'CRASH_MONTH':8, 'LATITUDE':9, 'LONGITUDE':10}
chicago_animals = [9,22,23]
chicago_streetnames = 'STREET_NAME'
vt_list = [2,5,8,14,15,22,24,26]
vt_dict = {'Crash Date':0,'AOT Route':1, 'Weather':2, 'Animal':3, 'Time of Day':4, 'Road Condition':5, 'Surface Condition':6, 'Coordinates':7}
vt_animals = [14]
vt_streetnames = 'AOT Route'
nyc_list = [3,5,6,7,19]
nyc_dict = {'on_street_name':0, 'date_time':1, 'latitude':2, 'longitude':3, 'contributing_factors':4}
nyc_animals = [19]
nyc_streetnames = 'on_street_name'
loc_to_info = {'chicago':[chicago_list,chicago_dict,'chicago_crashes.csv',chicago_animals, chicago_streetnames],
                'vt':[vt_list,vt_dict,'vt_anim_crashes.csv',vt_animals, vt_streetnames],
                'nyc':[nyc_list,nyc_dict,'nyc_crashes.csv',nyc_animals,nyc_streetnames]}

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


"""enter animal name in string, finds all crashes related to that animal, one can also enter 'animal' """
#use 'ANIMAL' for chicago, and e.g. 'Deer' for vt, 
def crash_source_finder(loc,animal):
    field_to_col_num =  loc_to_info[loc][1]
    field_list = loc_to_info[loc][0]
    source = loc_to_info[loc][2]
    animals_colnums = loc_to_info[loc][3]
    anim_crashes = []
    with open(source) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        found = False
        for row in csv_reader:
            column_count = 0
            row_info = []
            for colnum in animals_colnums:
                if animal in row[colnum]:
                    found = True
            if found == True:
                for column in row:
                    if column_count in field_list:
                        row_info.append(column)
                    column_count += 1
                anim_crashes.append(row_info)
            found = False            
        line_count += 1
    return anim_crashes

#chicago_animal_crashes = crash_source_finder('chicago','ANIMAL')
vt_deer_crashes = crash_source_finder('vt','Deer')
#nyc_animal_crashes = crash_source_finder('nyc','Animal')

"""given crash table, talleys field name"""
def counter(loc,crash_table,field_name):
    field_to_col_num =  loc_to_info[loc][1]
    field_list = loc_to_info[loc][0]
    source = loc_to_info[loc][2]
    seen = set()
    counts = {}
    col_num = field_to_col_num[field_name]
    row_num = 0
    if field_name == 'date_time':
        monthseen = set()
        hourseen = set()
        monthcounts = {}
        hourcounts = {}
        for row in crash_table:
            if row_num == 0:
                pass
            else:
                month = row[col_num][5:7]
                hour = row[col_num][11:13]
                if month not in monthseen:
                    monthseen.add(month)
                    monthcounts[month] = 1
                else:
                    monthcounts[month] = monthcounts[month] + 1
                if hour not in hourseen:
                    hourseen.add(hour)
                    hourcounts[hour] = 1
                else:
                    hourcounts[hour] = hourcounts[hour] + 1
            row_num += 1
        return (monthcounts,hourcounts)
    elif field_name == 'Crash Date':
        monthseen = set()
        hourseen = set()
        monthcounts = {}
        hourcounts = {}
        for row in crash_table:
            if row_num == 0:
                pass
            else:
                month = row[col_num].split(' ')[0]
                hour = row[col_num][-8:-6]
                hour = int(hour)
                if row[col_num][-2:]=='PM':
                    hour = hour+12
                if month not in monthseen:
                    monthseen.add(month)
                    monthcounts[month] = 1
                else:
                    monthcounts[month] = monthcounts[month] + 1
                if hour not in hourseen:
                    hourseen.add(hour)
                    hourcounts[hour] = 1
                else:
                    hourcounts[hour] = hourcounts[hour] + 1
            row_num += 1
        return (monthcounts,hourcounts)
    for row in crash_table:
        if row_num == 0:
            pass
        else:
            field = row[col_num]
            if field not in seen:
                seen.add(field)
                counts[field] = 1
            else:
                counts[field] = counts[field] + 1     
        row_num += 1
    return counts

#print(counter('vt',vt_deer_crashes,'Crash Date'))

def high_freq(loc,crash_table,freqval,category):
    catcounts = counter(loc,crash_table,category)
    if type(catcounts) == tuple:
        freqcounts0 = {}
        for catname in catcounts[0].keys():
            if catcounts[0][catname] > freqval:
                freqcounts0[catname] = catcounts[0][catname]
        freqcounts1 = {}
        for catname in catcounts[1].keys():
            if catcounts[1][catname] > freqval:
                freqcounts1[catname] = catcounts[1][catname]
        return freqcounts0,freqcounts1
    else:
        freqcounts = {}
        for catname in catcounts.keys():
            if catcounts[catname] > freqval:
                freqcounts[catname] = catcounts[catname]
        return freqcounts

#print(high_freq('vt',vt_deer_crashes,40,'AOT Route'))
#print(high_freq('vt',vt_deer_crashes,50,'Crash Date'))
#print(high_freq('nyc',nyc_animal_crashes,5,'on_street_name'))


#not coordinates tho
def print_all_fieldcounts(loc,crash_table):
    field_to_col_num =  loc_to_info[loc][1]
    field_list = loc_to_info[loc][0]
    source = loc_to_info[loc][2]
    animals_colnums = loc_to_info[loc][3]
    for field_name in field_to_col_num.keys():
        if field_name == 'date_time' or field_name == 'Crash Date':
            date_time_count = counter(loc,crash_table,field_name)
            print('month')
            print(date_time_count[0])
            print('hour')
            print(date_time_count[1])
        elif field_name.upper()!='LATITUDE' and field_name.upper()!='LONGITUDE' and field_name.lower()!='coordinates':
            print(field_name)
            print(counter(loc,crash_table,field_name))
    return

def freqgrapher(freq_table):
    yvals = []
    xvals = []
    try:
        a = int(random.choice(list(freq_table.keys())))
        for field in freq_table.keys():
            xvals.append(int(field))
        xvals.sort()
        for field in xvals:
            yvals.append(freq_table[field])
        plt.plot(xvals,yvals)
        plt.show()
        return
    except:
        for field in freq_table.keys():
            xvals.append(field)
            yvals.append(freq_table[field])
        plt.plot(xvals,yvals)
        plt.show()
        return

#freqgrapher(counter('vt',vt_deer_crashes,'Crash Date')[0])
#freqgrapher(counter('vt',vt_deer_crashes,'Crash Date')[1])

#print_all_fieldcounts('chicago',chicago_animal_crashes)
#print_all_fieldcounts('vt',vt_deer_crashes)
#print_all_fieldcounts('nyc',nyc_animal_crashes)