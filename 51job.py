# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 11:42:00 2019
@author: Moc
"""
import pymysql
import requests
import time
from lxml import etree
from bs4 import BeautifulSoup
#from urllib.parse import quote

def parse_page(url,city_code):
    try:
        soup = requests_(url)
        resultList = soup.find_all('div', id ='resultList')
        con_result = etree.HTML(str(resultList).replace('\u3000','').replace('\n','').strip())
        
        job_list = [name.strip() for name in con_result.xpath('//div[@class="el"]/p[contains(@class,"t1")]/span/a//text()')]
        job_url_list = con_result.xpath('//div[@class="el"]/p[contains(@class,"t1")]/span/a//@href')
        company_list = con_result.xpath('//div[@class="el"]/span[contains(@class,"t2")]/a//text()')
        company_url = con_result.xpath('//div[@class="el"]/span[contains(@class,"t2")]/a//@href')
        location = con_result.xpath('//div[@class="el"]/span[contains(@class,"t3")]//text()')
        salary = con_result.xpath('//div[@class="el"]/span[contains(@class,"t4")]//text()')
        date = con_result.xpath('//div[@class="el"]/span[contains(@class,"t5")]//text()')

        for i in range(len(job_list)):
    #        data = [company,size,type_,company_url,eduLevel,emplType,jobName,jobTag,jobType,positionURL,rate,salary,workingExp]
            insert_sql = """insert into	jobs_salary(job,job_url,company,company_url,location,salary,city_code,produce) 
                                values ('{}','{}','{}','{}','{}','{}','{}','{}');
                        """.format(job_list[i],job_url_list[i],company_list[i],company_url[i],location[i],salary[i],city_code,date[i])
            print(company_list[i])
            print(job_list[i])
            print(salary[i])
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
    
def requests_(url):
    data = requests.get(url)
    data.encoding = 'gb18030'
    d = data.text
    soup = BeautifulSoup(d, 'lxml')
    return soup
    
def parse_main(url,pages,city_code,job):
    for page in range(1,pages+1):
        url_r = url.format(city_code=city_code,job=job,page=page)
        print('开始爬取第{}页链接'.format(page+1))
        print(url_r)
        parse_page(url_r,city_code)
        time.sleep(3)
        
if __name__ == '__main__':
    conn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="123456",
            db="lagou_jobs",
            port=3306,
            charset="utf8"
        )
    cur = conn.cursor()

    url = "https://search.51job.com/list/{city_code},000000,0000,00,9,99,{job},2,{page}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
    pages=20  #共2000
    job='%25E7%25A0%2594%25E5%258F%2591' #研发   '%25E6%258C%2596%25E6%258E%2598':挖掘
    city_code_list = ['040000','010000','020000','030200']
    #北京：010000; 全国：489,深圳：040000,上海：020000,广州：030200
    city_code = '%252C'.join(city_code_list)
    print(city_code)
    parse_main(url,pages,city_code,job)
    conn.close()


