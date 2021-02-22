# -*- coding: utf-8 -*-

from datetime import datetime, timezone
import requests
import jwt
from feedgen.feed import FeedGenerator
import comment_with_link

class CommentsFeed():

    def __init__(self, URL, API_secret, output_feed_directory):
        self.URL = URL
        self.shaarli_endpoint = "{}/api/v1".format(URL.rstrip('/'))
        print(self.shaarli_endpoint)

        self.encoded_jwt = jwt.encode({"iat": datetime.now(timezone.utc)}, API_secret, algorithm="HS512")
        print(self.encoded_jwt)

        self.shaarli_endpoint_links = "{}/links".format(self.shaarli_endpoint)
        print(self.shaarli_endpoint_links)

        self.output_feed_directory = output_feed_directory


    # Not used - was written to test API call
    def fetch_shaarli_links(self):
        response = requests.get(self.shaarli_endpoint_links,
            headers={
            "Authorization": "Bearer {}".format(self.encoded_jwt),
            "Content-Type": "text/plain; charset=UTF-8"
            }
        )
        print(response)

        links_data = response.json()
        print(links_data)


    def fetch_link_ID(self, uid):
        shaarli_endpoint_linkID = "{}/links/{}".format(self.shaarli_endpoint, uid)
        print(shaarli_endpoint_linkID)

        response = requests.get(shaarli_endpoint_linkID,
            headers={
            "Authorization": "Bearer {}".format(self.encoded_jwt),
            "Content-Type": "text/plain; charset=UTF-8"
            }
        )
        print(response)

        linkID_data = response.json()
        print(linkID_data)

        return linkID_data


    def fetch_isso_comments(self):
        limit=50

        isso_endpoint = "{}/isso".format(self.URL.rstrip('/'))
        print(isso_endpoint)

        isso_endpoint_latest = "{}/latest?limit={}".format(isso_endpoint, limit)
        print(isso_endpoint_latest)

        response = requests.get(isso_endpoint_latest)
        print(response)

        comments_data = response.json()
        print(comments_data)

        return comments_data


    def fetch_link_info_for_comments(self, comments_data):
        # Fetch link info for each uid given in comments

        # Array of CommentWithLinkInfo objects
        comments_with_link_title = []

        for comment in comments_data:
            print("comment={}".format(comment))
            linkID_data = self.fetch_link_ID(comment["uri"])
            link_url = "{}/shaare/{}".format(self.URL.rstrip('/'), linkID_data["shorturl"])
            author = comment["author"]
            if not author:
                author = "anonyme"
            a_comment_with_link = comment_with_link.CommentWithLinkInfo(comment["text"], author, linkID_data["title"], link_url, comment["id"], comment["created"])
            comments_with_link_title.append(a_comment_with_link)

        return comments_with_link_title


    def generate_feed_files(self, comments_with_link_title):

        # Generate feeds

        URL_feed = "{}/comments_feed".format(self.URL.rstrip('/'))
        html_CR = "<br>"

        fg = FeedGenerator()
        fg.id(URL_feed)
        fg.title('Derniers commentaires de {}'.format(self.URL))
        #fg.author( {'name':'John Doe','email':'john@example.de'} )
        #fg.link( href=URL_feed, rel='alternate' )
        fg.logo('{}/tpl/shaarli-default-dark/img/favicon.png'.format(self.URL.rstrip('/')))
        #fg.subtitle('This is a cool feed!')
        fg.link( href=URL_feed, rel='self' )
        fg.language('fr')
        fg.description('Derniers commentaires associés aux shaares de {}'.format(self.URL))
        #fg.updated('2021-02-13T21:18:26.779943+00:00')

        for c in comments_with_link_title:
            fe = fg.add_entry()
            fe.id('{}/{}'.format(c.link_url, c.comment_id))
            fe.title('{}'.format(c.link_title))
            fe.description('{} a commenté :{}{}'.format(c.comment_author, html_CR, c.comment_text))
            fe.link(href="{}#isso-thread".format(c.link_url))
            comment_datetime = datetime.fromtimestamp(c.comment_timestamp).replace(tzinfo=timezone.utc)
            fe.updated(comment_datetime)
            fe.pubDate(comment_datetime)

            atomfeed = fg.atom_str(pretty=True) # Get the ATOM feed as string
            rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
            atom_file = "{}/atom.xml".format(self.output_feed_directory)
            rss_file = "{}/rss.xml".format(self.output_feed_directory)
            fg.atom_file(atom_file) # Write the ATOM feed to a file
            fg.rss_file(rss_file) # Write the RSS feed to a file

    def generate_feeds(self):
        comments_data = self.fetch_isso_comments()
        comments_with_link_title = self.fetch_link_info_for_comments(comments_data)
        self.generate_feed_files(comments_with_link_title)

