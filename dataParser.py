import os
import requests
import traceback
import pandas as pd
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup as bs


def normalizer(text):
    text = text.replace('-\n', '')
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    text = text.replace('ﬁ', 'fi')
    text = text.replace('ﬀ', 'ff')
    text = text.replace('ﬂ', 'fl')
    text = text.replace('ﬃ', 'ffi')
    text = text.replace('ﬃ', 'ffi')
    text = text.replace('ﬄ', 'ffl')
    text = text.replace('\x0c', 'fi')
    text = text.replace('\xa0', ' ')
    text = text.replace('Abstract', '')
    return text


def articleParser(article, keywords):
    line = [normalizer(article.find(class_='page_title').get_text()),
            ', '.join([normalizer(name.get_text()) for name in article.find_all(class_='name')]),
            normalizer(article.find(class_='item doi').a.get_text()),
            normalizer(article.find('section', 'item abstract').get_text())]
    try:
        line.append(normalizer(article.find('section', 'item keywords').span.get_text()))
    except:
        keywords = keywords.replace(';', ',')
        line.append(keywords)
    return {'Title': line[0], 'Authors': line[1], 'Doi': line[2], 'Abstract': line[3], 'Keywords': line[4]}


def comboParser(link):
    df = pd.DataFrame(columns=['Title', 'Authors', 'Doi', 'Keywords', 'Abstract'])
    for filename in os.listdir(link):
        with open(os.path.join(link, filename), 'rb') as f:
            reader = PdfReader(f)
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                text = page.extract_text()
                text = normalizer(text)
                if text.find("DOI") != -1:
                    doiText = (text[text.find('DOI'):])[5:24]
                    if doiText.find('jsfi') != -1:
                        print(doiText)
                        text = text[:text.find("Introduction")]
                        start = text.find('eywords:')
                        keywords = ''
                        if start != -1:
                            keywords += text[start+9:text.find('.', start)]
                            r = requests.get('https://doi.org/' + doiText)
                            soup = bs(r.text, "html.parser")
                            row = pd.DataFrame([articleParser(soup, keywords)])
                            df = pd.concat([df, row], ignore_index=True)
    return df


def webParser(link):
    df = pd.DataFrame(columns=['Title', 'Authors', 'Doi', 'Keywords', 'Abstract'])
    response = requests.get(link)
    soup = bs(response.content, 'html.parser')
    journals = soup.find_all('a', class_="cover")
    while soup.find('a', class_='next'):
        r = requests.get(soup.find('a', class_='next')['href'])
        soup = bs(r.text, "html.parser")
        journals.extend(soup.find_all('a', class_="cover"))
    for journal in journals:
        print(journal['href'])
        r = requests.get(journal['href'])
        soup = bs(r.text, "html.parser")
        articles = soup.find_all('div', 'obj_article_summary')
        for article in articles:
            meta = article.find_all('div', 'meta')
            if len(meta) == 2:
                arResponse = requests.get(meta[1].a['href'])
                arData = bs(arResponse.text, "html.parser")
                row = pd.DataFrame([articleParser(arData, '')])
                df = pd.concat([df, row], ignore_index=True)
    return df


def csvWriter(data):
    data.to_csv("data.csv", sep=";", encoding='utf-8-sig', index=False)
    return 1


def getRequest(key, link):
    try:
        if key == 'Web-parsing':
            data = webParser(link)
        elif key == 'PDF':
            data = comboParser(link)
        csvWriter(data)
        return 1
    except Exception as e:
        return traceback.format_exc()
