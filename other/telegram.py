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
        self.bot_id = CowrieConfig.get("output_telegram","bot_token") 
        self.chat_id = CowrieConfig.get("output_telegram","chat_id") 

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