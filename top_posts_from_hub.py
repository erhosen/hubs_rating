#!/usr/bin/env python
# encoding: utf-8

from grab.spider import Spider, Task
import sqlite3 as lite
import logging

class HabraParser(Spider):

    initial_urls = ['http://habrahabr.ru/hubs/']

    def prepare(self):
        self.post = []
        self.con = lite.connect('files/habra_hubss.db')

    def task_initial(self, grab, task):
        nav = grab.doc.select('//ul[@class="next-prev"]/li/a[@class="next"]')

        for elem in grab.doc.select('//div[@class="info"]/div[@class="stat"]/a[2]'):
            self.add_task(Task(name='hub', url=elem.attr('href')))

        if nav.exists():
            self.add_task(Task(name='initial', url=nav.attr('href')))

    def task_hub(self, grab, task):
        nav = grab.doc.select('//a[@class="next" and @id="next_page"]')

        for elem in grab.doc.select('//div[@class="posts shortcuts_items"]/div'):
            if elem.attr('class') == 'ufo-was-here':
                continue
            comments = ''
            score = ''
            favs = ''
            post_url = elem.node.find('h1[@class="title"]/a').get('href')
            post_title = elem.node.find('h1[@class="title"]/a').text
            try:
                comments = int(elem.node.find('.//span[@class="all"]').text)
            except:
                comments = 0

            try:
                score = int(elem.node.find('.//span[@class="score"]').text)
            except:
                score = 0

            try:
                favs = int(elem.node.find('.//div[@class="favs_count"]').text)
            except:
                favs = 0


            self.post.append([
                score,
                comments,
                favs,
                post_url,
                post_title
            ])

        if nav.exists():
            self.add_task(Task(name='hub', url=nav.attr('href')))
        else:
            hub = task.url.split('/')[4]
            self.save_data(hub)

    def save_data(self, hub):
        with self.con:
            self.cur = self.con.cursor()
            self.cur.execute("DROP TABLE IF EXISTS %s"%hub)
            self.cur.execute("CREATE TABLE %s(Score INT, Comments INT, Favs INT, Url TEXT, PostTitle TEXT)"%hub)

            self.cur.executemany("INSERT INTO %s VALUES(?, ?, ?, ?, ?)"%hub, self.post)

        self.post = []


def main():
    bot = HabraParser(thread_number=1, network_try_limit=3, task_try_limit=3, priority_mode="const")
    bot.setup_grab(timeout=96, connect_timeout=10)
    bot.run()
    print bot.render_stats()


if __name__ == '__main__':
    logging.basicConfig(filename='files/parser.log',level=logging.DEBUG)
    main()

