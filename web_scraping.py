#Author= Yasar Unlu
#Disclaimer: I am not responsible for the use of this software for other non-educational purposes.

import requests
import easygui
import webbrowser as wb
import sys
import sqlite3 as sql
from PIL import Image, ImageDraw, ImageFont
import os
import datetime
import time
from dateutil import parser
from chart import chart as ch
from bs4 import BeautifulSoup as bs
img = Image.new('RGB', (800, 500), color=("white"))
fnt = ImageFont.truetype('font/CALIBRI.ttf', 25)
fnt2 = ImageFont.truetype('font/CALIBRI.ttf', 50)
fnt3= ImageFont.truetype("arial.ttf", 15)
d = ImageDraw.Draw(img)
d.text((250, 30), "Welcome",font=fnt2, fill="green")
d.text((20, 80), "With this PYTHON programma you can:",font=fnt, fill="blue")
d.text((20, 110), "*Request your data from website internetofthings.glr-imd.nl",font=fnt, fill="red")
d.text((20, 140), "*Analyze your data",font=fnt, fill="red")
d.text((20, 170), "*Create a chart",font=fnt, fill="red")
d.text((20, 200), "*Store your data in database",font=fnt, fill="red")
d.text((250, 260), "Click OK to continue",font=fnt, fill="green")
d.text((300, 300), "made by Yasar",font=fnt3, fill="purple")




img.save("images/welcome.png")

easygui.msgbox("", image="images/welcome.png")
database= sql.connect("iot2.db") #creating database
cursor=database.cursor()
url2="https://internetofthings.glr-imd.nl"

page2=requests.get(url2)
soup2=bs(page2.content,'html.parser')

device_names=soup2.find_all("option")
devices= []
for x in device_names:
    dev= x["value"]
    device_check = soup2.find_all("option", {"value": "{}".format(dev)})
    if len(device_check)==1 and "Conn" not in dev:
        devices.append(dev.strip())
device_choosing= easygui.choicebox("Choose a device", "https://internetofthings.glr-imd.nl", devices)
if device_choosing==None:
    sys.exit(0)

#creating database table
cursor.execute("DROP table IF EXISTS {}".format(device_choosing));
cursor.execute("CREATE TABLE if not exists {}"
                "(id INTEGER PRIMARY KEY AUTOINCREMENT ,"
               " tijd TEXT, value float);".format(device_choosing))

#We delete the existing table to prevent data from being saved in the database over and over
def delete_tables():
    for x in devices:
        try:
            if x!=device_choosing:
                cursor.execute("DROP table IF EXISTS {}".format(x));
        except :pass

url= "https://internetofthings.glr-imd.nl/read.php?dev="+device_choosing

page= requests.get(url)

soup= bs(page.content, 'html.parser')

get_details  = soup.find_all("td")

data_value=[]
data_time=[]
data_time_s=[]
list=[]
for x in get_details:
    a=x.text
    if a!="Device" and a!="Value" and a!=device_choosing and a!="Tijd":
        list.append(a)
for x in range(len(list)):
    if x%2==0:
        tijd_s = list[x]
        tijd = tijd_s[0:16]
        # data_object= datetime.datetime.strptime(tijd,'%d-%m-%y %H:%M:%S')
        data_time.append(tijd)
        data_time_s.append(tijd_s)
    if x%2!=0:
        value= float(list[x])
        if value<=60 and value!=0:
            data_value.append(value)

        cursor.execute("insert into {} values (null,'{}',{})".format(device_choosing,tijd,value))

database.commit()
avarage= sum(data_value)/len(data_value)
max_value=max(data_value)
min_value=min(data_value)
total_input=len(data_value)
first_input= data_time_s[0]
last_input=data_time_s[-1]
max=data_time_s[data_value.index(max_value)]
min=data_time_s[data_value.index(min_value)]
if len(data_time_s)>1:
    delay= parser.parse(data_time_s[1])-parser.parse(data_time_s[0])
else:
    delay=0
now= datetime.datetime.now().replace(second=0, microsecond=0)
difference= now-parser.parse(data_time_s[-1])



ch(data_time,data_value,device_choosing,device_choosing) #creating a chart
img = Image.new('RGB', (800, 500), color=("white"))
fnt = ImageFont.truetype('CALIBRI.ttf', 25)
fnt2 = ImageFont.truetype('CALIBRI.ttf', 30)
d = ImageDraw.Draw(img)
text="--All data is stored in the database"
text2 = "--A chart has been created. "
text3= "To open database and chart click OK"
d.text((20, 20), "Device name", font=fnt, fill="blue")
d.text((220, 20), device_choosing, font=fnt, fill="green")
d.text((20, 50), "First input",font=fnt, fill="blue")
d.text((220, 50), first_input,font=fnt, fill="green")
d.text((20, 80), "Last input",font=fnt, fill="blue")
d.text((220, 80), "{} ------- {} ago".format(last_input,difference),font=fnt, fill="green")
d.text((20, 110), "Interval",font=fnt, fill="blue")
d.text((220, 110), str(delay),font=fnt, fill="green")
d.text((20, 140), "Total input", font=fnt, fill="blue")
d.text((220, 140), str(total_input),font=fnt, fill="green")
d.text((20, 170), "Maximum value", font=fnt, fill="blue")
d.text((220, 170), "{}{}{}".format (str(max_value),"-"*32,max),font=fnt, fill="green")
d.text((20, 200), "Minumum value", font=fnt, fill="blue")
d.text((220, 200), "{}{}{}".format (str(min_value),"-"*32,min),font=fnt, fill="green")
d.text((20, 230), "Avarage", font=fnt, fill="blue")
d.text((220, 230), "{:.2f}".format(avarage),font=fnt, fill="green")
d.text((20, 280), "*"*70, font=fnt, fill="purple")
d.text((20, 310), text, font=fnt2, fill="red")
d.text((20, 340), text2, font=fnt2, fill="red")
d.text((20, 370), text3, font=fnt2, fill="red")

img.save("images/{}2.png".format(device_choosing))

easygui.msgbox(" ",title="https://internetofthings.glr-imd.nl", image="images/{}2.png".format(device_choosing))







def buttons():
    choices = ["Exit"]
    button = easygui.buttonbox("", choices=choices, images=["images/db.GIF", "images/ch.GIF", "images/wb.GIF"])
    if button=="images/db.GIF":
        os.startfile("IOT2.db")
    elif button=="images/ch.GIF":
        os.startfile('{}.png'.format(device_choosing))
    elif button=="images/wb.GIF":
        device_page = url2 + "/index.php?device=" + device_choosing
        wb.open(device_page)
    else:
        sys.exit(0)
    return buttons()

buttons()
















