# -*- coding: utf-8 -*-
# !/usr/bin/env python
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from collections import defaultdict
import pandas as pd
from config.config import *
def main_solve(): 
    csvFile =  open('../spider/data/Info.csv','r',encoding='utf-8')
    df = pd.read_csv(csvFile)
    city_set = df.所在城市.unique()
    job_set = df.职业类别.unique()
    degree_set  = df.最低学历.unique()
    city_salary_avg = {city :int(df[df['所在城市']==city]['薪资待遇'].mean()) for city in city_set if int(df[df['所在城市']==city]['所在城市'].value_counts())>30}
    job_salary_avg = {job : int(df[df['职业类别']==job]['薪资待遇'].mean()) for job in job_set}
    degree_salary_avg = {degree : int(df[df.最低学历== degree].薪资待遇.mean()) for degree in degree_set}
    
    page = Page()
    #各城市平均月薪
    geo = Geo(title_color="white",height=550, background_color='#404a59')
    city,salary = geo.cast(city_salary_avg)
    geo.add("", city, salary, visual_range=[0, 25] ,visual_text_color="black", symbol_size=15, is_visualmap=True)
    page.add(geo)

    #各岗位热度
    pie_salary = Pie()
    key ,value = pie_salary.cast(dict(df.职业类别.value_counts()))
    pie_salary.add("", key, value, center=[50, 70], is_random=True, radius=[20, 55], is_legend_show=True, is_label_show=True)
    page.add(pie_salary)

    #各岗位平均工资
    pie_salary = Bar()
    key ,value = pie_salary.cast(job_salary_avg)
    pie_salary.add("", key, value,mark_point=['max','min'],mark_line=['average'],xaxis_rotate =60  )
    page.add(pie_salary)
    
    #最低学历平均工资
    pie_salary = Bar()    
    key ,value = pie_salary.cast(degree_salary_avg)
    pie_salary.add("", key, value, is_label_show=True,mark_line=['average'])
    page.add(pie_salary)
    page.render()
if __name__ == '__main__':
    main_solve()
    