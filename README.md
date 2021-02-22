# Generates a feed of the comments posted on a Shaarli website with Isso plugin

This tool addresses the following situation:
- [Shaarli](https://github.com/shaarli/Shaarli) provides a feed (atom + RSS) for the latest shaares
- [Isso](https://github.com/posativ/isso) provides an API listing the latest comments but only in JSON format (not in atom / RSS formats)\
&rarr; This tools generates a feed listing the new comments, quoting the associated shaare title.\
&rarr; You then have to move those feed files to the shaarli webserver instance so that they are available to users.

The feed is generated based on the Isso API "/latest", then enriched with the title of the shaares.
The generated files are in Atom and RSS formats.

BEWARE:
- The Isso API "/latest" gives all comments, included those related to private shaares.
- All my code is coded with claws :) (it's dirty yet it works)

Pre-requisites:
- Python3 (tested on 3.7.3), preferably with virtual environment support
- Shaarli (tested on v0.12.1) with the Isso plugin working
- Isso server (tested on v0.12.4) with the "latest-enabled" option enabled (https://github.com/posativ/isso/pull/610 / https://github.com/posativ/isso/issues/556)
- The isso API "/latest" is expected to be in the path "<shaarli_context>/isso/latest"

Usage:
- Call main.py with the needed arguments (for example with cron)
  - source <venv_path>/bin/activate
  - python main.py https://myshaarliwebsite.org/ <my_api_secret_value> <output_directory_for_feeds>
- Copy the atom.xml and rss.xml generated files into your webserver directory (for example with cron & sudo)
- Make sure you don't enable caching (client side) of those files

