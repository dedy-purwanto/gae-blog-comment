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
import webapp2
import json
from datetime import datetime
from google.appengine.ext import db

class Comment(db.Model):
    url = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    comment = db.StringProperty(required=True)
    date = db.DateTimeProperty(required=True)

class PostCommentHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        super(PostCommentHandler, self).dispatch()

    def get(self):
        name = self.request.get('name');
        comment = self.request.get('comment');
        url = self.request.get('url');
        if name and comment and len(name) > 0 and len(comment) > 0:
            c = Comment(url=url, name=name, comment=comment, date=datetime.now())
            c.put()

            new_comment = {'name': name, 'comment': comment, 'date': c.date.__str__()}
            self.response.headers['Access-Control-Allow-Origin'] = '*'
            self.response.write(json.dumps(new_comment))


class GetCommentsHandler(webapp2.RequestHandler):
    def get(self):
        comments = {'comments':[]}
        for c in db.GqlQuery("SELECT * FROM Comment WHERE url = :1 ORDER BY date DESC", self.request.get('url')):
            comment = c.comment
            comment = comment.replace('\n', '<br />')
            comment = comment.replace('\r', '<br />')
            comment = comment.replace('\n\r', '<br />')

            comments['comments'].append({
                'name': c.name,
                'comment': comment,
                'date': c.date.__str__(),
            })

        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps(comments))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/get/', GetCommentsHandler),
    ('/post/', PostCommentHandler),
    ('/', MainHandler),
], debug=True)
