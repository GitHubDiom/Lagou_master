import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
import csv
from pyecharts import Bar, Scatter3D,Pie,Line,Parallel,WordCloud
from pyecharts import Page
import re,json
from util.file_reader import parse_job_xml

from pyecharts import Geo
import jieba.analyse
import jieba.posseg as pseg

page = Page()         # step 1


degree_averange_salary={
                        "不限":0,     "大专":0,       
                        "本科":0,     "硕士":0,         
                        "博士":0
                        }
degree_total_salary={
                        "不限":0,     "大专":0,       
                        "本科":0,     "硕士":0,         
                        "博士":0
                        }

degree_cnt={
                        "大专人数":0,
                        "本科人数":0,   "硕士人数":0,
                        "不限人数":0,   "博士人数":0
}

col =   [
            u'职位编码',        u'职位名称',            u'所在城市',
            u'发布日期',        u'薪资待遇',            u'公司编码',
            u'公司名称',        u'公司全称',            u'公司规模',
            u'所在区域',        u'最低学历',            u'融资状态',
            u'公司类型',        u'经度',                u'纬度',   
            u'全职/实习',       u'工作经验'
        ]



key_word_vis = []
key_word_cnt={}

def solve_word_cloud():
    with open('keyword.txt','w',encoding='utf-8') as f:
        for job in os.listdir('../spider/data'):
            csvFile =  open('../spider/data/'+job,'r',encoding='utf-8')
            reader =  csv.reader(csvFile)
            job = job.rstrip('.csv')
            for item in reader:
                if reader.line_num == 1:
                    continue
                f.write(item[13]+'\n')
    f.close()  
    
    


city_degree_salary={}
city_degree_salary_cnt={}
    
def solve_degree(degree,salary,city):
    degree_total_salary[degree]+=salary
    degree_cnt[degree+'人数']+=1
    city_degree_salary[city][degree]+=salary
    city_degree_salary_cnt[city][degree]+=1
    


exp_vis=[]
exp_cnt={}

def solve_avg_pro():
    for city in city_vis:
        data[city]/=cnt_city[city]
        
    for city  in city_degree_salary:
        for degree in city_degree_salary[city]:
            if city_degree_salary_cnt[city][degree] != 0:
                city_degree_salary[city][degree]=int(city_degree_salary[city][degree]/city_degree_salary_cnt[city][degree])
                    
    #print(city_degree_salary)
    
    for degree in degree_averange_salary:
        if len(degree)<=2:
            degree_averange_salary[degree] = int(degree_total_salary[degree]/degree_cnt[degree+'人数'])

    for exp in exp_vis:
        exp_avg_salary[exp]=int(exp_total_salary[exp]/exp_cnt[exp])


average_salary={}
data = {}
city_vis =[]
cnt_city={}
job_cnt={}
cnt_salary={}
def solve_average_salary(salary,job,city,finSta):
    average_salary[job]+=salary
    job_cnt[job]+=1
    data[city]+=salary
    cnt_city[city]+=1
    cnt_salary[job]+=1
    if finSta == '':
        return 
    finance_average_salary[finSta]=int(finance_total_salary[finSta]/finance_cnt[finSta])



def solve_exp_cnt(exp):
    if exp not in exp_vis:
        exp_vis.append(exp)
        exp_cnt[exp]=1
        exp_total_salary[exp]=0
    else:
        exp_cnt[exp]+=1

def solve_city_vis(city):
    if city not in city_vis:
        city_degree_salary[city]={
                    "不限":0,     "大专":0,       
                    "本科":0,     "硕士":0,         
                    "博士":0
                }
        city_degree_salary_cnt[city]={
                    "不限":0,     "大专":0,       
                    "本科":0,     "硕士":0,         
                    "博士":0
                }
        city_vis.append(city)
        cnt_city[city]=0
        data[city]=0

exp_total_salary={}
exp_avg_salary={}

finance_total_salary={}
finance_average_salary={}
finance_cnt={}
finance_vis=[]
def solve_finance(finSta , salary):
    if finSta not in finance_vis:
        finance_vis.append(finSta)
        finance_total_salary[finSta]=salary
        finance_cnt[finSta]=1
    else:
        finance_cnt[finSta]+=1
        finance_total_salary[finSta]+=salary
    
def main_solve():
    sum=0
    cnt=0
    for job in os.listdir('../spider/data'):
        csvFile =  open('../spider/data/'+job,'r',encoding='utf-8')
        reader =  csv.reader(csvFile)
        job = job.rstrip('.csv')
        job_cnt[job]=0
        average_salary[job]=0
        cnt_salary[job]=0
        for item in reader:
            if reader.line_num == 1:
                continue     
            salary = int(float(item[5]))
            sum+=salary
            cnt+=1
            city = item[3]
            lowest_degree = item[11]
            exp = item[17]
            finSta=item[12]
            solve_exp_cnt(exp)
            exp_total_salary[exp]+=salary
            
            solve_finance(finSta,salary)
            solve_city_vis(city)           
            
            solve_degree(lowest_degree,salary,city)
            
            solve_average_salary(salary,job,city,finSta)

        average_salary[job]=int(average_salary[job]/cnt_salary[job])

main_solve()
#solve_word_cloud()
solve_avg_pro()

#geo = Geo("全国主要城市平均月薪", "data from Diom", title_color="#fff", title_pos="center",width=1350, height=670, background_color='#404a59')
geo = Geo("各城市平均月薪", "data from Diom",title_color="white",height=550, background_color='#404a59')
city,salary = geo.cast(data)
geo.add("", city, salary, visual_range=[0, 25] ,visual_text_color="black", symbol_size=15, is_visualmap=True)
page.add(geo)


#各岗位招聘数量占比
pie_job = Pie()
key ,value = pie_job.cast(job_cnt)
pie_job.add("", key, value, center=[50, 70], is_random=True, radius=[20, 55], is_legend_show=True, is_label_show=True)
page.add(pie_job)


#各岗位平均工资
pie_salary = Bar()
key ,value = pie_salary.cast(average_salary)
pie_salary.add("", key, value, center=[50, 70], is_random=True, radius=[20, 55], is_legend_show=True, is_label_show=True,mark_point=['max','min'],mark_line=['average'])
page.add(pie_salary)



line = Line("")
degree, avg_salary=line.cast(degree_averange_salary)
key, value=line.cast(degree_total_salary)
#line.add("商家A",key, value, is_fill=True, line_opacity=0.2, area_opacity=0.4, symbol=None)





#最低学历需求占比
pie_degree = Pie()
key , value = pie_degree.cast(degree_cnt)
pie_degree.add("", key, value, center=[50, 70], is_random=True, radius=[20, 55], is_legend_show=True, is_label_show=True)
page.add(pie_degree)


#不同学历对应平均工资
pie_degree_salary  = Bar()
key , value = pie_degree_salary.cast(degree_averange_salary)
pie_degree_salary.add("", key, value, center=[50, 70], is_random=True, radius=[20, 55], is_legend_show=True, is_label_show=True)

#line.add("最低学历对应平均工资", degree, avg_salary, is_fill=False, area_color='#001', area_opacity=0.9, is_smooth=True)
page.add(pie_degree_salary)



#工作经验需求占比
exp = Pie()
key, value = exp.cast(exp_cnt)
exp.add("", key, value, center=[50, 70], is_random=True, radius=[20, 55], is_legend_show=True, is_label_show=True)
page.add(exp)


#不同工作经验对应的平均工资
exp_salary = Bar()
key, value = exp_salary.cast(exp_avg_salary)
exp_salary.add("", key, value,mark_line = ['average'],mark_point=['min','max'])
page.add(exp_salary)



company_type=WordCloud()
key, value = company_type.cast(key_word_cnt)
company_type.add("",key, value,word_size_range=[20, 100])
#page.add(company_type)

fin_sta  = Bar()
key,value = fin_sta.cast(finance_average_salary)
fin_sta.add("", key, value,mark_line = ['average'],mark_point=['min','max'])
page.add(fin_sta)
page.render()