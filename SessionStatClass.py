# -*- coding: UTF-8 -*-


from data_source import *
#使用dataFilter中的函数确定输入的数据为SessionStat之后，生成对应类，再根据需求调用特定的类方法
class SessionStatClass(object):

    def __init__(self,source):
        self.data = source
        self.uid = source['_source']['content']['uid']
        self.model = source['_source']['content']['net']['model']
        self.csq = source['_source']['content']['net']['csq']
        self.content_dict = source['_source']['content']

    def output1(self):
        print self.uid

    def signal_status(self):
        if self.model == 'G2':
            if self.csq in range (16,32):
                return 'normal csq'
            else:
                return 'bad csq'
        elif self.model == 'G3':
            return '3g model'

# 在SessionStat中一般会监听到大于一个会话内容，每个会话内容将人性化为一句话，那么多个会话需要创建描述列表
    def listen_status(self):
        humanized_description = []
        listen_num = len(self.data['_source']['content']['listen'])
        for i in range(listen_num):
            curr_dict = self.data['_source']['content']['listen'][i]
            FirstPT = self.timestr(curr_dict['recvFirstPacketTime'])
            ReleaseMT = self.timestr(curr_dict['memReleaseMicTime'])
            GetMT = self.timestr(curr_dict['memGetMicTime'])

            SessionLastTime = self.lasttime()

            description = '由id{memId}于{RMT}发起的持续{lastTime}的会话'.format(memId=curr_dict['memId'],RMT=curr_dict['memReleaseMicTime'][:-4],lastTime=SessionLastTime)
            humanized_description.append(description)

        return humanized_description

    def geolocation(self):
        if self.content_dict.has_key('coordinate'):
            print '日志数据含有地理位置信息'
            #然后读取地理位置数据，再依靠api接口返回用户的位置信息
            #usr_lati = self.content_dict['coordinate']['latitude']
            #usr_longti = self.content_dict['coordinate']['longtitude']
            #print usr_lati,usr_longti
        else:
            print '日志数据不含有地理位置信息'
            #print 'not exist'
            #print '地理信息存在'


#以下是针对SessionStat日志中 监听通话（listen）中时间内容的简易处理
#比如memGetMicTime、memReleaseMicTime的格式均为"2017-03-09 08:22:09 976"

    @staticmethod
    def timestr(strform):
        import time
        targstr = strform[0:-4]
        timestrc = time.strptime(targstr, '%Y-%m-%d %H:%M:%S')
        return timestrc
#这样文档中的时间内容就被处理成time.struct_time的类对象

#当使用上面的方法转化了日志中的时间信息之后，进行计算监听（listen）到对话的持续时间(以秒为单位）
# 因为对讲的时间一般来说不会太久，所以上面仅仅判断2个时间分钟数值是否相同，相同的话仅做秒数的相减

    @staticmethod
    def lasttime(end_time,starttime):
        import time
        if end_time.tm_min == starttime.tm_min:
            lasttime = end_time.tm_sec - starttime.tm_sec
        elif end_time.tm_min != starttime.tm_min:
            pass
        return lasttime

