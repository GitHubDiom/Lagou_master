# -*- coding: utf-8 -*-
# !/usr/bin/env python
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from collections import defaultdict
import pandas as pd
def main_solve(): 
    csvFile =  open('../spider/data/Info.csv','r',encoding='utf-8')
    df = pd.read_csv(csvFile)
    city_set = set(df.所在城市)
    job_set = set(df.职业类别)
    print(df['所在城市'].value_counts())
    city_salary_avg = {city :df[df['所在城市']==city]['薪资待遇'].mean() for city in city_set}
    job_salary_avg = {job : df[df['职业类别']=='图像处理']['薪资待遇'].mean() for job in job_set}
    
if __name__ == '__main__':
    main_solve()
    