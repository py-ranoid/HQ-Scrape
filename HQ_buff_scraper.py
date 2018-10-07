import re,requests,json
import datetime
from bs4 import BeautifulSoup as soup

def get_questions(content,source="NA"):
    reg = b"hqbuff.currentGame = ([^;]*);"
    try:
        q_list = json.loads(re.findall(reg,content)[0].decode('utf-8'))['questions']
        q_dump = []
        for x in q_list:
            try:q_dump.append([x['text'],x['category'],source])
            except:print ("No Q? :",x)
        return q_dump
    except IndexError:
        print ("No questions found")
        return []

def prev_day_link(s):
    return s.select('.pagination > a')[0].attrs['href']

def quiz_links(s):
    return [x.attrs['href'] for x in s.select('.tab-item a')]

def hb_link(link):
    return "https://hqbuff.com" + link if link.startswith('/') else link

def spider(seed="https://hqbuff.com/uk", questions = []):
    print ("SEED :",seed)
    cont = requests.get(hb_link(seed)).content
    s = soup(cont,"lxml")
    quizzes = quiz_links(s)
    if len(quizzes) > 1:
        for l in quizzes:
            print (l,end=' :: ')
            cont_page = requests.get(hb_link(l)).content
            try :page_questions = get_questions(cont_page)
            except : 
                print ("Problem : ",hb_link(l))
                page_questions = []
            questions+=page_questions
        print ()
    else:
        page_questions = get_questions(cont)
        questions+=page_questions
    try:prev = prev_day_link(s)
    except:print("Prev not found :",seed)
    if prev:
        return questions + spider(hb_link(prev))    
    else:
        return questions

ALLOWED_COUNTRIES = {'us','uk','de','au'}
all_questions = []
day = datetime.timedelta(days=1)

def spider_iter(start = datetime.datetime.now()-day,country="us"):
    if country not in ALLOWED_COUNTRIES:
        print ("Country Name must be in ",ALLOWED_COUNTRIES)
        return
    global all_questions
    date = start
    while True:
        URL = "https://hqbuff.com/"+country+"/game/"+date.strftime("%Y-%m-%d")
        print (URL)
        cont = requests.get(hb_link(URL)).content
        s = soup(cont,"lxml")
        quizzes = quiz_links(s)
        if len(quizzes) > 1:
            for l in quizzes:
                print (l,end=' :: ')
                cont_page = requests.get(hb_link(l)).content
                all_questions+=get_questions(cont_page,source='hq_buff_'+country)
            print ()
        else:
            page_questions = get_questions(cont,source='hq_buff_'+country)
            all_questions+=page_questions
        date -= day    