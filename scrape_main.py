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
readable_date = datetime.today().strftime('%d %B')
#Clean string in case of zero padded number (e.g. 08)
cleaned_date = readable_date.lstrip('0')

for date in dates:
    if re.search(str(cleaned_date),date):
        print("match found")
        
#current_release_date = tags
#prices = doc.find_all(string="$")
#print(prices)
# 
