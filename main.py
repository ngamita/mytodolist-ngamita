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
import wsgiref.handlers


from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db


class MyTodoModel(db.Model):
    description = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add = True) 




class MainHandler(webapp.RequestHandler):
    def get(self):
        
        #my_todo = MyTodoModel.all().order('-created').fetch(4)
        my_todo = db.GqlQuery("SELECT * FROM MyTodoModel ORDER BY created DESC LIMIT 4")
        template_values = {
            'my_todo': my_todo
        
        }
        
    
    
        template_files = os.path.join(os.path.dirname(__file__),'index.html')
        self.response.out.write(template.render(template_files,template_values))
        
        
    def post(self):
        todo = MyTodoModel()
        todo.description = self.request.get("my_todo")       
        todo.put()
        self.redirect('/')
        
        
        
        
        
        
      



def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
