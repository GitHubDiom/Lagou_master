# -*- coding: utf-8 -*-
# !/usr/bin/env python
import os
import re,os,time,requests,sys,traceback,json,csv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from util.file_reader import parse_job_xml
import pandas as pd
import numpy as np
import seaborn as sns
from collections import Counter,defaultdict

from pyecharts import Bar, Scatter3D,Pie,Line,Parallel,WordCloud,Geo,Page,Grid,Polar

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import matplotlib.pyplot as plt
from operator import itemgetter
try:
    from urllib import parse as parse
except:
    import urllib as parse
import xlwt
from util import log

import smtplib
from email.mime.text import MIMEText
from email.header import Header

TIME_SLEEP = 2

LOGGER_FORMAT = "%(asctime)s-%(name)s-%(levelname)s-%(message)s"
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
