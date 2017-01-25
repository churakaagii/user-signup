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
            <p style="font-size: .8em;">coded by ada nakama</p>
        """

        totalpage = header
        input_dict = []
        
        for e in inputelem: # builds dict for passing kwargs to internal form builder
            e.append(kwargs.get("%s_err"%e[0], ""))
            e.append(kwargs.get("%s_init"%e[0], ""))
            thisdict = dict(zip(["internal", "external", "thistype", "thiserror", "thisinit"], e))
            input_dict.append(thisdict)
            e.pop()
            e.pop()
            
        
        for d in input_dict:
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
    
    def get(self):
        self.write(self.build_form())
        
    def post(self):
        passed_dict = self.request.POST 
        prep_validation = list(filter(lambda x: x != "verify", passed_dict.iterkeys())) 
        # creates filter for all input to be validated
                
        checklist = { ("valid " + key): self.check_valid(passed_dict.get(key), REGEX_DICT.get(key)) for key in prep_validation } # dict of validity results
        
        if passed_dict["verify"] == passed_dict["password"]: 
            checklist["matching password"] = True
        else:
            checklist["matching password"] = False
              
        if passed_dict["email"] == "": # ensures validity if no email given
            checklist["valid email"] = True

        if all(checklist.itervalues()): # confirms validation and redirects or shows errors
            self.redirect("/welcome?username="+passed_dict.get("username"))
        else: 
            init_prep = list(filter(lambda x: not(x == "password" or x == "verify"), passed_dict.iterkeys())) # creates filter for kept values
            error_dict = { (key + "_init"): passed_dict.get(key) for key in init_prep }
            # initializes error_dict with kept values
            
            for key in checklist.iterkeys(): # populates error_dict with user errors
                if not checklist.get(key): 
                    if key == "matching password": 
                        key_name = "verify_err"
                    else: 
                        var_name = key.partition("valid ")
                        key_name = var_name[2] + "_err" 
                    error_dict[key_name] = "Please enter a %s" % key
            
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
            
        self.write(self.build_welcome(username))
    

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
