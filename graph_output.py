import datetime
import matplotlib.pyplot as plt
import mysql.connector
from mysql.connector import Error

def top_ten_user_pass_graph(conn):
    sql = f"""SELECT username, password FROM auth;"""
    cur = conn.cursor()
    i = 0
    cur.execute(sql)
    res = cur.fetchall()

    totals = {}
    for pair in res:
        usr, p = pair
        combined = usr + ": " + p
        if combined not in totals: #沒有在total,表示第一次出現,先紀錄一次
            totals.update({combined : 1})
        else:
            totals[combined] += 1 # 出現過找到該組合再加一次
    sortedDictionary = sorted(totals.items(), key = lambda x : x[1], reverse=True)
    x_list = []
    frequency_list = []
    while i < 10 and i < len(sortedDictionary):
        key, value = sortedDictionary[i]
        x_list.append(key)
        frequency_list.append(value)
        i += 1
    plt.figure(figsize=(12,5))
    plt.bar(x_list , frequency_list)
    plt.xticks(rotation=-15)
    dt_now = datetime.datetime.now()
    #dt_format = dt_now.strftime('%Y年%m月%d日_%H:%M:%S')
    dt_title = dt_now.strftime('%Y-%m-%d_%H:%M:%S')
    plt.title(f"""{dt_title}_top_ten_user_pass_graph""")
    plt.savefig(f"""./img/user_pass.png""")
    #plt.savefig(f"""./img/{dt_format}_user_pass.png""")
    plt.cla()
    cur.close()

def query_top_ten_graph(conn, col, table):
    sql = f"""SELECT {col} , COUNT({col}) AS cnt FROM {table} GROUP BY {col} ORDER BY cnt DESC;"""
    cur = conn.cursor()
    
    i = 0
    cur.execute(sql)
    res = cur.fetchall()
    stop_val = 10 # 要印出出現次數前多少的值
    x_list = []
    frequency_list = []
    while i < stop_val and i < len(res): # 當結束有兩種,一種是到達指定印的名次,另一種是已經沒有了
        key, frequency = res[i] 
        i += 1
        x_list.append(key)
        frequency_list.append(frequency)
    plt.bar(x_list , frequency_list)
    plt.xticks(rotation=-15)
    dt_now = datetime.datetime.now()
    #dt_format = dt_now.strftime('%Y年%m月%d日_%H:%M:%S')
    dt_title = dt_now.strftime('%Y-%m-%d_%H:%M:%S')
    plt.title(f"""{dt_title}_top_ten_{col}_graph""")
    plt.savefig(f"""./img/{col}.png""")
    #plt.savefig(f"""./img/{dt_format}_{col}.png""")
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
            query_top_ten_graph(connection, "ip" , "sessions")
            query_top_ten_graph(connection, "username", "auth")
            query_top_ten_graph(connection, "password", "auth")
            top_ten_user_pass_graph(connection)
            
    except Error as e:
        print("資料庫連接失敗：", e)
    finally:
        if (connection.is_connected()):
            connection.close()
