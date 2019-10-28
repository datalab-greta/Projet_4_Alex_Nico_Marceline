library(tidyverse)
library(config)
library(DBI)
library(RPostgreSQL)
library(ggplot2)
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

selection= DBI::fetch(dbSendQuery(mydb, "SELECT * FROM mooc_grp_man.nicolas2 ORDER BY date"), n=-1)
#Select2=DBI::fetch(dbSendQuery(mydb, "SELECT course_id, date FROM mooc_grp_man.nicolas2 ORDER BY date"), n=-1)

Count=DBI::fetch(dbSendQuery(mydb,"SELECT nicolas2.course_id AS cid, COUNT(course_id) FROM mooc_grp_man.nicolas2 GROUP BY cid"), n=-1)


#-----------Pour la déconnection!-----------------------
dbDisconnect(mydb)


#----------Dataviz-----------------------------------
#Creation of a color palette with different sizes for plots
ColorschemeBG<-grDevices::colorRampPalette(colorRamps::blue2green(30))
Colours<-ColorschemeBG(100)
Col_L<-ColorschemeBG(300)
Col_S<-ColorschemeBG(6)
fillBG<-ggplot2::scale_fill_manual(values=Colours)
L_fillBG<-ggplot2::scale_fill_manual(values=Col_L)
S_fillBG<-ggplot2::scale_fill_manual(values=Col_S)
coulBG<-ggplot2::scale_color_manual(values=Colours)
L_coulBG<-ggplot2::scale_color_manual(values=Col_L)
S_coulBG<-ggplot2::scale_color_manual(values=Col_S)

#-------Plot global---------

Select2<-selection
Select2$date<-substr(Select2$date, 0, 10)
Select2$date<-as.Date(Select2$date)

Global<-ggplot(Select2) + 
  aes(x = date) +
  geom_bar(fill = "purple") +
  labs(x = "Années", y = "Nombre", title = "Vue d'ensemble des messages envoyés", subtitle = "de 2014 à 2019") +
  scale_x_date(breaks = "1 year", date_minor_breaks = "1 month", date_labels = "%Y")
Global

#-------Nombre de messages par année-------
Dates<-selection %>%
  dplyr::group_by(id, course_id, date, body, title, courseware_title, thread_type, username) %>%
  dplyr::summarise(Nombre = n())
Dates$date<-substr(Dates$date, 0, 4)


plot1<-ggplot2::ggplot(Dates)+ geom_col(aes(x= date, y=Nombre, fill=date)) + S_fillBG + ggplot2::labs(title ="Nombre de messages de 2014 à 2019", x = "Années", y="Nombre de messages")
plot1

#---------------Comparaison des nombres de questions et de discussion-------------

ggplot(selection) +
  aes(x = thread_type, fill = thread_type) +
  geom_bar() +
  scale_fill_hue() +
  scale_fill_brewer(palette = "Set1") +
  labs(title = "Comparaison des nombres de questions et de discussions", x='Type de thread', y="Nombre d'occurences", fill="Type de thread")

#----------------Nombres de questions et de discussion 2019------------------

ggplot(Select2) +
  aes(x = date, fill = thread_type) +
  geom_histogram(bins = 30L) +
  scale_fill_hue() +
  scale_fill_brewer(palette = "Set1")+
  labs(title = "Nombres de questions et de discussions", subtitle = "De 2014 à 2019", x='Type de thread', y="Nombre d'occurences", fill="Type de thread") +
  scale_x_date(breaks = "1 year", date_minor_breaks = "1 month", date_labels = "%Y")

#----Dataframes des plots

cours_questions<-selection %>%
  dplyr::group_by(course_id, thread_type) %>%
  dplyr::summarise(Nombre = n()) %>%
  filter(thread_type == 'question')

cours_discussions<-selection %>%
  dplyr::group_by(course_id, thread_type) %>%
  dplyr::summarise(Nombre = n()) %>%
  filter(thread_type == 'discussion')

Tous<-selection %>%
  dplyr::group_by(course_id, thread_type) %>%
  dplyr::summarise(Nombre = n())


#-------Combinaison top 20 question et discussions

ggplot(Tous[1:38,]) +
  aes(x = reorder(course_id, Nombre), y=Nombre, fill = thread_type) +
  geom_col() +
  coord_flip()+
  scale_fill_brewer(palette = "Set1") +
  labs(title = "Top 20 des questions et discussions par cours", x='Cours', y="Nombre d'occurences", fill="Type de thread")


#---------Plot du top 20 des discussions----------

Discussions<-ggplot2::ggplot(cours_discussions[1:20,]) +
  geom_col(aes(x = reorder(course_id, Nombre), y= Nombre, fill=Nombre))
Discussions + S_coulBG + labs(title = "Top 20 de discussions par cours", x='Cours', y="Nombre d'occurences") + coord_flip()+scale_fill_gradient(low = "red", high = "darkred")

#---------Plot du top 20 des questions----------

Questions<-ggplot2::ggplot(cours_questions[1:20,]) +
  geom_col(aes(x = reorder(course_id, Nombre), y= Nombre, fill=Nombre)) +
  scale_fill_gradient(low = "blue", high = "darkblue")
Questions + coord_polar() + S_coulBG + labs(title = "Top 20 de questions par cours", x='Cours', y="Nombre d'occurences") +  scale_x_discrete(labels = abbreviate)
