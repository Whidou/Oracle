#!/usr/bin/python
# -*- Coding: Utf-8 -*-

###########################################################################
# Dodone : Dodone Ordonne les Données d'Oracle Naturellement Eparpillées
# Desc: Mets à jour deux bdd l'une par rapport à l'autre
# Date: 26/07/2011
###########################################################################
# 	This file is part of Oracle.
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

VERSION = "1.0.0"

import os, sys, sqlite3

# Usage: dodone DB1 [DB2] [TABLE_1] [TABLE_2]
# If no DB2 is specified, ~/.Oracle/Oracle.sq3 will be used
# If no TABLE_1 is specified, Oracle will be used
# If no TABLE_2 is specified, TABLE_1 will be used

# Vérification des chemins
if len(sys.argv) > 2:
    db2 = sys.argv[2]
else:
    db2 = os.path.join(os.path.expanduser("~"), ".Oracle", "Oracle.sq3")
dbPath = (sys.argv[1], db2)
if not (os.path.exists(dbPath[0]) and os.path.exists(dbPath[1])):
    sys.stderr.write("ERROR : Invalid path to database.\n")
    sys.exit(1)

# Ouverture des bases
conn = (sqlite3.connect(dbPath[0]), sqlite3.connect(dbPath[1]))
conn[0].text_factory = conn[1].text_factory = str
db = (conn[0].cursor(), conn[1].cursor())

# Requête sur la première base
if len(sys.argv) > 3:
    table1 = sys.argv[3]
else:
    table1 = "Oracle"
if len(sys.argv) > 4:
    table2 = sys.argv[4]
else:
    table2 = table1
try:
    db[0].execute("SELECT * FROM '%s'"%table1)
except sqlite3.OperationalError:
    sys.stderr.write("ERROR : No such table: %s\n"%table1)
    sys.exit(2)
except sqlite3.DatabaseError:
    sys.stderr.write("ERROR : Not an SQLite3 database: %s\n"%dbPath[0])
    sys.exit(3)

# Update de la seconde base
for result in db[0].fetchall():
    link = result[3]
    keys = result[4]
    try:
        db[1].execute("SELECT keywords FROM '%s' WHERE link='%s'"%(table2,
                                                                   link))
    except sqlite3.OperationalError:
        sys.stderr.write("ERROR : No such table: %s\n"%table2)
        sys.exit(4)
    except sqlite3.DatabaseError:
        sys.stderr.write("ERROR : Not an SQLite3 database: %s\n"%dbPath[1])
        sys.exit(5)
    old_result = db[1].fetchall()
    if len(old_result):
        keywords = []
        for key in (keys + old_result[0][0]).split(","):
            if key not in keywords and key != "":
                keywords.append(key)
        db[1].execute("UPDATE '%s' SET keywords='%s,' WHERE link='%s'"%(table2,
                                                                       ",".join(keywords),
                                                                       link))
    else:
        chan = result[1]
        author = result[2]
        date = result[5]
        db[1].execute("INSERT INTO '%s' VALUES(NULL,'%s','%s', '%s', '%s', %i);"%(table2,
                                                                                  chan,
                                                                                  author,
                                                                                  link,
                                                                                  keys.replace(",,", ","),
                                                                                  date))
conn[1].commit()

# Clôture des bases
db[1].close()
db[0].close()
conn[1].close()
conn[0].close()
