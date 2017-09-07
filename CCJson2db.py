# -*- coding:utf-8 -*-  
#!/usr/bin/python
#
#  Created by CC on 2017/09/07.
#  Copyright © 2017 - now  CC | ccworld1000@gmail.com . All rights reserved.
#  https://github.com/ccworld1000/CCJSON2DB

import re
import json
import sqlite3

def json2db (jFile, dbFile, createSQL, dropSQL, insertSQL) :
    dicset = json.load(open(jFile))
    conn = sqlite3.connect (dbFile)

    print conn;

    c = conn.cursor()

    c.execute(dropSQL)
    c.execute(createSQL)

    print "create data table success"
    conn.commit()

    #print dicset

    index = 0;
    usMarkType = "222222";
    hkMarkType = "111111";
    markType = ""
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
                prueCode = re.sub (r'(.hk)', '', dataType)
                print "CC prueCode : " + prueCode
            elif (ret_match2) :
                markType = usMarkType
                pureCode = code;
            
            data = [code, cnName, dataType, enName, cnSpell, cnSpellAbbr, ftName, prueCode, markType]
            c.execute (insertSQL, data)

            conn.commit()
            print str(index) + " :: " + code + " " + cnName
            index += 1


    c.close()


