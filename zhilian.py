# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 22:08:06 2019
@author: Moc
"""

import pymysql
import requests
#import time
#from urllib.parse import quote

def parse_page(url,city_code):
    try:
        response = requests.get(url).json()
        result = response['data']['results']
        for r in result:
            company = r['company']['name']
            size = r['company']['size']['name']
            type_ = r['company']['type']['name']
            company_url = r['company']['url']
            eduLevel = r['eduLevel']['name']
            emplType = r['emplType']
            jobName = r['jobName']
            jobTag = r['jobTag']['searchTag']
            jobType = r['jobType']['display']
            positionURL = r['positionURL'] #招聘链接
            rate = r['rate']  #反馈率
            salary = r['salary'] #工资
            workingExp = r['workingExp']['name'] #工作经验
    #        data = [company,size,type_,company_url,eduLevel,emplType,jobName,jobTag,jobType,positionURL,rate,salary,workingExp]
            insert_sql = """insert into	jobs_salary(company,size,type_,company_url,eduLevel,emplType,jobName,jobTag,jobType,positionURL,rate,salary,workingExp,city_code) 
                                values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');
                        """.format(company,size,type_,company_url,eduLevel,emplType,jobName,jobTag,jobType,positionURL,rate,salary,workingExp,city_code)
            print(company)
            print(positionURL)
            print('\n')
            try:
                cur.execute(insert_sql)
                conn.commit()
            except Exception as e:
                print(e)
                pass
    except Exception as e:
        print(e)
        pass
    
def parse_main(url,pages,city_code,job):
    for page in range(pages):
        p = page*90
        url_r = url.format(page=p,city_code=city_code,job=job)
        print('开始爬取第{}页链接'.format(page+1))
        print(url_r)
        parse_page(url_r,city_code)
#        time.sleep(5)
        
if __name__ == '__main__':
    conn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="123456",
            db="zhilian_jobs",
            port=3306,
            charset="utf8"
        )
    cur = conn.cursor()
    url ="https://fe-api.zhaopin.com/c/i/sou?start={page}&pageSize=90&cityId={city_code}&industry=10100&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={job}&kt=3&=0&_v=0.33977872&x-zp-page-request-id=b0434b03d11e4b9daf4cf3a887fbd121-1547573058264-851670"
#    url = "https://fe-api.zhaopin.com/c/i/sou?start={page}&pageSize=90&cityId={city_code}&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={job}&kt=3&=0&_v=0.12367974&x-zp-page-request-id=4b1c9ae01d674decbc440cd60082872d-1547563110403-998176"
    pages=12
    job='%E7%A0%94%E5%8F%91' #研发
    city_code_list = ['530','765','538','763']
#    city_code='530' #北京：530; 全国：489,深圳：765,上海：538,广州：763
    for city_code in city_code_list:
        print(city_code)
        parse_main(url,pages,city_code,job)
    conn.close()
