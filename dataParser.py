import os
import requests
import traceback
import pandas as pd
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup as bs


def normalizer(text):
    symbols = {'-\n': '', '\n': '', '\t': '', 'ﬁ': 'fi', 'ﬀ': 'ff', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl', '\x0c': 'fi',
               '\xa0': ' ', 'Abstract': ''}
    for symbol in symbols:
        text = text.replace(symbol, symbols[symbol])
    return text


def articleParser(article, keywords, link):
    line = [normalizer(article.find(class_='page_title').get_text()),
            ', '.join([normalizer(name.get_text()) for name in article.find_all(class_='name')])]
    try:
        doi = normalizer(article.find(class_='item doi').a.get_text())
        line.append(doi)
    except:
        line.append(link)

    try:
        abstract = normalizer(article.find('section', 'item abstract').get_text())
        if abstract == 'N/A':
            abstract = '-'
        line.append(abstract)
    except:
        line.append('-')

    try:
        line.append(normalizer(article.find('section', 'item keywords').span.get_text()))
    except:
        keywords = keywords.replace(';', ',')
        line.append(keywords)

    print(line)
    return {'Title': line[0], 'Authors': line[1], 'Doi': line[2], 'Abstract': line[3], 'Keywords': line[4]}


def comboParser(link):
    df = pd.DataFrame(columns=['Title', 'Authors', 'Doi', 'Keywords', 'Abstract'])
    for filename in os.listdir(link):
        print(filename)
        with open(os.path.join(link, filename), 'rb') as f:
            reader = PdfReader(f)
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                text = page.extract_text()
                text = normalizer(text)
                if text.find("DOI") != -1:
                    doiText = (text[text.find('DOI'):])[5:24]
                    if doiText.find('jsfi') != -1:
                        text = text[:text.find("Introduction")]
                        start = text.find('eywords:')
                        keywords = ''
                        if start != -1:
                            keywords += text[start + 9:text.find('.', start)]
                            r = requests.get('https://doi.org/' + doiText)
                            soup = bs(r.text, "html.parser")
                            row = pd.DataFrame([articleParser(soup, keywords, doiText)])
                            df = pd.concat([df, row], ignore_index=True)
    return df


def webParser(link):
    df = pd.DataFrame(columns=['Title', 'Authors', 'Doi', 'Keywords', 'Abstract'])
    response = requests.get(link)
    soup = bs(response.content, 'html.parser')
    journals = soup.find_all('a', class_="title")
    print(soup.find('a', class_='next'))
    while soup.find('a', class_='next'):
        r = requests.get(soup.find('a', class_='next')['href'])
        soup = bs(r.text, "html.parser")
        journals.extend(soup.find_all('a', class_="title"))

    for journal in journals:
        r = requests.get(journal['href'])
        soup = bs(r.text, "html.parser")
        articles = soup.find_all('div', 'obj_article_summary')

        for article in articles:
            meta = article.find('h3', 'title')
            arResponse = requests.get(meta.a['href'])
            arData = bs(arResponse.text, "html.parser")
            row = pd.DataFrame([articleParser(arData, '-', meta.a['href'])])
            df = pd.concat([df, row], ignore_index=True)
    return df


def csvWriter(data):
    data.to_csv("data.csv", sep=";", encoding='utf-8-sig', index=False)
    return 1


# Функция выполняет извлечение данных о статьях
# parsingType – строковый параметр, содержащий тип парсинга
# link – строковый параметр, содержащий путь к данным
# result – возвращаемое значение: 1 при успешном выполнении или ошибка
def getRequest(parsingType, link):
    try:
        if parsingType == 'Web-parsing':
            data = webParser(link)

        elif parsingType == 'PDF-parsing':
            data = comboParser(link)

        csvWriter(data)
        return 1
    except Exception as e:
        return (traceback.format_exc().splitlines())[-1]

