#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:59:06 2019

@author: dubiez
"""

# Librairies pour selenuim
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

#~ import creds
import os,configparser, time # credentials: 

#Lien de l'url
url = "https://www.fun-mooc.fr/"

#set webdriver path
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

#driver.implicitly_wait(10)
driver.get(url)

#Clic boutton pour les cookies 'i agree cookie'
 
#cookie_button = driver.find_element_by_css_selector('.cookie-banner-button').click() #click sur accepter les coockies
login=driver.find_element_by_css_selector('.login-link').click()
#login_button.click() #click accepter les coockies
#time.sleep(1)
config = configparser.ConfigParser()
login = config.read_file(open(os.path.expanduser("~/.datalab.cnf")))
config['mooc']['user']

driver.find_element_by_name("email").send_keys(config['mooc']['user'])
driver.find_element_by_name("password").send_keys(config['mooc']['password'] )
driver.find_element_by_id("submit").click()
driver.find_element_by_css_selector('li.course-item:nth-child(11) > div:nth-child(1) > article:nth-child(1) > section:nth-child(1) > div:nth-child(2) > h3:nth-child(1) > a:nth-child(1)').click() #Cours Python3
time.sleep(6)
#driver.find_element_by_css_selector('.course-tabs > li:nth-child(6) > a:nth-child(1)').click() #1er cours de ma liste
driver.find_element_by_css_selector('.course-tabs > li:nth-child(4) > a:nth-child(1)').click() #Ouverture de discussion (change sur chaque cours?)
time.sleep(5)
driver.find_element_by_css_selector('li.forum-nav-thread:nth-child(1)').click() #Ouverture du premier fil (Merci)

driver.find_element_by_css_selector('li.forum-nav-thread:nth-child(2)').click()

#for a in driver.find_element_by_class_name('')