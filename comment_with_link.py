# -*- coding: utf-8 -*-

# Contains tuple (comment_text, comment_author, link_title, link_url, comment_id, comment_timestamp)
class CommentWithLinkInfo():

    def __init__(self, comment_text, comment_author, link_title, link_url, comment_id, comment_timestamp):
        self.comment_text = comment_text
        self.comment_author = comment_author
        self.link_title = link_title
        self.link_url = link_url
        self.comment_id = comment_id
        self.comment_timestamp = comment_timestamp

