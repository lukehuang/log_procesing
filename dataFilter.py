# -*- coding: UTF-8 -*-
from data_source import *
import json

#这里假设已经读取到单条且为dict类型的数据,先忽略数据合法性审查
def data_type_check(input_data):
    input_data_type = 0
    if isinstance(input_data,dict):
        if 'Base' in input_data['_type']:
            input_data_type = 1
        elif 'Net' in input_data['_type']:
            input_data_type = 2
        elif 'Session' in input_data['_type']:
            input_data_type = 3
        else:
            raise StandardError,'无法判断输入数据的类型'
    else:
        raise TypeError,'输入数据不是字典类型'
    return input_data_type


#原始数据筛选与判断
class raw_str_filter(object):
    def __init__(self,source):
        self.mark_num = source.find(':')
        self.targ_name = source[1,self.mark_num]
        self.targ_data = source[self.mark_num+1:-1]
        self.targ_dict = json.loads(self.targ_data)

#返回标签名 {标签名:{JSON数据块}}
#    def tag_name(self):\
#        if 'Netstat' in self.targ_name:
#            return 3

#返回数据块
    def source_data(self):
        return self.targ_dict


