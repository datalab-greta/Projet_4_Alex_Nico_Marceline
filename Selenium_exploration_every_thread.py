"""
Created on Thu Oct  3 16:38:40 2019

@author: shikshik
"""

# Librairies pour selenuim
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

#~ import creds
import os,configparser # credentials: 

#Lien de l'url
url = "https://www.fun-mooc.fr/"

#Chemin du webdriver
driver = webdriver.Firefox(executable_path ='/usr/bin/geckodriver')

# Fonction de la connection
def simple_get(url):
    """
    Se connecte a l'url, si statut = 200 retourne le contenu ( en appelant is_good_response)
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
driver.get(url)

# Mail & Mdp du site FUN MOOC
config = configparser.ConfigParser()
login = config.read_file(open(os.path.expanduser("~/Bureau/Projet 4/.datalab.cnf")))
config['mooc']['user']  
import time

# Identification sur FUN MOOCS
login=driver.find_element_by_css_selector('.login-link').click() 

driver.find_element_by_name('email').send_keys(config['mooc']['user'] )
driver.find_element_by_name('password').send_keys(config['mooc']['password'])
driver.find_element_by_id("submit").click()

driver.find_element_by_css_selector('li.course-item:nth-child(7) > div:nth-child(1) > article:nth-child(1) > section:nth-child(1) > div:nth-child(2) > h3:nth-child(1) > a:nth-child(1)').click() #Cours Python3
time.sleep(7)
driver.find_element_by_css_selector('.course-tabs > li:nth-child(4) > a:nth-child(1)').click() #Ouverture de discussion (change sur chaque cours?)
time.sleep(7)

###################################################################################

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

desc_list =[]

i = 1
#a = str(i)
while i < 300:
    try:
        beach_balls = driver.find_elements_by_css_selector('.forum-nav-thread-list')
        
        for ball in beach_balls:
             try:
                 a = str(i)
                 print(a)
                 desc = ball.find_element_by_css_selector('li.forum-nav-thread:nth-child('+a+') > a:nth-child(1) > div:nth-child(2) > span:nth-child(1)').text
                 print (desc)
                                  
                 desc_list.append(desc)
                 time.sleep(5)
                 driver.find_element_by_css_selector('.forum-nav-load-more').click() or driver.find_element_by_css_selector('.forum-nav-load-more-link').click()   
             except NoSuchElementException:
                 if i == None:
                     break
        i += 1
    except: #exceptions.StaleElementReferenceException:
         print('merde CUL CUL CUL CASSE LES COUILLES NORMALEMENT ICI PAS DE PROBLEME FUCK FUCK'+ a)
         pass
     