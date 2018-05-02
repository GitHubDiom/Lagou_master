# -*- coding: utf-8 -*-
# !/usr/bin/env python
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from config.config import *

log_temp = log.Logger()#实例化日志对象
log = log_temp.getLoger('log')

def get_headers():
    headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "55",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "JSESSIONID=ABAAABAAAFCAAEGD661EDF927F899A28C8FC98364C7D666; _ga=GA1.2.933738451.1522827762; user_trace_token=20180404154313-d4278f01-37db-11e8-b38f-525400f775ce; LGUID=20180404154313-d427918b-37db-11e8-b38f-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=f2e9d38019f213d292bdeda3963420e0; _gid=GA1.2.310176793.1523414629; ab_test_random_num=0; _putrc=F5AD82AF68E98230123F89F2B170EADC; login=true; hasDeliver=0; unick=%E5%90%B4%E6%9C%9D%E9%94%90; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1523262125,1523273493,1523273673,1523426562; TG-TRACK-CODE=jobs_again; gate_login_token=3af9570b22fc05b500808a35f2736e805b09112a59e79cc56d6eeaa07b8d1e6f; LGSID=20180412100812-5a428a3a-3df6-11e8-b9f9-525400f775ce; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1523501196; LGRID=20180412104713-cdf5da2c-3dfb-11e8-b747-5254005c3644; SEARCH_ID=9b47ea98eed14343a1636263dd420b0b",
            "Host": "www.lagou.com",
            "Origin": "https://www.lagou.com",
            "Referer": "https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98?px=default&gx=%E5%85%A8%E8%81%8C&gj=&isSchoolJob=1&city=%E5%85%A8%E5%9B%BD",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
            "X-Anit-Forge-Code": "0",
            "X-Anit-Forge-Token": "None",
            "X-Requested-With": "XMLHttpRequest"
                }
    return headers

def get_Info(positionName,pn):
    form_data={
                "first": "true",
                "pn": pn,
                "kd": str(positionName)
                    }
    return form_data

def crawl_jobs(positionName):
    """crawl the job info from lagou H5 web pages"""
    try:
        JOB_DATA = list()
        max_page_number = get_max_pageNo(positionName)
        info_str=positionName, "共有",max_page_number,"页记录, 共约",max_page_number * 15,"条记录"
        str_info = ''
        for s in info_str:
            if s=='"':
                continue
            else:
                str_info=str_info+str(s)
        log.info(str_info)
        for pn in range(1, max_page_number + 1):
            headers=get_headers()
            form_data=get_Info(positionName,pn)
            url="https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
            response = requests.post(url,headers=headers,data=form_data)
            if response.status_code == 200:
                for each_item in response.json()['content']['positionResult']['result']:#通过分析Ajax返回的JSON数据进行筛选
                    a= re.findall('\d\d?',each_item['salary'])
                    l=int(a[0])
                    try:
                        r=int(a[1])
                    except:
                        r=l
                    JOB_DATA.append([each_item['positionId'],       each_item['positionName'],      each_item['city'],
                                        each_item['createTime'],       (l+(r-l)*0.4),           each_item['companyId'], 
                                        each_item['companyShortName'], each_item['companyFullName'],   each_item['companySize'],
                                        each_item['district'],         each_item['education'],         each_item['financeStage'],
                                        each_item['industryField'],    each_item['longitude'],         each_item['latitude'],
                                        each_item['jobNature'],        each_item['workYear'],          each_item['companyLabelList']
                                    ])
                print("当前页数：{0} 总进度为:{1}%".format(pn,round((pn + 1) * 100 / max_page_number)), end="\r")
                time.sleep(0.01)
                if pn%20 ==0:
                    time.sleep(TIME_SLEEP)
            elif response.status_code == 403:
                log.error('request is forbidden by the server...')
            else:
                log.error(response.status_code)
        return JOB_DATA
    except Exception:
        log.error('error in '+positionName+' at page :'+str(pn)+'\n')
        send_email(traceback.format_exc())        
        log.error(traceback.format_exc())

def get_max_pageNo(positionName):
    """return the max page number of a specific job"""
    request_url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
    headers = get_headers()
    form_data=get_Info(positionName,1)
    response = requests.post(request_url, headers=headers, data = form_data,timeout=10)
    if response.status_code == 200:
        max_page_no = int(int(response.json()['content']['positionResult']['totalCount']) / 15 + 1)
        return max_page_no
    elif response.status_code == 403:
        log.error('request is forbidden by the server...')
        return 0
    else:
        log.error(response.status_code)
        return 0


#def write_to_excel(df,position):
#    path = "./data/"
#    excel_path = path+position+".xlsx"
#    try:
#        if not os.path.exists(path):
#            os.mkdir(path)
#        if not os.path.exists(excel_path):
#            filename = xlwt.Workbook()
#            sheet=filename.add_sheet(position)
#        df.to_excel(path + position + ".xlsx", sheet_name=position, index=False)
#        log.info("Excel表格创建成功，文件名路径为"+excel_path)
#    except:
#        log.error("路径为 "+excel_path+"的Excel表格创建失败")

def write_to_csv(df , position,position_catalog):
    path ='./data/'+position_catalog+'/'
    csv_path = path+position+'.csv'
    try:
        if not os.path.exists('./data'):
            os.mkdir('./data')
        if not os.path.exists(path):
            os.mkdir(path)
        df.to_csv(csv_path)
        log.info("CSV文件创建成功，文件名路径为"+csv_path)
    except:
        log.error("路径为 "+csv_path+"的CSV文件创建失败")

def send_email(text):
    # 第三方 SMTP 服务
    mail_host="smtp.163.com"  #设置服务器
    mail_user="diom_wu@163.com"#用户名
    mail_pass="XXXXXX"   #SMTP口令 
    
    sender = 'diom_wu@163.com'
    receivers = ['diom_wu@163.com']  
    
    message = MIMEText(text, 'plain', 'utf-8')
    #message['From'] = Header("测试", 'utf-8')
    #message['To'] =  Header("测试", 'utf-8')
    
    subject = '文件运行错误报告'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException:
        log.error(traceback.print_exc())
        print("Error: 无法发送邮件")

if __name__ == '__main__':
    craw_job_list = parse_job_xml('../config/job.xml')
    try:
        for position_catalog in craw_job_list:
            for position in craw_job_list[position_catalog]:
                joblist = crawl_jobs(position)
                col = [
                    u'职位编码',        u'职位名称',            u'所在城市',
                    u'发布日期',        u'薪资待遇(k)',         u'公司编码',
                    u'公司名称',        u'公司全称',            u'公司规模',
                    u'所在区域',        u'最低学历',            u'融资状态',
                    u'公司类型',        u'经度',                u'纬度',           
                    u'全职/实习',       u'工作经验',            u'吸引条件'
                    ]
                df = pd.DataFrame(joblist, columns=col)
                #write_to_excel(df,position)
                write_to_csv(df,position,position_catalog)
        log.info('爬取任务完成！')
    except Exception as e:
        #send_email(traceback.format_exc())
        log.error(traceback.format_exc())

        
