
"""
Created on Thu Oct 3rd 2019

@author: Paul Warren
"""
import pandas as pd
import simplekml
import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename 


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

kml.save(path = 'C:/temp/comm-cam_DENM.kml')

print("cam path kml created") #break point 

print("select HMI log file")
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename1 = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename1)

hmiDENM = pd.read_csv(filename1) #
hmiDENM.drop(columns=['log_stationid','glosaalert','glosablanked','iviroadblanked','iviroadalert','ivilanealert'],inplace=True)
DENM_displayed = hmiDENM['denmalert']=='RWW'
hmiDENM = hmiDENM[DENM_displayed] #filter DENM road display messages
hmiDENM['log_timestamp1'] = pd.to_datetime(hmiDENM['log_timestamp'], unit= 'ms', infer_datetime_format=True)
hmiDENM['generationtimestamputc2'] = hmiDENM['log_timestamp1'].dt.strftime('%Y-%m-%dT%H:%M:%S')
hmiDENM['environmentalSituation'] = 'z'
hmiDENM['regulatory'] ='z'
hmiDENM['extent'] ='z'
hmiDENM['speed'] ='z'

hmiDENM.drop_duplicates(subset='generationtimestamputc2',keep='first',inplace=True)

count1 = hmiDENM.shape[0] # count number of rows in hmidenm for loop
z = 0
while count1 > 0:
   
   s  = hmiDENM.iloc[0+z,4] #this starts at row zero. column 4 xml and increments through
   s2 = re.search(r'''<environmentalSituation type="(.*?)">''', s) #search for the phase tag
   if s2:
         hmiDENM.iloc[0+z,7] = s2.group(1) #load the value into the row in new column
   count1 = count1-1 #increment the row in df
   z = z+1 #increment the row in df for timestamp

  
count2 = hmiDENM.shape[0] # count number of rows in hmidenm for loop
z = 0
while count2 > 0:
        
   s3  = hmiDENM.iloc[0+z,4] #this starts at row zero. column 4 xml and increments through
  
   s12 = re.search(r'''<extent unit='meters' status='ending'>(.*?)</extent>(.*?)''', s3) #search for the time advisory tag
   if s12:
        hmiDENM.iloc[0+z,9] = s12.group(1) #environmental situation extent
   s13 = re.search(r'''<speed unit='kph' regulatory='(.*?)'>(.*?)''', s3) #search for the time advisory tag
   if s13:
        hmiDENM.iloc[0+z,8] = s13.group(1) #regulatory type for speed
   s14 = re.search(r'''<speed unit='kph' regulatory='(.*?)'>(.*.?)</speed></environmentalSituation>''', s3) #search for the time advisory tag
   if s14:
        hmiDENM.iloc[0+z,10] = s14.group(2) #speed value

    
   count2 = count2-1 #increment the row in df
   z = z+1 #increment the row in df for timestamp 


result = df # copy cam table and reduce before time comparison with IVI messages
result.drop(columns=['log_action','log_messagetype','generationtimestamputc','stationtype','referencepositionlatitude','referencepositionlongitude','generationtimestamputc1'],inplace=True)


count3 = hmiDENM.shape[0] # count number of rows in hmispat for loop
count4 = result.shape[0] # count number of rows in result for loop

result1 = hmiDENM.merge(result,how='right')
result1.dropna(axis=0,inplace=True)


kml = simplekml.Kml()

count5 = result1.shape[0] # count number of rows in df for loop
y = 0
while count5 > 0:
   
   pnt = kml.newpoint(name=(result1.iloc[0+y,10]))
   pnt.style.labelstyle.color = simplekml.Color.orange  # Make the text blue
   pnt.style.labelstyle.scale = 0.8 # Make the text twice as big
   pnt.style.iconstyle.scale = 1  # 
   pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/caution.png'
   pnt.timestamp.when = result1.iloc[0+y,6]
   lon = result1.iloc[0+y,12]
   lat = result1.iloc[0+y,11]
   pnt.coords = [(lon, lat)] 
   count5 = count5-1 #increment the row in df
   y = y+1 #increment the row in df for timestamp

kml.save(path = 'C:/temp/DENM_displayed.kml')

print("DENM HMI display kml created") #break point


kml = simplekml.Kml()

count6 = result1.shape[0] # count number of rows in df for loop
y = 0
while count6 > 0:
   
   pnt = kml.newpoint(name=(result1.iloc[0+y,9]))
   pnt.style.labelstyle.color = simplekml.Color.blue  # Make the text blue
   pnt.style.labelstyle.scale = 0.8 # Make the text twice as big
   pnt.style.iconstyle.scale = 1  # 
   pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/caution.png'
   pnt.timestamp.when = result1.iloc[0+y,6]
   lon = result1.iloc[0+y,12]
   lat = result1.iloc[0+y,11]
   pnt.coords = [(lon, lat)] 
   count6 = count6-1 #increment the row in df
   y = y+1 #increment the row in df for timestamp

kml.save(path = 'C:/temp/DENM_countdown_displayed.kml')

print("DENM HMI display kml created") #break point



