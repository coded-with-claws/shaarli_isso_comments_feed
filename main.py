# -*- coding: utf-8 -*-

import sys
import os
import comments_feed

# Check arguments

if len(sys.argv) != 4:
    print("usage: {} <URL> <API_secret> <output_feed_directory>".format(sys.argv[0]))
    exit(1)

URL = sys.argv[1]
API_secret = sys.argv[2]
output_feed_directory = sys.argv[3]

if not os.access(output_feed_directory, os.W_OK):
    print("Can't write into {}".format(output_feed_directory))
    exit(1)

# Generate comments feed

my_comments_feed = comments_feed.CommentsFeed(URL, API_secret, output_feed_directory)
my_comments_feed.generate_feeds()

