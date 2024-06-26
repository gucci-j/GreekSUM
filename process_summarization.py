import zipfile
from random import shuffle
import os
import json
import pandas as pd
from pathlib import Path
import math
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from clean_text import cleaner
#create dataset for abstract and title


zip_path = "./data/sum_data.zip"
extract_dir = "./data"

if not os.path.isdir(extract_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

path_articles = os.path.join(extract_dir,'crawled_articles')
articles = os.listdir(path_articles)
title_abstract = {'culture':'culture_with_summary.csv','economy':'economy_with_summary.csv','international':'international_with_summary.csv','politics':'politics_with_summary.csv'}


path_parsed = os.path.join(extract_dir,'parsed/')

if not os.path.isdir(path_parsed):
    os.mkdir(path_parsed)

dfs = {}
for category in title_abstract.keys():
    df=pd.read_csv(os.path.join(extract_dir,title_abstract[category]), header=0)
    dfs[category] = df

for article in articles:
    dc = {}
    body = ""
    with open(os.path.join(path_articles, article), 'r', encoding='UTF-8') as f:
        line_not_1 = "Ακολουθήστε το News247.gr στο Google News και μάθετε πρώτοι όλες τις ειδήσεις"
        line_not_2 = "Διαβάστε τις Ειδήσεις από την Ελλάδα και τον κόσμο, με την αξιοπιστία και την εγκυρότητα του News247.gr"
        for line in f:
            if line!=line_not_1 and line!=line_not_2:
                t = cleaner(line.strip())
                body=body+" "+t
    dc["article"]=body
    category = None
    for key in dfs.keys():
        if key in article:
            category = key
    ind = int(article[article.find("_")+1:]) - 1
    print(category, article, ind)
    df = dfs.get(category)
    row = df.loc[ind]
    # title,summary,time,url
    if row["title"]!=row["title"]:
        continue
    if row["summary"]!=row["summary"]:
        continue
    dc["title"]=row["title"].strip().replace("\n"," ")
    dc["abstract"]=row["summary"].strip().replace("\n"," ")
    dc["time"]=row["time"]
    dc["url"]=row["url"]
    dc["label"]=category
    with open(path_parsed+article+".json", 'w', encoding='utf8') as jfile:
        json.dump(dc, jfile, sort_keys=True, indent=4, ensure_ascii=False)
