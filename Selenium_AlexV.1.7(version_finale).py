# Librairies pour selenuim
	
from selenium import webdriver
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
#from bs4 import BeautifulSoup
#from pymongo import MongoClient # librairie qui va bien
import configparser, os, time, pickle 

import pandas as pd
from selenium.common.exceptions import NoSuchElementException
#from selenium import webdriver

#Création de la liste des urls

#Lien de l'url
url = "https://www.fun-mooc.fr/"

#set webdriver path
driver = webdriver.Firefox(executable_path ='/usr/bin/geckodriver')
#driver= webdriver.Chrome(executable_path='/snap/bin/chromium.chromedriver')
# Fonction de la connection

def simple_get(url):
    """
    Se connecte a l'url, si statut = 200 retourne le contenu (en appelant is_good_response)
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None
def is_good_response(resp):
    """
    Renvoie 200 si connection a l'url
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)
def log_error(e):
    """
    retourne l'erreur
    """
    print(e)
#driver.implicitly_wait(10)
driver.get(url)

login=driver.find_element_by_css_selector('.login-link').click()

config = configparser.ConfigParser()
login = config.read_file(open(os.path.expanduser("~/.datalab.cnf")))
config['mooc']['user']

driver.find_element_by_name("email").send_keys(config['mooc']['user'])
driver.find_element_by_name("password").send_keys(config['mooc']['password'] )
driver.find_element_by_id("submit").click()

pickle.dump(driver.get_cookies() , open("cookies.pkl","wb"))
cookname=[]
cookies = pickle.load(open("cookies.pkl", "rb"))
#print(cookies)
for cook in cookies:
    print(cook['name'], ':', cook['value'])
    co=cook['name'], cook['value']
    cookname.append(co)
cookname=dict(cookname)
csrftok=(cookname.get('csrftoken'))
time.sleep(3)

driver.find_element_by_css_selector('li.course-item:nth-child(1) > div:nth-child(1) > article:nth-child(1) > section:nth-child(1) > div:nth-child(2) > h3:nth-child(1) > a:nth-child(1)').click() #Cours Python3
time.sleep(5)
driver.find_element_by_css_selector('.course-tabs > li:nth-child(6) > a:nth-child(1)').click() #1er cours de ma liste
#driver.find_element_by_css_selector('.course-tabs > li:nth-child(4) > a:nth-child(1)').click() #Ouverture de discussion (change sur chaque cours?)
#time.sleep(5)

urlsmooc =[]


chargeur = 1

while chargeur < 15:
    try: 
        flop = driver.find_elements_by_css_selector('.forum-nav-thread-list')
        for flip in flop:
            try:
                print(chargeur)
                time.sleep(3)
                driver.find_element_by_css_selector('.forum-nav-load-more').click() or driver.find_element_by_css_selector('.forum-nav-load-more-link').click()
            except NoSuchElementException:
                if chargeur == None:
                    break
        chargeur += 1
    except: #exceptions.StaleElementReferenceException:
         print('stop')
         pass
         break
print('Chargé!!!')
time.sleep(3)

i = 0
a = str(i)

while i < 300:
    try:
        beach_balls = driver.find_elements_by_css_selector('.forum-nav-thread-list')
        i = i + 1
        for ball in beach_balls:
            try:
                a = str(i)
                print(a)
                desc = driver.find_element_by_css_selector('li.forum-nav-thread:nth-child('+a+') > a:nth-child(1) > div:nth-child(2) > span:nth-child(1)')#.text
                desc2 = driver.find_element_by_css_selector('li.forum-nav-thread:nth-child('+a+') > a:nth-child(1)')
#                time.sleep(5)
                desc.click() or desc2.click()
                time.sleep(4)
                urlsmooc.append(driver.current_url)
                time.sleep(4)
#                driver.find_element_by_css_selector('.forum-nav-load-more').click() or driver.find_element_by_css_selector('.forum-nav-load-more-link').click()
                 
            except NoSuchElementException:
#                print('Et galère!')
                pass
                continue
                if i == None:
                    print('Oh merde!')
                    break

#        i += 1
#        links=driver.find_element_by_class_name('forum-nav-thread-title')
    except: #exceptions.StaleElementReferenceException:
         print('Damned'+ a)
         break
access_num=driver.current_url

#urlsmooc = []
#
#page=driver.page_source
##conn = urllib2.urlopen(driver.current_url)
#
#print(driver.page_source)
#soup = BeautifulSoup(page, features="lxml")
#print(soup)
#for tag in soup.find_all('li', class_='forum-nav-thread'):
#    urlsmooc.append(tag['data-id'])
print(urlsmooc)
urlsmooc=pd.DataFrame(urlsmooc)
#urlsmooc.to_csv('~/Documents/Projet_4/Urls_mooc_Accessibilite.csv',index=False, header=False)

##SUIVANT
##Changement de menu et choix du cours sur Python 3
driver.find_element_by_css_selector('#sandwich-menu-icon').click() #clic sur le menu
driver.find_element_by_css_selector('#sandwich-overlay > ul:nth-child(1) > li:nth-child(5) > a:nth-child(1)').click()# clic menu cours
# cours  Python3 (NE MARCHE PAS!)
driver.find_element_by_css_selector('li.course-item:nth-child(11) > div:nth-child(1) > article:nth-child(1) > section:nth-child(1) > div:nth-child(2) > h3:nth-child(1) > a:nth-child(1)').click()
# ouverture de discution
driver.find_element_by_css_selector('.course-tabs > li:nth-child(4) > a:nth-child(1)').click()
time.sleep(2)
## Boucle pour Charger plus de discussions
timing = 0

while timing < 55:
    try: 
        flop = driver.find_elements_by_css_selector('.forum-nav-thread-list')
        for flip in flop:
            try:
                print(timing)
                time.sleep(5)
                driver.find_element_by_css_selector('.forum-nav-load-more-link').click() #or driver.find_element_by_css_selector('.forum-nav-load-more').click()
            except NoSuchElementException:
                if timing == None:
                    break
        timing = timing + 1
    except: #exceptions.StaleElementReferenceException:
         print('stop')
         pass
         break
print('Chargé!!!')
time.sleep(3)

## récup du contenu de Python 3
py3=driver.current_url

urlsmoocpy3 = []

page=driver.page_source
#conn = urllib2.urlopen(driver.current_url)

#print(driver.page_source)
soup = BeautifulSoup(page, features="lxml")
#print(soup)
for tag in soup.find_all('li', class_='forum-nav-thread'):
    urlsmoocpy3.append(tag['data-id'])
for tag in soup.find_all('a'):
    print(tag['href'])
print(urlsmoocpy3)
urlsmoocpy3=pd.DataFrame(urlsmoocpy3)
urlsmoocpy3.to_csv('Mooc_python3.csv',index=False, header=False)


config = configparser.ConfigParser()
config.read_file(open(os.path.expanduser("~/.datalab.cnf")))

CNF = "mongo"
BDD = "Datalab"

# Ouverture connection -> mongo sur serveur
client = MongoClient('mongodb://%s:%s@%s/?authSource=%s' % (config[CNF]['user'], config[CNF]['password'], config[CNF]['host'], BDD))
print(client)

bdd = client['MOOC_GRP_MAN'] # BDD "Datalab" de mongoDB sur serveur
bdd
print("'MOOC_GRP_MAN' Collections:")
for cn in bdd.list_collection_names():
    print("-"+cn)
collec = client['MOOC_GRP_MAN']['Triss_Merigold']
cternazscie=urlsmoocAcces1[14]

#for urlsmooc in urlsmoocAcces1:
response = requests.get(
    "https://www.fun-mooc.fr/courses/course-v1:inria+41012+self_paced/discussion/forum/i4x-inria-41012S02-course-session02/threads/"+cternazscie+"?ajax=1&resp_skip=0&resp_limit=999",
    #params={'q': 'requests+language:python'},
    #headers={'Accept': 'application/vnd.github.v3.text-match+json'},
    headers={
        #"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:69.0) Gecko/20100101 Firefox/69.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        #"Accept-Language": "en-US,en;q=0.5",
        "X-CSRFToken": ""+csrftok+"", #Change à chaque fois!!!!
        "X-Requested-With": "XMLHttpRequest",
        #'Referer': 'https://www.fun-mooc.fr/courses/course-v1:MinesTelecom+04026+session05/discussion/forum/204c764cf87424d86a6259562d1d200afe30ab9a/threads/5d9481db1c89dcf269015b6f' ,
        'Cookie': 'Cookie: defaultRes=900%2C0; csrftoken='+csrftok+'; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%222bcd8684-307f-4536-8925-aef21cd909ff%22%2C%22options%22%3A%7B%22end%22%3A%222020-11-02T08%3A43%3A21.983Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-602676-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; sessionid=xh3lf4oa1xsdnjukvsf25zvx1scyib69; edxloggedin=true; edx-user-info="{\"username\": \"Gerikk\"\054 \"version\": 1\054 \"email\": \"alexandreblt4@gmail.com\"\054 \"header_urls\": {\"learner_profile\": \"https://www.fun-mooc.fr/u/Gerikk\"\054 \"logout\": \"https://www.fun-mooc.fr/logout\"\054 \"account_settings\": \"https://www.fun-mooc.fr/account/settings\"}}"'
    },
)
print(response)
#    print(response.content)
pprint.pprint(response.json())

collec.insert_one(response.json())



for d in response.content:
    test=response.json()


print(response.content)
pprint.pprint(response.json())
Dico=response.json()
