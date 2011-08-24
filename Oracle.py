#!/usr/bin/python
# -*- Coding: Utf-8 -*-

###########################################################################
# Oracle
# Desc: Irc Bot allowing users to store URLs in a database and search for
# these URLs via keywords or authors.
# Based on Maurice, by Whidou (http://whidou.free.fr/Maurice)
# Date: 26/07/2011
###########################################################################
#	 This file is part of Oracle.
#
# 	Oracle is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	Oracle is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
# 	along with Oracle.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

# -- Idées --
#   - Ajouter une gestion des exceptions.
#   - Ajuster la création de bdd aux systèmes non-UNIX
#   - Ajouter des options de recherche
#   - Gérer plusieurs URLs dans un même message

VERSION = "1.2.0"

import re, os, sys, socket, time, sqlite3, urllib



class Oracle:
    """Oracle : Oracle Recherche, Accepte et Consulte les Liens Etonnants"""

    def __init__(self, network, chan, name="Oracle", database=None):
        self.network = str(network)
        if ',' in str(chan):
            self.chan=str(chan).split(',')
        else:
            self.chan = [str(chan)]
        self.name = str(name)
        self.configure()
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stop()
        self.lasturl={}
        if not database:
            oraclePath = os.path.join(os.path.expanduser("~"), ".Oracle")
            if not os.path.exists(oraclePath):
                os.mkdir(oraclePath)
            database = os.path.join(oraclePath, "Oracle.sq3")
        if not os.path.exists(database):
            os.system("echo 'create table %s(id INTEGER PRIMARY KEY,\
chan_orig TEXT,\
auteur TEXT,\
link TEXT,\
keywords TEXT,\
date INTEGER);'|sqlite3 %s"%(self.name, database)) # Unix only
        self.conn = sqlite3.connect(str(database))
        self.conn.text_factory = str
        self.db = self.conn.cursor()

    def configure(self):
        """Links commands to methods"""
        self.orders = {"^PING":self.pong,                                       # ^ indique un début de ligne
                       "(?i)PRIVMSG .*? :!help$":self.help,                     # (?i) précise que la casse est ignorée
                       "(?i)PRIVMSG .*? :!version$":self.version,               # $ indique une fin de ligne
                       "(?i)PRIVMSG .*? :!quit$":self.bye,                      # Le nom d'un chan est composé de 1 à 49 caractères
                       "(?i)PRIVMSG .*? :!goto #[-_#a-z0-9]{1,49}$":self.goto,  # lettres, nombres, -, _, et #
                       "(?i)(https?|ftp)://[a-z0-9\\-.@:]+\\.[a-z]{2,3}([.,;:]*[a-z0-9\\-_?'/\\\\+!&%$#=~])*":self.url,
                           # "(https?|ftp)://" : http://, https:// ou ftp://
                           # "[a-z0-9\-.@:]+" : Domaine de x-ième niveau (google, www.perdu, hgpub.druil)
                           # "\.[a-z]{2,3}" : Domaine de premier niveau (.com, .fr, .org, etc...)
                           # "([.,;:]*[a-z0-9\\-_?'/\\\\+&%$#=~])*" Bordel de fin d'adresse
                           #                                        Ne peut se terminer par ., ,, ; ou :
                           #                                        Afin d'éviter de prendre la ponctuation
                           #                                        Du message dans l'URL
                       "(?i)PRIVMSG .*? :!delete( (https?|ftp)://[a-z0-9\\-.@:]+\\.[a-z]{2,3}([.,;:]*[a-z0-9\\-_?'/\\\\+&%$#=~])*)?":self.delete,
                       "(?i)PRIVMSG .*? :!\\+.*$":self.tagadd,
                           # "\+[a-z0-9]+" Un + suivi d'au moins 1 caractère alphnumérique
                           # " ?" Suivi d'un espace ou pas
                           # "+" Le tout répété au moins une fois
                           #    "+tag01", "+234 +tag2" et "+tag1+tag2" sont donc des expressions valides
                       "(?i)PRIVMSG .*? :!-.*$":self.tagdel,
                       "(?i)PRIVMSG .*? :!search .*$":self.search,
                       "(?i)PRIVMSG .*? :!last$":self.last,
                           # " [a-z0-9]+" Un espace suivi d'au moins un caractère alphanumérique
                           # "+" Répété au moins une fois
                       " :End of /MOTD command\\.":self.join,
                           # Il ne faut pas oublier que \\ dans un string python équivaut à \ dans la regex
                           # Un antislash littéral se note donc \\\\, ce qui est chiant
                           # Le problème aurait pu être contourné avec des strings unicode
                           # Mais bon, moi je trouve pas ça franchement gênant
                       "^ERROR :Closing Link: ":self.stop}

    def mainloop(self, freq=1):
        """Serve forever"""
        if not self.go:
            self.go = True
            self.irc.connect((self.network, 6667)) # Should we let the user choose the port instead ?
            self.sendToServ("NICK %s"%self.name)
            self.sendToServ("USER %s %s_2 %s_3 :%s"%((self.name, )*4))
            while self.go:
                data = re.split("\r|\n", self.irc.recv(4096))   # Réception des données
                for i in data:                                  # Pour chaque ligne reçue
                    for j in self.orders:                       # On passe en revue chaque regex
                        match =  re.search(j, i)                # Et on la recherche dans la ligne
                        if match:                               # Si l'une d'elles correspond
                            self.orders[j](i, match.span())     # On exécute la méthode associée
                time.sleep(freq)
            self.irc.shutdown(socket.SHUT_RDWR)
            self.db.close()
            self.conn.close()

    def sendTo(self, target, message):
        """Sends a message to the choosen target"""
        for i in re.split("\r|\n",str(message)):
            for j in range(1+len(i)/400):
                self.sendToServ("PRIVMSG %s :%s"%(target,i[400*j:400*(j+1)]))

    def sendToServ(self, line):
        """Sends a message to the server"""
        self.irc.send("%s\n"%str(line))

    def stop(self, *args):
        """Stops the main loop"""
        self.go = False
        
    def pong(self, msg, match):
        """Keeps the link alive"""
        self.sendToServ("PONG %s"%(msg.split()[1]))

    def join(self, msg, match):
        """Joins a new channel on startup"""
        for chan in self.chan:
            self.sendToServ("JOIN %s"%chan)

    def gettarget(self, msg):
        """Obtains sender's name from message"""
        to = msg[msg.find("PRIVMSG ")+8:msg.find(" :")]
        if(to.lower() == self.name.lower()):
            return msg[1:msg.find("!")]
        return to

    def goto(self, msg, match):
        """Joins another channel"""
        target = msg.split()[-1]
        if target.lower() not in map(str.lower, self.chan):
            self.chan.append(target)
            self.sendToServ("JOIN %s"%target)
            self.lasturl[target] = ""

    def bye(self, msg, match):
        """Quits current channel"""
        target = self.gettarget(msg)
        if target.lower() in map(str.lower, self.chan):
            self.sendToServ("PART %s :All your link are belong to us."%target)
            del self.lasturl[target]
            self.chan.remove(target)
            if len(self.chan) == 0:
                self.stop()

# Here are Oracle's core methods :

    def url(self, msg, match):
        """Detects and stores URLs"""
        chan = self.gettarget(msg)
        if (msg.find("PRIVMSG %s :!"%chan) == -1) and (chan.lower() in map(str.lower, self.chan)): # Ne réponds pas aux messages privés ni aux commandes comme !delete
            url = msg[match[0]:match[1]]
            # Ajout d'une méthode de vérification de la présence des liens dans la base.
            self.db.execute("SELECT link, keywords FROM %s WHERE link='%s'"%(self.name, # Nom du bot/de la table
                                                                             url))      # URL
            fetch = self.db.fetchall()
            if fetch == []:
                self.db.execute("INSERT INTO %s VALUES (NULL,'%s','%s', '%s', '', %i);"%(self.name,                 # Nom du bot/de la table
                                                                                         chan,                      # Chan
                                                                                         msg[1:msg.find("!")],      # Pseudo du posteur
                                                                                         url,                       # URL
                                                                                         int(time.time())))         # Timestamp
                self.conn.commit()
            else:
                #Ligne envoyée au chan si le lien est déjà présent.
                self.sendTo(chan,fetch[0][1].replace(",", ", ")[:-2])
            self.lasturl[chan] = url # Stockage de l'url dans la "case" correspondant au chan
            self.tagadd("PRIVMSG %s :%s"%(chan, msg[match[1]:]), (0, 0))

    def tagadd(self, msg, match):
        """Adds tag(s) to last URL"""
        chan = self.gettarget(msg)
        if self.lasturl.has_key(chan):
            newtags = re.findall("[a-zA-Z0-9_\\-À-ž]{3,30}", msg[msg.find(" :"):])
            if len(newtags):
                self.db.execute("SELECT keywords FROM %s WHERE link='%s'"%(self.name,
                                                                           self.lasturl[chan]))
                fetch = self.db.fetchall()
                if len(fetch):
                    tags = []
                    for tag in fetch[0][0].split(",") + newtags:
                        if tag.lower() not in map(str.lower, tags) and tag != "":
                            tags.append(tag)
                    self.db.execute("UPDATE %s SET keywords='%s,' WHERE link='%s'"%(self.name,
                                                                                   ','.join(tags),
                                                                                   self.lasturl[chan]))
                else:
                    self.db.execute("INSERT INTO %s VALUES (NULL,'%s','%s', '%s', '%s,', %i);"%(self.name,               # Nom du bot/de la table
                                                                                                chan,                    # Chan
                                                                                                msg[1:msg.find("!")],    # Pseudo du posteur
                                                                                                self.lasturl[chan],      # URL
                                                                                                ','.join(newtags),       # Tags
                                                                                                int(time.time())))       # Timestamp
                self.conn.commit()

    def tagdel(self, msg, match):
        """Deletes tag(s) from last URL"""
        chan = self.gettarget(msg)
        if self.lasturl.has_key(chan):
            self.db.execute("SELECT keywords FROM %s WHERE link='%s'"%(self.name,
                                                                       self.lasturl[chan]))
            tags = self.db.fetchall()[0][0].split(",")
            for deleted in re.findall("[a-zA-Z0-9_\\-À-ž]{1,30}", msg[msg.find(" :"):]):
                for tag in tags[::-1]:
                    if tag.lower() == deleted.lower() or tag == "":
                        tags.remove(tag)
            self.db.execute("UPDATE %s SET keywords='%s,' WHERE link='%s'"%(self.name,
                                                                           ','.join(tags),
                                                                           self.lasturl[chan]))
            self.conn.commit()

    def search(self, msg, match):
        """Searches for an URL with the given tags"""
        chan = self.gettarget(msg)
        search = re.findall("[a-zA-Z0-9_\\-À-ž]{3,30}",
                            msg[msg.find(" :!search")+9:])
        if len(search):
            self.db.execute("SELECT link, keywords FROM '%s' WHERE keywords LIKE '%%%s%%'"%(self.name,
                                                                                            "%%' AND keywords LIKE '%%".join(search)))
            fetch = self.db.fetchall()
            if len(fetch):
                for result in fetch:
                    self.sendTo(chan, "%s (%s)"%(result[0],
                                                                result[1][:-1].replace(",", ", ")))
                url = result[0]
            else:
                query = urllib.urlencode({'q' : msg[msg.find("!search ")+8:]})
                url = 'http://ajax.googleapis.com/ajax/services/search/images?v=1.0&%s'% (query)
                search_results = urllib.urlopen(url)
                url = search_results.read()
                search_results.close()
                url = url[url.find("\"url\":\"")+7:]
                url = url[:url.find("\",\"")]
                self.sendTo(chan, "%s"%url)
            self.lasturl[chan] = url

    def last(self, msg, match):
        """Searches for an URL with the given tags"""
        chan = self.gettarget(msg)
        url = self.lasturl[chan]
        if url != "":
            self.db.execute("SELECT keywords FROM '%s' WHERE link='%s'"%(self.name,
                                                                         url))
            fetch = self.db.fetchall()
            if len(fetch):
                keywords = " (" + fetch[0][0][:-1].replace(",", ", ") + ")"
            self.sendTo(chan, "%s%s"%(url, keywords))

    def delete(self, msg, match):
        """Deletes a previously added url"""
        # Deux formes: "!delete" et "!delete [URL]"
        chan = self.gettarget(msg)
        if msg[-9:] == " :!delete" and self.lasturl.has_key(chan):
            if self.lasturl[chan]!="":
                url = self.lasturl[chan]
                self.lasturl[chan]="" # Correction du ticket #2
        else:                           # Si une URL est fournie
            url = msg[msg.find("!delete ")+8:]
        self.db.execute("DELETE FROM %s WHERE link='%s'"%(self.name,
                                                          url))
        self.conn.commit()

    def help(self, msg, match):
        """Displays a minimal manual"""
        self.sendTo(self.gettarget(msg),"""!help : Displays this message.
!version : Displays Oracle's version.
!delete url : Deletes URL.
!+ tag1 tag2 : Adds tags to the last link.
!- tag1 tag2 : Removes tags from the last link.
!search tag1 tag2 : Searches links linked to tag1 AND tag2.
!last : Displays last link.
!goto #foo : Goes to #foo.
!quit : Leaves current channel.""")
        
    def version(self, msg, match):
        """Displays version data"""
        self.sendTo(self.gettarget(msg),"""Oracle : Oracle Recherche, Accepte et Consulte les Liens Etonnants
v%s
Website : http://trac.druil.net/Oracle/
Interface HTTP : http://oracle.druil.net/"""%VERSION)



if __name__ == "__main__":
    database = None
    if len(sys.argv) == 5:      # It's up to the user to choose the default
        database = sys.argv[4]  # database in ~/.Oracle or another one.
    Oracle(sys.argv[1],             # Serveur
           sys.argv[2],             # Chan (ne pas oublier \ avant #)
           sys.argv[3],             # Nom du bot
           database).mainloop()     # Base de données optionelle

# Usage: oracle SERVER CHANNEL BOTNAME [DATABASE]
# If no database is specified, ~/.Oracle/Oracle.sq3 will be used
