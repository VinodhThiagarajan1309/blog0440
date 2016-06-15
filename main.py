#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import webapp2
import jinja2
import re

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir) , autoescape = True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params ):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw ):
        self.write(self.render_str(template , **kw))

class Art(db.Model):
	title = db.StringProperty(required = True)
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class Blogpost(db.Model):
	title = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = created = db.DateTimeProperty(auto_now_add = True)

class BlogHandler(Handler):
	def get(self):
		blogList = db.GqlQuery("select * from Blogpost order by created desc")
		self.render("blogHome.html" , blogList=blogList)

class NewPostHandler(Handler):
	def get(self):
		self.render("newPost.html")

	def post(self):
		title = self.request.get("title")
		content = self.request.get("content")

		blogObj = Blogpost(title=title,content=content)
		blogObj.put()
		blogId = blogObj.key().id()
		self.redirect("/blog/"+str(blogId))

class ViewPostHandler(Handler):
	def get(self , blogId):
		key = db.Key.from_path("Blogpost" , int(blogId))
		blogItem = db.get(key)
		self.render("viewBlogItem.html",blogItem=blogItem)


   
app = webapp2.WSGIApplication([
    (r'/', BlogHandler),
    (r'/newpost', NewPostHandler),
    (r'/blog/(\d+)', ViewPostHandler)
], debug=True)