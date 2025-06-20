# create_db.py
import sqlite3


# 初始化数据库
conn = sqlite3.connect('example.db')
# 创建游标
cur = conn.cursor()

# 创建表
cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')
cur.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, user_id INTEGER, amount FLOAT)')

# 插入数据
cur.executemany('INSERT INTO users (name, age) VALUES (?, ?)', [('Alice',28),('Bob',35)])
cur.executemany('INSERT INTO orders (user_id, amount) VALUES (?,?)', [(1,100),(2,150),(2,50)])

# 提交事务
conn.commit()
conn.close()
