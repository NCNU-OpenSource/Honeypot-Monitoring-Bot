import datetime
import matplotlib.pyplot as plt
import mysql.connector
from mysql.connector import Error

def last_10days_conn_line_chart(conn):
    sql = f"""SELECT DATE(starttime) AS day , COUNT(*) AS cnt FROM sessions WHERE DATEDIFF(DATE(starttime), CURDATE()) <= 0 AND DATEDIFF(DATE(starttime),CURDATE())>-10 GROUP BY DATE(starttime) ORDER BY day ;"""
    cur = conn.cursor()
    i = 0
    cur.execute(sql)
    res = cur.fetchall()

    x_list = []
    frequency_list = []
    while i < 10 and i < len(res):
        key, value = res[i]
        x_list.append(key.strftime('%Y-%m-%d'))
        frequency_list.append(value)
        i += 1
    plt.figure(figsize=(12,6))
    plt.plot(x_list , frequency_list)
    plt.xticks(rotation=-15)
    dt_now = datetime.datetime.now()
    dt_title = dt_now.strftime('%Y-%m-%d_%H:%M:%S')
    plt.title(f"""{dt_title}_last_10_days_line_chart""")
    plt.xlabel('Date')
    plt.ylabel('Frequency')
    plt.savefig(f"""./img/last_10_days_conn_line_chart.png""")
    plt.cla()
    cur.close()

if __name__ == "__main__":
    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='localhost',  # 主機名稱
            database='cowrie', # 資料庫名稱
            user='cowrie',     # 帳號
            password='cowrie') # 密碼

        if connection.is_connected():
            last_10days_conn_line_chart(connection)
            
    except Error as e:
        print("資料庫連接失敗：", e)
    finally:
        if (connection.is_connected()):
            connection.close()
