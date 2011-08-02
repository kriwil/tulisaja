#!/usr/bin/env python

from ftplib import FTP
import os


username = 'kriwil@littlebrain.org'
password = ''
source_dir = '../../kriwil.com/content'
target_dir = '/tmp/kriwil.com'


#ftp = FTP('littlebrain.org')
#ftp.login(username, password)
#ftp.retrlines('LIST')

for root, dirs, files in os.walk(source_dir):

    # create dirs
    new_dir = root.replace(source_dir, target_dir)
    try:
        os.makedirs(new_dir)
    except OSError:
        pass

    for name in files:
        old_path = "%s/%s" % (root, name)
        new_path = old_path.replace(source_dir, target_dir)
        print new_path

