#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from pymongo import MongoClient
import subprocess

ip='localhost'
port=27017
client=MongoClient(ip,port)
db=client.poker

dbnameTemplete='card%d_player%d_with_%s_range'

def generateDB(toDealNum=5,playerNum=2,rangee='169',prefix='',postfix=''):
    name=dbnameTemplete%(toDealNum,playerNum,rangee)
    if len(prefix)>0:
        name=prefix+'_'+name
    if len(postfix)>0:
        name=name+'_'+postfix
    return db[name]

def getSortedData(db,key='winRate',des=-1):
    res=db.find({}).sort([(key,des)])
    return res

c5p2r169db=db['card5_player2_with_169_range']

try:
    c5p2r169db.count()
except:
    dockerCmd='docker run -p 27017:27017 -d mongo mongo'
    subprocess.call(dockerCmd, shell=True)