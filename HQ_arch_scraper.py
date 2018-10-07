import requests
from bs4 import BeautifulSoup as soup

def get_questions(s):
    rows = s.select('tr')
    q_dump = []
    for r in rows:
        try:q_dump.append(r.select('td')[1].text)
        except:pass
    return q_dump

def get_links():
    s = soup(requests.get("https://hqtriviaarchive.com").content,'lxml')
    return [a.attrs['href'] for a in s.select(".entry-content a")[-102:-3]]

def get_all_questions():
    all_questions = []
    for l in get_links():
        s = soup(requests.get(l).content)
        all_questions+=get_questions(s)
    return all_questions