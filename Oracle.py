#!/usr/bin/python
# -*- Coding: Utf-8 -*-

###########################################################################
# Oracle
# Desc: Irc Bot allowing users to store URLs in a database and search for these URLs via keywords or authors. Based on a code by Whidou on irc.netrusk.net.
# Date: 26/07/2011
###########################################################################



#idées
# lorsque un lien est posté, le bot stock et demande en query des mots cle
# 

import random, re, sys, socket, time, sqlite3



class IrcBot:

    def __init__(self, network, chan, name="Oracle"):
        self.network = network
        self.chan = [chan]
        self.name = name
        self.configure()
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stop()
        self.bits = {}
        self.conn = sqlite3.connect(name+".sq3")

    def configure(self):
        self.orders = {"^PING":self.pong,
                       "(?i) :!help$":self.help,
                       "(?i) :!version$":self.version,
                       "(?i) :!goto #[-_#a-zA-Z0-9]{1,49}$":self.goto,
                       " :End of /MOTD command\\.":self.join,
                       "^ERROR :Closing Link: ":self.stop}

    def mainloop(self, freq=1):
        """Serve forever"""
        if(not self.go):
            self.go = True
            self.irc.connect((self.network, 6667))
            self.sendToServ("NICK %s"%self.name)
            self.sendToServ("USER %s %s_2 %s_3 :%s"%((self.name, )*4))
            while(self.go):
                data = re.split("\r|\n", self.irc.recv(4096))
                for i in data:
                    print i
                    for j in self.orders:
                        match =  re.search(j, i)
                        if(match):
                            self.orders[j](i, match.span())
                time.sleep(freq)
                self.irc.shutdown(socket.SHUT_RDWR)

    def sendTo(self, target, message):
        """Sends a message to the choosen target"""
        for i in re.split("\r|\n",str(message)):
            for j in range(1+len(i)/400):
                self.sendToServ("PRIVMSG %s :%s"%(target,i[400*j:400*(j+1)]))

    def sendToServ(self, line):
        """Sends a message to the server"""
        self.irc.send("%s\n"%str(line))

    def stop(self, *args):
        """Stop """
        self.go = False

    # Tech Stuff:
        
    def pong(self, msg, match):
        self.sendToServ("PONG %s"%(msg.split()[1]))

    def join(self, msg, match):
        self.sendToServ("JOIN %s"%self.chan[0])

    def gettarget(self, msg):
        to = msg[msg.find("PRIVMSG ")+8:msg.find(" :")]
        if(to.lower() == self.name.lower()):
            return msg[1:msg.find("!")]
        return to     


    def goto(self, msg, match):
        target = msg.split()[-1]
        if(target.lower() not in map(lambda x:x.lower(), self.chan)):
            self.chan.append(target)
            self.sendToServ("JOIN %s"%target)

    def bye(self, msg, match):
        target = self.gettarget(msg)
        if(target.lower() in map(lambda x:x.lower(), self.chan)):
            self.sendToServ("PART %s :ICI UN MESSAGE DE QUIT"%target)
            self.chan.remove(target)
            if len(self.chan) == 0:
                self.stop()

    def help(self, msg, match):
	    self.sendTo(self.gettarget(msg),"""A venir""")
        
    def version(self, msg, match):
	    self.sendTo(self.gettarget(msg),"""A venir""")

# Main :

if __name__ == "__main__":
    IrcBot(sys.argv[1], sys.argv[2], sys.argv[3]).mainloop()
