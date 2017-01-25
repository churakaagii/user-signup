import webapp2, re

UNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PW_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
# list of regex to use

class Handler(webapp2.RequestHandler): #helper class
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
            <p style="font-size: .8em;">coded by ada nakama</p>
        """
        
        totalpage = header
        
        inputelem = (
            ("username", "Username", "text", kwargs.get("uname_err", ""), 
                kwargs.get("uname_init", "")), 
            ("password", "Password", "password", kwargs.get("pw_err", ""), ""), 
            ("verify", "Re-enter Password", "password", kwargs.get("v_err", ""), ""),
            ("email", "Email (optional)", "text", kwargs.get("email_err", ""), 
                kwargs.get("email_init",""))
        ) # update this to get more form fields 
        # format is: (field name, label text, field type, error message, default text)
        
        for element in inputelem:
            totalpage += self.build_input(*element)
            
        totalpage += footer

        return totalpage
        
    def build_input(self, internal, external, thistype="text", error="", init_value=""):
        # html not-a-template to build each form
        htmlused = """
        <label for='%(internal)s'>%(external)s: </label>
        <br/><input type='%(thistype)s' name='%(internal)s' value='%(init_value)s'> 
        <span style='color: red;'>%(error)s</span>
        <br/>
        <br/>
        """
        return htmlused % {"internal": internal, "external": external, "error": error, "thistype": thistype, "init_value": init_value}
    
    def check_valid(self, string, regex): # general regex check
        return regex.match(string)
    
    def get(self):
        self.write(self.build_form())
        
    def post(self):
        checklist = {} # initialize passed values, update if more
        username = self.request.get("username")
        pw = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        
        checklist_init = [
            ("uname", username, UNAME_RE), 
            ("pw", pw, PW_RE)
        ] # list of all strings to by checked by regex
        # format is (checklist key, user data from field, regex to use)
        
        if email: # checks if email exists
            checklist_init.append(("email", email, EMAIL_RE))
        else:
            checklist["email_valid"] = True
        
        for checkset in checklist_init: # builds dictionary of validated user input
            checklist["%s_valid"%checkset[0]] = self.check_valid(checkset[1], checkset[2])
        
        if verify == pw: # checks if pw and re-entered pw match
            checklist["v_valid"] = True
        else:
            checklist["v_valid"] = False
        
        if all(checklist.itervalues()):
            self.redirect("/welcome?username="+username) # redirect on success
        else:
            if not checklist["uname_valid"]:
                uname_err = "Please enter a valid username (you can use letters, numbers, underscore or dash)"
            else:
                uname_err = ""
                
            if not checklist["pw_valid"]:
                pw_err = "Please enter a valid password of at least 3 characters"
            else:
                pw_err = ""
                
            if not checklist["v_valid"]:
                v_err = "Passwords do not match"
            else:
                v_err = ""
                
            if not checklist["email_valid"]:
                email_err = "Please enter a valid email"
            else:
                email_err = ""
                
            self.write(self.build_form(
                uname_err = uname_err,
                pw_err = pw_err,
                v_err = v_err,
                email_err = email_err, 
                uname_init = username, 
                email_init = email
            )) # builds error page, make sure to pass error message and initial values

class WelcomeHandler(Handler):
    def build_welcome(self, username): # builds welcome page
        welc_html = """
            <h1>Welcome, %s</h1>
        """
        return welc_html % username
    
    def get(self):
        username = self.request.get("username")
        if username.lower() == "ada": # v important
            username = "magnificent princess Ada, who must be obeyed in all things"
            
        self.write(self.build_welcome(username))
    

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
