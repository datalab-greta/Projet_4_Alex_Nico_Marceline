












import requests, pprint

response = requests.get(
        #URL de un cours avec tout les commentaires dedans
    "https://www.fun-mooc.fr/courses/course-v1:MinesTelecom+04026+session05/discussion/forum/204c764cf87424d86a6259562d1d200afe30ab9a/threads/5d9481db1c89dcf269015b6f?ajax=1&resp_skip=0&resp_limit=25",
    #params={'q': 'requests+language:python'},
    #headers={'Accept': 'application/vnd.github.v3.text-match+json'},
    headers={
        #"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:69.0) Gecko/20100101 Firefox/69.0",
        #"Accept": "application/json, text/javascript, */*; q=0.01",
        #"Accept-Language": "en-US,en;q=0.5",
        "X-CSRFToken": "LvmImlOzFWNoC8oQbAdPUvlP7a4ab3KZ", # token change a chaque nouvelle connection !
        "X-Requested-With": "XMLHttpRequest",
        #'Referer': 'https://www.fun-mooc.fr/courses/course-v1:MinesTelecom+04026+session05/discussion/forum/204c764cf87424d86a6259562d1d200afe30ab9a/threads/5d9481db1c89dcf269015b6f' ,
        'Cookie': 'defaultRes=2400%2C0; csrftoken=LvmImlOzFWNoC8oQbAdPUvlP7a4ab3KZ; __utma=218362510.833297836.1474796751.1542221217.1542232713.415; acceptCookieFun=on; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%2231d3b730-8db4-4c4b-9b98-be9e14c92513%22%2C%22options%22%3A%7B%22end%22%3A%222020-09-27T13%3A54%3A31.376Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-602676-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; sessionid=kyxq7top4gplpn8dinb5y1ez0wdg6hrl; edxloggedin=true; edx-user-info="{\"username\": \"EGo41\"\054 \"version\": 1\054 \"email\": \"emmanuel.goudot@gmail.com\"\054 \"header_urls\": {\"learner_profile\": \"https://www.fun-mooc.fr/u/EGo41\"\054 \"logout\": \"https://www.fun-mooc.fr/logout\"\054 \"account_settings\": \"https://www.fun-mooc.fr/account/settings\"}}"'
    },#cookie change tout le temps
)




print(response.content)
pprint.pprint(response.json())
Dico=response.json()