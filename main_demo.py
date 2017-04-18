# -*- coding: UTF-8 -*-

from SessionStatClass import SessionStatClass
from BaseInfoClass import BaseInfoClass
from NetStatClass import NetStatclass
from transportElasticsearch import SessionStat_badcsq,BaseInfo_iplocation,NetStat_reconbody
from pykafka import KafkaClient
import json
import sys
import time
import os

def ceshi(source):
    if isinstance(source,dict):
        if 'BaseInfo' in source['_type']:
            sourcet = BaseInfoClass(source)
            if sourcet.usr_ipcheck() is not None:
                BaseInfo_iplocation(sourcet.uid, sourcet.ipaddr, sourcet.usr_ipcheck())
                print 'id为{uid}的用户BaseInfo中的ip地址所在城市为{city}，已经写入es'.format(uid=sourcet.uid, city=sourcet.usr_ipcheck())
            else:
                print 'id为{uid}的用户BaseInfo中的ip地址查询城市失败，不将内容写入es'.format(uid=sourcet.uid)

        if 'SessionStat' in source['_type']:
            sourcet = SessionStatClass(source)
            if sourcet.signal_status() == 'normal csq':
                print 'id为{uid}的csq数值正常，不将日志写入es'.format(uid=sourcet.uid)
            elif sourcet.signal_status() == 'bad csq':
                SessionStat_badcsq(sourcet.uid, sourcet.csq)

        if 'NetStat' in source['_type']:
            sourcet = NetStatclass(source)
            targ = json.loads(sourcet.fabricate_es_body())
            NetStat_reconbody(targ)
    else:
        print 'cant define the input type'




print '开始时间', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
print sys.getdefaultencoding()



client = KafkaClient(hosts='192.168.5.8:9092')
topic = client.topics['wr_test1']
consumer = topic.get_balanced_consumer(consumer_group='test-consumer-group', auto_commit_enable=True,zookeeper_connect='192.168.5.8:2121')

a_error_count = 0
a_success_count = 0
path_os = os.path.abspath('offset.txt')
f1 = open(path_os, 'r')
a_offset_start = int(f1.readline())
print(a_offset_start)
f1.close()

data_group = []

for message in consumer:
    if message is not None and message.offset > a_offset_start:
        try:
            a = json.loads(message.value)
            #c = message.offset
            data_group.append(a)
            for item in data_group:
                ceshi(item)
                a_success_count += 1
            data_group.pop()
        except:
            print('error_message')
            a_error_count += 1
            continue
    c1 = message.offset

f = open(path_os, 'w+')
f.truncate()
f.write(str(c1))
f.write('\n' + '开始时间=' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
f.write('\n' + 'a_success_count=' + str(a_success_count))
f.write('\n' + 'a_error_count=' + str(a_error_count))
f.close()