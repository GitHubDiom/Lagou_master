import time,sys,os,re,json,csv
from collections import Counter,defaultdict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from pyecharts import Bar, Scatter3D,Pie,Line,Parallel,WordCloud,Geo,Page
from util.file_reader import parse_job_xml

col =   [
            u'职位编码',        u'职位名称',            u'所在城市',
            u'发布日期',        u'薪资待遇',            u'公司编码',
            u'公司名称',        u'公司全称',            u'公司规模',
            u'所在区域',        u'最低学历',            u'融资状态',
            u'公司类型',        u'经度',                u'纬度',   
            u'全职/实习',       u'工作经验'
        ]

job_count = defaultdict(int)
degree_count = defaultdict(int)
city_count = defaultdict(int)
exp_count = defaultdict(int)
finSta_count = defaultdict(int)

salary_city = defaultdict(int)
salary_job = defaultdict(int)
salary_degree = defaultdict(int)
salary_exp = defaultdict(int)
salary_finSta = defaultdict(int)


def solve_alot_problem(city,salary,job,degree,exp,finSta):
    salary_city[city] += salary
    city_count[city] += 1

    salary_job[job] += salary
    job_count[job] += 1

    salary_degree[degree] += salary
    degree_count[degree]  += 1

    salary_exp[exp] += salary
    exp_count[exp] += 1

    salary_finSta[finSta] += salary
    finSta_count[finSta] +=1

def main_solve():
    for job in os.listdir('../spider/data'):
        csvFile =  open('../spider/data/'+job,'r',encoding='utf-8')
        reader =  csv.reader(csvFile)
        job = job.rstrip('.csv')
        for item in reader:
            if reader.line_num == 1:
                continue     
            salary = int(float(item[5]))
            city = item[3]
            degree = item[11]
            exp = item[17]
            finSta = item[12]
            solve_alot_problem(city,salary,job,degree,exp,finSta)

def do_something(item):
    salary_list= [salary_city,salary_degree,salary_exp,salary_finSta,salary_job]
    pass
def creat_picture():
    page = Page()
    Item_list = ['job_count','degree_count','exp_count','finSta_count']
    #job_avg, degree_avg, exp_avg = [do_something(dictionary) for dictionary in (job_count, degree_count, exp_count)]
    
    #job_salary_avg, degree_salary_avg, exp_salary_avg, finSta_salary_avg = {item.split('_')[0] :do_something(item) for item in Item_list }

    city_salary_avg = {city:salary_city[city]//city_count[city] for city in city_count if city_count[city]!=0}

    job_salary_avg = {job:salary_job[job]//job_count[job] for job in job_count}
    
    degree_salary_avg = {degree : salary_degree[degree]//degree_count[degree] for degree in degree_count}

    exp_salary_avg =  {exp : salary_exp[exp]//exp_count[exp] for exp in exp_count}
    
    finSta_salary_avg = {finSta :salary_finSta[finSta]//finSta_count[finSta] for finSta in finSta_count if finSta!=''}

    geo = Geo("各城市平均月薪", "data from Diom",title_color="white",height=550, background_color='#404a59')
    city,salary = geo.cast(city_salary_avg)
    geo.add("", city, salary, visual_range=[0, 25] ,visual_text_color="black", symbol_size=15, is_visualmap=True)
    page.add(geo)
    
    
    #各岗位招聘数量占比
    pie_job = Pie()
    key ,value = pie_job.cast(degree_count)
    pie_job.add("", key, value, center=[50, 70], is_random=True, radius=[20, 55], is_legend_show=True, is_label_show=True)
    page.add(pie_job)
    
    
    #各岗位平均工资
    pie_salary = Bar()
    key ,value = pie_salary.cast(job_salary_avg)
    pie_salary.add("", key, value, is_label_show=True,mark_line=['average'])
    page.add(pie_salary)

    #最低学历需求占比
    pie_degree = Pie()
    key , value = pie_degree.cast(degree_count)
    pie_degree.add("", key, value, center=[50, 70], is_random=True, radius=[20, 55], is_legend_show=True, is_label_show=True)
    page.add(pie_degree)
    
    
    #不同学历对应平均工资
    pie_degree_salary  = Bar()
    key , value = pie_degree_salary.cast(degree_salary_avg)
    pie_degree_salary.add("", key, value, is_label_show=True,mark_line=['average'])
    page.add(pie_degree_salary)
    
    #工作经验需求占比
    exp = Pie()
    key, value = exp.cast(exp_count)
    exp.add("", key, value, center=[50, 70], is_random=True, radius=[20, 55], is_legend_show=True, is_label_show=True)
    page.add(exp)
    
    
    #不同工作经验对应的平均工资
    exp_salary = Bar()
    key, value = exp_salary.cast(exp_salary_avg)
    exp_salary.add("", key, value, is_label_show=True,mark_line=['average'])
    page.add(exp_salary)

    fin_sta  = Bar()
    key,value = fin_sta.cast(finSta_salary_avg)
    fin_sta.add("", key, value, is_label_show=True,mark_line=['average'])
    page.add(fin_sta)
    page.render()

if __name__ == '__main__':
    main_solve()
    creat_picture()
