import requests,re
from bs4 import BeautifulSoup
from collections import defaultdict
import bs4,json
from xml.dom.minidom import Document  
import numpy as np
def getHtmlText(request_url):
    try:
        response  = requests.get(request_url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except:
        return ""
def write_to_xml(dic):
    #doc = Document()  
    #people = doc.createElement("people")  
    #doc.appendChild(people)  
    #aperson = doc.createElement("person")  
    #people.appendChild(aperson)  
    #name = doc.createElement("name")  
    #name1 = doc.createElement("name")  
#
    #aperson.appendChild(name)
    #aperson.appendChild(name1)  
    #personname = doc.createTextNode("Annie")  
    #personname1 = doc.createTextNode('Bob')
    #name.appendChild(personname)  
    #name1.appendChild(personname1)  
    #filename = "people.xml"  
    #f = open(filename, "w")  
    #f.write(doc.toprettyxml(indent="  "))  
    #f.close()  
    f = open('../config/job.xml','w',encoding='utf-8')
    doc = Document()  
    job_list = doc.createElement("job_list")  
    doc.appendChild(job_list)
    for each_catalog in dic:
        print(str(each_catalog))
        job_catalog = doc.createElement('job_catalog')
        job_list.appendChild(job_catalog)
        job_catalog_text = doc.createTextNode(str(each_catalog))
        job_catalog.appendChild(job_catalog_text)
        for  each_job in dic[each_catalog]:
            job = doc.createElement('job')
            job_catalog.appendChild(job)
            job_text = doc.createTextNode(str(each_job))
            job.appendChild(job_text)
               
    f.write(doc.toprettyxml(indent='    '))
    f.close

if __name__ == '__main__':
    request_url  = 'https://www.lagou.com'
    html = getHtmlText(request_url)
    soup = BeautifulSoup(html,'html.parser')
    blocks  = soup.find('div',class_='menu_sub dn')
    dic = {}
    for item in blocks:
        #print(type(item))
        if isinstance(item,bs4.element.Tag):
            span_tag = item.find_all('span')
            a_tag = item.find_all('a')
            for span in span_tag:
                list_text=[]
                for a in a_tag:
                    list_text.append(a.string)
                dic[span.get_text()]=list_text
    write_to_xml(dic)