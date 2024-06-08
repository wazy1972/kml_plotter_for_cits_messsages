
"""
Created on Thu Sept 19 th 2019

@author: Paul Warren & Rob Murcott (xer extraction and spat analysis)
"""
import pandas as pd
import simplekml
import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename 

import csv
import os.path
import os
import re
import datetime
import time


print("select CAM log file")
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)

campath = pd.read_csv(filename)
#campath = pd.read_csv('C:/temp/comm-cam_1210072766_20190911T1005.csv')

df = pd.DataFrame(data=campath)
df.set_index('rowid',inplace=True)
df.drop(columns=['log_stationid','log_applicationid','log_timestamp','log_communicationprofile','log_messageuuid','protocolversion','messageid','stationid','generationdeltatime','generationtimestamptai','referencepositionsemimajorconfidence','referencepositionsemiminorconfidence','referencepositionsemimajororientation','referencepositionaltitudevalue','referencepositionaltitudeconfidence','headingvalue','headingconfidence','speedvalue','speedconfidence','drivedirection','vehiclelengthvalue','vehiclelengthconfidenceindication','vehiclewidth'],inplace=True)
is_SENT = df['log_action']=='SENT'
df = df[is_SENT] #filter for cam sent from obu
df['log_messagetype']
df['generationtimestamputc1'] = pd.to_datetime(df['generationtimestamputc'], unit='ms', infer_datetime_format=True)
df['generationtimestamputc2'] = df['generationtimestamputc1'].dt.strftime('%Y-%m-%dT%H:%M:%S')

df['referencepositionlatitude1'] = df['referencepositionlatitude']/10000000
df['referencepositionlongitude1'] = df['referencepositionlongitude']/10000000

df.drop_duplicates(keep='first',inplace=True)

kml = simplekml.Kml()


count = df.shape[0] # count number of rows in df for loop

y = 0
while count > 0:
   
   pnt = kml.newpoint(name=None)
   pnt.style.iconstyle.scale = 0.5  # 
   pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pal4/icon49.png'
   pnt.timestamp.when = df.iloc[0+y,7] #this starts at row zero. column 7 generationtimestamputc2 and increments through
   lon = df.iloc[0+y,9]
   lat = df.iloc[0+y,8]
   pnt.coords = [(lon, lat)] 
   count = count-1 #increment the row in df
   y = y+1 #increment the row in df for timestamp

kml.save(path = 'C:/temp/comm-cam_1210072286_20190813T1212.kml')

print("cam path kml created") #break point 

print("select HMI log file")
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)

hmispat = pd.read_csv(filename) #
hmispat.drop(columns=['log_stationid','denmalert','denmblanked','iviroadalert','ivilaneblanked','iviroadblanked','ivilanealert','ivilaneblanked'],inplace=True)
glosa_displayed = hmispat['glosaalert']=='GLOSA'
hmispat = hmispat[glosa_displayed] #filter glosa display messages
hmispat['log_timestamp1'] = pd.to_datetime(hmispat['log_timestamp'], unit= 'ms', infer_datetime_format=True)
hmispat['generationtimestamputc2'] = hmispat['log_timestamp1'].dt.strftime('%Y-%m-%dT%H:%M:%S')
hmispat['phase'] = 'z'
hmispat['timeAdvisory'] = 'none' #set to a impossible value so i can see the change has been made.
hmispat['speedadvisory'] = 'none' #set to a impossible value so i can see the change has been made.
hmispat.drop_duplicates(keep='first',inplace=True)

count1 = hmispat.shape[0] # count number of rows in hmispat for loop
z = 0
while count1 > 0:
   
   s  = hmispat.iloc[0+z,3] #this starts at row zero. column 4 xml and increments through
   s2 = re.search(r'''phase='(.*?)'><''', s) #search for the phase tag
   if s2:
         hmispat.iloc[0+z,6] = s2.group(1) #load the value into the row in new column
   count1 = count1-1 #increment the row in df
   z = z+1 #increment the row in df for timestamp

  
count2 = hmispat.shape[0] # count number of rows in hmispat for loop
z = 0
while count2 > 0:
   
   s3  = hmispat.iloc[0+z,3] #this starts at row zero. column 4 xml and increments through
   s4 = re.search(r'''<timeAdvisory unit='sec'>(.*?)</timeAdvisory>(.*?)''', s3) #search for the time advisory tag
   if s4:
        hmispat.iloc[0+z,7] = s4.group(1) #load the value into the row in new column
   count2 = count2-1 #increment the row in df
   z = z+1 #increment the row in df for timestamp 


count3 = hmispat.shape[0] # count number of rows in hmispat for loop
z = 0
while count3 > 0:
   
   s5  = hmispat.iloc[0+z,3] #this starts at row zero. column 4 xml and increments through
   s6 = re.search(r'''<speedAdvisory unit='kph'>(.*?)</speedAdvisory>(.*?)''', s5) #search for the speed advisory tag
   if s6:
         hmispat.iloc[0+z,8] = s6.group(1) #load the value into the row in new column
   count3 = count3-1 #increment the row in df
   z = z+1 #increment the row in df for timestamp 


result = df # copy cam table and reduce before time comparison with SPAT messages
result.drop(columns=['log_action','log_messagetype','generationtimestamputc','stationtype','referencepositionlatitude','referencepositionlongitude','generationtimestamputc1'],inplace=True)


count4 = hmispat.shape[0] # count number of rows in hmispat for loop
count5 = result.shape[0] # count number of rows in result for loop

result1 = hmispat.merge(result,how='right')
result1.dropna(axis=0,inplace=True)

kml = simplekml.Kml()


count6 = result1.shape[0] # count number of rows in df for loop
y = 0
while count6 > 0:
   
   pnt = kml.newpoint(name=(result1.iloc[0+y,7]))
   pnt.style.labelstyle.color = simplekml.Color.antiquewhite  # Make the text blue
   pnt.style.labelstyle.scale = 0.8 # Make the text twice as big
   pnt.style.iconstyle.scale = 1  # 
   pnt.style.iconstyle.icon.href = 'https://www.google.com/mapfiles/traffic.png'
   pnt.timestamp.when = result1.iloc[0+y,5]
   lon = result1.iloc[0+y,10]
   lat = result1.iloc[0+y,9]
   pnt.coords = [(lon, lat)] 
   count6 = count6-1 #increment the row in df
   y = y+1 #increment the row in df for timestamp

kml.save(path = 'C:/temp/spat_timeadvice_1210072286_20190813T1212.kml')

kml = simplekml.Kml()

print("spat timeadvice kml created") #break point 

count7 = result1.shape[0] # count number of rows in df for loop
y = 0
while count7 > 0:
   
   pnt = kml.newpoint(name=(result1.iloc[0+y,6]))
   pnt.style.labelstyle.color = simplekml.Color.cyan  # Make the text cyan
   pnt.style.labelstyle.scale = 0.8 # Make the text twice as big
   pnt.style.iconstyle.scale = 1  # 
   pnt.style.iconstyle.icon.href = 'https://www.google.com/mapfiles/traffic.png'
   pnt.style.balloonstyle.text = (result1.iloc[0+y,7]) 
   pnt.style.balloonstyle.text = (result1.iloc[0+y,8]) 
   pnt.style.balloonstyle.bgcolor = simplekml.Color.white
   pnt.style.balloonstyle.textcolor = simplekml.Color.rgb(0, 0, 255)
   pnt.timestamp.when = result1.iloc[0+y,5]
   lon = result1.iloc[0+y,10]
   lat = result1.iloc[0+y,9]
   pnt.coords = [(lon, lat)] 
   count7 = count7-1 #increment the row in df
   y = y+1 #increment the row in df for timestamp

kml.save(path = 'C:/temp/spat_phase_displayed_1210072286_20190813T1212.kml')

print("spat phase advice kml created") #break point

kml = simplekml.Kml()


count8 = result1.shape[0] # count number of rows in df for loop
y = 0
while count8 > 0:
   
   pnt = kml.newpoint(name=(result1.iloc[0+y,8]))
   pnt.style.labelstyle.color = simplekml.Color.orange  # Make the text blue
   pnt.style.labelstyle.scale = 0.8 # Make the text twice as big
   pnt.style.iconstyle.scale = 1  # 
   pnt.style.iconstyle.icon.href = 'https://www.google.com/mapfiles/traffic.png'
   pnt.timestamp.when = result1.iloc[0+y,5]
   lon = result1.iloc[0+y,10]
   lat = result1.iloc[0+y,9]
   pnt.coords = [(lon, lat)] 
   count8 = count8-1 #increment the row in df
   y = y+1 #increment the row in df for timestamp

kml.save(path = 'C:/temp/spat_speedadvice_displayed_1210072286_20190813T1212.kml')

print("spat speed advice kml created") #break point

result1.to_excel("hmi_spat_advise_1210072286_20190813T1212.xlsx")

print("spat speed advice excel file created")

print('The script has created a number of kml files that provide a time based view of  GLOSA based advice given on the HMI')
print(' output files created in temp directory on C:')


start = ('{:%H:%M:%S}'.format(datetime.datetime.now()))

print('Commencing xer extraction...')
print('Start: ' + start)

outputfile = 'xer_analysis.csv'
if os.path.isfile(outputfile) is True:
    out = open(outputfile, 'a')
    
else:
    out = open(outputfile, 'w')
    out.write('Log_timestamp,Stationid,Intersection_Name,SignalGroup,CurrentEvent,CurrentMinEndTime,CurrentMETCountdown,CurrentLikelyTime,CurrentLTCountdown,FutureEvents,xer\n')

print("select comm-xer log file")
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename2 = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename2)

with open(filename2) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        messagetype = row[5]
        if messagetype == 'ETSI.SPATEM':
            log_timestamp2 = row[0]
            log_timestamp2 = float(log_timestamp2)
            log_timestamp2 = log_timestamp2 / 1000.0
            log_timestamp = datetime.datetime.utcfromtimestamp(log_timestamp2).strftime('%Y-%m-%d %H:%M:%S.%f')
            xer = row[9]
            # Set date and time to be used to generate timestamp of minEndtime or likelytime
            year = datetime.datetime.utcfromtimestamp(log_timestamp2).strftime('%Y')
            month = datetime.datetime.utcfromtimestamp(log_timestamp2).strftime('%m')
            day = datetime.datetime.utcfromtimestamp(log_timestamp2).strftime('%d')
            moy = re.findall(r'''<moy>(.*?)</moy>''',xer)
            moy = moy[0]
            hour = int((int(moy)/60) % 24)
            current_hourdate = datetime.datetime(int(year),int(month),int(day),hour,0,0)
            # Capture intersection naming details
            stationid = re.findall(r'''<stationID>(.*?)</stationID>''',xer)
            stationid = stationid[0]
            intersectionID = re.findall(r'''<IntersectionState><name>(.*?)<''',xer)
            intersectionID = intersectionID[0]
            # Capture and seperate the movement states
            MovementStates = re.findall(r'''<MovementState>(.*?)</MovementState>''',xer)
            # Print each movement state seperately
            for i in MovementStates:
                MovementState = i
                # Confirm Signal Group
                Signal_Group = re.findall(r'''<signalGroup>(.*?)<''',i)
                Signal_Group = Signal_Group[0]
                # Capture and list all MovementEvents for each MovementState. Used to narrow search to give current movementevent timings
                MovementEvents = re.findall(r'''<MovementEvent>(.*?)</MovementEvent''',MovementState)
                CurrentMovementEvent = MovementEvents[0]
                # List all eventstates for this signal and seperate out the current and future states
                EventStates = re.findall(r'''<eventState>(.*?)</eventState>''', MovementState)
                CurrentES = EventStates[0]
                FutureES = ''
                for f in EventStates[1:]:
                    FutureES += f
                # Return minEndtime and likelytime if present for current movementevent
                CurrentMeT = re.findall(r'''<minEndTime>(.*?)</minEndTime>''',CurrentMovementEvent)
                if CurrentMeT == []:
                    CurrentMeT = ''
                    CurrentMeTtime = ''
                    CurrentMeTCD = ''
                if CurrentMeT != '':
                    CurrentMeT = CurrentMeT[0]
                    # 36001 and 36002 are set aside values in the standards to communicate situations
                    if CurrentMeT == '36001':
                        CurrentMeTtime = "invalid"
                        CurrentMeTCD = "Morethan1hour"
                    elif CurrentMeT == '36002':
                        CurrentMeTtime = "Not-available"
                        CurrentMeTCD = "Not-available"
                    # assumed any other value tenths of seconds past the current hour. Current hour taken from the moy
                    else:
                        # convert to seconds
                        CurrentMeT = int(CurrentMeT) / 10
                        # calculate timestamp for minend time for insertion to csv
                        CurrentMeT = current_hourdate + datetime.timedelta(0,CurrentMeT)
                        CurrentMeTtime = datetime.datetime.strftime(CurrentMeT,'%H:%M:%S.%f')
                        # calculate the countdown
                        CurrentMeTCD = datetime.datetime.strftime(CurrentMeT,'%Y-%m-%d %H:%M:%S.%f')
                        CurrentMeTCD = datetime.datetime.strptime(CurrentMeTCD,'%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(log_timestamp,'%Y-%m-%d %H:%M:%S.%f')
                        # used to check if the countdown presents a negative value
                        if CurrentMeTCD.days == -1:
                            CurrentMeTCD = 'negative value'
                        else:
                            CurrentMeTCD = str(CurrentMeTCD.seconds)
                CurrentLyt = re.findall(r'''<likelyTime>(.*?)</likelyTime>''',CurrentMovementEvent)
                if CurrentLyt == []:
                    CurrentLyt = ''
                    CurrentLyttime = ''
                    CurrentLytCD = ''
                if CurrentLyt != '':
                    # 36001 and 36002 are set aside values in the standards to communicate situations
                    CurrentLyt = CurrentLyt[0]
                    if CurrentLyt == '36001':
                        CurrentLyttime = "invalid"
                        CurrentLytCD = "Morethan1hour"
                    elif CurrentLyt == '36002':
                        CurrentLyttime = "Not-available"
                        CurrentLytCD = "Not-available"
                    # assumed any other value tenths of seconds past the current hour. Current hour taken from the moy
                    else:
                        # convert to seconds
                        CurrentLyt = int(CurrentLyt) / 10
                        # calculate timestamp for likely time for insertion to csv
                        CurrentLyt = current_hourdate + datetime.timedelta(0,CurrentLyt)
                        CurrentLyttime = datetime.datetime.strftime(CurrentLyt,'%H:%M:%S.%f')
                        # calculate the countdown
                        CurrentLytCD = datetime.datetime.strftime(CurrentLyt,'%Y-%m-%d %H:%M:%S.%f')
                        CurrentLytCD = datetime.datetime.strptime(CurrentLytCD,'%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(log_timestamp,'%Y-%m-%d %H:%M:%S.%f')
                        # used to check if the countdown presents a negative value
                        if CurrentLytCD.days == -1:
                            CurrentLytCD = 'negative value'
                        else:
                            CurrentLytCD = str(CurrentLytCD.seconds)
                # Add line to csv output
                newline = log_timestamp + ',' + stationid + ',' + intersectionID + ',' + Signal_Group + ',' + CurrentES + ',' +  CurrentMeTtime + ',' + CurrentMeTCD + ',' + CurrentLyttime + ',' + CurrentLytCD + ',' + FutureES + ',' + xer +'\n'
                out = open(outputfile, 'a')
                out.write(newline)
                out.close()

end = ('{:%H:%M:%S}'.format(datetime.datetime.now()))
print('End: ' + end)
print('script successfully completed')

