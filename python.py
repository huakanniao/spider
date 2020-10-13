import pymysql
class WangyiproPipeline(object):
    def process_item(self, item, spider):
        print(item)
        return item
class mysqlpipeline:
    conn=None
    cursor=None
    def open_spider(self,spider):
        self.conn=pymysql.Connect(host='localhost',port=3306,user='root',password='241299',db='test',charset='utf8')
        self.conn.cursor().execute('create table if not exists wangyinews(title varchar(25),content mediumtext)')
    def process_item(self, item, spider):
        self.cursor=self.conn.cursor()
        try:
            self.cursor.execute('insert into wangyinews values("%s","%s")' %(item['title'],item['content']))
            self.conn.commit()
        except:
            self.conn.rollback()
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
11
