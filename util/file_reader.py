from lxml import etree
from collections import defaultdict
import re
def parse_job_xml(job_xml_filepath):
    """
    parse the job.xml file in res directory, and return job list
    :param job_xml_filepath:
    :return:
    """
    catalog_job = defaultdict(list)
    tree = etree.parse(job_xml_filepath)
    job_catalog_tag = tree.xpath('//job_catalog')
    for item in job_catalog_tag:
        v = item.xpath('string(.)').split()
        job_list = []
        for i in range(1,len(v)):
            job_list.append(v[i])
        catalog_job[v[0]]=job_list
    return catalog_job
