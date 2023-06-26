from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

def get_conn():
    conn = pymysql.connect(host="localhost", user="root", password="000000", db="tmp", charset="utf8")
    cursor = conn.cursor()
    return conn, cursor

def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def query(sql, *args):
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    conn.commit()
    close_conn(conn, cursor)
    return res

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['post'])
def data_query():
    user_input = request.form.get('keyword')
    test_input = 1
    sql = "SELECT * FROM data_table where id = %s"
    res = query(sql, user_input)
    return render_template('index.html', data=res)


# @app.route('/query', methods=['post'])
# def data_query():
#     user_input = request.form.get('keyword')  # 获取用户输入的关键词
#     sql = "SELECT * FROM data_table WHERE id = %s"  # 使用用户输入的关键词作为查询参数
#     res = query(sql, user_input)  # 执行参数化查询
#     return render_template('index.html', data=res)



if __name__ == '__main__':
    app.run('0.0.0.0')
