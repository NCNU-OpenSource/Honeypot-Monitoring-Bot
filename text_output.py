import mysql.connector
from mysql.connector import Error

def longest_durations(conn):
    output_str = ""
    sql = """SELECT id , TIMESTAMPDIFF(SECOND, starttime, endtime) as duration FROM sessions AS duration ORDER BY duration DESC;"""
    cur = conn.cursor()
    i = 0
    cur.execute(sql)
    res = cur.fetchall()

    strReturn = "最久停留的 session 前十名： \n<session id> : <duration (second)> \n"
    print_num = 1
    while i < 10 and i < len(res):
        session_id , duration = res[i]
        if print_num == 10:
            strReturn += str(print_num) + ". " + str(session_id) + " : " + str(duration) + "\n"
        else:
            strReturn += str(print_num) + ".  " + str(session_id) + " : "+ str(duration) + "\n"
        print_num += 1
        i += 1
    first_s , first_d = res[0]
    first= str(first_s) + " : " + str(first_d)
    cur.close()
    return (strReturn, first)

def top_ten_user_pass(conn):
    sql = f"""SELECT username, password FROM auth;"""
    cur = conn.cursor()
    i = 0
    cur.execute(sql)
    res = cur.fetchall()

    strReturn = "出現最多的 username/password pair 前十名：\n" # 結果字串
    totals = {}
    for pair in res:
        usr, p = pair
        combined = usr + ": " + p
        if combined not in totals: #沒有在total,表示第一次出現,先紀錄一次
            totals.update({combined : 1})
        else:
            totals[combined] += 1 # 出現過找到該組合再加一次
    sortedDictionary = sorted(totals.items(), key = lambda x : x[1], reverse=True)
    while i < 10 and i < len(sortedDictionary):
        key, value = sortedDictionary[i]
        if i == 9:
            strReturn += str(i + 1) + ". " + str(key) + "\n"
        else:
            strReturn += str(i + 1) + ".  " + str(key) + "\n"
        i += 1
    first, val = sortedDictionary[0]
    return strReturn, first

def query_top_ten(conn, col, table):
    sql = f"""SELECT {col} , COUNT({col}) AS cnt FROM {table} GROUP BY {col} ORDER BY cnt DESC;"""
    cur = conn.cursor()
    try:
        i = 0
        cur.execute(sql)
        res = cur.fetchall()
        stop_val = 10 # 要印出出現次數前多少的值
        print_num = 1 # 印出1到10的標題
        strReturn = f"出現最多的 {col} 前 {stop_val} 名：\n" # 印出排行結果字串
        while i < stop_val and i < len(res): # 當結束有兩種,一種是到達指定印的名次,另一種是已經沒有了
            key, _ = res[i] # 印出鍵（欄位名稱）
            if print_num == 10:
                strReturn += str(print_num) + ". " + str(key) + "\n"
            else:
                strReturn += str(print_num) + ".  " + str(key) + "\n"
            print_num += 1
            i += 1
        first, _ = res[0]
        cur.close()
        return (strReturn, first)
    except:
        print(f"Failed {col}")
        return None

if __name__ == "__main__":
    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='localhost',  # 主機名稱
            database='cowrie', # 資料庫名稱
            user='cowrie',     # 帳號
            password='cowrie') # 密碼

        if connection.is_connected():
            strIPaddress , first_ipaddress = query_top_ten(connection, "ip" , "sessions")
            print(strIPaddress)
            strUsername , first_username = query_top_ten(connection, "username", "auth")
            print(strUsername)
            strPassword , first_password = query_top_ten(connection, "password", "auth")
            print(strPassword) 
            strUPpair , firstUPpair = top_ten_user_pass(connection) 
            print(strUPpair)
            strDuration , firstDuration = longest_durations(connection)
            print(strDuration)
            print(f"各報告的第一名：")
            print(f" - ip: {first_ipaddress} \n - usr : {first_username} \n - pass : {first_password} \n - User/Pass : {firstUPpair} \n - duration : {firstDuration}")

    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            connection.close()
