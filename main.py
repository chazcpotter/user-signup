
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
import re

def build_page(error_username='', error_password='',
                error_verify='', error_email='',
                 username='', email=''):
    stylecss = """
    <style type='text/css'>
        #error {color: red}
    </style>
    """
    user_name_label = "<td><label>UserName</label></td>"
    password_label = "<td><label>Password</label></td>"
    verify_password_label = "<td><label>Verify Password</label></td>"
    email_label = "<td><label>Email (optional)</label></td>"

    user_name_input = "<td><input name='username' type='text' value='" + username + "' required></td>"
    password_input = "<td><input name='password' type='password'  required></td>"
    verify_password_input = "<td><input name='verify' type='password' required></td>"
    email_input = "<td><input name='email' type='text' value='" + email + "'></td>"

    error_username = "<td id='error'>" + error_username + "</td>"
    error_password = "<td id='error'>" + error_password + "</td>"
    error_verify = "<td id='error'>" + error_verify + "</td>"
    error_email = "<td id='error'>" + error_email + "</td>"

    submit_button = "<input type='submit'>"
    header = "<h1>Signup!</h1>"
    line_br = "<br>"

    form = header + stylecss + ("<form action='/welcome' method='post'> <table> <tr>" +
        user_name_label + user_name_input + error_username + "</tr>" +
        "<tr>" + password_label + password_input + error_password + "</tr> <tr>" +
        verify_password_label + verify_password_input + error_verify + "</tr>" +
        "<tr>" +email_label + email_input + error_email + "</tr></table>" +
        submit_button + "</form>")
    return form

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(build_page())

class Welcome(webapp2.RequestHandler):
    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
            email = email)

        content = "<h1>Welcome, " + username + "!</h1>"
        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            params['username'] = ''
            have_error = True
        else:
            params['error_username'] = ''

        if not valid_password(password):
            params['error_password'] = "That's not a valid password."
            have_error = True
        else:
            params['error_password'] = ''

        if password != verify:
            params['error_verify'] = "Your Password didnt match."
            have_error = True
        else:
            params['error_verify'] = ''

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            params['email'] = ''
            have_error = True
        else:
            params['error_email'] = ''


        if have_error:
            self.response.write(build_page(params['error_username'],
                params['error_password'],params['error_verify'],
                params['error_email'], params['username'], params['email']))
        else:
            self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
