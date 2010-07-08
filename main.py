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
from google.appengine.api import users


class MyTodoModel(db.Model):
    owner = db.UserProperty()
    description = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add = True) 



#Main Page where the User can Login and Logout 
class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = users.create_login_url(self.request.uri)
        url_linktext = 'Login'
        
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            
            
        #GQL - is kind of similar the SQL 
        #my_todo = MyTodoModel.all().order('-created').fetch(4)
        my_todo = db.GqlQuery("SELECT * FROM MyTodoModel WHERE owner = :owner ORDER BY created DESC LIMIT 4" ,owner = users.get_current_user())
        template_values = {
            'my_todo': my_todo,
            'num_my_todo': my_todo.count(),
            'user':user,
            'url': url,
            'url_linktext': url_linktext,
        
        }
    
    
        template_files = os.path.join(os.path.dirname(__file__),'index.html')
        self.response.out.write(template.render(template_files,template_values))
        
        
    def post(self):
        user = users.get_current_user()
        
        if user:
            todo = MyTodoModel()
            todo.owner = users.get_current_user()
            todo.description = self.request.get("my_todo")       
            todo.put()
            self.redirect('/')
        
        
        
        
        
        
      



def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
