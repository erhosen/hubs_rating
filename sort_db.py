#!/usr/bin/env python
# encoding: utf-8

import grab
import sqlite3 as lite

def create_top(cur, hub, hub_name, j_file):
    result = []
    result.append(u'<spoiler title="%s">\nПо количеству комментариев:' % hub_name)
    cur.execute("SELECT * FROM %s" % hub)
    cur.execute("SELECT * FROM %s ORDER BY Comments DESC LIMIT 10" % hub)
    rating_rows = cur.fetchall()
    for row in rating_rows:
        result.append("<a href='" + row[3] + "'>" + row[4] + "</a> " + "<b>" + str(row[1]) + "</b>")
    result.append(u'\nПо количеству добавлений в избранное')
    cur.execute("SELECT * FROM %s ORDER BY Favs DESC LIMIT 10" % hub)
    favs_rows = cur.fetchall()
    for row in favs_rows:
        result.append("<a href='" + row[3] + "'>" + row[4] + "</a> " + "<b>" + str(row[2]) + "</b>")
    result.append('</spoiler>')
    for item in result:
        j_file.write("%s\n" % item.encode('utf-8'))


def main():
    con = lite.connect('files/habra_hubs.db')

    o_file = open('files/top_hubs.txt').readlines()
    j_file = open('files/result4.html', 'w')

    with con:

        cur = con.cursor()
        for elem in o_file:
            data = elem.replace('\n', '').split('|')
            hub = data[0]
            hub_name = data[1].decode('utf-8')
            create_top(cur, hub, hub_name, j_file)
        j_file.close()

if __name__ == '__main__':
    main()

