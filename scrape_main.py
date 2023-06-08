from bs4 import BeautifulSoup
import requests

url = "https://www.gamespot.com/articles/2023-upcoming-games-release-schedule/1100-6508202/"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

tags = doc.find_all("p")
parent = tags[0].parent

print(parent)

#current_release_date = tags
#prices = doc.find_all(string="$")
#print(prices)