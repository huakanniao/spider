import pandas as pd
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import pymysql
import time
from sqlalchemy import create_engine
starttime=time.time()
def get_one_page(i):
    try:
        pares={
            'reportTime':'2017-12-31',#可以改报告日期，比如2018-6-30获得的就是该季度的信息
            'pageNum':i
        }
        url='https://s.askci.com/stock/a/?'+urlencode(pares)
        headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.text
        return None
    except :
        # 函数回调解决ConnectionResetError: [WinError 10054] 远程主机强迫关闭了一个现有的连接。
        get_one_page(i)


def parse_one_page(html):
    soup=BeautifulSoup(html,'html.parser')
    # prettify()优化代码,[0]从pd.read_html返回的list中提取出DataFrame
    table=pd.read_html(soup.select('#myTable04')[0].prettify(), header=0)[0]
    table.rename(columns={'序号': 'serial_number', '股票代码': 'stock_code', '股票简称': 'stock_abbre', '公司名称': 'company_name',
                        '省份': 'province', '城市': 'city', '主营业务收入(201712)': 'main_bussiness_income',
                        '净利润(201712)': 'net_profit', '员工人数': 'employees', '上市日期': 'listing_date', '招股书': 'zhaogushu',
                        '公司财报': 'financial_report', '行业分类': 'industry_classification', '产品类型': 'industry_type',
                        '主营业务': 'main_business'}, inplace=True)

    return table

def con_mysql():
    conn = pymysql.Connect(host='127.0.0.1', port=3307, user='root', password='password',
                           db='test',
                           charset='utf8')
    # mediumtext解决Data too long for column 'main_business' at row 4的问题
    sql = 'CREATE TABLE IF NOT EXISTS listed_company (serial_number INT(20) NOT NULL,stock_code INT(20) ,stock_abbre VARCHAR(20) ,company_name VARCHAR(100) ,province VARCHAR(20) ,city VARCHAR(20) ,main_bussiness_income VARCHAR(20) ,net_profit VARCHAR(20) ,employees VARCHAR(20),listing_date DATETIME(0) ,zhaogushu VARCHAR(20) ,financial_report VARCHAR(20) , industry_classification mediumtext ,industry_type mediumtext,main_business VARCHAR(255) ,PRIMARY KEY (serial_number))'
    cur=conn.cursor()
    cur.execute(sql)
    cur.close()
    conn.close()


def inser_table(table):
    host = '127.0.0.1'
    user = 'root'
    passwd = 'password'
    db = 'test'
    pot = 3307
    engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8".format(user, passwd, host, pot, db))
    try:
        table.to_sql('listed_company',con=engine,if_exists='append',index=False)
        # append表示在原有表基础上增加，但该表要有表头
    except Exception as e:
        print(e)
def main(page):
    con_mysql()

    for i in range(1,page):
        html=get_one_page(i)
        table=parse_one_page(html)
        inser_table(table)
        print('第%d页爬取成功' % i)
# 单进程
if __name__=='__main__':
    main(178)
    print(time.time()-starttime)

# 多进程
# from multiprocessing import Pool
# if __name__ == '__main__':
# 	pool = Pool(4)
# 	pool.map(main, [i for i in range(1,178)])  #共有178页
# 	endtime = time.time()-start_time
# 	print('程序运行了%.2f秒' %(time.time()-start_time))
