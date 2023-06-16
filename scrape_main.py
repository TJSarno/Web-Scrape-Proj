from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import pandas as pd
from pathlib import Path


url_games = "https://www.gamespot.com/articles/2023-upcoming-games-release-schedule/1100-6508202/"
url_films = "https://www.gamesradar.com/movie-release-dates/"
filepath_games = "\\csvs\\gamedates.csv"
filepath_films = "\\csvs\\filmdates.csv"

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

    #Write to CSV
    cwd = str(Path(__file__).resolve().parent)
    output_dir = cwd + filepath

    df = pd.DataFrame(dates)
    df.to_csv(output_dir, index= False,header= False)


def return_todays_matches(filepath):
    #Get month
    month = datetime.today().strftime('%B')

    #Get day and clean string in case of zero padded number (e.g. 08)
    day = datetime.today().strftime('%d').lstrip('0')
    cleaned_date = month + " " + day

    #Open and read csv
    cwd = str(Path(__file__).resolve().parent)
    output_dir = cwd + filepath

    with open(output_dir) as csv:
        contents = csv.read()
    #Match regex of current date
    pattern = r'(^.*{}.*$)'.format(re.escape(cleaned_date))
    matches = re.findall(pattern,contents, re.MULTILINE)
    print(matches)

    #If empty, say so
    if not matches:
        print("None found")


#update_csv(url_films, "li", filepath_films)
#update_csv(url_games, "p", filepath_games)
#return_todays_matches(filepath_games)

