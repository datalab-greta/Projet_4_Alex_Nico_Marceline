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

#-------test général---------

Select2<-selection
Select2$date<-substr(Select2$date, 0, 10)
Select2$date<-as.Date(Select2$date)

# Global<-ggplot2::ggplot(Select2) + geom_bar(aes(x=date, fill=date))
# Global + ggplot2::ggtitle("Nombre de résultats entre 2014 et 2019") + scale_x_discrete
#library(ggplot2)

Global<-ggplot(Select2) + 
  aes(x = date) +
  geom_bar(fill = "#a50f15") +
  labs(x = "Années", y = "Nombre", title = "Nombre de résultats", subtitle = "2014 à 2019") +
  theme_minimal()
Global

#--------Tri données---------
##--------2014_2015----
Select2014 <- Select2 %>%
 filter(date >= "2014-02-03" & date <= "2015-06-27")

Années14_15<-ggplot(Select2014) +
 aes(x = date) +
 geom_histogram(bins = 30L, fill = "#ef3b2c") +
 theme_minimal()
Années14_15

##---------2015-2016-------
Select2015 <- Select2 %>%
  filter(date >= "2015-06-27" & date <= "2016-12-10")

Années15_16<-ggplot(Select2015) +
  aes(x = date) +
  geom_histogram(bins = 30L, fill = "darkblue") +
  theme_minimal()
Années15_16

#-------Nombre de messages par année-------
Dates<-selection %>%
  dplyr::group_by(id, course_id, date, body, title, courseware_title, thread_type, username) %>%
  dplyr::summarise(Nombre = n())
Dates$date<-substr(Dates$date, 0, 4)


plot1<-ggplot2::ggplot(Dates)+ geom_col(aes(x= date, y=Nombre, fill=date)) + S_fillBG + ggplot2::labs(title ="Nombre de messages de 2014 à 2019", x = "Années", y="Nombre de messages")
plot1

#----Dataframes des plots

cours_questions<-selection %>%
  dplyr::group_by(course_id, thread_type) %>%
  dplyr::summarise(Nombre = n()) %>%
  filter(thread_type == 'question')
cours_questions$course_id <- factor(cours_questions$course_id, levels = cours_questions$course_id[order(cours_questions$Nombre)])

cours_discussions<-selection %>%
  dplyr::group_by(course_id, thread_type) %>%
  dplyr::summarise(Nombre = n()) %>%
  filter(thread_type == 'discussion')
cours_discussions$course_id <- factor(cours_discussions$course_id, levels = cours_discussions$course_id[order(cours_discussions$Nombre)])


#---------Plot du top 20 des questions----------

Questions<-ggplot2::ggplot(cours_questions[1:20,]) + geom_col(aes(x = course_id, y= Nombre, fill=Nombre))+scale_fill_gradient(low = "yellow", high = "orange")
Questions + coord_polar() + S_coulBG + labs(title = "Top 20 de questions par cours", x='Cours', y="Nombre d'occurences")

#---------Plot du top 20 des discussions----------

Discussions<-ggplot2::ggplot(cours_discussions[1:20,]) + geom_col(aes(x = course_id, y= Nombre, fill=Nombre))
Discussions + S_coulBG + labs(title = "Top 20 de discussions par cours", x='Cours', y="Nombre d'occurences") + coord_flip()+scale_fill_gradient(low = "#007F7F", high = "green")
