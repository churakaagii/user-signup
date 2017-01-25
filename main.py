import webapp2, re
from cgi import escape


UNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PW_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


class Handler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.write(*args, **kwargs)

class MainHandler(Handler):
    def build_form(self, **kwargs):   
        header = """
            <h1>User Signup</h1>
            <form method='post'>
        """
        
        footer = """
                <input type='submit'>
            </form>
        """
        
        totalpage = header
        
        inputelem = (
            ("username", "Username", kwargs.get("uname_err", "")), 
            ("password", "Password", kwargs.get("pw_err", "")), 
            ("verify", "Re-enter Password", kwargs.get("ver_err", "")),
            ("email", "Email (optional)", kwargs.get("email_err", ""))
        )
        
        for element in inputelem:
            totalpage += self.build_input(element[0], element[1], element[2])
            
        totalpage += footer

        return totalpage
        
    def build_input(self, internal, external, error=""):
        htmlused = """
        <label for='%(internal)s'>%(external)s: </label>
        <br/><input type='text' name='%(internal)s'> %(error)s
        <br/>
        <br/>
        """
        return htmlused % {"internal": internal, "external": external, "error": error}
    
    def check_valid(self, string, regex):
        return regex.match(string)
    
    def get(self):
        self.write(self.build_form())
        
    def post(self):
        checklist = {}
        username = self.request.get("username")
        pw = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        
        checklist_init = [
            ("uname", username, UNAME_RE), 
            ("pw", pw, PW_RE)
        ]
        
        if email:
            checklist_init.append(("email", email, EMAIL_RE))
        
        for checkset in checklist_init:
            checklist["%s_valid"%checkset[0]] = self.check_valid(checkset[1], checkset[2])
        
        if verify == pw:
            checklist["v_valid"] = True
        else:
            checklist["v_valid"] = False
        
        if all(checklist.itervalues()):
            self.redirect("/welcome?username="+username)
        else:
            self.write("butts")

class WelcomeHandler(Handler):
    def build_welcome(self, username):
        welc_html = """
            Welcome, %s
        """
        return welc_html % username
    
    def get(self):
        username = self.request.get("username")
        self.write(self.build_welcome(username))
    

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
