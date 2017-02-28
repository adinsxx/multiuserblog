import webapp2

from handlers.post_handler import BlogHandler, SinglePostHandler, AddPostHandler
from handlers.post_handler import EditPostHandler, DeletePostHandler, UserPostHandler, LikePosthandler
from handlers.post-handler import PostCommentsHandler, CommentEditHandler, CommentDeleteHandler
from handlers.user_handler import RegiserHandler, LoginHandler, LogoutHandler, WelcomeHandler
from google.appengine.ext import db

app = webapp2.WSGIApplication([
    ('/', BlogHandler),
    ('/register', RegisterHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/welcome', WelcomeHandler),
    ('/blog', BlogHandler),
    ('/blog/addpost', AddPostHandler),
    ('/blog/myposts', UserPostHandler),
    ('/blog/([0-9]+)', SinglePostHandler),
    ('/blog/([0-9]+)/comments', SinglePostHandler),
    ('/blog/([0-9]+)/comments/new', PostCommentsHandler),
    ('/blog/([0-9]+)/edit', EditPostHandler),
    ('/blog/([0-9]+)/like', LikePostHandler),
    ('/blog/([0-9]+)/delete', DeletePostHandler),
    ('/blog/([0-9]+)/comment/([0-9]+)/edit', CommentEditHandler),
    ('/blog/([0-9]+)/comment/([0-9]+)/delete', CommentDeleteHandler)
    ], debug=True)
