##### CONNECTION AVEC PARSER ##############################

library(mongolite)
library(jsonlite)
library(config)

# Chemin du fichier utilisé pour l'identification
conf <- config::get("mongo", file = "/home/shikshik/Bureau/Projet 4/config.yml", use_parent = FALSE)

# Paramètres utilisés par le fichier conf
user<-conf$user
password<-conf$password
Dt<-conf$data
host<-conf$host
 
# URL de la base, avec les paramètres des mot de passes etc utilisé...
dturl<-paste("mongodb://",user,":",password,"@",host,"/",Dt, sep = "")
connection <- mongo(db="MOOC_GRP_MAN", collection = 'Forum',  url = dturl)#"mongodb://rondet:QKfv3nakd4tgzNNz3pbnPEQXMyCPzm@127.0.0.1:27018/Datalab")

# recherche générale sur la DB utilisé
connection$find()

##### FIND ###################################

# on met la recherche générale dans une data frame pour pouvoir la traiter comme on le souhaite
alldata <- connection$find('{}')
print(alldata)

# le contenu de la clé "content"
alldata$content

# [[1]] pour l'objet dans la db choisi... 
# Username de la personne qui pose le 1er "commentaire" du Fil de discussion.
alldata$content$username[[1]]

# Usernames des personnes qui ont commentés le premier "commentaire" du Fil de discussion.
alldata$content$children[[1]]$username

# Le texte des commentaires des personnes qui ont commentés le premier "commentaire".
alldata$content$children[[1]]$body

#children de children....
alldata$content$children[[1]]$children[[10]]

# pseudo de la personne qui répond a un commentaire du file
alldata$content$children[[1]]$children[[10]]$username 

# pseudo des personnes qui ont répondu(3) au commentaire ciblé
# ( 23eme commentaire dans le cas précis)
alldata$content$children[[1]]$children[[23]]$username

# liste des commentaires de comentaires...
alldata$content$children[[1]]$children





alldata$find(query='{"content": {"username" : {"$regex": "^C"}}}')

# La commande $regex permet d’utiliser des expressions régulières :
alldata$find(query='{"name": {"$regex": "^C", "$options" : "i"} }',
                fields='{"_id":0, "name":1, "alias":1}')