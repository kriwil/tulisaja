#!/usr/bin/env python
import MySQLdb
import json
import os


source_dir = 'source/'
conn = MySQLdb.connect(host='localhost', user='root', passwd='akarakar',
                       db='kriwil')

cursor = conn.cursor()
cursor.execute("SELECT title, content, time, url_title FROM posts WHERE status=1 ORDER BY time ASC")
while (True):
    row = cursor.fetchone()
    if row is None:
        break

    title = row[0]
    content = row[1]
    time = row[2]
    slug = row[3]

    date_path = time.strftime("%Y/%m/%d")
    full_path = source_dir + date_path
    try:
        os.makedirs(full_path)
    except OSError:
        pass

    meta_data = {
        'title': title,
        'time': str(time),
    }

    meta_data = "\r\n\r\n<!-- %s -->\r\n" % json.dumps(meta_data)

    content_file = open("%s/%s.md" % (full_path, slug), "wb")
    content_file.write("### %s\r\n\r\n" % title)
    content_file.write(content)
    content_file.write(meta_data)
    content_file.close()
