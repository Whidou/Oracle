#!/usr/bin/python
# -*- Coding: Utf-8 -*-

###########################################################################
# Oracle
# Desc: Irc Bot allowing users to store URLs in a database and search for
# these URLs via keywords or authors.
# Based on Maurice, by Whidou (http://whidou.free.fr/Maurice)
# Date: 26/07/2011
###########################################################################


# -- Idées --
#   - lorsque un lien est posté, le bot stock et demande en query des mots cle
#   - Ajouter une gestion des exceptions.


VERSION = "0.1.3"

import re, os, sys, socket, time, sqlite3



class Oracle:
    """Oracle : """ # Please add the expanded acronym here

    def __init__(self, network, chan, name="Oracle", database=None):
        self.network = str(network)
        self.chan = [str(chan)]
        self.name = str(name)
        self.configure()
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stop()
        self.lasturl={} #id de la derniere url postée sur un chan pour chaque self.chan[]
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
        self.db = self.conn.cursor()

    def configure(self):
        """Links commands to methods"""
        self.orders = {"^PING":self.pong,
                       "(?i) :!help$":self.help,
                       "(?i) :!version$":self.version,
                       "(?i) :!quit$":self.bye,
                       "(?i) :!goto #[-_#a-zA-Z0-9]{1,49}$":self.goto,
                       "(?i)(https?|ftp)://[a-z0-9\\-.@:]+\\.[a-z]{2,3}([.,;:]*[a-z0-9\\-_?'/\\\\+&%$#=~])*":self.url,
                       "(?i) :(\+[a-z0-9]+ ?)+$":self.tag,
                       "(?i) :!search( [a-z0-9]+)+$":self.search,
                       " :End of /MOTD command\\.":self.join,
                       "^ERROR :Closing Link: ":self.stop}

    def mainloop(self, freq=1):
        """Serve forever"""
        if not self.go:
            self.go = True
            self.irc.connect((self.network, 6667)) # Should we let the user choose the port instead ?
            self.sendToServ("NICK %s"%self.name)
            self.sendToServ("USER %s %s_2 %s_3 :%s"%((self.name, )*4))
            while self.go:
                data = re.split("\r|\n", self.irc.recv(4096))
                for i in data:
                    for j in self.orders:
                        match =  re.search(j, i)
                        if match:
                            self.orders[j](i, match.span())
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
        self.sendToServ("JOIN %s"%self.chan[0])

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

    def bye(self, msg, match):
        """Quits current channel"""
        target = self.gettarget(msg)
        if target.lower() in map(str.lower, self.chan):
            self.sendToServ("PART %s :All your link are belong to us."%target)
            self.chan.remove(target)
            if len(self.chan) == 0:
                self.stop()

# Here are Oracle's core methods :

    def url(self, msg, match):
        """Detects and stores URLs"""
        chan = self.gettarget(msg)
        if chan.lower() in map(str.lower, self.chan): # Ne réponds pas aux messages privés
            url = msg[match[0]:match[1]]
            # Ajout d'une méthode de vérification de la présence des liens dans la base.
            self.db.execute("SELECT * FROM %s WHERE link='%s'"%(self.name,  # Nom du bot/de la table
                                                                url))       # URL
            if self.db.fetchall() == []:
                self.db.execute("INSERT INTO %s VALUES (NULL,'%s','%s', '%s', '', %i);"%(self.name,                 # Nom du bot/de la table
                                                                                         chan,                      # Chan
                                                                                         msg[1:msg.find("!")],      # Pseudo du posteur
                                                                                         url,                       # URL
                                                                                         int(time.time())))         # Timestamp
                self.conn.commit()
            else:
                #Ligne envoyée au chan si le lien est déjà présent.
                self.sendTo(chan,"'%s' est déjà présente avec '%s' comme mots-clefs"%(url,                          # URL
                                                                                      self.db.fetchall()[0][4]))    # Tags

            self.lasturl[chan]=self.db.fetchall()[0][0] #stock l'id de l'url dans la "case" correspondant au chan

    def tag(self, msg, match):
        """Adds tag(s) to last URL"""
        pass

    def search(self, msg, match):
        """Searches for an URL with the given tags"""
        pass

    def help(self, msg, match):
        """Displays a minimal manual"""
        self.sendTo(self.gettarget(msg),"""!help : Displays this message.
!version : Displays Oracle's version.
!goto #foo : Goes to #foo.
!quit : Leaves current channel.""")
        
    def version(self, msg, match):
        """Displays version data"""
        self.sendTo(self.gettarget(msg),"""Oracle
v%s
Semi-functional beta version.
http://hgpub.druil.net/Oracle/"""%VERSION)



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
