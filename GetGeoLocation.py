# importing requests and json
from ast import Str
from pickle import TRUE
from turtle import goto
import requests, json
import os
from datetime import datetime, timedelta
import os.path
from pathlib import Path


#def main():
BASE_URL = "http://api.openweathermap.org/geo/1.0/direct?"
CITY = input("What is the name of your city?:  ") ##User needs to input
print(" ")
LIMIT = '&limit=1&&' 
API_KEY = "appid=6c842471aabfff2ae2f180d84788f526"
URL = BASE_URL + "q=" + CITY + LIMIT + API_KEY

## Filename will be stored
filename = CITY+".txt"  
path_to_file = filename
path = Path(path_to_file)

if path.is_file():
   print(f'The file {path_to_file} exists')
   FileExits = 1
else:
 print(f'The file {path_to_file} does not exist, use API to create one')  
 FileExits = 0


if FileExits == 1:       
## Compare file modification times, if more than 1 min ago fetch new details from API
   file_mod_time = datetime.fromtimestamp(os.stat(filename).st_mtime)  
   now = datetime.today()
   print(now) 
   print(file_mod_time)
   max_delay = timedelta(minutes=1)

   if now-file_mod_time > max_delay:
      print ("Filename: {} last modified on {} is older than {} minutes.".format(filename, file_mod_time, max_delay.seconds/60))
      FileExits = 0
   else:
      print ("A file was already created/appended {} minutes ago.".format((now-file_mod_time).seconds/60)) 
      file = open(filename, "r",encoding='utf-8')
      text = file.read()
      HEAD = "City Summary (Text File)"
      print(f"{HEAD:-^30}")
      print(' ')
      #print(text)
      #json_object = json.loads(text)

      
      with open(filename, encoding='utf-8') as json_file:
         json_data = json.load(json_file)
         ##print(json_data)
         print ("City Name:   ",json_data[0]['name'])
         #print ("Province:    ",json_data[0]['state'])      
         print ("Latitude:    ",json_data[0]['lat'])    
         print ("Longitude:   ",json_data[0]['lon'])   
         print ("Country:     ",json_data[0]['country']) 

      file.close()

   #exit()

if FileExits == 0:  
# API request
   response = requests.get(URL)

#Some basic error handling (Blanks, No results etc)
   if response.text == '[]':
      print('City: '+CITY+' Not Found Sorry, please try again!')  
         
   elif response.text == '{"cod":"400","message":"Nothing to geocode"}':
      print('No results - You entered a blank city name')   
   else:
         #print('City Results Found!')

      data = response.json()
      HEAD = "City Summary (API 1)"
      print(f"{HEAD:-^30}")
      print(' ')
      print ("City Name: ",data[0]['name'])
      #print ("Province:  ",data[0]['state'])      
      print ("Latitude:  ",data[0]['lat'])    
      print ("Longitude: ",data[0]['lon'])   
      print ("Country:   ",data[0]['country'])  
      print(' ')
         # base URL (second API CALL)
      BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
         # City Name CITY = "Randburg"
      LONG = '&lon='+str(data[0]['lon']) 
         # Limit Results
      LAT = 'lat='+str(data[0]['lat'])
         # API key 
      API_KEY = "units=metric&appid=6c842471aabfff2ae2f180d84788f526"
         # URL string combined
      URL = BASE_URL + LAT + LONG+'&' + API_KEY
         #print (URL)
      ## Writing to files
      # Clean the file fist then append new data from API
      f = open(filename, 'a+')
      f.truncate(0) # need '0' when using r+  

      with open(filename, 'a+',encoding='utf-8') as f:
         f.write(response.text)
         
         
         #with open(filename, 'wb') as fd:
          #for chunk in response.iter_content(chunk_size):
             #fd.write(chunk)
      
   # API request
      response = requests.get(URL)
      #print (response.text)
      data2 = response.json()
      HEAD2 = "Weather Details (API 2)"
      print(f"{HEAD2:-^30}")
      print(' ')
      print('Overview:     '+str(data2['weather'][0]['main'])+' - '+data2['weather'][0]['description'])
      print('Cur Temp:     '+str(data2['main']['temp'])+' °C')
      print('Min Temp:     '+str(data2['main']['temp_min'])+' °C')
      print('Max Temp:     '+str(data2['main']['temp_max'])+' °C')
      print(' ')
      exit()

