from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import numpy as np
import pandas as pd

url = "https://www.gamespot.com/articles/2023-upcoming-games-release-schedule/1100-6508202/"
filepath = "C:\\Users\\Tom\\Desktop\\Web Scraper Project\\Web-Scrape-Proj\\csvs\\gamedates.csv"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

#Store all release dates found in an array.
##Note this includes dummy data, however no workaround possible due to website formatting.
dates = []
tags = doc.find_all('p')
for tag in tags:
    content = tag.text
    dates.append(content)

##Write to CSV
a = np.asarray(dates)
df = pd.DataFrame(dates)
print(df)
df.to_csv(filepath, index= False,header= False)

#file = open(filepath)
#with file:
#    write = csv.writer(file)
#    write.writerows(dates)

#Get current date
my_date = datetime.today()
#Convert to 'readable' (e.g. 08 June)
month = datetime.today().strftime('%B')
#Clean string in case of zero padded number (e.g. 08)
day = datetime.today().strftime('%d').lstrip('0')
cleaned_date = month + " " + day

r = re.compile('{}'.format(cleaned_date))
newlist = list(filter(r.findall,dates))
print (newlist)

