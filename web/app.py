from flask import Flask, render_template, request
import pymysql
from flask import send_file
import os
import io
app = Flask(__name__)


def get_conn():
    conn = pymysql.connect(host="localhost", user="root", password="000000", db="pdbqtDB", charset="utf8")
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

# @app.route('/download', methods=['GET', 'POST'])
# def download_file():
#     user_input = request.args.get('keyword')
#     sql = "SELECT pdbqtText FROM pdbqtData where fileName = %s;"
#     res = query(sql, user_input)
    
#     # Convert the results to text format
#     result_text = '\n'.join([str(row) for row in res])
    
#     # Write the result to a temporary file
#     filename = f'{user_input}'
#     with open(filename, 'w') as file:
#         file.write(result_text)
    
#     return send_file(filename, mimetype='text/plain', as_attachment=True)
#     # Send the file as a response
#     # return send_file(filename, mimetype='text/plain', as_attachment=True)

@app.route('/download', methods=['GET', 'POST'])
def download_file():
    user_input = request.args.get('keyword')
    sql = "SELECT pdbqtText FROM pdbqtData where fileName = %s;"
    res = query(sql, user_input)
    
    # Fetch the result
    result = res[0] if res else None
    
    # If result exists, write to a pdbqt file
    if result:
        filename = f'{user_input}'
        with open(filename, 'w') as file:
            file.write(result[0])
        return send_file(filename, mimetype='text/plain', as_attachment=True)
    else:
        return "No data found for this keyword."


@app.route('/query', methods=['POST'])
def data_query():
    user_input = request.form.get('keyword')
    sql = "SELECT pdbqtText FROM pdbqtData where fileName = %s;"
    res = query(sql, user_input)
    print(user_input)
    return render_template('index.html', data=res, keyword=user_input)


# @app.route('/query', methods=['post'])
# def data_query():
#     user_input = request.form.get('keyword')  # 获取用户输入的关键词
#     sql = "SELECT * FROM data_table WHERE id = %s"  # 使用用户输入的关键词作为查询参数
#     res = query(sql, user_input)  # 执行参数化查询
#     return render_template('index.html', data=res)



if __name__ == '__main__':
    app.run('0.0.0.0')
