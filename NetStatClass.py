# -*- coding: UTF-8 -*-
from data_source import ns1
from datetime import timedelta
from config import discon_reason1, discon_reason2, discon_reason3, discon_reason4, discon_reason5

from transportElasticsearch import NetStat_reconbody

#从外部引入原始日志中disCon中reason数值对应的解释
discon_reason = {1: discon_reason1, 2: discon_reason2, 3: discon_reason3, 4: discon_reason4, 5: discon_reason5}

#使用dataFilter中的函数确定输入的数据为Stat之后，生成对应类，再根据需求调用特定的类方法
#进入
class NetStatclass(object):

    def __init__(self,source):
        self.data = source
        try:
            #获取数据块中的用户信息
            self.uid = source['_source']['content']['uid']
            #获取数据块中的断网信息
            self.discon_data = source['_source']['content']['disCon']
            self.discon_rea_type = self.discon_data['reason']
            self.discon_time = self.discon_data['time']
            #获取数据块中的重连步骤数
            self.recon_data = source['_source']['content']['reCon']
            self.recon_info_num = len(source['_source']['content']['reCon'])
        except Exception,e:
            print Exception,':',e

#！！！构造写入elasticsearch NetStat类型原始数据处理后的 的json格式文本内容！！！
#构造完的内容将会被传入transportElasticsearch模块的写入方法中
    def fabricate_es_body(self):
        last_endtime = self.recon_data[self.recon_info_num - 1]['time'][11:]
        discon_time = self.discon_time[11:]
        last_time = (self.strptimedelta(last_endtime) - self.strptimedelta(discon_time))
        last_time_sec = last_time.seconds
        last_time_microsec = last_time.microseconds
        last_time_descrip = '{sec}secs{microsec}microsecs'.format(sec = last_time_sec, microsec = last_time_microsec)

        step_decri_col = []
        for i in range(self.recon_info_num):
            step = self.recon_data[i]['step']
            try_times = str((self.recon_data[i]['retry']) + 1)
            net_stat = 'model:' + self.recon_data[i]['net']['model'] + ',csq:' + str(self.recon_data[i]['net']['csq'])
            descrip = 'STEP:' + step + ',TRIED:' + try_times + 'times,NET_STAT:' + net_stat
            step_decri_col.append(descrip)

        #part1 基本信息，用户id，断开原因（对数字字段进行解释），基准时间，断开时间
        body_part1 = '{' + '"uid":{uid},"disConnect-reason":"'.format(uid = self.uid) + discon_reason[self.discon_rea_type] + '", "criterion-time":"{criterion_time}"'.format(
        criterion_time = self.discon_time[0:10]) + ', "disConnect-time":"{discon_time}"'.format(discon_time = discon_time)
        #part2 重连信息，最后一次连接时间，从断开到最后一次连接（连接成功）所消耗的时间
        body_part2 = '"last-try-endtime":"{last_endtime}","total-last-time":"{total_last_time}"'.format(last_endtime = last_endtime, total_last_time= last_time_descrip)
        #part3 重连尝试信息，把有用的内容过滤之后整合添加到新的数据中
        body_part3 = str(step_decri_col).replace(' ','_')
        combi = '{"basic-info":'+body_part1 + '},"reconnect-info":{' + body_part2 +'},"reconnect-step-info":"'+ body_part3 + '"}'


        print combi
        #print last_endtime, type(last_endtime)


    def get_recon_fulltime(self):
        try:
            #计算断开连接与重连成功时间的timedelta对象
            disct = self.strptimedelta(self.discon_time)
            recont = self.strptimedelta(self.discon_data[self.recon_info_num - 1]['time'])
        except:
            pass


    @staticmethod
    def strptimedelta(input_str):
        tm = map(int,input_str.replace(' ',':').split(':'))
        tm1 = timedelta(hours=tm[0],minutes=tm[1],seconds=tm[2],microseconds=tm[3])
        return tm1


#类定义输出模块
    def output1(self):
        try:
            print self.recon_info_num
            print self.uid
        except Exception,e:
            print Exception,":",e



#ns1c = NetStatclass(ns1)
#ns1c.fabricate_es_body()
#NetStat_reconbody(ns1c.fabricate_es_body())
#ns1c.output1()
