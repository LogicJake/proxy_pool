# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-16 13:24:52
# @Last Modified time: 2019-01-16 20:32:28
from .database import DataBase
import pymysql
from config import db_conf, logger


class MySqlDB(DataBase):

    def __init__(self):
        self.host = db_conf.get_value('host')
        self.user = db_conf.get_value('user')
        self.password = db_conf.get_value('password')
        self.dbname = db_conf.get_value('dbname')
        self.port = db_conf.get_value('port')

    def connect(self):

        conn = pymysql.connect(host=self.host, user=self.user,
                               passwd=self.password, db=self.dbname,
                               port=self.port, charset='utf8', autocommit=True)
        self.conn = conn
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def insert(self, table_name, key_values):
        origin_sql = 'INSERT INTO {}({}) VALUES ({})'
        if type(key_values) != dict:
            logger.error('type of key_values must be dict')
            exit(-1)
        else:
            keys = []
            values = []
            for key, value in key_values.items():
                keys.append(str(key))
                values.append(str(value))

            names = ','.join(keys)
            values = ','.join(values)
            sql = origin_sql.format(table_name, names, values)
            sql = sql + ' ON DUPLICATE KEY UPDATE UPDATE_TIME = UPDATE_TIME'
            self.cursor.execute(sql)

    def is_table_exist(self, table_name):
        try:
            self.select(table_name, ['*'])
        except Exception:
            return False
        else:
            return True

    def select(self, table_name, column_name, where=None, limit=None, order_by=None, order='desc'):
        origin_sql = 'SELECT {} FROM {}'

        if type(table_name) != str:
            logger.error('type of table_name must be str')
            exit(-1)

        if type(column_name) != list:
            logger.error('type of column_name must be list')
            exit(-1)
        else:
            column_name = ','.join(column_name)

        sql = origin_sql.format(column_name, table_name)

        if order_by is not None:
            sql = '{} order by {} {}'.format(sql, order_by, order)

        if where is not None:
            sql = '{} WHERE {}'.format(sql, where)

        if limit is not None:
            if type(limit) != int:
                logger.error('type of limit must be int')
                exit(-1)
            else:
                sql = '{} LIMIT {}'.format(sql, limit)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        results = list(results)
        results = [list(r) for r in results]
        return results

    def delete(self, table_name, where=None):
        sql = 'DELETE from {}'.format(table_name)
        if where is not None:
            sql = '{} WHERE {}'.format(sql, where)
        self.cursor.execute(sql)

    def create_required_tables(self):
        if not self.is_table_exist('origin'):
            sql = "CREATE TABLE origin (ID INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,IP  CHAR(20) NOT NULL,PORT  INT(20) NOT NULL,UPDATE_TIME int(11) NOT NULL,UNIQUE (IP))"
            self.cursor.execute(sql)
            logger.info('Create table "origin"')

        if not self.is_table_exist('available'):
            sql = "CREATE TABLE available (ID INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,IP  CHAR(20) NOT NULL,PORT  INT(20) NOT NULL,UPDATE_TIME int(11) NOT NULL,SPEED FLOAT NOT NULL,UNIQUE (IP),STATUS int(1) NOT NULL DEFAULT 0)"
            self.cursor.execute(sql)
            logger.info('Create table "available"')
