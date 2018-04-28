# -*- coding: utf-8 -*-
# !/usr/bin/env python
import re,os,time,requests,sys,traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from util.file_reader import parse_job_xml
import pandas as pd
from config.config import *
try:
    from urllib import parse as parse
except:
    import urllib as parse
import xlwt
from util import log

log_temp = log.Logger()#实例化日志对象
log = log_temp.getLoger('log')

request_url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
try:
    response = requests.get(request_url)
    print(response.json()['content']['positionResult']['totalCount'])

except Exception as e:
    log.error(traceback.format_exc())
