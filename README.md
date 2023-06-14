# Real-time Honeypot Monitoring Bot Assistant
## Concept Development
- 因為接觸資安領域，想學習攻擊者如何在進入系統後進行攻擊的技巧與方法，透過網路查詢通常不太可能有太多實務上的攻擊技巧可以透漏，因此我們想藉由密罐蒐集這類資訊，透過 telegram 即時通知我們，現在有攻擊者在我們架設的密罐上的偽系統中下的指令，使我們能夠及時收看一場場精彩的攻擊轉播。

## Architecture
- ![](https://hackmd.io/_uploads/rkbv1XIv3.png)
  - 呈現被禁止 ip (封鎖暴力破解登入並蒐集被禁止 IP)
    - 當攻擊者嘗試 ssh 登入三次後，會被 Fail2ban 封鎖一段時間，並且 Fail2Ban 會將 ban IP 傳送至 telegram bot 輸出通知我們。
  - 攻擊通知
    - 攻擊者嘗試 ssh 登入，會進入密罐，所有攻擊者輸入的 password 會被即時轉傳到 telegram bot (對應是哪一個攻擊者 ip 輸入的用戶名/密碼)  
  - 監控
    - 當今天攻擊者成功 ssh 登入，會進入密罐事先設定好的假作業系統環境，攻擊者在裡頭輸入的指令與 wget 下載的檔案，都會被即時紀錄並轉傳到 telegram bot 
    - 訊息會對應是哪一個攻擊者 ip 輸入的指令
  - 顯示分析報告 
    - 系統管理員能向 telegram bot 發送特定指令，使其統整現有密罐所蒐集來的資訊，並製作圖表傳送到 Telegram。
## Implementation Resources
- 軟體
  - cowrie
  - fail2ban 
  - mysql 
  - telegram
- 硬體
  - 電腦(筆電) * 1 
    - OS 以測試過 ubuntu 22.04 
  - 行動裝置(手機) * 1 
    - 下載 telegram app

## Existing Library/Software
- Cowrie
  - Cowrie is a medium to high interaction SSH and Telnet honeypot designed to log brute force attacks and the shell interaction performed by the attacker. 
  - Github 專案 : https://github.com/cowrie/cowrie
- Fail2Ban 
  - Fail2Ban scans log files and bans IP addresses conducting too many failed login attempts.
  - Github 專案 : https://github.com/fail2ban/fail2ban
- Telegram
  - 是跨平台的即時通訊軟體，其用戶端是自由及開放原始碼軟體
## Implementation Process
### Step 1. 更改主機預設的 ssh port
- 更改 `/etc/ssh/sshd_config` 的 Port 22222 (沒有人用的)
- ![](https://hackmd.io/_uploads/rkt7tL_Ih.png)
- 重啟 ssh 服務
```cmd=
systemctl restart ssh
systemctl status ssh
```
### Step 2. Cowrie 安裝
* 安裝需要的軟體、依賴項 
    * `sudo apt-get install git python3-virtualenv libssl-dev libffi-dev build-essential libpython3-dev python3-minimal authbind virtualenv`
* 建立使用者帳號 
    * `adduser cowrie`
* 切換使用者 
    * `sudo su cowrie`
* 下載 cowrie 
    * `git clone http://github.com/cowrie/cowrie`
* 進入 cowrie 資料夾，建立 python 的虛擬環境
    * `cd cowrie/`
    * `virtualenv --python=python3 cowrie-env`
* 啟動虛擬環境
    * `source cowrie-env/bin/activate`
    * 重新啟動 `/home/cowrie/cowrie/bin/cowrie restart`
    * 在這裡使用 python 虛擬環境，主要是為了將 OS 本機 python 環境與我們將為 cowrie 安裝的依賴項隔離開來。
* 升級 pip
    * `pip install --upgrade pip`
* 安裝 Cowrie 所需的依賴項
    * `pip install --upgrade -r requirements.txt`
* 新增一個預設範例設定檔，方便再裏頭修改設定
    > 預設讀取的設定檔是 `cowrie.cfg.dist`
    * 直接複製一份 `cp etc/cowrie.cfg.dist etc/cowrie.cfg`
    > 之後將讀取的設定檔是 `cowrie.cfg`
* 將從 22 port 進來的連線分別導向 2222 port
    * `exit` 
       * 先回到主機環境
    * `sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222`
#### 補充 : 自動啟用 iptables 設定
* 查看目前 iptables nat 表裡面的 PREROUTING chain
    * `iptables -t nat -n -L PREROUTING`
* 永久保存 iptables
    * `sudo apt-get install iptables-persistent`
#### 補充 : 使用 ssh 連線時線出現錯誤
![](https://hackmd.io/_uploads/HkXEGPuUh.png)
* 刪除與連線 IP 相關的密鑰
    * `ssh-keygen -R <要連線的 ip>`
    * Ex. `ssh-keygen -R 10.107.38.92`
#### 設定 cowrie honeypot
- 以下操作都是使用 cowrie 身份在該啟用的虛擬環境中執行
- 設定 假的 SSH、telnet 可使用的帳號密碼
  - 先複製一份原先預設提供的範例
     - `cp ~/cowrie/etc/userdb.example ~/cowrie/etc/userdb.txt`
  - `vim ~/cowrie/etc/userdb.txt` 
  - ![](https://hackmd.io/_uploads/B1LkUUuUh.png)
### Step 3. 配置 Fail2ban
#### 安裝
- `sudo apt install fail2ban`
#### 設定
- 新增一個過濾檔 `/etc/fail2ban/filter.d/cowrie.conf`
  - ![](https://hackmd.io/_uploads/ryD67iOUn.png)
- 新增一個設定檔 `/etc/fail2ban/jail.d/cowrie.conf`
  - ![](https://hackmd.io/_uploads/Hkr-mi_Uh.png)

- 記得將兩服務重啟
```cmd=
sudo service fail2ban restart
/home/cowrie/cowrie/bin/cowrie restart
```
- 自動啟用 fail2ban 
  - `sudo systemctl enable fail2ban`
### Step 4. 配置 Telegram Bot
#### 建立 Telegram Bot
* 找到 [@BotFather](https://t.me/botfather)
* 輸入 `/newbot` 建立一個機器人
* 輸入機器人名稱、輸入使用者名稱（以 bot 結尾）
  * 我們的機器人名稱 : `Cowrie-log-analyzer-bot`
  * 我們的使用者名稱 : `CowrieHoneypot_Bot` 
* 得到 Telegram bot 的連結、token
> token 記得妥善保管，以免其他人透過這組 token 操控你的機器人
![](https://hackmd.io/_uploads/BJbI1aZP2.jpg =60%x)

#### fail2ban 訊息發送至 telegram bot
- `git clone https://github.com/deividgdt/fail2ban_telegram_notifications`
- 加入 action 設定在 `/etc/fail2ban/jail.d/cowrie.conf`
```
          action=iptables[name=COWRIE,port=2222,protocol=tcp]
          telegram
```
- Download the file `telegram.conf` and move it to `/etc/fail2ban/action.d/` 
- Download the file `send_telegram_notif.sh` move it to `/etc/fail2ban/scripts/`
- Bot_Token : `9999999999:XXXXXXXXXXXXXXXXXXXXXXXXX`
- 取得 ChatID
  - ![](https://hackmd.io/_uploads/r1CHoq-w2.png)
- Modify the file `/etc/fail2ban/scripts/send_telegram_notif.sh` and add your Token and your Chat ID:
```
telegramBotToken=YOUR_BOT_TOKEN
telegramChatID=YOUR_CHAT_ID
```
- `chmod +x /etc/fail2ban/scripts/send_telegram_notif.sh `
- `systemctl restart fail2ban`
#### 將 cowrie 訊息即時發送至 telegram bot
- 編輯 `etc/cowrie.cfg`，找到 `[output_telegram]` ，注意 `bot_token` 跟 `chat_id` 不要改名稱，後面接的值改成自己 Bot 的值
```
[output_telegram]
enabled = true
bot_token = 5922090657:AAEVkZJ3XXXXXXXXXXXXXXXXXX
chat_id = 123456789
```
- 編輯 `src/cowrie/output/telegram.py`
```python=
# Simple Telegram Bot logger

from __future__ import absolute_import, division

import urllib3
import certifi
from twisted.python import log
from cowrie.core.config import CowrieConfig
import cowrie.core.output

class Output(cowrie.core.output.Output):
    """
    telegram output
    """

    def start(self):
        self.bot_id = CowrieConfig.get("output_telegram","bot_token") # 改成自己的 bot token
        self.chat_id = CowrieConfig.get("output_telegram","chat_id") # 改成自己的 chat_id

    def stop(self):
        pass

    def write(self, logentry):
        for i in list(logentry.keys()):
            # remove twisted 15 legacy keys
            if i.startswith('log_'):
                del logentry[i]

        if "login attempt" in logentry['message']:
            msgtxt = "[cowrie] " + logentry['timestamp']
            msgtxt += "  " + logentry['message']
            msgtxt += "  (session " + logentry['session'] + ")"
            msgtxt += "  (source ip " + logentry['src_ip'] + ")"
            try:
                https = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
                r = https.request('GET', 'https://api.telegram.org/bot' + self.bot_id + '/sendMessage?chat_id=' + str(self.chat_id) + '&text=' + msgtxt)
            except urllib3.exceptions.SSLError as err:
                print('[ERROR] Telegram SSL error', err)
        elif "CMD" in logentry['message']:
            msgtxt = "cowrie" + logentry['timestamp']
            msgtxt += "   " + logentry['message']
            msgtxt += "   (session " + logentry['session'] + ")"
            msgtxt += "   (source ip " + logentry['src_ip'] + ")"
            try:
                https = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
                r = https.request('GET', 'https://api.telegram.org/bot' + self.bot_id + '/sendMessage?chat_id=' + str(self.chat_id) + '&text=' + msgtxt)
            except urllib3.exceptions.SSLError as err:
                print('[ERROR] Telegram SSL error', err)
```
### Step 5. 配置 MySQL 
- 安裝 mysql
```terminal=
$ sudo apt-get install mysql-server
$ service mysql status
$ sudo netstat -tap | grep mysql
$ sudo mysqladmin -u root password 'lsa123'
$ sudo mysql -u root -p 'lsa123'
```
- 在 `mysql>` 指令中輸入以下指令
```terminal=
$ CREATE DATABASE cowrie;
$ CREATE USER 'cowrie'@'localhost' IDENTIFIED BY 'cowrie';
$ GRANT ALL PRIVILEGES ON cowrie.* TO 'cowrie'@'localhost';
$ exit
```

- cowrie 虛擬環境需安裝 mysql-connector-python
```terminal=
$ sudo su - cowrie
$ source cowrie/cowrie-env/bin/activate
$ pip3 install mysql-connector-python
```
- 在 python 虛擬環境，載入 docs/sql/ 目錄中提供的資料庫模板
```termianl=
$ cd ~/cowrie/docs/sql/
$ mysql -u cowrie -p
$ USE cowrie;
$ source mysql.sql;
$ exit
```
#### 將 cowrie log 訊息傳輸到 MySQL 存放
```terminal=
$ cd ~/cowrie/etc
$ vim cowrie.cfg
```
- 找到 `[output_mysql]` 關鍵字
```
[output_mysql]
enabled = true
host = localhost
database = cowrie
username = cowrie
password = PASSWORD HERE (cowrie)
port = 3306
debug = false
```
- 重啟 cowrie
  - `/home/cowrie/cowrie/bin/cowrie start`
- 檢查`~/cowrie/var/log/cowrie/cowrie.log` 的末尾以確保 MySQL 輸出引擎已成功加載
  - `tail -f ~/cowrie/var/log/cowrie/cowrie.log`
  - ![](https://hackmd.io/_uploads/HJGAglQv3.png)
### Step 6. 放入此專案的 Python Script 
- 使用 `cowrie` 使用者在 python 虛擬環境中
- `cd /home/cowrie`
- `git clone https://github.com/wyping314/Real-time-Honeypot-Monitoring-Bot-Assistant.git`
- 此專案的架構
```
Real-time_Honeypot_Monitoring_Bot/
    |
    |________ requirements.txt
    |________ telegram_notify.py
    |________ text_output.py
    |________ graph_output.py
    |________ img/
    |          |____ (存放 graph_output.py 輸出的圖片)
    |
    |________ tty_output.py
    |________ video/
    |          |_____ (存放 tty_output.py 輸出的影片)
    |
    |________ README.md
    
```
- 安裝此專案需要的依賴項
  - `pip install --upgrade -r requirements.txt`
- 檢查 mysql 連線設定
  - 修改 `text_output.py`、`graph_output.py`、 `tty_output.py`
- 檢查 telegram bot 連線設定 
  - 修改 `telegram_notify.py` token 以及
- 啟動 `telegram_notify.py`
  - `python3 telegram_notify.py`
## Installation
- 當完成上述 inmpletation process，之後要安裝只要確認以下
  - 確認 python script 是否運行 
## Usage

### Demo Telegram Bot 功能
- 接收 fail2ban 所 ban / uban ip address 
- 即時地接收成功登入的攻擊者，所下的所有指令(需對應攻擊者 ip)
- 傳送 ip_graph ，bot 回傳前十大 ip address 長條圖
- 傳送 user_passwd_graph ，bot 回傳前十大頻繁的用戶名密碼長條圖
- 傳送 show_tty 指令，將指定的 tty 文件執行 playlog，重現攻擊者在密罐中的所有過程

## 碰到的問題

## Job Assignment
- 建立 MySQL，python 圖表視覺化輸出 : `王念祖`
- telegram bot 架設、撰寫 python 程式與 telegram 互動  : `王詠平`
- 其他部份 : `王念祖` 、 `王詠平`
  - 建立與設定 Cowrie、Fail2Ban
  - 撰寫文件 
## 感謝名單
- `陳柏瑋` : 題材發想
## References
- https://github.com/deividgdt/fail2ban_telegram_notifications
- https://github.com/nuno-carvalho/cowrie-output-telegram
- https://github.com/jasonmpittman/cowrie-log-analyzer