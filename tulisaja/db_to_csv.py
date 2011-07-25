#!/usr/bin/env python
import csv
import MySQLdb


fields = ['title', 'content', 'time', 'url_title']
writer = csv.DictWriter(open("kriwil.csv", "wb"), fields)
conn = MySQLdb.connect(host='localhost', user='root', passwd='akarakar',
                       db='kriwil')

cursor = conn.cursor()
cursor.execute("SELECT title, content, time, url_title FROM posts WHERE status=1 ORDER BY time ASC")

writer.writeheader()
while (True):
    row = cursor.fetchone()
    if row is None:
        break

    csv_row = {
        'title': row[0],
        'content': row[1],
        'time': row[2],
        'url_title': row[3],
    }

    writer.writerow(csv_row)
