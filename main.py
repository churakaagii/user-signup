import webapp2, re

REGEX_DICT = {
    "username": re.compile(r"^[a-zA-Z0-9_-]{3,20}$"),
    "password": re.compile(r"^.{3,20}$"),
    "email": re.compile(r"^[\S]+@[\S]+.[\S]+$")
} # dictionary of regex to use, must be extended

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
            ("username", "Username", "text", kwargs.get("username_err", ""), kwargs.get("username_init", "")), 
            ("password", "Password", "password", kwargs.get("password_err", ""), ""), 
            ("verify", "Re-enter Password", "password", kwargs.get("v_err", ""), ""),
            ("email", "Email (optional)", "text", kwargs.get("email_err", ""), kwargs.get("email_init",""))
        ) # a set of variables to initialize form fields, must be extended
        # format is: (field name, label text, field type, error message variable, default text)
        
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
        checklist = {} # will be filled with validated user input
        checklist_init = [] # will be passed into checklist constructor
        passed_dict = self.request.POST # user input
        prep_validation = list(filter((lambda x: not(x == "verify" or x == "email")), passed_dict.iterkeys())) # list of all input to be validated
        
        for key in prep_validation: # populated list for checklist constructor
            checklist_init.append((key, passed_dict[key], REGEX_DICT[key]))
        
        if passed_dict["email"]: # checks if email exists
            checklist_init.append(("email", passed_dict["email"], REGEX_DICT["email"]))
        else:
            checklist["valid email"] = True
        
        for checkset in checklist_init: # constructs checklist
            checklist["valid %s"%checkset[0]] = self.check_valid(checkset[1], checkset[2])
        
        if passed_dict["verify"] == passed_dict["password"]: # checks if pws match
            checklist["matching password"] = True
        else:
            checklist["matching password"] = False
        
        if all(checklist.itervalues()):
            self.redirect("/welcome?username="+passed_dict["username"]) # redirect on success
        else: # otherwise generate error messages and build a new form 
            errordict = {} # will be populated with errors to show to user
            
            for key in checklist.iterkeys(): # constructs errordict
                if not checklist[key]: # if input not valid, adds error
                    if key == "matching password": # unique check for matching pw
                        key_name = "v_err"
                    else:
                        var_name = key.partition("valid ")
                        key_name = var_name[2] + "_err"
                        
                    errordict[key_name] = "Please enter a %s" % key
            
            self.write(self.build_form(**errordict)) # builds error page

class WelcomeHandler(Handler):
    def build_welcome(self, username): # builds welcome page
        welc_html = """
            <h1>Welcome %s</h1>
        """
        return welc_html % username
    
    def get(self):
        username = self.request.get("username")
        if username.lower() == "ada": # v important
            username = "international space princess Ada, who must be obeyed in all things"
            
        self.write(self.build_welcome(username))
    

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
