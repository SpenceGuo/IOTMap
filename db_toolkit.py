"""
该部分python代码用于将本repo提供的csv文件数据存入MySQL数据库中

本py文件提供了两种方法：
1.使用 pymysql 开发包动态连接数据库并逐条插入数据库（速度较慢，不推荐）
2.生成sql文件然后在数据库管理工具上运行sql文件即可（速度较快，推荐）
"""

import pymysql
import time

from config import *


def dump_to_database(csv_file_path: str, tb_name: str):
    """
    此函数使用pymysql开发包动态将csv数据插入mysql数据库
    :param csv_file_path: 保存结点所有信息的csv文件，路径默认在 'data/china.csv'
    :param tb_name: 需要插入的数据库表名
    :return: null
    """
    # 打开数据库连接
    db = pymysql.connect(
        config['ip'],
        config['username'],
        config['password'],
        config['db_name']
    )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    f = open(csv_file_path, "r", encoding="utf-8")
    data = f.read().splitlines()
    index = len(data)
    print("开始入库......")
    for i in range(1, index):
        line = data[i].split(',')
        sql = f"INSERT INTO {tb_name}(province,city,district,longitude,latitude,device_type)" \
              f"VALUES ('{line[0]}','{line[1]}','{line[2]}','{line[3]}','{line[4]}','{line[5]}')"
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            if i % 1000 == 0:
                cur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print(str(cur_time) + "--当前数据入库进度：{}%".format(round(100 * i / index)))
        except:
            # 如果发生错误则回滚
            db.rollback()
            print("Insert failed!")
    db.close()


def dump_to_sql_file(csv_file_path: str, sql_file_path: str, tb_name: str):
    """
    此函数将根据csv数据生成插入数据库的sql文件，方便在数据库管理工具中快速导入数据
    :param csv_file_path: 保存结点所有信息的csv文件，路径默认在 'data/china.csv'
    :param tb_name: 需要插入的数据库表名
    :return: null
    """
    f1 = open(sql_file_path, "w", encoding="utf-8")
    f = open(csv_file_path, "r", encoding="utf-8")
    data = f.read().splitlines()
    index = len(data)
    for i in range(1, index):
        line = data[i].split(',')
        sql = f"INSERT INTO {tb_name}(province,city,district,longitude,latitude,device_type)" \
              f"VALUES ('{line[0]}','{line[1]}','{line[2]}','{line[3]}','{line[4]}','{line[5]}');\n"
        f1.write(sql)
        if i % 1000 == 0:
            cur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print(str(cur_time) + "--当前完成进度：{}%".format(round(100 * i / index)))
    f.close()
    f1.close()


def create_table(tb_name: str):
    """
    在数据库中建立数据表，请确保执行代码前您已经建立好mysql数据库
    编码格式为 utf-8， 排序规则为 utf-8_general_ci
    :param tb_name: 你即将建立的数据表的名称
    :return: null
    """
    # 打开数据库连接,此处需要你手动配置你的数据库信息, 修改在同级目录下的 'config.py' 文件中
    db = pymysql.connect(
        config['ip'],
        config['username'],
        config['password'],
        config['db_name']
    )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute(f"DROP TABLE IF EXISTS {tb_name}")
    # 使用预处理语句创建表
    sql = f"CREATE TABLE `{tb_name}` (" \
          f"`_id` int(11) NOT NULL AUTO_INCREMENT," \
          f"`province` varchar(25) DEFAULT NULL," \
          f"`city` varchar(50) DEFAULT NULL," \
          f"`district` varchar(50) DEFAULT NULL," \
          f"`longitude` varchar(10) DEFAULT NULL," \
          f"`latitude` varchar(10) DEFAULT NULL," \
          f"`device_type` varchar(5) DEFAULT NULL," \
          f"PRIMARY KEY (`_id`)) " \
          f"ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    cursor.execute(sql)
    # 关闭数据库连接
    db.close()


def main():
    create_table('devices_location')
    # dump_to_database('data/china.csv', 'devices_location')
    dump_to_sql_file('data/china.csv', 'data/china.sql', 'devices_location')
    print("Finished!")


if __name__ == '__main__':
    main()
