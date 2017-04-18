# -*- coding: UTF-8 -*-
from configparser import ConfigParser

#读取程序需要的参数，比如kafka、es的连接信息，写入es的索引名等
cfg = ConfigParser()
cfg.read('config.ini')



#NetStat相关内容读取
#NetStatRecon_INDEX = cfg.get('es_indexs', 'NetStatRecon_INDEX')
#NetStatRecon_DOCTYPE = cfg.get('es_indexs', 'NetStatRecon_DOCTYPE')
discon_reason1 = cfg.get('rawinfo_note','discon_reason1')
discon_reason2 = cfg.get('rawinfo_note','discon_reason2')
discon_reason3 = cfg.get('rawinfo_note','discon_reason3')
discon_reason4 = cfg.get('rawinfo_note','discon_reason4')
discon_reason5 = cfg.get('rawinfo_note','discon_reason5')

esurl = cfg.get('es_setup','esurl')