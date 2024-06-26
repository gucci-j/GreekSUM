# Script used to crawl news articles from https://www.news247.gr/ . 
# crawl_news.py has to be executed before hand 

from bs4 import BeautifulSoup
import requests
import csv
import time as timelibrary
from os import path
import os

input_directory = "./data/"
output_directory = "./data/crawled_articles"

if not path.isdir(output_directory):
    os.mkdir(output_directory)

for category in ["economy", "culture", "international"]:
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
        print(row_number)
        
        html = requests.get(row[-1]).content
        soup = BeautifulSoup(html, "html.parser")
        article = soup.find("article", {"class":"single_article"})
        if article is not None:
            summary = article.find("h2", {"class":"article__lead"})
        else:
            summary = None

        fname = "./data/crawled_articles/" + category + "_" + str(row_number)
        if article is None or summary is None:
            temp = open(fname, 'w')
            temp.close()
            news_writer.writerow([row[0], "", row[1], row[2]])
            continue

        summary = summary.text.strip()
        news_writer.writerow([row[0], summary, row[1], row[2]])

        article = article.find("div", {"class": "paragraph"})
        text = []
        for paragraph in article.find_all("p"):
            text.append(paragraph.text.strip()) 
        with open(fname, 'w') as f:
            f.write("\n".join(text))
        timelibrary.sleep(5)

    news_r.close()
    news_w.close()
