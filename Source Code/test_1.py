from bs4 import BeautifulSoup
from multiprocessing import Pool
import requests
import urllib
from urllib.request import urlopen
import re
import ssl
import sys
import random
import os

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


def get_page_content(url):
    try:
        html_response_text = urlopen(url).read()
        page_content = html_response_text.decode('utf-8')
        return page_content
    except Exception as e:
        return None


def clean_title(title):
    invalid_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for c in invalid_characters:
        title = title.replace(c,'')
        return title


def get_urls(take):
    soup = BeautifulSoup(take, 'html.parser')
    links = soup.find_all('a')
    urls = []
    for link in links:
        urls.append(link.get('href'))
    return urls

def is_url_valid(url):
    if url is None:
        return False
    if re.search('#', url):
        return False
    match = re.search('^/wiki/', url)
    match2 = re.search('^/technology/', url)
    match3 = re.search('https://www.britannica.com/', url)
    if match or match2 or match3:
        return True
    else:
        return False

def reformat_url(url):
    match = re.search('^/wiki/', url)
    if match:
        return "https://en.wikipedia.org"+url
    else:
        return url


def save(text, path):
    f = open("/Users/hrithik/PycharmProjects/testpy/Webpages.txt", 'a+', encoding='utf-8', errors='ignore')
    f.write(text+'\n')
    f.close()


def save2(text, path):
    f = open("/Users/hrithik/PycharmProjects/testpy/Webpages.txt", 'a+', encoding='utf-8', errors='ignore')
    f.write(text+'\n\n\n')
    f.close()


def download_website(url, title):
    urllib.request.urlretrieve(url, title+".html")


def webSearcher(url,term):
    soup = BeautifulSoup(url, 'html.parser')
    main_content = soup.get_text
    page = urlopen(url).read().decode('utf-8')
    return(len(re.findall(term, page,re.IGNORECASE)))

def get_terms(url):
    termList = []
    tempList = []
    page_content = get_page_content(url)
    soup = BeautifulSoup(page_content, 'html.parser')
    main_content = soup.get_text
    links = soup.find_all('p')
    for link in links:
        if link.find('a'):
            continue
        elif link.find('i'):
                continue
        elif link.find('class'):
                continue
        elif link.find('style'):
                continue
        elif link.find('em'):
                continue
        elif link.find('text-align'):
                continue
        elif link.find('strong'):
            all_links = link.find_all("strong")
            try:
                pre_terms = all_links[0].get_text()
                if(len(pre_terms.split()) < 4):
                    tempList.append(pre_terms)
                    while(pre_terms[-1] == ":" or pre_terms[-1] == " "):
                        pre_terms = pre_terms[:-1]
                    termList.append(pre_terms)
            except:
                continue
        else:
            continue
    return termList

staticcount = 0
def countingPages(n):
    list = list()
    randint = random.randint((n-1)*10,n*10+1)
    if randint not in list:
        list.append(randint)
        return randint
    else:
        countingPages(n)







seedUrls = ["https://en.wikipedia.org/wiki/Artificial_intelligence", "https://www.britannica.com/technology/artificial-intelligence","https://en.wikipedia.org/wiki/Machine_learning", "https://en.wikipedia.org/wiki/Robot","https://en.wikipedia.org/wiki/Artificial_neural_network","https://en.wikipedia.org/wiki/Computer_vision#Recognition"]
queue = []
path = "/Users/hrithik/PycharmProjects/testpy"
visitedLinks = []
count = 0
page_counter = 0
savedUrlList = []
finalLinklist = []
related_terms = []
for url in seedUrls:
    queue.append(url)
    visitedLinks.append(url)

i = 0;
related_terms = get_terms("https://learn.g2.com/artificial-intelligence-terms")
print(related_terms)

for i in range(6):
    url = queue[0]
    del queue[0]
    print(i)
    print(str(url))
    page_content = get_page_content(url)
    if not page_content:
        continue
    soup = BeautifulSoup(page_content, 'html.parser')
    main_content = soup.get_text()
    outgoing_urls = get_urls(page_content)
    for eachUrl in outgoing_urls:
        if( is_url_valid(eachUrl) and eachUrl not in visitedLinks):
            #queue.append(eachUrl)
            visitedLinks.append(eachUrl)
            if i == 0:
                finallink = "https://en.wikipedia.org/"+str(eachUrl)
                finalLinklist.append(finallink)

            else:
                if re.search('https://www.britannica.com/', eachUrl):
                    finallink = str(eachUrl)
                else:
                    finallink = "https://www.britannica.com/"+str(eachUrl)
                finalLinklist.append(finallink)

print(len(finalLinklist))

related_terms = get_terms("https://learn.g2.com/artificial-intelligence-terms")
tempcount = 1;

def scrape(url):
    global count
    global tempcount
    global page_counter
    res = requests.get(url)
    count = 0
    tempcount += 1;
    for term in related_terms:
        count +=  webSearcher(url,term)
    if res.status_code == 200:
        if count >= 2:
            page_content = get_page_content(url)
            soup = BeautifulSoup(page_content, 'html.parser')
            temp_title = soup.title.string
            title = clean_title(temp_title)
            save(title, path)
            print(temp_title)
            download_website(url, title)
            savedUrlList.append(url)
            page_counter += 1
            #finalcount = countingPages(page_counter)
            print("Term counter: "+str(count)+" url: "+str(url))
            line = "Term counter: "+str(count)+" url: "+str(url)
            save2(line,path)

        if(page_counter > 3):
            sys.exit()



p = Pool(10)
p.map(scrape, finalLinklist)
p.terminate()
p.join()

