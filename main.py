import datetime
import requests
from bs4 import BeautifulSoup

def scrape_number_1(url):
    source = requests.get(url).text
    source_soup = BeautifulSoup(source, "html.parser")
    song_name = source_soup.find("h2", {"class": "chart-row__song"})
    song_artist = source_soup.find("a", {"class": "chart-row__artist"})
    return song_name.string+" - "+song_artist.string.strip()

def today_date_adjuster(date):
    days_away_from_saturday = 5-date.weekday()
    if days_away_from_saturday >= 0:
        date += datetime.timedelta(days=days_away_from_saturday)
    else:#sunday
        date += datetime.timedelta(days=6)
    return date_formatter(date)

def date_formatter(date):
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    if int(day) < 10:
        day = "0" + day
    if int(month) < 10:
        month = "0" + month
    formatted_date = year + "-" + month + "-" + day
    return formatted_date

for i in range(0,11):
    closest_saturday = today_date_adjuster(datetime.datetime.today() - datetime.timedelta(days=365*i))
    print(date_formatter(datetime.datetime.today() - datetime.timedelta(days=365*i)))
    print(scrape_number_1("http://www.billboard.com/charts/r-b-hip-hop-songs/" + closest_saturday))