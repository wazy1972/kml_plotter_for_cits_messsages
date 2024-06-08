
"""
Created on Thu Sept 12 th 2019

@author: Paul Warren
"""
import pandas as pd
import simplekml
import re
    
campath = pd.read_csv('D:/temp/comm-cam_1210072766_20190911T1005.csv')

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

kml.save(path = 'D:/temp/comm-cam_1210072766_20190911T1005.kml')

print("cam path kml created") #break point 

hmispat = pd.read_csv('D:/temp/hmi_1210072766_20190911T1005.csv') #
hmispat.drop(columns=['log_stationid','denmalert','denmblanked','iviroadalert','ivilaneblanked','iviroadblanked','ivilanealert','ivilaneblanked'],inplace=True)
glosa_displayed = hmispat['glosaalert']=='GLOSA'
hmispat = hmispat[glosa_displayed] #filter glosa display messages
hmispat['log_timestamp1'] = pd.to_datetime(hmispat['log_timestamp'], unit= 'ms', infer_datetime_format=True)
hmispat['generationtimestamputc2'] = hmispat['log_timestamp1'].dt.strftime('%Y-%m-%dT%H:%M:%S')
hmispat['phase'] = 'z'
hmispat['timeAdvisory'] = 'none' #set to a impossible value so i can see the change has been made.
hmispat['speedadvisory'] = 'none' #set to a impossible value so i can see the change has been made.

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

kml.save(path = 'D:/temp/spat_timeadvice_1210072766_20190911T1005.kml')

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

kml.save(path = 'D:/temp/spat_phase_displayed_1210072766_20190911T1005.kml')

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

kml.save(path = 'D:/temp/spat_speedadvice_displayed_1210072766_20190911T1005.kml')

print("spat speed advice kml created") #break point

result1.to_excel("hmi_spat_advise_1210072766_20190911T1005.xlsx")

print("spat speed advice excel file created")