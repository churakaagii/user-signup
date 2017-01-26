import webapp2, re
from cgi import escape
 
inputelem = (
    ["username", "Username", "text"], 
    ["password", "Password", "password"], 
    ["verify", "Re-enter Password", "password"],
    ["email", "Email (optional)", "text"]
) # a set of variables to initialize form fields, can be extended
# format is: [input name, label text, input type]

REGEX_DICT = {
    "username": re.compile(r"^[a-zA-Z0-9_-]{3,20}$"),
    "password": re.compile(r"^.{3,20}$"),
    "email": re.compile(r"^[\S]+@[\S]+.[\S]+$")
} # dictionary of regex to use, extension not mandatory

class Handler(webapp2.RequestHandler): #helper class
    def write(self, *args, **kwargs): 
        self.response.write(*args, **kwargs)

class MainHandler(Handler):
    def build_form(self, *args, **kwargs):   
        header = """
            <h1>User Signup</h1>
            <form method='post'>
        """
        
        footer = """
                <input type='submit'>
            </form>
            <p style="font-size: .8em;">coded by ada n.</p>
        """

        totalpage = header
        input_dicts = []
        
        for e in inputelem: # builds dict for passing arguments to internal form builder
            e.append(kwargs.get("%s_err"%e[0], ""))
            e.append(kwargs.get("%s_init"%e[0], ""))
            thisdict = dict(zip(["internal", "external", "thistype", "thiserror", "thisinit"], e))
            input_dicts.append(thisdict)
            e.pop()
            e.pop()
            
        
        for d in input_dicts:
            totalpage += self.build_input(**d)
        
        totalpage += footer

        return totalpage
        
    def build_input(self, **kwargs):
        # html not-a-template to build each form element
        htmlused = """
        <label for='%(internal)s'>%(external)s: </label>
        <br/><input type='%(thistype)s' name='%(internal)s' value='%(thisinit)s'> 
        <span style='color: red;'>%(thiserror)s</span>
        <br/>
        <br/>
        """
        return htmlused % {
            "internal": kwargs.get("internal"), 
            "external": kwargs.get("external"), 
            "thistype": kwargs.get("thistype"), 
            "thiserror": kwargs.get("thiserror"), 
            "thisinit": escape(kwargs.get("thisinit"))
        }
    
    def check_valid(self, string, regex): # general regex check
        if regex is not None:
            return regex.match(string)
        else:
            return True
    
    def get(self):
        self.write(self.build_form())
        
    def post(self):
        passed_dict = self.request.POST
        passed_dict_keys = list(passed_dict.iterkeys())
        checkagainstform = [ l[0] for l in inputelem ]
        
        for key in passed_dict_keys: # checks to make sure malicious code not passed in header
            if key not in checkagainstform:
                raise NameError("Some input was sent that is not in the form. Please enter all information correctly.")
        
        validation_filter = list(filter(lambda x: x != "verify", passed_dict_keys)) 
        # creates filter for all input to be validated
                
        validity = { key: self.check_valid(passed_dict.get(key), REGEX_DICT.get(key)) for key in validation_filter } 
        # dict of validity results
        
        if passed_dict.get("verify") != passed_dict.get("password"): 
            validity["verify"] = False
              
        if passed_dict.get("email") == "": # ensures validity if no email given
            validity["email"] = True

        if all(validity.itervalues()): # confirms validation and redirects or shows errors
            self.redirect("/welcome?username="+passed_dict.get("username"))
        else:
            error_filter = [ key for key in validity.iterkeys() if validity[key] == None ]
            init_filter = list(filter(lambda x: not(x == "password" or x == "verify"), passed_dict_keys))
            # creates filters for use in populating error_dict
            
            error_dict = { (key + "_err"): "Please enter a valid %s"%key for key in error_filter }
            init_dict = { (key + "_init"): passed_dict.get(key) for key in init_filter }
            error_dict.update(init_dict)
            if validity.get("verify") == False:
                error_dict["verify_err"] = "Passwords must match"
            # populates error_dict with all values to be passed to the build function
            
            self.write(self.build_form(**error_dict))

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
            
        self.write(self.build_welcome(escape(username)))
    

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
