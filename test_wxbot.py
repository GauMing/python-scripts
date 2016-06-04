#!/usr/bin/env python
# coding: utf-8

import time
from wxbot import *
from turing_reply import *


t = turing()
class MyWXBot(WXBot):


    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            self.send_msg_by_uid('%s' % t.get_answer(msg['content']['data']), msg['user']['id'])
        elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0 and msg['user']['id'] == self.get_user_id('we are 逼格伐木累'):
            self.send_msg_by_uid('%s' % t.get_answer(msg['content']['data']), msg['user']['id'])
        # elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0:
        #     self.send_msg_by_uid('%s' % t.get_answer(msg['content']['data']), msg['user']['id'])
        elif msg['msg_type_id'] == 1 and msg['content']['type'] == 0:
            self.send_msg_by_uid('%s' % t.get_answer(msg['content']['data']), msg['user']['id'])

    def schedule(self):
        # self.send_msg('小太阳',self.get_user_id('小太阳'))
        # time.sleep(1)
        pass

def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.run()

if __name__ == '__main__':
    main()