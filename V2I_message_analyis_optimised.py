
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

kml.save(path = 'C:/temp/comm-cam_test.kml')

print("cam path kml created") #break point 

print("select HMI log file")
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename1 = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename1)

hmiIVI = pd.read_csv(filename1) #
hmiIVI.drop(columns=['log_stationid','denmalert','denmblanked','glosaalert','glosablanked'],inplace=True)
IVI_displayed = hmiIVI['iviroadalert']=='IVIRoad'
hmiIVI = hmiIVI[IVI_displayed] #filter ivi road display messages
hmiIVI['log_timestamp1'] = pd.to_datetime(hmiIVI['log_timestamp'], unit= 'ms', infer_datetime_format=True)
hmiIVI['generationtimestamputc2'] = hmiIVI['log_timestamp1'].dt.strftime('%Y-%m-%dT%H:%M:%S')
hmiIVI['servicecategory'] = 'z'
hmiIVI['pictogramcode'] = 'none' #set to a impossible value so i can see the change has been made.
hmiIVI['freetext'] = 'none' #set to a impossible value so i can see the change has been made.
hmiIVI.drop_duplicates(subset='generationtimestamputc2',keep='first',inplace=True)

count9 = hmiIVI.shape[0] # count number of rows in hmiivi for loop
z2 = 0
while count9 > 0:
   
   s7  = hmiIVI.iloc[0+z2,5] #this starts at row zero. column 4 xml and increments through
   s8 = re.search(r'''<pictogram serviceCategory="(.*?)">''', s7) #search for the servicecategory tag
   if s8:
         hmiIVI.iloc[0+z2,8] = s8.group(1) #load the value into the row in new column
   count9 = count9-1 #increment the row in df
   z2 = z2+1 #increment the row in df for timestamp

  
count10 = hmiIVI.shape[0] # count number of rows in hmiivi for loop
z3 = 0
while count10 > 0:
   
   s9  = hmiIVI.iloc[0+z3,5] #this starts at row zero. column 4 xml and increments through
   s10 = re.search(r'''">(.*?)</pictogram>(.*?)''', s9) #search for the pictogram tag
   if s10:
        hmiIVI.iloc[0+z3,9] = s10.group(1) #load the value into the row in new column
   count10 = count10-1 #increment the row in df
   z3 = z3+1 #increment the row in df for timestamp 


count11 = hmiIVI.shape[0] # count number of rows in hmiivi for loop
z4 = 0
while count11 > 0:
   
   s10  = hmiIVI.iloc[0+z4,5] #this starts at row zero. column 4 xml and increments through
   s11 = re.search(r'''<freeText>(.*?) ''', s10) #search for the freetext tag
   if s11:
         hmiIVI.iloc[0+z4,10] = s11.group(1) #load the value into the row in new column
   count11 = count11-1 #increment the row in df
   z4 = z4+1 #increment the row in df for timestamp 



result2 = hmiIVI.merge(df,how='right')
result2.dropna(axis=0,inplace=True)
result2.drop_duplicates(keep='first',inplace=True)

kml = simplekml.Kml()


count12 = result2.shape[0] # count number of rows in df for loop
y2 = 0
while count12 > 0:
   
    pnt = kml.newpoint(name=(result2.iloc[0+y2,10]))
    pnt.style.labelstyle.color = simplekml.Color.pink  # Make the text blue
    pnt.style.labelstyle.scale = 0.8 # 
    pnt.style.iconstyle.scale = 1  # 
    pnt.style.iconstyle.icon.href = 'http://www.google.com/mapfiles/markerI.png'
    pnt.timestamp.when = result2.iloc[0+y2,7]
    lon = result2.iloc[0+y2,19]
    lat = result2.iloc[0+y2,18]
    pnt.coords = [(lon, lat)] 
    count12 = count12-1 #increment the row in df
    y2 = y2+1 #increment the row in df for timestamp

kml.save(path = 'C:/temp/IVI__test.kml')

print("IVI kml created") #break point


#hmiIVI = pd.read_csv('C:/temp/hmi_1210072766_20190911T1005.csv') #
#hmiIVI.drop(columns=['log_stationid','denmalert','denmblanked'],inplace=True)
#IVI_displayed = hmiIVI['ivilanealert']=='IVILane'
#hmiIVI = hmiIVI[IVI_displayed] #filter ivi road display messages
#hmiIVI['log_timestamp1'] = pd.to_datetime(hmiIVI['log_timestamp'], unit= 'ms', infer_datetime_format=True)
#hmiIVI['generationtimestamputc2'] = hmiIVI['log_timestamp1'].dt.strftime('%Y-%m-%dT%H:%M:%S')
#hmiIVI['servicecategory'] = 'z'
#hmiIVI['pictogramcode'] = 'none' #set to a impossible value so i can see the change has been made.
#hmiIVI['freetext'] = 'none' #set to a impossible value so i can see the change has been made.
#hmiIVI.drop_duplicates(keep='first',inplace=True)

#count9 = hmiIVI.shape[0] # count number of rows in hmiivi for loop
#z2 = 0
#while count9 > 0:
   
#   s7  = hmiIVI.iloc[0+z2,7] #this starts at row zero. column 4 xml and increments through
#   s8 = re.search(r'''<pictogram serviceCategory="(.*?)">''', s7) #search for the servicecategory tag
#   if s8:
#         hmiIVI.iloc[0+z2,10] = s8.group(1) #load the value into the row in new column
#   count9 = count9-1 #increment the row in df
 #  z2 = z2+1 #increment the row in df for timestamp

  
#count10 = hmiIVI.shape[0] # count number of rows in hmiivi for loop
#z3 = 0
#while count10 > 0:
   
 #  s9  = hmiIVI.iloc[0+z3,7] #this starts at row zero. column 4 xml and increments through
 #  s10 = re.search(r'''">(.*?)</pictogram>(.*?)''', s9) #search for the pictogram tag
  # if s10:
 #       hmiIVI.iloc[0+z3,11] = s10.group(1) #load the value into the row in new column
 #  count10 = count10-1 #increment the row in df
  # z3 = z3+1 #increment the row in df for timestamp 


#count11 = hmiIVI.shape[0] # count number of rows in hmiivi for loop
#z4 = 0
#while count11 > 0:
   
#   s10  = hmiIVI.iloc[0+z4,7] #this starts at row zero. column 4 xml and increments through
#   s11 = re.search(r'''<freeText>(.*?)</freeText>''', s10) #search for the freetext tag
#   if s11:
#         hmiIVI.iloc[0+z4,12] = s11.group(1) #load the value into the row in new column
#   count11 = count11-1 #increment the row in df
 #  z4 = z4+1 #increment the row in df for timestamp 



#result2 = hmiIVI.merge(result,how='right')
#result2.dropna(axis=0,inplace=True)
#result2.drop_duplicates(keep='first',inplace=True)

#kml = simplekml.Kml()


#count12 = result2.shape[0] # count number of rows in df for loop
#y2 = 0
#while count12 > 0:
   
#    pnt = kml.newpoint(name=(result2.iloc[0+y2,11]))
#    pnt.style.labelstyle.color = simplekml.Color.pink  # Make the text blue
#    pnt.style.labelstyle.scale = 0.8 # 
#    pnt.style.iconstyle.scale = 1  # 
#    pnt.style.iconstyle.icon.href = 'http://www.google.com/mapfiles/markerI.png'
 #   pnt.timestamp.when = result2.iloc[0+y2,9]
#    lon = result2.iloc[0+y2,14]
#    lat = result2.iloc[0+y2,13]
#    pnt.coords = [(lon, lat)] 
#    count12 = count12-1 #increment the row in df
#    y2 = y2+1 #increment the row in df for timestamp

#kml.save(path = 'C:/temp/IVIlane__1210072766_20190911T1005.kml')

#print("IVI lane kml created") #break point





