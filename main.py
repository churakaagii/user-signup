import webapp2, re
from cgi import escape


def check_thingy(string, regularex):
    return None
    
def print_error(error, thistype):
    if error == True:
        return "Error! The %s is invalid.  Please try again." % thistype
    else:
        return ""

class Handler(webapp2.RequestHandler):
    def write(self, towrite):
        self.response.write(towrite)

class MainHandler(Handler):
    def build_form(self):
        form = """
            <h1>User Signup</h1>
            <form method='post'>
                <label for='username'>Username: </label>
                <br/><input type='text' name='username'> 
                <br/>
                <br/>
                <label for='password'>Password: </label>
                <br/><input type='text' name='pw'> 
                <br/>
                <br/>
                <label for='verify'>Re-enter Password: </label>
                <br/><input type='text' name='verify'> 
                <br/>
                <br/>
                <label for='email'>Email (optional): </label>
                <br/><input type='text' name='email'> 
                <br/>
                <br/>
                <input type="submit"/>
            </form>
        """
        return form    
    
    def get(self):
        self.write(self.build_form())
        
    def post(self):
        username = self.request.get("username")
        self.redirect("/welcome?username="+username)

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
