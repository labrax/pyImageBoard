#!/usr/bin/env python

"""This executable start the web server, sql and web protocols."""

import web

#connection with the database
from dbconn import DbConn
#root page details
from rootPage import rootPage
#thread page details
from threadPage import threadPage
#image return details
from utils import Output
#cache of pages
from cache import Cache
#anti-flooding mecanism
from security import AntiFlood
#statistics
#from admin import Statistics
#definitions
from definitions import template_dir, static_dir, img_dir

#defined here to be used in both pages
render = web.template.render(template_dir)
antiflood = AntiFlood()
#stats = Statistics()
cache = Cache()

#settings
urls = (
		'/', 'root', 
        '/post', 'post',
        '/thread/(.+)', 'thread_list',
		'/(.+)', 'not_found'
        )
app = web.application(urls, globals())

class root:
	"""This class connects with the rootPage internals."""
	
	def GET(self):
		return rootPage(DbConn(), render, cache).GET()

	def POST(self):
		if antiflood.delayToPost(web.ctx.ip) == 0:
			antiflood.post(web.ctx.ip)
			return rootPage(DbConn(), render, cache).POST(web)
		else:
			return Output().pageReturnError("To be able to post you need to wait %s seconds!" % antiflood.delayToPost(web.ctx.ip))


class thread_list:
	"""This class connects with the threadPage and imageReturn internals."""
			
	def GET(self, thread):
		return threadPage(DbConn(), render, cache).GET(thread)

	def POST(self, thread):
		if antiflood.delayToPost(web.ctx.ip) == 0:
			antiflood.post(web.ctx.ip)
			return threadPage(DbConn(), render, cache).POST(thread, web)
		else:
			return Output().pageReturnError("To be able to post you need to wait %s seconds!" % antiflood.delayToPost(web.ctx.ip))

class not_found:
	def GET(self, thread):
		return Output().pageReturnErrorSubFolderRefreshBack("Invalid page!")

if __name__ == "__main__":
	app.run()
