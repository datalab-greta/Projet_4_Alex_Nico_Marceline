#install.packages("mongolite")
library(config)
library(RPostgreSQL)
#Définition du chemin du dossier config.rml (à créer avant)
conf <- config::get("Postgre", file="~/Documents/Projet_4/.config.yml", use_parent = FALSE)

#-----------------Définition des variables issues de config--------------------
user1<-conf$user
password1<-conf$password
Dt<-conf$database
host<-conf$host

#--------------URL pour connection à la base sans mot de passe--------------

drv <- dbDriver("PostgreSQL")
mydb<- dbConnect(drv, user=user1, password=password1, dbname=Dt, host=host)
DBI::dbListTables(mydb)

usernames10 = DBI::fetch(dbSendQuery(mydb, "select * from test.all_moocs_alex limit 10"), n=-1)
#-----------Pour la déconnection!-----------------------
dbDisconnect(mydb)
