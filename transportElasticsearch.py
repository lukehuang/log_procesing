# -*- coding: UTF-8 -*-
#将处理之后的数据存入elasitsearch

from elasticsearch import Elasticsearch
from datetime import datetime
from config import esurl
#from config import  ... 从配置文件py中取得python连接elasticsearch的连接信息


#es写入基础函数01
def normal_write(index_name,doc_type,id,body):
    es = Elasticsearch(esurl)
    es.index(index=index_name,doc_type=doc_type,id=id,body=body)

def SessionStat_badcsq( uid, csq):
    es = Elasticsearch(esurl)
    res = es.index(index='my-index',doc_type='ss_badcsq',body={"uid":uid,"timestamp":datetime.now(),"description":"bad csq,csq = {csq}".format(csq=csq)})
# 使用elastic search的api进行es的index插入之后，会获得一个json数据块，然后通过这个块来进行判断
    if res['created'] is True:
        print '用户{uid}的SessionStat 信号恶劣 日志存储成功'.format(uid=uid)
    else:
        print '用户{uid}的SessionStat 信号恶劣 日志存储失败，已将elasticsearch api返回的错误内容写入[日志]'.format(uid=uid)
        _reasonJudge(res)

def BaseInfo_iplocation( uid, ip, location):
    es = Elasticsearch(esurl)
    res = es.index(index='my-index',doc_type='bi_iplocation',body={"uid":uid,"timestamp":datetime.now(),"description":"{ip}locate in {location}".format(ip=ip,location=location)})

def NetStat_reconbody( body):
    es = Elasticsearch(esurl)
    res = es.index(index='my-index', doc_type='ns_recon_demo', body=body)

#def NetStat_demo1():


#如果写入失败，则将elasticsearch返回的json数据块进行分析，比如分析返回的shards信息，是否有失败，总量是否正常 u'create' u'result'的结果如何
def _reasonJudge(res):
    pass