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
import os
import jinja2
import string
from rhyme_analyzer import sort_by_rhyme

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                    autoescape=True)

def render_str(template, **params):
  t = jinja_env.get_template(template)
  return t.render(params)

class MainHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def get(self):
        self.render('main.html')

    def post(self):
        ''' submit the input lyric and generate suggested lyrics '''
        user_verse = self.request.get('input_lyric')
        lyrics_db = open('generated_lines.txt').read().splitlines()
        output_lyrics = sort_by_rhyme(user_verse, lyrics_db)
        self.render('main.html', input_lyric=input_lyric, output_lyrics=output_lyrics)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
