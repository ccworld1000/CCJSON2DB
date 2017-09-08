# -*- coding:utf-8 -*-
#!/usr/bin/python
#
#  Created by CC on 2017/09/07.
#  Copyright © 2017 - now  CC | ccworld1000@gmail.com . All rights reserved.
#  https://github.com/ccworld1000/CCJSON2DB

# Licensed under the BSD 3-Clause License (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of
# the License at
#
#       https://opensource.org/licenses/BSD-3-Clause
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
                prueCode = re.sub (r'(.hk)', '', dataType, flags = re.I)
                print "[CC HK] prueCode : " + pureCode 
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


