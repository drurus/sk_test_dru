# -*- coding: utf-8 -*-


from config import Config
from sk_base import sk_date, sk_mysql
from json import dumps, loads



# jdata = sk_date.get_json(url=Config.SK_URL)
jdata = loads(sk_date.get_fake_json(), encoding='utf-8')

cc = sk_mysql()
cc.base_remove(f'''{Config.BASE_BASE}.{Config.SK_TABLE}''')
cc.base_create(Config.SK_TABLE)

if jdata:
    for row in jdata:
        print(row)
        cc.base_insert(tablename=f'''{Config.BASE_BASE}.{Config.SK_TABLE}''', module=row.get('module'), id_mod=row.get('id'))
        if row.get('submodules'):
            nid = row.get('id')
            for srow in row['submodules']:
                cc.base_insert(tablename=f'''{Config.BASE_BASE}.{Config.SK_TABLE}''', module=srow.get('module'),
                               id_mod=srow.get('id'), id_parent=nid)
                print(srow)


cc.showall()

