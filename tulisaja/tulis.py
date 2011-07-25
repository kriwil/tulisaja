#!/usr/bin/env python

from datetime import date
from jinja2 import Environment, PackageLoader
from markdown2 import markdown
import os
import re


def main():
    source_dir = '../../kriwil.com/source/'
    content_dir = '../../kriwil.com/content/'
    journal_dir = content_dir + 'journal/'
    archive_dir = content_dir + 'archive/'

    # jinja
    env = Environment(loader=PackageLoader('tulis', 'templates'))
    template = env.get_template('base.html')

    # get current date set
    # only processing data <= current date
    current_year = date.today().year
    current_month = date.today().month
    current_day = date.today().day

    years = os.listdir(source_dir)
    archives = {}

    for year in years:
        if int(year) > current_year:
            continue

        archives[year] = {}

        source_year = source_dir + "%s/" % year
        months = os.listdir(source_year)

        for month in months:
            if all([int(year) == current_year, int(month) > current_month]):
                continue

            source_month = source_year + "%s/" % month
            days = os.listdir(source_month)

            for day in days:
                if all([int(year) == current_year, int(month) == current_month, int(day) > current_day]):
                    continue

                item_date = "%s%s" % (month, day)
                item_date = str(int(item_date))
                archives[year][item_date] = []

                source_day = source_month + "%s/" % day
                items = os.listdir(source_day)

                for item in items:

                    source_item = source_day + item
                    # print "processing %s ..." % source_item

                    # get title
                    # file is in format 'nn_journal-title.md'
                    # where nn is number to have article in correct order
                    title = re.sub('\.md$', '', item)

                    item_markdown = open(source_item)

                    raw_content = item_markdown.read()
                    html_content = markdown(raw_content)

                    title_search = re.match("## (.+)\r\n", raw_content)
                    real_title = title_search.group(1)
                    archives[year][item_date].append(real_title)

                    # create directory
                    target = journal_dir + "%s/" % title
                    try:
                        os.makedirs(target)
                    except OSError:
                        print "Directory %s exists. Delete it first, or change %s file name." % (target, source_item)
                        continue

                    full_html = template.render(entry_content=html_content)

                    # create index.html
                    index = open(target + "index.html", 'w')
                    index.write(full_html)
                    index.close()

                    print "%s%s created" % (target, title)

        # create archive
        target_archive = archive_dir + "%s/" % year
        try:
            os.makedirs(target_archive)
        except OSError:
            pass

        # sort archives
        archive_dates = [int(blog_date) for blog_date, blog_titles in archives[year].items()]
        archive_dates.sort()
        archive_dates.reverse()

        # create index
        archive_index = open(target_archive + "index.html", 'w')
        for blog_date in archive_dates:
            blog_date = str(blog_date)

            titles = archives[year][blog_date]
            for blog_title in titles:
                archive_index.write("%s %s\r\n" % (blog_date, blog_title))

        #for blog_date, blog_titles in archives[year].items():
        #    for blog_title in blog_titles:
        #        archive_index.write("%s %s\r\n" % (blog_date, blog_title))

        archive_index.close()

        print "%s created" % target_archive


if __name__ == '__main__':
    main()
