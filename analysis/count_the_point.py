import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
import csv
import pandas as pd

degree_point={
    '大专':4,    '本科':5,
    '硕士':4.5,    '博士':4,    '不限':4.2,

}

work_year={
    '1年以下':4.2,     '1-3年':5,           '3-5年':5,   '5-10年':4.7,
    '10年以上':4     ,'应届毕业生':3.9,     '不限':4,

}

finnance_stage={
    '天使轮':4.1,           'A轮':4.2,            
    'B轮':4.7,              'C轮':5,
    'D轮及以上':4.5,        '上市公司':4.4,        
    '不需要融资':4.0,       '未融资':3.8
}
col =   [
            u'职位编码',        u'职位名称',            u'所在城市',
            u'发布日期',        u'薪资待遇',            u'公司编码',
            u'公司名称',        u'公司全称',            u'公司规模',
            u'所在区域',        u'最低学历',            u'融资状态',
            u'公司类型',        u'经度',                u'纬度',   
            u'全职/实习',       u'工作经验',            u'总得分'
        ]

total_point={}
job_vis=[]

def write_to_excel(df):
    df.to_excel('total_point.xlsx')

def turn_salary(salary):
    if salary<20 and salary>10:
        return salary/10+5
    return salary/10

def main():
    job_list = []
    
    for job in os.listdir('../spider/data'):
        csvFile =  open('../spider/data/'+job,'r',encoding='utf-8')
        reader =  csv.reader(csvFile)
        for item in reader:
            if reader.line_num == 1:
                continue
            job = item[2]
            if job not in job_vis:
                job_vis.append(job)
            salary = turn_salary(int(float(item[5])))
            if item[12]=='':
                finnance_stage[item[12]]=4.2
            total_point[job]= salary+work_year[item[17]]+finnance_stage[item[12]]+degree_point[item[11]]   
            temp= []
            for i in range(1,18):
                temp.append(item[i])
            temp.append(total_point[job])
            job_list.append(temp)
    df = pd.DataFrame(job_list,columns=col)
    write_to_excel(df)


if __name__ == '__main__':
    main()