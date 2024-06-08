
"""
Created on Thu Sept 20 th 2019

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

kml.save(path = 'C:/temp/comm-cam_ivi.kml')

print("cam path kml created") #break point 



print("select HMI log file")
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename1 = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename1)

hmiIVI = pd.read_csv(filename1) #
hmiIVI.drop(columns=['log_stationid','denmalert','denmblanked','glosaalert','glosablanked','iviroadblanked'],inplace=True)
IVI_displayed = hmiIVI['ivilanealert']=='IVILane'
hmiIVI = hmiIVI[IVI_displayed] #filter ivi road display messages
hmiIVI['log_timestamp1'] = pd.to_datetime(hmiIVI['log_timestamp'], unit= 'ms', infer_datetime_format=True)
hmiIVI['generationtimestamputc2'] = hmiIVI['log_timestamp1'].dt.strftime('%Y-%m-%dT%H:%M:%S')
hmiIVI['laneStatus1'] = 'none' #set to a impossible value so i can see the change has been made.
hmiIVI['laneStatus2'] = 'none' #set to a impossible value so i can see the change has been made.
hmiIVI['laneStatus3'] = 'none' #set to a impossible value so i can see the change has been made.
hmiIVI['laneStatus4'] = 'none' #set to a impossible value so i can see the change has been made.
hmiIVI['laneSpeed1'] = 'z'
hmiIVI['laneSpeed2'] = 'z'
hmiIVI['laneSpeed3'] = 'z'
hmiIVI['laneSpeed4'] = 'z'
hmiIVI['pictogramServiceCat1'] = 'z'
hmiIVI['pictogramServiceCat2'] = 'z'
hmiIVI['pictogramServiceCat3'] = 'z'
hmiIVI['pictogramServiceCat4'] = 'z'
hmiIVI['pictogram1'] = 'z'
hmiIVI['pictogram2'] = 'z'
hmiIVI['pictogram3'] = 'z'
hmiIVI['pictogram4'] = 'z'

hmiIVI.drop_duplicates(subset='generationtimestamputc2',keep='first',inplace=True)

  
count2 = hmiIVI.shape[0] # count number of rows in hmispat for loop
z = 0
while count2 > 0:
        
   s3  = hmiIVI.iloc[0+z,4] #this starts at row zero. column 4 xml and increments through


   s4 = re.search(r'''<lane position='1' status='(.*?)'(.*?)''', s3) #lane 1 status 
   if s4:
        hmiIVI.iloc[0+z,7] = s4.group(1) #lane 1 status
   s5 = re.search(r'''<lane position='2' status='(.*?)'(.*?)''', s3) #lane 2 status
   if s5:
        hmiIVI.iloc[0+z,8] = s5.group(1) #lanes 2 status
   s6 = re.search(r'''<lane position='3' status='(.*?)'(.*?)''', s3) #lane 3 status
   if s6:
        hmiIVI.iloc[0+z,9] = s6.group(1) #lane 3 status
   s7 = re.search(r'''<lane position='4' status='(.*?)'(.*?)''', s3) #lane 4 status
   if s7:
        hmiIVI.iloc[0+z,10] = s7.group(1) #lane 4 status
    
   s8 = re.search(r'''<lane position='1' status='(.*?)'><speed unit='mph' regulatory='(.*?)'>(.*?)</speed>(.*?)''', s3) #search for speed advice
   if s8:
        hmiIVI.iloc[0+z,11] = s8.group(3) #lane 1 speed
   s9 = re.search(r'''<lane position='2' status='(.*?)'><speed unit='mph' regulatory='(.*?)'>(.*?)</speed>(.*?)''', s3) #search for speed advice
   if s9:
        hmiIVI.iloc[0+z,12] = s9.group(3) #lane 2 speed
   s10 = re.search(r'''<lane position='3' status='(.*?)'><speed unit='mph' regulatory='(.*?)'>(.*?)</speed>(.*?)''', s3) #search for speed advice
   if s10:
        hmiIVI.iloc[0+z,13] = s10.group(3) #lane 3 speed
   s11 = re.search(r'''<lane position='4' status='(.*?)'><speed unit='mph' regulatory='(.*?)'>(.*?)</speed>(.*?)''', s3)  #search for speed advice
   if s11:
        hmiIVI.iloc[0+z,14] = s11.group(3) #lane 4 speed

   s12 = re.search(r'''<lane position='1' status='(.*?)'><pictogram serviceCategory="(.*?)"(.*?)''', s3) 
   if s12:
        hmiIVI.iloc[0+z,15] = s12.group(2) #load pictogram category lane 1
   s13 = re.search(r'''<lane position='2' status='(.*?)'><pictogram serviceCategory="(.*?)"(.*?)''', s3) 
   if s13:
        hmiIVI.iloc[0+z,16] = s13.group(2) #load pictogram category lane 2
   s14 = re.search(r'''<lane position='3' status='(.*?)'><pictogram serviceCategory="(.*?)"(.*?)''', s3) 
   if s14:
        hmiIVI.iloc[0+z,17] = s14.group(2) #load pictogram category lane 3  
    
   s15 = re.search(r'''<lane position='4' status='(.*?)'><pictogram serviceCategory="(.*?)"(.*?)''', s3) 
   if s15:
        hmiIVI.iloc[0+z,18] = s15.group(2) #load pictogram category lane 4
  
   s16 = re.search(r'''<lane position='1' status='(.*?)'><pictogram serviceCategory="(.*?)">(.*?)</pictogram></lane>(.*?)''', s3) #search for the time advisory tag
   if s16:
        hmiIVI.iloc[0+z,19] = s16.group(3) #load pictorgram code for lane 1
   s17 = re.search(r'''<lane position='2' status='(.*?)'><pictogram serviceCategory="(.*?)">(.*?)</pictogram></lane>(.*?)''', s3) #search for the time advisory tag
   if s17:
        hmiIVI.iloc[0+z,20] = s17.group(3) #load pictogram code for lane 2
   s18 = re.search(r'''<lane position='3' status='(.*?)'><pictogram serviceCategory="(.*?)">(.*?)</pictogram></lane>(.*?)''', s3) #search for the time advisory tag
   if s18:
        hmiIVI.iloc[0+z,21] = s18.group(3) #load pictogram code for lane 3
   s19 = re.search(r'''<lane position='4' status='(.*?)'><pictogram serviceCategory="(.*?)">(.*?)</pictogram></lane>(.*?)''', s3) #search for the time advisory tag
   if s19:
        hmiIVI.iloc[0+z,22] = s19.group(3) #load pictogram code for lane 4
    
   count2 = count2-1 #increment the row in df
   z = z+1 #increment the row in df for timestamp 


result = df # copy cam table and reduce before time comparison with IVI messages
result.drop(columns=['log_action','log_messagetype','generationtimestamputc','stationtype','referencepositionlatitude','referencepositionlongitude','generationtimestamputc1'],inplace=True)


count3 = hmiIVI.shape[0] # count number of rows in hmispat for loop
count4 = result.shape[0] # count number of rows in result for loop



result1 = hmiIVI.merge(result,how='left')

#%%

result1['pictogramCat&Code1'] = result1['pictogramServiceCat1'] + '_' + result1['pictogram1'] # Concatenate category code and pictogram code for each lane
result1['pictogramCat&Code2'] = result1['pictogramServiceCat2'] + '_' + result1['pictogram2']
result1['pictogramCat&Code3'] = result1['pictogramServiceCat3'] + '_' + result1['pictogram3']
result1['pictogramCat&Code4'] = result1['pictogramServiceCat4'] + '_' + result1['pictogram4']

result1['pictogramAll'] = result1['pictogramCat&Code1'] + ' ' + result1['pictogramCat&Code2'] + ' ' + result1['pictogramCat&Code3'] + ' ' + result1['pictogramCat&Code4'] # Concatenate lane codes together


#%%
result1 = result1[(result1['pictogram1'] != 'z') & (result1['pictogram3'] != 'z') & (result1['pictogram4'] != 'z')]
#%%

result1.dropna(axis=0,inplace=True)

kml = simplekml.Kml()

kml.save(path = 'C:/temp/IVILane_displayed/IVILane_displayed.kml')

count5 = result1.shape[0] # count number of rows in df for loop
y = 0
while count5 > 0:
       
    path = kml.addfile('C:/temp/IVILane_displayed/pictograms/13_659.png')
    pnt = kml.newpoint(name=(result1.iloc[0+y,29]))
    pnt.style.labelstyle.color = simplekml.Color.orange  # Make the text orange
    pnt.style.labelstyle.scale = 0.8 # Make the text twice as big
    pnt.style.iconstyle.scale = 1  # 
    pnt.style.iconstyle.icon.href = path
    pnt.timestamp.when = result1.iloc[0+y,6]
    lon = result1.iloc[0+y,24]
    lat = result1.iloc[0+y,23]
    pnt.coords = [(lon, lat)] 
    count5 = count5-1 #increment the row in df
    y = y+1 #increment the row in df for timestamp

kml.savekmz(path = 'C:/temp/IVILane_displayed/IVILane_displayed.kmz')

print("IVILane HMI display kmz created")