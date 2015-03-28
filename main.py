import webapp2
import os
import jinja2
import cgi

#Setup templating engine
template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.write(*a,**kw)

	def render_Str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_Str(template, **kw))


#Basic
class MainPage(Handler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		visits = self.request.cookies.get('visits','0')
		userid = self.request.cookies.get('userid','guest')
		if visits.isdigit():
			visits = int(visits) + 1
		else:
			visits = 0
		self.render("login.html", visits = visits)
		self.response.headers.add_header('Set-cookie', 'visits = %s' % visits)
		self.response.headers.add_header('Set-cookie', 'userid = %s' % str(userid))

	def post(self):

		#Fetch the username, from the form and from the cookie.
		self.response.headers['Content-Type'] = 'text/html'
		userid_from_cookies = self.request.cookies.get('userid','guest')
		userid_from_form = self.request.get('username')
		visits = self.request.cookies.get('visits','0')

		#Print out the number of visits
		if visits.isdigit():
			visits = int(visits) + 1
		else:
			visits = 0

		#If the names don't match, then simply welcome the new user differently.
		if userid_from_form != userid_from_cookies:
			self.write("Welcome Mr. %s" % userid_from_form)
			visits = 0
		
		#Set cookies
		self.response.headers.add_header('Set-cookie', 'visits = %s' % visits)
		self.response.headers.add_header('Set-cookie', 'userid = %s' % str(userid_from_form))

		#Render the form
		self.render("welcome.html", visits = visits)	





application = webapp2.WSGIApplication([
									('/',MainPage)
									], debug=True)


