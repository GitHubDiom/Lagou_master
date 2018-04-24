from lxml import etree


def parse_job_xml(job_xml_filepath):
    """
    parse the job.xml file in res directory, and return job list
    :param job_xml_filepath:
    :return:
    """
    tree = etree.parse(job_xml_filepath)
    return tree.xpath('//job/text()')
