import pymysql

# 连接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='111111',
    database='spider',
    charset='utf8mb4',  # 设置字符集，避免中文乱码
    cursorclass=pymysql.cursors.DictCursor  # 返回字典类型的游标，方便使用键值对访问结果
)

class User:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.password = data['password']

    def __str__(self):
        return f'User(id={self.id}, name={self.name}, password={self.password})'

try:
    with conn.cursor() as cursor:
        sql = 'select * from users'
        cursor.execute(sql)
        result = cursor.fetchall()
        users = [User(a) for a in result]
        for a in users:
            print(a)

        users = list(map(User, result))

finally:
    # 关闭数据库连接
    conn.close()

