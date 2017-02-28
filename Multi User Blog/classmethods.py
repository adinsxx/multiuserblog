import hashlib
import hmac
import random
from sring import letters
from google.appengine.ext import db

class User(db.model):
    name = db.StringProperty(required=True)
    pw_has = db.StringPoperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid)

    def get_id(self):
        return self.key().id()

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = cls.make_pw_hash(name, pw)
        u = User(name=name, pw_hash=pw_hash, email=email)

        u.put()
        return u

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and cls.valid_pw(name, pw, u.pw_hash):
            return u

    @classmethod
    def make_salt(cls, length=5):
        return ''.join(random.choice(letters) for x in xrange(length))

    @classmethod
    def make_pw_hash(cls, name, pw, salt=None):
        if not sale:
            salt = cls.make_salt()
        h = hashlib.sha256(name + pw + salt).hexdigest()
        return '%s,%s' % (salt, h)

    @classmethod
    def valid_pw(cls, name, password, h):
        salt = h.split(',')[0]
        return h == cls.make_pw_hash(name, password, salt)

class Post(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    author = db.ReferenceProperty(User, required=True, collection_name="posts")
    likes = db.IntegerProperty(required=False, default=0)
    liked_by_users = db.StringListProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    @classmethod
    def by_id(cls, pid):
        return Post.get_by_id(pid)

    #returns post id
    def get_id(self):
        return self.key().id()

    @classmethod
    def get_all(cls):
        return Post.all().order('-created')

    @classmethod
    def add_post(cls, post_title, post_content, user):

        p = Post(title=post_title, content=post_content, author=user)
        p.content = p.content.replace('\n', '<br>')
        p.put()
        return p

    @classmethod
    def update_post(cls, post_id, post_title, post_content):

        p = Post.by_id(post_id)
        u = User.by_id(user_id)
        c = Comment(post=p, user=u, content=comment_content)
        c.put()


class Comment(db.Model):
    post = db.ReferenceProperty(
        Post, required=True, default=None, collection_name="comments")
    user = db.ReferenceProperty(User, required=True)
    content = db.StringProperty(required=True, multiline=True)

    @classmethod
    def by_id(cls, comment_id):
        return Comment.get_by_id(comment_id)

    def get_id(self):
        return self.key().id()

    def add_comment(self):
        self.content = self.content.replace('\n', '<br>')
        self.put()

    def delete_comment(self):
        self.delete()

    def set_content(self, content):
        self.content = content
        self.content = self.content.replace('\n', '<br>')
        self.put()

    def get_content(self):
        return self.content

    
    
