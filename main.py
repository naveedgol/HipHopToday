#!/usr/bin/env python

import datetime
import requests
import urllib.request
from bs4 import BeautifulSoup

def scrape_number_1(url, year):
    source = requests.get(url).text
    source_soup = BeautifulSoup(source, "html.parser")
    song_name = source_soup.find("h2", {"class": "chart-row__song"})
    song_artist = source_soup.find("a", {"class": "chart-row__artist"})

    image_file_name = "Assets/Images/" + str(year) + ".jpg"
    image_link = source_soup.find("div", {"class": "chart-row__image"}).get("style")
    urllib.request.urlretrieve(image_link[22:len(image_link)-1], image_file_name)

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

def write_to_html(info):
    html_file = open('index.html', "r+")
    html_doc_soup = BeautifulSoup(html_file, "html.parser")
    counter = 0
    year = 2017
    for i in html_doc_soup.findAll("p"):
        i.string = str(year-counter) + ": " + info[counter]
        counter += 1

    date = html_doc_soup.find("h2")
    months = ["zero", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    date.string = months[datetime.datetime.today().month] + " " + str(datetime.datetime.today().day) + ", " + str(datetime.datetime.today().year)

    html_file.close()
    html_output = html_doc_soup.prettify("utf-8")
    with open("index.html", "wb") as file:
        file.write(html_output)

day_counter = 0
# date = [""]*11
song_info = [""]*10
for i in range(0,10):
    if i == 1 or i == 5 or i == 9:
        day_counter += 1
    closest_saturday = today_date_adjuster(datetime.datetime.today() - datetime.timedelta(days=day_counter))
    # print(closest_saturday)
    # date[i] = (datetime.datetime.today() - datetime.timedelta(days=day_counter)).year
    song_info[i] = scrape_number_1("http://www.billboard.com/charts/r-b-hip-hop-songs/" + closest_saturday, int(closest_saturday[:4]))
    day_counter += 365

write_to_html(song_info)
