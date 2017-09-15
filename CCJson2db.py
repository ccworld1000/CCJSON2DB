# -*- coding:utf-8 -*-
#!/usr/bin/python
#
#  CCJson2db.py
#
#  Created by CC on 2017/09/07.
#  Copyright © 2017 - now  CC | ccworld1000@gmail.com . All rights reserved.
#  https://github.com/ccworld1000/CCJSON2DB

#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import re
import json
import sqlite3

def json2db (jFile, dbFile, createSQL, dropSQL, insertSQL) :
    dicset = json.load(open(jFile))
    conn = sqlite3.connect (dbFile)

    c = conn.cursor()
    c.execute ("SELECT tbl_name  FROM sqlite_master where type = 'table' and tbl_name = 'CCSQLite.Database2'")
    table = c.fetchone()

    if (table) :
    	if table[0] == 'CCSQLite.Database2' :
		print ("execute json2db")
	else :
		print ("ill CCSQLite")
		return 	-1
    else :
	print ("NO Table, Please check database is right!");
	return 	-1

    c.execute(dropSQL)
    c.execute(createSQL)

    print "create data table success"
    conn.commit()

    index = 0;
    usMarkType = "222222";
    hkMarkType = "111111";
    markType = ""
    pureCode = "" 
    for dic in dicset :
            code = dic["code"]
            cnName = dic["cnName"]
            dataType = dic["dataType"]
            enName = dic["enName"]
            cnSpell = dic["cnSpell"]
            cnSpellAbbr = dic["cnSpellAbbr"]
            ftName = dic["ftName"]
            pureCode = code;
            
            ret_match1 = re.match("1", dataType)
            ret_match2 = re.match("2", dataType)
            
            if (ret_match1) :
                markType = hkMarkType
		tmp = code
                pureCode = re.sub (r'.hk', '', pureCode, flags = re.I)
                print "[CC HK] pureCode : " + pureCode 
            elif (ret_match2) :
                markType = usMarkType
                pureCode = code;
                print "[CC US] pureCode : " + pureCode
            
            data = [code, cnName, dataType, enName, cnSpell, cnSpellAbbr, ftName, pureCode, markType]
            c.execute (insertSQL, data)

            conn.commit()
            print str(index) + " :: " + code + " " + cnName
            index += 1

    c.close()


