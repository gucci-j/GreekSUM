# Script used to crawl news articles from https://www.news247.gr/ . 
# crawl_news.py has to be executed before hand 

from bs4 import BeautifulSoup
import requests
import csv
import time as timelibrary
from os import path
import os

input_directory = "./"
output_directory = "crawled_articles"

if not path.isdir(output_directory):
    os.mkdir(output_directory)

for category in ["politics", "economy", "culture", "international"]:
    news_r = open(path.join(input_directory, category + ".csv"), "r")
    news_reader = csv.reader(news_r, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    news_w = open(path.join(input_directory, category + "_with_summary.csv"), "w")
    news_writer = csv.writer(news_w, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    news_writer.writerow(["title", "summary", "time", "url"])

    row_number = -1
    for row in news_reader:
        row_number += 1
        if row_number < 1:
            continue
        fname = "crawled_articles/" + category + "_" + str(row_number)
        if path.exists(fname):
            continue
        html = requests.get(row[-1]).content
        soup = BeautifulSoup(html, "html.parser")
        article = soup.find("article", {"class":"single_article"})
        summary = article.find("h2", {"class":"article__lead"})

        if article is None or summary is None:
            temp = open(fname, 'w')
            temp.close()
            continue

        summary = summary.text.strip()
        summary = article.find("h2", {"class":"article__lead"})

        article = article.find("div", {"class": "paragraph"})
        text = []
        for paragraph in article.find_all("p"):
            text.append(paragraph.text) 
        with open(fname, 'w') as f:
            f.write("\n".join(text))
        timelibrary.sleep(5)

    news_r.close()
    news_w.close()
