from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

url = "https://www.gamespot.com/articles/2023-upcoming-games-release-schedule/1100-6508202/"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

##Working
dates = []
tags = doc.find_all('p')
for tag in tags:
    content = tag.text
    dates.append(content)

#Get current date
my_date = datetime.today()
#Convert to 'readable' (e.g. 08 June)
readable_date = datetime.today().strftime('%B %d')
#Clean string in case of zero padded number (e.g. 08)
month = datetime.today().strftime('%B')
day = datetime.today().strftime('%d').lstrip('0')
cleaned_date = month + " " + day
print(cleaned_date)

r = re.compile('{}'.format(cleaned_date))
#r = re.compile("June 8")
newlist = list(filter(r.findall,dates))
print (newlist)

        
#current_release_date = tags
#prices = doc.find_all(string="$")
#print(prices)
# 
