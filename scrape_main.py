from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import pandas as pd

urlT = "https://www.gamespot.com/articles/2023-upcoming-games-release-schedule/1100-6508202/"
filepathT = "C:\\Users\\Tom\\Desktop\\Web Scraper Project\\Web-Scrape-Proj\\csvs\\gamedates.csv"

def update_csv(url, tag_type, filepath):
    #Http request
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    #Store all release dates found in an array.
    #NOTE: this can include dummy data, workarounds sometimes not possible due to website formatting.
    dates = []
    tags = doc.find_all(tag_type)
    for tag in tags:
        content = tag.text
        dates.append(content)

    ##Write to CSV
    df = pd.DataFrame(dates)
    df.to_csv(filepath, index= False,header= False)

update_csv(urlT, 'p', filepathT)



#Get current date
my_date = datetime.today()
#Convert to 'readable' (e.g. 08 June)
month = datetime.today().strftime('%B')
#Clean string in case of zero padded number (e.g. 08)
day = datetime.today().strftime('%d').lstrip('0')
cleaned_date = month + " " + day

#Open and read csv
with open(filepathT) as csv:
    contents = csv.read()
#Match regex of current date
pattern = r'(^.*{}.*$)'.format(re.escape(cleaned_date))
matches = re.findall(pattern,contents, re.MULTILINE)
print(matches)

