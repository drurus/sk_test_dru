# -*- coding: utf-8 -*-

from config import Config
import pymysql.cursors
import json
import requests
from datetime import datetime


class NoConnect(Exception):
    pass


class sk_mysql():

    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host=Config.BASE_HOST,
                user=Config.BASE_USER,
                password=Config.BASE_PASSWORD,
                db=Config.BASE_BASE,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            self.connection = None
            raise NoConnect

    def base_execute(self, sql: str):
        ret = False
        try:
            if not self.connection:
                raise NoConnect
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
            self.connection.commit()
            ret = True
        except Exception as e:
            if Config.DEBUG:
                print(f'''SQL error: {str(e)}''')
        return ret

    def showall(self):
        sql = f'''select * from {Config.SK_TABLE}'''
        if not self.connection:
            raise NoConnect
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            for row in cursor:
                print('showall: %s' % row)

    def base_create(self, name: str):
        sql=f'''CREATE TABLE `{name}` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `module` varchar(255) COLLATE utf8_bin NOT NULL,
            `id_mod` varchar(20) COLLATE utf8_bin NOT NULL,
            `id_parent` varchar(20) COLLATE utf8_bin,
            `date` datetime NOT NULL,
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
            AUTO_INCREMENT=1 ;'''
        if not self.base_execute(sql):
            if Config.DEBUG:
                print('Error create base')

    def base_remove(self, name: str):
        sql = f'''DROP TABLE {name};'''
        if not self.base_execute(sql):
            if Config.DEBUG:
                print('Error remove base')

    def base_insert(self, tablename, module, id_mod, id_parent: str = None):
        sql = f'''INSERT INTO {tablename} (module, id_mod, date) VALUES('{module}', '{id_mod}', '{datetime.now()}');'''
        if id_parent:
            sql = f'''INSERT INTO {tablename} (module, id_mod, id_parent, date) VALUES('{module}', '{id_mod}', '{id_parent}', '{datetime.now()}');'''
        if not self.base_execute(sql):
            if Config.DEBUG:
                print('Error insert base')


class sk_date():

    @staticmethod
    def get_json(url: str):
        try:
            r = requests.get(url, timeout=Config.URL_TIMEOUT)

            if Config.DEBUG:
                print(f'''Retrived from {url}''')
            return r.json()
        except requests.exceptions.ReadTimeout:
            if Config.DEBUG:
                print(f'''TIMEOUT for {url}''')
        except json.decoder.JSONDecodeError:
            if Config.DEBUG:
                print(f'''Unparsed json data for {url}''')
        return False

    @staticmethod
    def get_fake_json():
        # jdat = {
        #     "1. Наименование модуля": "id_1",
        #     "2. Наименование модуля": "id_2",
        #     "2.2 Наименование модуля": "id_2.2",
        #     "2.3 Наименование модуля": "id_2.3",
        #     "3. Наименование модуля": "id_3"
        # }
        jdat = [
          {
          "module": "1. Наименование модуля",
          "id": "id_1"
          },
          {
            "module": "2. Наименование модуля",
            "id": "id_2",
            "submodules": [
                {
                  "module": "2.2. Наименование модуля",
                  "id": "id_2.2"
                },
                {
                  "module": "2.3. Наименование модуля",
                  "id": "id_2.3"
                }
            ]
          },
          {
          "module": "3. Наименование модуля",
          "id": "id_3"
          }
        ]

        return json.dumps(jdat)
