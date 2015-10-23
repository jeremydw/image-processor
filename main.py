import process
import webapp2


class MainHandler(webapp2.RequestHandler):

  def get(self):
    process.main()


app = webapp2.WSGIApplication([
    ('/', MainHandler),
])
