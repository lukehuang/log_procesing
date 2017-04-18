# -*- coding: UTF-8 -*-

import urllib2
import json
#从config模块中读取BaseInfoClass 类方法模块需要的相关参数
from config import *

#使用dataFilter中的函数确定输入的数据为之后，生成对应类，再根据需求调用特定的类方法
#默认输入的数据已经是 dict 类型的 BaseInfo 数据块
class BaseInfoClass(object):

#数据读取必须含有，否则会报错，所以要先检查数据合法性
    def __init__(self,source):
#读取数据块中用户的基本信息
        self.data = source
        self.uid = source['_source']['content']['user']['uid']
        self.name = source['_source']['content']['user']['name']
#读取数据块中服务节点信息
        self.ipaddr = source['_source']['content']['server']['addr']
        self.dnscont = source['_source']['content']['server']['context']
#读取数据块中用户终端信息
        self.pocV = source['_source']['content']['terminal']['pocVersion'] #应用版本
        self.iccid = source['_source']['content']['terminal']['iccid'] #sim卡iccid信息
        self.type = source['_source']['content']['terminal']['type'] #终端类型 MC8332/GD83/BREW/ANDROID
        self.gpioType = source['_source']['content']['terminal']['gpioType'] #终端硬件标识 MCU/GPIO
        self.hardwareSN = source['_source']['content']['terminal']['hardwareSN'] #终端硬件序号
        #self.platformVersion = source['_source']['content']['terminal']['platformVersion'] #终端平台版本

        self.uploadT = source['_source']['time']

    def usr_netinfo(self):#测试数据读取基础函数
        print 'id为{uid}的用户所处的服务节点ip地址为{ipaddr},节点dns标识信息为{dnscont}'.format(uid=self.uid,ipaddr=self.ipaddr,dnscont=self.dnscont)
        #print self.platformVersion
        print self.uploadT, type(self.uploadT)


    def usr_ipcheck(self):#根据返回的客户ip数据查询客户所在服务节点的ip地址等信息
        #ip地址合法性判断
        return self.ipaddr_API(self.ipaddr)

    def usr_iccidcheck(self):#
        pass

#此静态方法是使用geoip等开源ip信息查询api查询BaseInfo中客户服务节点ip的信息，可根据需求进行修改
    @staticmethod
    def ipaddr_API(ipaddr):
        get_url = 'http://freegeoip.net/json/{ipaddr}'.format(ipaddr = ipaddr)
        raw_data = urllib2.urlopen(get_url)
        json_data = json.loads(raw_data.read())
        print 'ip{ipaddr} located in {posi}'.format(ipaddr=ipaddr,posi=json_data['city'])

#使用iccid开发者接口，由数据块中的iccid数值
    @staticmethod
    def iccid_API(iccid):
        pass



