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
        checklist = {} # will be populated with validation results on user input
        passed_dict = self.request.POST 
        prep_validation = list(filter((lambda x: not(x == "verify" or x == "email")), passed_dict.iterkeys())) # list of all input to be validated
        
        if passed_dict["email"] == "": 
            checklist["valid email"] = True
        else:
            prep_validation.append("email")
            
        if passed_dict["verify"] == passed_dict["password"]: 
            checklist["matching password"] = True
        else:
            checklist["matching password"] = False
        
        for key in prep_validation: # constructs checklist (validation results)
            checklist["valid %s"%key] = self.check_valid(passed_dict[key], REGEX_DICT[key])
              
        if all(checklist.itervalues()): # confirms validation and redirects or shows errors
            self.redirect("/welcome?username="+passed_dict["username"])
        else: 
            errordict = {} # will be populated with errors to show user
            
            for key in checklist.iterkeys(): # constructs errordict (user errors)
                if not checklist[key]: 
                    if key == "matching password": 
                        key_name = "v_err"
                    else: 
                        var_name = key.partition("valid ")
                        key_name = var_name[2] + "_err" 
                    errordict[key_name] = "Please enter a %s" % key
            
            self.write(self.build_form(**errordict))

class WelcomeHandler(Handler):
    def build_welcome(self, username):
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
