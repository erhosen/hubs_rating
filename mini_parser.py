#!/usr/bin/env python
# encoding: utf-8

from grab.spider import Spider, Task
import sqlite3 as lite
from grab.tools.logs import default_logging
import re

class MiniHabraParser(Spider):

    base_url = 'http://habrahabr.ru/'
    initial_urls = ['http://habrahabr.ru/hubs/']

    def prepare(self):
        print "Let's start parse need hubs from Habrahabr"
        self.hubs = []

    def task_initial(self, grab, task):
        nav = grab.doc.select('//ul[@class="next-prev"]/li/a[@class="next"]')

        for elem in grab.doc.select('//div[@class="hub "]'):
            hub_url = elem.node.find('div[@class="info"]/div[1]/a').get('href')
            print hub_url
            hub_name = elem.node.find('div[@class="info"]/div[1]/a').text
            hub_index = ''
            try:
                hub_index = float(elem.node.find('./div[@class="habraindex"]').text.replace(" ", "").replace(',', '.'))
            except:
                hub_index = 0.0
            hub_posts = int(re.findall(r'\d+', elem.node.find('div[@class="info"]/div[@class="stat"]/a[2]').text)[0])
            if hub_posts > 200 and hub_index > 100.0:
                self.hubs.append(hub_url.split('/')[4] + '|' + hub_name)

        if nav.exists():
            self.add_task(Task(name='initial', url=nav.attr('href')))
        else:
            self.save_file()

    def save_file(self):
        file = open('files/top_hubs.txt', 'w')
        for item in self.hubs:
            file.write("%s\n" % item.encode('utf-8'))
        file.close()

def main():
    bot = MiniHabraParser(thread_number=1, network_try_limit=3, task_try_limit=3, priority_mode="const")
    bot.setup_grab(timeout=96, connect_timeout=10)
    bot.run()
    print bot.render_stats()


if __name__ == '__main__':
    default_logging()
    main()
