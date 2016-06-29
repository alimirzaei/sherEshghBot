# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 09:24:04 2016

@author: toranado
"""

import urllib
import urllib2
import json


TOKEN = "167654974:AAGT2kRX7fJQCXjfSlx4g_-BKMMIYbNqY4k"
chat_id = 104729667


msg = "Please choose"
BASE_URL = "https://api.telegram.org/bot{}/".format(TOKEN)
options = [['خوشم اومد'],['ای بد نیست'],['اصلا حال نکردم'],['بسه رای دادم']];
reply_markup = {'keyboard': options, 'resize_keyboard': True, 'one_time_keyboard': True}
reply_markup = json.dumps(reply_markup)
params = urllib.urlencode({
      'chat_id': str(chat_id),
      'text': msg.encode('utf-8'),
      'reply_markup': reply_markup,
      'disable_web_page_preview': 'true',
      # 'reply_to_message_id': str(message_id),
})
resp = urllib2.urlopen(BASE_URL + 'sendMessage', params).read()