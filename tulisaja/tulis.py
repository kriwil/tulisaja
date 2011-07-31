#!/usr/bin/env python

from datetime import date, datetime
from jinja2 import Environment, PackageLoader
from markdown2 import markdown
import json
import os
import re


def rss_datetime_format(value, format="%a, %d %b %Y %H:%M:%S +0700"):
    return value.strftime(format)


source_dir = '../../kriwil.com/source/'
content_dir = '../../kriwil.com/content/'
journal_dir = content_dir + 'journal/'
archive_dir = content_dir + 'archive/'
latest_post_count = 10

# jinja
env = Environment(loader=PackageLoader('tulis', 'templates'))
env.filters['rss_datetime_format'] = rss_datetime_format

template = env.get_template('journal.html')
archive_template = env.get_template('archive.html')
index_template = env.get_template('index.html')
feed_template = env.get_template('rss.xml')

# get current date set
# only processing data <= current date
current_year = date.today().year
current_month = date.today().month
current_day = date.today().day

years = os.listdir(source_dir)
years.sort()
months_ref = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
]

latest_posts = []
archive_posts = {}


def process_items(items, year, item_date, source_day):

    for item in items:
        source_item = source_day + item

        # get title
        # file is in format 'nn_journal-title.md'
        # where nn is number to have article in correct order
        title = re.sub('\.md$', '', item)

        item_markdown = open(source_item)
        raw_content = item_markdown.read()

        title_search = re.match("### (.+)", raw_content)
        real_title = title_search.group(1)

        raw_content = raw_content.replace(title_search.group(0), '')
        html_content = markdown(raw_content)

        metadata_search = re.search("METADATA: (.+) -->", raw_content, re.DOTALL).group(1)
        metadata = json.loads(metadata_search)

        post_set = {
            'title': real_title,
            'slug': title,
            'content': html_content,
            'time': datetime.strptime(metadata['time'], "%Y-%m-%d %H:%M:%S"),
        }

        # create directory
        target = journal_dir + "%s/" % title
        try:
            os.makedirs(target)
        except OSError:
            print "Directory %s exists" % target
            pass

        full_html = template.render(post=post_set)

        # create index.html
        index = open(target + "index.html", 'w')
        index.write(full_html)
        index.close()

        # if full, remove first content from list
        if len(latest_posts) == 10:
            latest_posts.pop(0)

        latest_posts.append(post_set)
        archive_posts[year].append(post_set)

        print "%s%s created" % (target, title)


def process_days(days, year, month, source_month):
    for day in days:
        if all([int(year) == current_year, int(month) == current_month, int(day) > current_day]):
            continue

        item_date = "%s%s" % (month, day)
        item_date = str(int(item_date))

        source_day = source_month + "%s/" % day
        items = os.listdir(source_day)

        process_items(items, year, item_date, source_day)


def process_months(months, year, source_year):
    for month in months:
        if all([int(year) == current_year, int(month) > current_month]):
            continue
 
        source_month = source_year + "%s/" % month
        days = os.listdir(source_month)
        days.sort()
 
        process_days(days, year, month, source_month)


def create_archives(year):
    # create archive
    target_archive = archive_dir + "%s/" % year
    try:
        os.makedirs(target_archive)
    except OSError:
        pass

    archives = archive_posts[year]
    archives.reverse()

    archive_html = archive_template.render(years=years, current_year=year, archives=archives)

    # create index
    archive_index = open(target_archive + "index.html", 'w')
    archive_index.write(archive_html)
    archive_index.close()

    print "%s created" % target_archive


def create_index(posts):
    # reverse
    index_posts = posts
    index_posts.reverse()

    index_html = index_template.render(posts=index_posts)
    index_file = open(content_dir + "index.html", 'w')
    index_file.write(index_html)
    index_file.close()


def create_rss(posts):
    # reverse
    rss_posts = posts
    #rss_posts.reverse()

    full_xml = feed_template.render(posts=rss_posts)
    xml_file = open(content_dir + "feed.xml", 'w')
    xml_file.write(full_xml)
    xml_file.close()


def main():

    for year in years:
        if int(year) > current_year:
            continue

        archive_posts[year] = []

        source_year = source_dir + "%s/" % year
        months = os.listdir(source_year)
        months.sort()

        process_months(months, year, source_year)
        create_archives(year)

    create_index(latest_posts)
    create_rss(latest_posts)

if __name__ == '__main__':
    main()
